<!-- components/CameraComponent.vue -->
<template>
  <div class="camera-container">
    <video ref="videoElement" autoplay playsinline style="display: none"></video>
    <canvas ref="canvasElement" style="display: none"></canvas>
    <img 
      ref="imgElement" 
      class="camera-display"
      :src="frameData ? 'data:image/jpeg;base64,' + frameData : ''"
      alt="camera feed"
    />
    <div class="camera-controls">
      <button @click="startStreaming">{{ buttonText }}</button>
    </div>
    <p v-if="emotions" class="emotion-text">감지된 감정: {{ emotions.emotion }}</p>
  </div>
</template>

<script setup>
import { defineEmits } from 'vue';
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

const emit = defineEmits(['capture', 'emotion-detected'])

const startStreaming = async () => {
  mode.value = !mode.value

  if (!mode.value) {
    try {
      buttonText.value = "카메라 중지"
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { 
          width: 640,
          height: 480
        } 
      })
      videoElement.value.srcObject = stream
      videoElement.value.play()

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

      ws.value.onmessage = (event) => {
        const data = JSON.parse(event.data)
        frameData.value = data.frame
        emotions.value = data.emotion
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
}

onUnmounted(() => {
  stopStreaming()
})
</script>

<style scoped>
.camera-container {
  width: 100%;
  max-width: 640px;
  margin: 0 auto;
  text-align: center;
}

.camera-display {
  width: 100%;
  max-width: 640px;
  height: auto;
  border-radius: 8px;
  border: 2px solid #ccc;
  background-color: #f0f0f0;
}

.camera-controls {
  margin-top: 15px;
  display: flex;
  justify-content: center;
  gap: 10px;
}

button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  background-color: #4CAF50;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #45a049;
}

.emotion-text {
  margin-top: 10px;
  font-size: 1.1em;
  color: #333;
}
</style>