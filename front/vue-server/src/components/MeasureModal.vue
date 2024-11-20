<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <div class="camera-container">
        <CameraComponent />
      </div>
      <div class="button-container">
        <button @click="completeModal">COMPLETE</button>
        <button @click="closeModal">CLOSE</button>
      </div>
    </div>
  </div>
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
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  /* background-color: rgba(0, 0, 0, 0.5); */
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: whitesmoke;
  padding: 20px;
  border: 2px solid darkgray;
  border-radius: 50%;  /* 원형으로 변경 */
  width: 800px;  /* StartView의 원보다 더 크게 */
  height: 800px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  justify-content: center;
  align-items: center;
}

.camera-container {
  position: relative;
  width: 90%;  /* 모달 내부 여백 확보 */
  height: 90%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

.button-container {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

/* 원형 테두리 애니메이션 */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.5s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
  transform: translate(-50%, -50%) scale(0.67);  /* StartView의 원 크기(400px)로 축소 */
}

.modal-enter-to,
.modal-leave-from {
  opacity: 1;
  transform: translate(-50%, -50%) scale(1);
}
</style>