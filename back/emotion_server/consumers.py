from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio, base64, time, cv2, torch, json
from sklearn.preprocessing import RobustScaler
from channels.exceptions import StopConsumer
import torchvision.transforms as tt
from os import path as pth, getcwd
import torch.nn.functional as F
from scipy import stats
from .models import *
import pandas as pd
import numpy as np


emotion={
    'Joy':1,
    'Sadness':2,
    'Anger':3,
    'Embarrassment':4,
    'Anxiety':5,
    'Pain':6,
    'Neutral':7,
}
assets=pth.join('emotion_server', 'assets')
class_labels = ['Joy', 'Embarrassment', 'Anger', 'Anxiety', 'Pain', 'Sadness', 'Neutral']
# class_labels = ['기쁨', '당황', '분노', '불안', '상처', '슬픔', '중립']
class_labels_dict = {'기쁨': 0, '당황': 1, '분노': 2, '불안': 3, '상처': 4, '슬픔': 5, '중립': 6}

display_color = (86, 189, 246)

model=None
face_classifier=None

def remove_outliers_iqr(df):
    # 각 열에 대해 IQR 계산
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1
    
    # IQR 범위 밖의 데이터를 이상치로 간주하고 제거
    df_filtered = df[~((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).any(axis=1)]
    return df_filtered

def load_model():
    global model, face_classifier
    face_classifier = cv2.CascadeClassifier(pth.join(getcwd(), assets,'face_classifier.xml'))

    if torch.cuda.is_available():
        device = 'cuda'
        # print('GPU On')
    else:
        device = 'cpu'
        print('GPU Off')

    model_state = torch.load(pth.join(getcwd(), assets, 'model.pth'), map_location=torch.device(device), weights_only=True)
    model = getModel('emotionnet', True)
    model.load_state_dict(model_state['model'])

class VideoStreamConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_phase_data = []
        self.second_phase_data = []
        self.is_analyzing = False
        self.is_second_phase = False
        self.emotion_model = model
        self.first_analysis_result={}
        self.second_analysis_result={}
        self.final_analysis_result={}
        self.emotion_time_series = []
        self.face_landmarks = []
        self.lighting_conditions = []
    
    async def connect(self):
        self.loop = asyncio.get_running_loop()
        await self.accept()

    async def disconnect(self, close_code):
        raise StopConsumer()

    async def receive(self, text_data):
        if not (text_data):
            print('Closed connection')
            await self.close()
        else:
            data = json.loads(text_data)
            message_type = data.get('type')

            if message_type == 'start_analysis':
                print('Analysis Start.')
                self.is_analyzing = True
                self.first_phase_data = []
                self.second_phase_data = []
                
            elif message_type == 'frame':
                if not self.is_analyzing:
                    return
                    
                image_data = data['data']
                # 이미지 데이터 처리를 비동기로 실행
                frame, emotion_data = await self.main(image_data)
                
                if self.is_second_phase:
                    self.second_phase_data.append(emotion_data)
                else:
                    self.first_phase_data.append(emotion_data)
                    
                # 처리된 결과를 클라이언트에 전송
                await self.send(text_data=json.dumps({
                    'frame': frame,
                    'emotion': emotion_data
                }))

            elif message_type == 'second_phase':
                print('In Second Phase.')
                self.is_second_phase = True
                self.first_analysis_result = await self.process_first_results(self.first_phase_data)

            elif message_type == 'restart_second_phase':
                if self.is_second_phase:
                    print('Second Phase Restart.')
                    self.second_phase_data = []
            
            elif message_type == 'stop_analysis':
                print('Stop Analysis.')
                self.is_analyzing = False
                self.second_analysis_result = await self.process_second_results(self.second_phase_data)
                
                self.final_analysis_result = await self.process_final_results(
                    self.first_analysis_result, 
                    self.second_analysis_result
                )
                
                await self.send(text_data=json.dumps({
                    'type': 'analysis_result',
                    'result': self.final_analysis_result
                }))


    async def main(self, frame_data):
        # base64 문자열에서 실제 이미지 데이터 부분만 추출
        if ',' in frame_data:
            frame_data = frame_data.split(',')[1]
        
        # base64 문자열을 바이트로 디코딩
        image_bytes = base64.b64decode(frame_data)
        # base64 데이터를 numpy 배열로 변환
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # 이미지가 제대로 디코딩되었는지 확인
        if frame is None:
            return None, None

        frame = cv2.normalize(frame, None, 0, 255, cv2.NORM_MINMAX)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        label = ''
        domination = False
        prob = ''
        emotion_data = ''

        frame = cv2.GaussianBlur(frame, (5, 5), 0)
        display_color = (255, 161, 54)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), display_color, 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

            if np.sum([roi_gray]) != 0:
                roi = tt.functional.to_pil_image(roi_gray)
                roi = tt.functional.to_grayscale(roi)
                roi = tt.ToTensor()(roi).unsqueeze(0)

                tensor = self.emotion_model(roi)
                probs = F.softmax(tensor, dim=1).detach().numpy()[0] * 100
                self.emotion_time_series.append({
                    'timestamp': time.time(),
                    'emotions': {class_labels[i]: float(prob) for i, prob in enumerate(probs)}
                })
                prob = {}
                for i, p in enumerate(probs):
                    prob[class_labels[i]] = round(float(p), 2)

                # print(prob)
                label = "Face Detected"
                flag = True
                domination = True
        else:
            if not label:
                label = 'No Face Found'
                display_color = (0, 255, 0)
                flag = False

        # 프레임을 base64로 인코딩
        _, buffer = cv2.imencode('.jpg', frame)
        frame_base64 = base64.b64encode(buffer).decode('utf-8')

        if domination:
            emotion_data = {
                'emotion': prob,
                'flag': flag
            }
        return frame_base64, emotion_data



    async def process_first_results(self, first_phase_data):
        """첫 번째 단계의 감정 데이터 정규화 및 표준편차 계산"""
        if not first_phase_data:
            return {}
        
        # 감정 데이터가 있는 프레임만 필터링
        valid_data = [data['emotion'] for data in first_phase_data if data and 'emotion' in data]
        
        if not valid_data:
            return {}
        
        # 데이터프레임 생성
        df = pd.DataFrame(valid_data)
        df_filtered = remove_outliers_iqr(df)
        
        # RobustScaler를 사용하여 정규화
        scaler = RobustScaler()
        normalized_data = scaler.fit_transform(df_filtered)
        df_normalized = pd.DataFrame(normalized_data, columns=df.columns)
        
        # 정규화된 데이터의 평균과 표준편차 계산
        normalized_means = df_normalized.mean()
        normalized_std = df_normalized.std()
        
        return {
            'normalized_means': normalized_means.to_dict(),
            'standard_deviation': normalized_std.to_dict(),
            'total_frames': len(valid_data),
            'raw_data': df.to_dict(orient='list')
        }

    async def process_second_results(self, second_phase_data):
        """두 번째 단계의 감정 데이터 정규화 및 표준편차 계산"""
        if not second_phase_data:
            return {}
        
        # 감정 데이터가 있는 프레임만 필터링
        valid_data = [data['emotion'] for data in second_phase_data if data and 'emotion' in data]
        
        if not valid_data:
            return {}
        
        # 데이터프레임 생성
        df = pd.DataFrame(valid_data)
        df_filtered = remove_outliers_iqr(df)
        
        # RobustScaler를 사용하여 정규화
        scaler = RobustScaler()
        normalized_data = scaler.fit_transform(df_filtered)
        df_normalized = pd.DataFrame(normalized_data, columns=df.columns)
        
        # 정규화된 데이터의 평균과 표준편차 계산
        normalized_means = df_normalized.mean()
        normalized_std = df_normalized.std()
        
        return {
            'normalized_means': normalized_means.to_dict(),
            'standard_deviation': normalized_std.to_dict(),
            'total_frames': len(valid_data),
            'raw_data': df.to_dict(orient='list')
        }
        
    async def process_final_results(self, first_analysis_result, second_analysis_result):
        if not first_analysis_result or not second_analysis_result:
            return {'error': '분석에 필요한 데이터가 부족합니다.'}

        # 감정 변화량 및 통계적 유의성 계산
        emotion_changes = {}
        significant_changes = {}
        for emotion in class_labels:
            first_value = first_analysis_result['normalized_means'].get(emotion, 0)
            second_value = second_analysis_result['normalized_means'].get(emotion, 0)
            change = round(second_value - first_value, 2)
            emotion_changes[emotion] = change

            # 통계적 유의성 검정 (t-test 사용)
            t_statistic, p_value = stats.ttest_ind(
                first_analysis_result['raw_data'][emotion],
                second_analysis_result['raw_data'][emotion]
            )
            if p_value < 0.05:  # 유의수준 0.05
                significant_changes[emotion] = change

        # 감정 변화량의 절대값과 현재 강도를 고려한 점수 계산
        emotion_scores = {}
        for emotion, change in emotion_changes.items():
            current_intensity = second_analysis_result['normalized_means'].get(emotion, 0)
            score = abs(change) * (1 + current_intensity)  # 변화량과 현재 강도를 모두 고려
            emotion_scores[emotion] = round(score, 2)

        # 점수에 따라 정렬
        sorted_emotions = sorted(emotion_scores.items(), key=lambda x: x[1], reverse=True)

        result = {
            'emotion_changes': emotion_changes,
            'significant_changes': significant_changes,
            'emotion_scores': emotion_scores,
            'first_phase_std': first_analysis_result['standard_deviation'],
            'second_phase_std': second_analysis_result['standard_deviation'],
            'frames_analyzed': {
                'first_phase': first_analysis_result['total_frames'],
                'second_phase': second_analysis_result['total_frames']
            }
        }

        # 주감정 선정 (점수가 가장 높고 통계적으로 유의한 변화)
        for emotion, score in sorted_emotions:
            if emotion in significant_changes:
                result['primary_emotion'] = {emotion: score}
                break

        # 부감정 선정 (주감정 점수의 60% 이상이면서 통계적으로 유의한 변화, 최대 2개)
        if 'primary_emotion' in result:
            primary_emotion = list(result['primary_emotion'].keys())[0]
            primary_score = list(result['primary_emotion'].values())[0]
            threshold = primary_score * 0.4
            secondary_emotions = []
            for emotion, score in sorted_emotions:
                if emotion != primary_emotion and score >= threshold and emotion in significant_changes:
                    secondary_emotions.append({emotion: score})
                if len(secondary_emotions) == 2:
                    break
            if secondary_emotions:
                result['secondary_emotions'] = secondary_emotions

        return result
