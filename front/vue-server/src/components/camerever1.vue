<template>
  <div class="camera-container">
    <video ref="videoElement" autoplay playsinline></video>
    <canvas ref="canvasElement" style="display: none"></canvas>
    <div class="camera-control">
      <button @click="startCamera">START</button>
      <button @click="stopCamera">STOP</button>
      <button @click="captureImage">SHOOT</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue';
import { defineEmits } from 'vue';

const videoElement = ref(null)
const canvasElement = ref(null)
let stream = null

const emit = defineEmits(['capture'])

const startCamera = async () => {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ 
      video: { 
        width: 640,
        height: 480
      } 
    })
    if (videoElement.value) {
      videoElement.value.srcObject = stream
    }
  } catch (err) {
    console.error("카메라 접근 오류:", err)
    alert("카메라를 시작할 수 없습니다.")
  }
}

const stopCamera = () => {
  if (stream) {
    stream.getTracks().forEach(track => track.stop())
    stream = null
    if (videoElement.value) {
      videoElement.value.srcObject = null
    }
  }
}

const captureImage = () => {
  if (videoElement.value && canvasElement.value) {
    const context = canvasElement.value.getContext('2d')
    canvasElement.value.width = videoElement.value.videoWidth
    canvasElement.value.height = videoElement.value.videoHeight
    context.drawImage(videoElement.value, 0, 0)
    
    const imageData = canvasElement.value.toDataURL('image/jpeg')
    emit('capture', imageData)
  }
}

onUnmounted(() => {
  stopCamera()
})
</script>

<style scoped>

</style>