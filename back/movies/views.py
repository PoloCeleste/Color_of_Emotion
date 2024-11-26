import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import MovieSerializer, EmotionColorSerializer

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Movie, EmotionColor
from skimage import color as skcolor
import json, random


## CPU 사용
import numpy as np
def rgb_to_lab(rgb):
    # RGB 값을 0-1 사이로 정규화
    rgb_normalized = np.array(rgb) / 255.0
    # 3차원 배열로 변환
    rgb_normalized = rgb_normalized.reshape(1, 1, 3)
    # RGB에서 LAB으로 변환
    lab = skcolor.rgb2lab(rgb_normalized)
    return lab[0, 0]

def delta_e_2000(lab1, lab2, kL=1, kC=1, kH=1):
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2
    
    # C1, C2 계산
    C1 = np.sqrt(a1**2 + b1**2)
    C2 = np.sqrt(a2**2 + b2**2)
    
    # C평균 계산
    Cbar = (C1 + C2) / 2
    
    # G 계산
    G = 0.5 * (1 - np.sqrt(Cbar**7 / (Cbar**7 + 25**7)))
    
    # a'1, a'2 계산
    a1_prime = (1 + G) * a1
    a2_prime = (1 + G) * a2
    
    # C'1, C'2 계산
    C1_prime = np.sqrt(a1_prime**2 + b1**2)
    C2_prime = np.sqrt(a2_prime**2 + b2**2)
    
    # h'1, h'2 계산
    h1_prime = np.degrees(np.arctan2(b1, a1_prime)) % 360
    h2_prime = np.degrees(np.arctan2(b2, a2_prime)) % 360
    
    # deltaL', deltaC' 계산
    deltaL_prime = L2 - L1
    deltaC_prime = C2_prime - C1_prime
    
    # deltah_prime 계산
    if C1_prime * C2_prime == 0:
        deltah_prime = 0
    else:
        if abs(h2_prime - h1_prime) <= 180:
            deltah_prime = h2_prime - h1_prime
        elif h2_prime - h1_prime > 180:
            deltah_prime = h2_prime - h1_prime - 360
        else:
            deltah_prime = h2_prime - h1_prime + 360
            
    deltaH_prime = 2 * np.sqrt(C1_prime * C2_prime) * np.sin(np.radians(deltah_prime) / 2)
    
    # L', C', H' 평균 계산
    Lbar_prime = (L1 + L2) / 2
    Cbar_prime = (C1_prime + C2_prime) / 2
    
    # hbar_prime 계산
    if C1_prime * C2_prime == 0:
        hbar_prime = h1_prime + h2_prime
    else:
        if abs(h1_prime - h2_prime) <= 180:
            hbar_prime = (h1_prime + h2_prime) / 2
        elif h1_prime + h2_prime < 360:
            hbar_prime = (h1_prime + h2_prime + 360) / 2
        else:
            hbar_prime = (h1_prime + h2_prime - 360) / 2
            
    # 가중치 계산
    T = (1 - 0.17 * np.cos(np.radians(hbar_prime - 30)) +
         0.24 * np.cos(np.radians(2 * hbar_prime)) +
         0.32 * np.cos(np.radians(3 * hbar_prime + 6)) -
         0.20 * np.cos(np.radians(4 * hbar_prime - 63)))
    
    deltaTheta = 30 * np.exp(-((hbar_prime - 275) / 25)**2)
    RC = 2 * np.sqrt(Cbar_prime**7 / (Cbar_prime**7 + 25**7))
    SL = 1 + (0.015 * (Lbar_prime - 50)**2) / np.sqrt(20 + (Lbar_prime - 50)**2)
    SC = 1 + 0.045 * Cbar_prime
    SH = 1 + 0.015 * Cbar_prime * T
    RT = -np.sin(np.radians(2 * deltaTheta)) * RC
    
    # 최종 색상 차이 계산
    return np.sqrt(
        (deltaL_prime/(kL*SL))**2 +
        (deltaC_prime/(kC*SC))**2 +
        (deltaH_prime/(kH*SH))**2 +
        RT * (deltaC_prime/(kC*SC)) * (deltaH_prime/(kH*SH))
    )

def calculate_color_similarity(color1, color2):
    lab1 = rgb_to_lab(color1)
    lab2 = rgb_to_lab(color2)
    return delta_e_2000(lab1, lab2)

@csrf_exempt
@require_POST
def recommend_movies(request):
    try:
        emotion_ids = json.loads(request.body)['emotions']
        
        # emotion_id 리스트로 EmotionColor 검색
        color_set = None
        for i in range(len(emotion_ids), 0, -1):
            current_emotions = emotion_ids[:i]
            try:
                color_set = EmotionColor.objects.filter(
                    emotion_id__in=current_emotions
                ).first()
                if color_set:
                    break
            except EmotionColor.DoesNotExist:
                continue
        
        if not color_set:
            return JsonResponse({'error': 'No matching color set found'}, status=400)
        
        # 장르 기반으로 영화 필터링
        matching_movies = Movie.objects.filter(
            genre_ids__name__in=[genre.name for genre in color_set.genres_id.all()]
        ).distinct()
        
        # 색상 유사도 계산
        movie_scores = []
        for movie in matching_movies:
            similarities = []
            for emotion_color in color_set.emotions_color:
                for poster_color in movie.poster_palette:
                    similarity = calculate_color_similarity(emotion_color, poster_color[:3])
                    similarities.append((similarity, poster_color[3]))
            
            if similarities:
                avg_similarity = np.mean([s[0] for s in similarities])
                weighted_dominance = np.average(
                    [s[1] for s in similarities],
                    weights=[1/s[0] if s[0] != 0 else 1 for s in similarities]
                )
                movie_scores.append((movie, avg_similarity * weighted_dominance))
        
        # 점수로 정렬하고 상위 50개 선택 -> 랜덤 -> 31개 잘라서 전송
        sorted_movies = [movie for movie, _ in sorted(movie_scores, key=lambda x: x[1])][:50]
        random.shuffle(sorted_movies)
        sorted_movies = sorted_movies[:31]
        
        serializer = MovieSerializer(sorted_movies, many=True)
        return JsonResponse(serializer.data, safe=False)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_POST
def emotion_colors(request):
    try:
        emotion_ids = json.loads(request.body)['emotions']
        
        # emotion_id 리스트로 EmotionColor 검색
        color_set = None
        for i in range(len(emotion_ids), 0, -1):
            current_emotions = emotion_ids[:i]
            try:
                color_set = EmotionColor.objects.filter(
                    emotion_id__in=current_emotions
                ).first()
                if color_set:
                    break
            except EmotionColor.DoesNotExist:
                continue
        
        if not color_set:
            return JsonResponse({'error': 'No matching color set found'}, status=400)
        
        serializer = EmotionColorSerializer(color_set)
        return JsonResponse(serializer.data, safe=False)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


tmdb = settings.API_KEY

@api_view(['GET'])
def Actors(request, movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    delp=['adult', 'gender', 'id', 'name', 'popularity', 'cast_id', 'credit_id', 'order']
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {tmdb}"
    }
    try:
        response = requests.get(url, headers=headers).json()['cast']
        if response:
            for re in response:
                try:re['profile_path']='https://image.tmdb.org/t/p/original'+re['profile_path']
                except:pass
                for d in delp:
                    try: del re[d]
                    except: continue
            
            data={
                'cast':response
            }
    except:
        data={
            'error':"Can't access TMDB API."
        }
    return Response(data)