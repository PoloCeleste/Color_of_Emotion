<template>
  <div>
    <div class="camera-container">
      <video ref="videoElement" autoplay playsinline style="display: none" width="600" height="500"></video>
      <canvas ref="canvasElement" style="display: none" width="600" height="500"></canvas>
      <!-- 초기 멘트 div -->
      <div v-if="showIntroMessages" class="intro-messages">
        <h2>{{ currentMessage }}</h2>
      </div>
      <!-- 카메라 화면 -->
      <div class="camera-display" v-else style="width: 400px; height: 300px;" @click="startStreaming">
        <img 
          v-if="frameData"
          ref="imgElement" 
          class="camera-display"
          :src="frameData ? 'data:image/jpeg;base64,' + frameData : ''"
          alt="camera feed"
          style="width: 100%; height: 100%; align-items: center;"
        />
        <h1 class="button" style="text-align: center;">{{ buttonText }}</h1>
      </div>
    </div>
    <!-- <p v-if="emotions" class="emotion-text">감지된 감정: {{ emotions.emotion }}</p> -->
    <!-- 상태 메시지 수정 -->
    <p class="emotion-text" style="height: 8px;width: 100%;">
      {{ showIntroMessages ? '측정 준비중' : emotions ? `측정중 (${Math.round(measurementProgress)}%)`  : '' }}
    </p>

    <!-- 선택적: 진행률 표시 바 추가 -->
    <div v-if="isFaceDetected && !showIntroMessages" class="progress-bar">
      <div 
        class="progress" 
        :style="{ width: `${measurementProgress}%` }"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { defineEmits } from 'vue'
import { ref, onUnmounted } from 'vue'

const videoElement = ref(null)
const canvasElement = ref(null)
const imgElement = ref(null)
const mode = ref(true)
const ws = ref(null)
const intervalId = ref(null)
const frameCount = ref(0)
const frameData = ref("")
const emotions = ref(null)
const buttonText = ref("카메라 시작")

// 표시할 멘트 배열
const showIntroMessages = ref(false)
const currentMessage = ref("")

const messages = [
  "카메라를 통해 감정을 측정합니다",
  "편안한 자세로 정면을 바라봐주세요",
  "자연스러운 표정을 지어주세요",
  "잠시 후 카메라가 시작됩니다",
  "준비하세요..."
]

// 얼굴인식 5초후에 종료하기
// 얼굴 인식 상태 및 타이머 관리를 위한 ref 추가
const isFaceDetected = ref(false)
const measurementStartTime = ref(null)
const totalMeasurementTime = 5000 // 5초
const measurementProgress = ref(0)

const showMessages = () => {
  showIntroMessages.value = true
  let messageIndex = 0
  
  const messageInterval = setInterval(() => {
    if (messageIndex < messages.length) {
      currentMessage.value = messages[messageIndex]
      messageIndex++
    } else {
      clearInterval(messageInterval)
      showIntroMessages.value = false
      // 측정 중 상태 알림
      emit('status-change', 'measuring')
    }
    
  }, 1000) // 1초마다 메시지 변경
}

// 카메라 작동 5초 후 자동으로 꺼짐
// const emit = defineEmits(['emotion-detected'])
const emit = defineEmits(['emotion-detected', 'auto-close'])
// const measurementTimer = ref(null)

const startStreaming = async () => {
  mode.value = !mode.value

  if (!mode.value) {
    try {
      buttonText.value = "카메라 중지"
      showMessages() // 메시지 표시 시작

      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: true 
      })
      videoElement.value.srcObject = stream
      videoElement.value.play()

      // // 메시지 표시가 끝나고 5초 후에 자동 종료
      // const totalMessageTime = messages.length * 1000 // 메시지 표시 시간
      // measurementTimer.value = setTimeout(() => {
      //   stopStreaming()
      //   emit('auto-close') // 부모 컴포넌트에 자동 종료 신호 전송
      // }, totalMessageTime + 5000) // 메시지 표시 시간 + 5초

      const context = canvasElement.value.getContext("2d")
      const width = videoElement.value.width
      const height = videoElement.value.height
      const delay = 100
      const jpegQuality = 0.7

      // WebSocket 연결
      ws.value = new WebSocket("ws://192.168.201.124:8000/ws/stream/")

      ws.value.onopen = () => {
        console.log("WebSocket 연결됨")
      }

      // 카메라 작동 5초 후 자동으로 꺼짐
      // WebSocket 메시지 핸들러 수정

      // ws.value.onmessage = (event) => {
      //   const data = JSON.parse(event.data)
      //   frameData.value = data.frame
      //   emotions.value = data.emotion
      //   console.log(emotions.value.flag)
      //   emit('emotion-detected', data.emotion)
      // }
      
      ws.value.onmessage = (event) => {
        const data = JSON.parse(event.data)
        frameData.value = data.frame
        emotions.value = data.emotion

      // 얼굴이 인식되었는지 확인 (이 부분은 서버에서 보내주는 데이터 형식에 따라 수정 필요)
      if (!showIntroMessages.value) {
        const isCurrentlyDetected = emotions.value.flag === true
        
        if (isCurrentlyDetected) {
          if (!isFaceDetected.value) {
            // 얼굴이 새로 인식되었을 때
            isFaceDetected.value = true
            measurementStartTime.value = Date.now()
            measurementProgress.value = 0 // 진행률 초기화
            console.log('얼굴 인식 시작')
          }
          
          // 측정 진행 시간 계산
          const elapsedTime = Date.now() - measurementStartTime.value
          measurementProgress.value = Math.min((elapsedTime / totalMeasurementTime) * 100, 100)
          
          // 5초 측정 완료 시
          if (elapsedTime >= totalMeasurementTime) {
            console.log('측정 완료')
            stopStreaming()
            emit('auto-close')
          }
        } else {
          // // 얼굴이 인식되지 않을 때
          // if (isFaceDetected.value) {
          //   // 측정 중이었다면 타이머 일시 정지
          //   measurementStartTime.value = null
          //   isFaceDetected.value = false
          //   console.log('얼굴 인식 중단')

          // 얼굴이 인식되지 않을 때 타이머 완전 초기화
          if (isFaceDetected.value) {
            isFaceDetected.value = false
            measurementStartTime.value = null
            measurementProgress.value = 0
            console.log('얼굴 인식 실패: 타이머 초기화')
          }
        }
      }
        emit('emotion-detected', data.emotion)
      }

      intervalId.value = setInterval(() => {
        if (frameCount.value % 5 !== 4) {
          context.drawImage(videoElement.value, 0, 0, width, height)
          canvasElement.value.toBlob(
            (blob) => {
              if (ws.value.readyState === WebSocket.OPEN) {
                ws.value.send(mode.value ? new Uint8Array([]) : blob)
              }
            },
            "image/jpeg",
            jpegQuality
          )
        }
        frameCount.value++
      }, delay)

    } catch (err) {
      console.error("카메라 접근 오류:", err)
      alert("카메라를 시작할 수 없습니다.")
    }
  } else {
    stopStreaming()
  }
}

const stopStreaming = () => {
  if (videoElement.value?.srcObject) {
    videoElement.value.srcObject.getTracks().forEach(track => track.stop())
    videoElement.value.srcObject = null
  }
  
  if (ws.value) {
    ws.value.close()
  }

  clearInterval(intervalId.value)
  mode.value = true
  frameCount.value = 0
  buttonText.value = "카메라 시작"
  frameData.value = ""
  emotions.value = null

  // 카메라 작동 5초 후 자동으로 꺼짐
  // 측정 관련 상태 초기화
  isFaceDetected.value = false
  measurementStartTime.value = null
  measurementProgress.value = 0
}

onUnmounted(() => {
  stopStreaming()
})
</script>

<style scoped>
.camera-container {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

.camera-display {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  max-width: 640px;
  height: auto;
  border-radius: 8px;
  border: 2px solid #ccc;
  background-color: #f0f0f0;
}

button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  background-color: #4CAF50;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

button:hover {
  transform: scale(1.1);
  color: #4CAF50;
}

.emotion-text {
  position: absolute;
  top: 70%;
  left: 50%;
  margin-top: 10px;
  font-size: 1.1em;
  color: #333;
}

/* 메세지 스타일 추가 */
.intro-messages {
  width: 400px;
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f0f0f0;
  border-radius: 8px;
  border: 2px solid #ccc;
  margin: 0 auto;
}

.intro-messages h2 {
  color: #333;
  text-align: center;
  padding: 20px;
  font-size: 1.5em;
}
</style>