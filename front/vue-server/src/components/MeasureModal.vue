<template>
  <Transition :name="useTransition ? 'modal' : ''">
    <div v-if="isOpen" class="modal-overlay">
      <div class="modal-content">
        <h2>Measure Modal</h2>
        <CameraComponent />
        <button @click="completeModal">완료</button>
        <button @click="closeModal">닫기</button>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';
import CameraComponent from './CameraComponent.vue';
defineProps({
  isOpen: Boolean,
  useTransition: Boolean
})

const emit = defineEmits(['close'])

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
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
}

/* 트랜지션 효과 */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

.modal-enter-to,
.modal-leave-from {
  opacity: 1;
  transform: scale(1);
}
</style>