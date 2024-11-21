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


assets=pth.join('emotion_server', 'assets')
#class_labels = ['happy', 'suprise', 'angry', 'anxious', 'hurt', 'sad', 'neutral']
class_labels = ['기쁨', '당황', '분노', '불안', '상처', '슬픔', '중립']
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
model = getModel('emotionnet')
model.load_state_dict(model_state['model'])

class VideoStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.prev = 0
        self.new = 0
        self.loop = asyncio.get_running_loop()
        await self.accept()

    async def disconnect(self, close_code):
        self.prev = 0
        self.new = 0
        raise StopConsumer()

    async def receive(self, bytes_data):
        if not (bytes_data):
            self.prev = 0
            self.new = 0
            print('Closed connection')
            await self.close()
        else:
            # 바이트 데이터를 numpy 배열로 변환
            self.frame = await self.loop.run_in_executor(None, cv2.imdecode, np.frombuffer(bytes_data, dtype=np.uint8), cv2.IMREAD_COLOR)
            # nparr = np.frombuffer(bytes_data, np.uint8)
            # self.frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            # OpenCV를 사용한 이미지 처리
            self.frame, self.emotion_data = await self.loop.run_in_executor(None, self.main, self.frame)
            # cv2.imshow("dd", processed_frame)
            # await self.fps_count()
            # cv2.putText(self.frame, "FPS: {}".format((self.fps)), (50,40),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (54, 161, 255), 1)
            # 처리된 프레임을 클라이언트로 다시 전송
            self.buffer = await self.loop.run_in_executor(None, cv2.imencode, '.jpeg', self.frame)
            self.b64_img = base64.b64encode(self.buffer[1]).decode('utf-8')
            data={
                'frame':self.b64_img,
                'emotion':self.emotion_data
            }
            
            asyncio.sleep(100/1000)
            await self.send(json.dumps(data))


    def softmax(x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()


    def main(self, frame):
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
                tensor = model(roi)
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

                # SUPPORT_UTF8 = True
                # if SUPPORT_UTF8:
                # font_path = pth.join(getcwd(), assets, 'NotoSansKR-Regular.otf')
                # font = ImageFont.truetype(font_path, 32)
                # img_pil = Image.fromarray(frame)
                # draw = ImageDraw.Draw(img_pil)
                # draw.text(label_position, label, font=font, fill=display_color)
                # frame = np.array(img_pil)
                # else:
                #     cv2.putText(frame, label, label_position,
                #     cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 3)
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
                # else:
                    # cv2.putText(frame, 'No Face Found', (120, 10),
                            # cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 3)
        if domination:
            emotion_data = {
                'domination':domination,
                'emotion':prob,
                'flag':flag
            }
        return frame, emotion_data
