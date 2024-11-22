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
                if not self.is_analyzing: return
                
                self.frame = await self.loop.run_in_executor(None, base64.b64decode, data['data'].split(',')[1])
                
                self.frame, self.emotion_data = await self.loop.run_in_executor(None, self.main, self.frame)
                
                if self.is_second_phase:
                    self.second_phase_data.append(self.emotion_data)
                else:
                    self.first_phase_data.append(self.emotion_data)
                    
            elif message_type == 'second_phase':
                self.is_second_phase = True
                self.first_analysis_result = await self.process_first_results(self.first_phase_data)

            elif message_type == 'stop_analysis':
                self.is_analyzing = False
                self.second_analysis_result = self.process_second_results(self.second_phase_data)
                
                self.finall_analysis_result = self.process_final_results(self.first_analysis_result, self.second_analysis_result)
                
                await self.send(text_data=json.dumps({
                    'type': 'analysis_result',
                    'result': self.finall_analysis_result
                }))


    async def main(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        label=''
        domination=''
        prob=''
        emotion_data=''
        label_position=(90, 10)
        
        display_color = (255, 161, 54)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), display_color, 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

            if np.sum([roi_gray]) != 0:
                roi = tt.functional.to_pil_image(roi_gray)
                roi = tt.functional.to_grayscale(roi)
                roi = tt.ToTensor()(roi).unsqueeze(0)

                # make a prediction on the ROI
                tensor = self.emotion_model(roi)
                probs = {class_labels[i]: round(prob, 2) for i, prob in enumerate(F.softmax(tensor, dim=1).detach().numpy()[0] * 100)}
                # probs = torch.exp(tensor).detach().numpy()
                # prob = np.max(probs) * 100
                pred = torch.max(tensor, dim=1)[1].tolist()
                label = class_labels[pred[0]]#('{} ({:.0f}%)'.format(class_labels[pred[0]], prob))
                prob={}
                for p in probs.keys():
                    prob[p]=round(float(probs[p]),2)
                    if p==label:
                        domination = {label:prob[label]}
                        label="Face Detected"
                print(label)
                print(prob)
                flag=True

        else:
            if not label:
                label='No Face Found'
                display_color = (0, 255, 0)
                flag=False
                # SUPPORT_UTF8 = True
                # if SUPPORT_UTF8:
        font_path = pth.join(getcwd(), assets, 'NotoSansKR-Regular.otf')
        font = ImageFont.truetype(font_path, 32)
        img_pil = Image.fromarray(frame)
        draw = ImageDraw.Draw(img_pil)
        draw.text(label_position, label, font=font, fill=display_color)
        frame = np.array(img_pil)

        if domination:
            emotion_data = {
                'domination':domination,
                'emotion':prob,
                'flag':flag
            }
        return frame, emotion_data

    async def process_first_results(self, first_phase_data):
        pass
    
    def process_first_results(self, second_phase_data):
        pass
    
    def process_first_results(self, first_analysis_result, second_analysis_result):
        pass