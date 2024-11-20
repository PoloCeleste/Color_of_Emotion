<template>
  <!-- 4. 트랜지션 적용 -->
  <transition name="fade">
    <div v-show="isOpen" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h2>Measure Modal</h2>
        <CameraComponent @capture="handleCapture" />
        <div class="button-container">
          <button @click="completeModal">COMPLETE</button>
          <button @click="closeModal">CLOSE</button>
        </div>
      </div>
    </div>
  </transition>
  
</template>

<script setup>
// 2. 측정 모달 띄우기
import { defineProps, defineEmits } from 'vue';
import CameraComponent from './CameraComponent.vue';
defineProps({
  isOpen: Boolean
})

const emit = defineEmits(['close', 'complete'])

const closeModal = () => {
  emit('close')
}

const completeModal = () => {
  emit('complete')
}

// 3. 카메라 연결하기
import { ref } from 'vue'

const capturedImage = ref(null)

const handleCapture = (imageData) => {
  capturedImage.value = imageData
  console.log('이미지가 캡처되었습니다')
}
</script>

<style scoped>
/* 2. 측정 모달 띄우기 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
}

/* 4. 트랜지션 적용 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>