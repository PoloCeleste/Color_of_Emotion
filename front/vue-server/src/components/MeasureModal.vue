<template>
  <Transition name="modal" :duration="transitionDuration">
    <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <div class="camera-container">
          <CameraComponent />
        </div>
        <div class="button-container">
          <button @click="completeModal">COMPLETE</button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { defineProps, defineEmits, onMounted, onUnmounted, ref } from 'vue';
import CameraComponent from './CameraComponent.vue';

defineProps({
  isOpen: Boolean
});

const emit = defineEmits(['close', 'complete']);

const transitionDuration = 500; // 트랜지션 시간 (밀리초)
const backgroundTransitionDuration = 2000; // 배경색 트랜지션 시간 (밀리초)

const originalColor = ref('');
const originalBodyColor = ref('');

onMounted(() => {
  const startContainer = document.querySelector('.start-container');
  originalColor.value = startContainer.style.backgroundColor;
  originalBodyColor.value = document.body.style.backgroundColor;
  
  updateBackgroundColors('#929191');
});

const updateBackgroundColors = (color) => {
  const startContainer = document.querySelector('.start-container');
  [startContainer, document.body].forEach(el => {
    el.style.transition = `background-color ${backgroundTransitionDuration}ms ease`;
    el.style.backgroundColor = color;
  });
};

const closeModal = () => {
  updateBackgroundColors(originalColor.value);
  emit('close');
};

const completeModal = () => emit('complete');

onUnmounted(() => {
  updateBackgroundColors(originalColor.value);
});
</script>

<style scoped>
:root {
  --transition-duration: v-bind(transitionDuration);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  /* background-color: rgba(0, 0, 0, 0.7); */
}

.modal-content {
  z-index: 1001;
  background-color: whitesmoke;
  padding: 20px;
  border: 2px solid darkgray;
  border-radius: 50%;
  width: 800px;
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
  width: 90%;
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

.modal-enter-active,
.modal-leave-active {
  transition: opacity var(--transition-duration) ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>