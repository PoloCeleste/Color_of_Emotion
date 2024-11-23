<template>
  <Transition name="modal" :duration="transitionDuration">
    <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
      <div class="camera">
        <div class="lens">
          <div class="camera-container">
            <CameraComponent />
          </div>
        </div>
        <div class="controls">
          <button class="complete-btn" @click="completeModal">COMPLETE</button>
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
}

.camera {
  background: #2a2a2a;
  border-radius: 50%;
  width: 800px;
  height: 800px;
  position: relative;
  box-shadow: 
    0 0 0 8px #353535,  /* 간격 축소 */
    0 0 0 16px #454545,
    0 0 0 24px #555555,
    0 0 100px rgba(0, 0, 0, 0.5);
}

.lens {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 70%;
  height: 70%;
  background: #1a1a1a;  /* 더 어두운 색상 */
  border-radius: 50%;
  box-shadow: 
    0 0 0 8px #404040,  /* 간격 축소 */
    inset 0 0 40px rgba(0, 0, 0, 0.7);
}

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
  width: 80%;  /* 렌즈에 맞춰 크기 조정 */
  height: 80%;
  border-radius: 50%;
  border: 2px solid #404040;
  background-color: #1a1a1a;
  overflow: hidden;
}

.camera-display img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: saturate(70%);  /* grayscale 대신 채도 낮추기 */
}

.controls {
  position: absolute;
  bottom: 10%;
  left: 50%;
  transform: translateX(-50%);
}

.complete-btn {
  padding: 12px 24px;
  background: #454545;
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 1.2em;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.complete-btn:hover {
  background: #555555;
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity var(--transition-duration) ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.intro-messages {
  width: 400px;
  height: 400px; /* 정사각형으로 변경 */
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #2a2a2a;
  border-radius: 50%;
  border: 2px solid #555;
  margin: 0 auto;
  color: #e0e0e0;
}

.intro-messages h2 {
  color: #e0e0e0;
  text-align: center;
  padding: 20px;
  font-size: 1.5em;
}

.emotion-text {
  position: absolute;
  top: 70%;
  left: 50%;
  margin-top: 10px;
  font-size: 1.1em;
  color: #e0e0e0;
}
</style>