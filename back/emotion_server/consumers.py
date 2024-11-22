import asyncio, base64, time
import cv2
import numpy as np
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from PIL import Image, ImageFont, ImageDraw
from os import path as pth, getcwd
import torch, json
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as tt
from .models import *

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

face_classifier = cv2.CascadeClassifier(pth.join(getcwd(), assets,'face_classifier.xml'))


display_color = (86, 189, 246)

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
                self.is_second_phase = True
                self.first_analysis_result = await self.process_first_results(self.first_phase_data)

            elif message_type == 'stop_analysis':
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

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        label = ''
        domination = ''
        prob = ''
        emotion_data = ''
        label_position = (90, 10)
        
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
                probs = {class_labels[i]: round(prob, 2) for i, prob in enumerate(F.softmax(tensor, dim=1).detach().numpy()[0] * 100)}
                pred = torch.max(tensor, dim=1)[1].tolist()
                label = class_labels[pred[0]]
                prob = {}
                for p in probs.keys():
                    prob[p] = round(float(probs[p]), 2)
                    if p == label:
                        domination = {label: prob[label]}
                        label = "Face Detected"
                print(label)
                print(prob)
                flag = True
        else:
            if not label:
                label = 'No Face Found'
                display_color = (0, 255, 0)
                flag = False

        font_path = pth.join(getcwd(), assets, 'NotoSansKR-Regular.otf')
        font = ImageFont.truetype(font_path, 32)
        img_pil = Image.fromarray(frame)
        draw = ImageDraw.Draw(img_pil)
        draw.text(label_position, label, font=font, fill=display_color)
        frame = np.array(img_pil)

        # 프레임을 base64로 인코딩
        _, buffer = cv2.imencode('.jpg', frame)
        frame_base64 = base64.b64encode(buffer).decode('utf-8')

        if domination:
            emotion_data = {
                'domination': domination,
                'emotion': prob,
                'flag': flag
            }
        return frame_base64, emotion_data

    async def process_first_results(self, first_phase_data):
        """첫 번째 단계의 감정 데이터 처리"""
        if not first_phase_data:
            return {}
        
        # 감정별 데이터 누적
        emotion_counts = {label: 0 for label in class_labels}
        total_frames = 0
        dominant_emotions = []
        
        for data in first_phase_data:
            if data and 'emotion' in data:
                emotions = data['emotion']
                for emotion, value in emotions.items():
                    emotion_counts[emotion] += value
                if 'domination' in data:
                    dominant_emotions.append(list(data['domination'].keys())[0])
                total_frames += 1
        
        if total_frames > 0:
            # 각 감정의 평균값 계산
            avg_emotions = {
                emotion: round(count/total_frames, 2) 
                for emotion, count in emotion_counts.items()
            }
            
            # 가장 많이 감지된 지배적 감정 찾기
            if dominant_emotions:
                from collections import Counter
                most_common = Counter(dominant_emotions).most_common(1)[0]
                main_emotion = {most_common[0]: round(most_common[1]/total_frames * 100, 2)}
            else:
                main_emotion = {}
            
            return {
                'main_emotion': main_emotion,
                'average_emotions': avg_emotions,
                'total_frames': total_frames
            }
        return {}

    async def process_second_results(self, second_phase_data):
        """두 번째 단계의 감정 데이터 처리"""
        if not second_phase_data:
            return {}
        
        # 첫 번째 단계와 동일한 처리 로직 사용
        emotion_counts = {label: 0 for label in class_labels}
        total_frames = 0
        dominant_emotions = []
        
        for data in second_phase_data:
            if data and 'emotion' in data:
                emotions = data['emotion']
                for emotion, value in emotions.items():
                    emotion_counts[emotion] += value
                if 'domination' in data:
                    dominant_emotions.append(list(data['domination'].keys())[0])
                total_frames += 1
        
        if total_frames > 0:
            avg_emotions = {
                emotion: round(count/total_frames, 2) 
                for emotion, count in emotion_counts.items()
            }
            
            if dominant_emotions:
                from collections import Counter
                most_common = Counter(dominant_emotions).most_common(1)[0]
                main_emotion = {most_common[0]: round(most_common[1]/total_frames * 100, 2)}
            else:
                main_emotion = {}
                
            return {
                'main_emotion': main_emotion,
                'average_emotions': avg_emotions,
                'total_frames': total_frames
            }
        return {}

    async def process_final_results(self, first_analysis_result, second_analysis_result):
        """두 단계의 분석 결과를 비교하여 최종 결과 생성"""
        if not first_analysis_result or not second_analysis_result:
            return {
                'status': 'error',
                'message': '분석에 필요한 데이터가 부족합니다.'
            }
        
        # 감정 변화량 계산
        emotion_changes = {}
        for emotion in class_labels:
            first_value = first_analysis_result['average_emotions'].get(emotion, 0)
            second_value = second_analysis_result['average_emotions'].get(emotion, 0)
            emotion_changes[emotion] = round(second_value - first_value, 2)
        
        # 가장 큰 변화를 보인 감정 찾기
        max_change_emotion = max(emotion_changes.items(), key=lambda x: abs(x[1]))
        
        return {
            'first_phase': {
                'main_emotion': first_analysis_result['main_emotion'],
                'emotions': first_analysis_result['average_emotions']
            },
            'second_phase': {
                'main_emotion': second_analysis_result['main_emotion'],
                'emotions': second_analysis_result['average_emotions']
            },
            'emotion_changes': emotion_changes,
            'most_changed_emotion': {
                'emotion': max_change_emotion[0],
                'change': max_change_emotion[1]
            },
            'frames_analyzed': {
                'first_phase': first_analysis_result['total_frames'],
                'second_phase': second_analysis_result['total_frames']
            }
        }