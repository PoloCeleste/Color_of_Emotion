<template>
  <div>
    <div class="camera-container">
      <video ref="videoElement" autoplay playsinline style="display: none" width="600" height="500"></video>
      <canvas ref="canvasElement" style="display: none" width="600" height="500"></canvas>
      
      <div v-if="showIntroMessages" class="intro-messages">
        <h2>{{ currentMessage }}</h2>
      </div>

      <div class="camera-display" v-else style="width: 400px; height: 300px;" @click="startStreaming">
        <img 
          v-if="frameData" 
          ref="imgElement"
          class="camera-display"
          :src="'data:image/jpeg;base64,' + frameData"
          alt="camera feed"
          style="width: 100%; height: 100%; align-items: center;"
        />
        <h1 class="button" style="text-align: center;">{{ buttonText }}</h1>
      </div>
    </div>

    <p class="emotion-text" style="height: 8px;width: 100%;">
      {{ showIntroMessages ? '측정 준비중' : emotions ? `측정중 (${Math.round(measurementProgress)}%)` : '' }}
    </p>

    <div v-if="isFaceDetected && !showIntroMessages" class="progress-bar">
      <div class="progress" :style="{ width: `${measurementProgress}%` }"></div>
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
const analyzing = ref(false)
const result = ref(null)

const showIntroMessages = ref(false)
const currentMessage = ref("")
const messages = [
  "카메라를 통해 감정을 측정합니다",
  "편안한 자세로 정면을 바라봐주세요",
  "자연스러운 표정을 지어주세요",
  "잠시 후 카메라가 시작됩니다",
  "준비하세요..."
]

const isFaceDetected = ref(false)
const measurementStartTime = ref(null)
const totalMeasurementTime = 5000
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
      emit('status-change', 'measuring')
    }
  }, 1000)
}

const emit = defineEmits(['emotion-detected', 'auto-close'])

const startStreaming = async () => {
  mode.value = !mode.value
  analyzing.value = true
  frameCount.value = 0

  if (!mode.value) {
    try {
      buttonText.value = "카메라 중지"
      showMessages()

      const stream = await navigator.mediaDevices.getUserMedia({ video: true })
      videoElement.value.srcObject = stream
      videoElement.value.play()

      const context = canvasElement.value.getContext("2d")
      const width = videoElement.value.width
      const height = videoElement.value.height
      const delay = 100
      const jpegQuality = 0.7
      const API_URL = process.env.VUE_APP_API_URL

      ws.value = new WebSocket(`ws://${API_URL}/ws/stream/`)
      
      ws.value.onopen = () => {
        console.log("WebSocket connected!!!")
        ws.value.send(JSON.stringify({
          type: "start_analysis"
        }))
      }

      ws.value.onmessage = (event) => {
        const data = JSON.parse(event.data)
        if (data.type === "analysis_result") {
          // 분석 결과를 로컬 스토리지에 저장
          localStorage.setItem('emotionResult', JSON.stringify(data.result))
          result.value = data.result
        } else {
          frameData.value = data.frame
          emotions.value = data.emotion
        }

        if (!showIntroMessages.value) {
          const isCurrentlyDetected = emotions.value.flag === true
          if (isCurrentlyDetected) {
            // 실시간 감정 데이터도 로컬 스토리지에 저장
            localStorage.setItem('currentEmotion', JSON.stringify(emotions.value))
            if (!isFaceDetected.value) {
              isFaceDetected.value = true
              measurementStartTime.value = Date.now()
              measurementProgress.value = 0
            }
            const elapsedTime = Date.now() - measurementStartTime.value
            measurementProgress.value = Math.min((elapsedTime / totalMeasurementTime) * 100, 100)
            if (elapsedTime >= totalMeasurementTime) {
              stopStreaming()
              emit('auto-close')
            }
          } else {
            if (isFaceDetected.value) {
              isFaceDetected.value = false
              measurementStartTime.value = null
              measurementProgress.value = 0
            }
          }
          emit('emotion-detected', data.emotion)
        }
      }

      intervalId.value = setInterval(() => {
        if (!analyzing.value) {
          clearInterval(intervalId.value)
          return
        }

        frameCount.value++
        if (frameCount.value % 5 === 4) return

        context.drawImage(videoElement.value, 0, 0, width, height)
        const imageData = canvasElement.value.toDataURL("image/jpeg", jpegQuality)

        if (ws.value.readyState === WebSocket.OPEN) {
          ws.value.send(JSON.stringify({
            type: "frame",
            data: imageData
          }))
        }
      }, delay)

      setTimeout(() => {
        if (analyzing.value) {
          ws.value.send(JSON.stringify({
            type: "second_phase"
          }))
        }
      }, 5000)

    } catch (err) {
      console.error("카메라 접근 오류:", err)
      alert("카메라를 시작할 수 없습니다.")
    }
  } else {
    stopStreaming()
  }
}

const stopStreaming = () => {
  analyzing.value = false

  if (ws.value && ws.value.readyState === WebSocket.OPEN) {
    ws.value.send(JSON.stringify({
      type: "stop_analysis"
    }))

    if (emotions.value) {
      localStorage.setItem('finalEmotion', JSON.stringify(emotions.value))
    }
  }

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