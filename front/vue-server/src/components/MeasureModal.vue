<template>
  <Transition name="modal">
    <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
      <div class="camera">
        <div class="flash-overlay" ref="flashOverlay"></div>
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
import { defineProps, defineEmits, onMounted, onUnmounted, ref } from 'vue'
import CameraComponent from './CameraComponent.vue'



defineProps({
  isOpen: Boolean
})

const emit = defineEmits(['close', 'complete'])
const originalColor = ref('')

onMounted(() => {
  const startContainer = document.querySelector('.start-container')
  originalColor.value = startContainer.style.backgroundColor
  updateBackgroundColors('#929191')
})

const updateBackgroundColors = (color) => {
  const startContainer = document.querySelector('.start-container')
  const body = document.body
  
  if (startContainer && body) {
    startContainer.style.backgroundColor = color
    body.style.backgroundColor = color
  }
}

const closeModal = () => {
  updateBackgroundColors(originalColor.value)
  emit('close')
}

const flashOverlay = ref(null)

const completeModal = () => {
  // 플래시 효과 실행
  if (flashOverlay.value) {
    flashOverlay.value.classList.add('flash')
    // 플래시 효과가 끝난 후 complete 이벤트 발생
    setTimeout(() => {
      flashOverlay.value.classList.remove('flash')
      emit('complete')
    }, 300)
  }
}

onUnmounted(() => {
  updateBackgroundColors(originalColor.value)
})
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

.flash-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 0;
  height: 0;
  background: radial-gradient(circle, rgba(255,255,255,1) 0%, rgba(255,255,255,0) 70%);
  border-radius: 50%;
  pointer-events: none;
  z-index: 1000;
}

@keyframes flash {
  0% {
    width: 0;
    height: 0;
    opacity: 0;
  }
  10% {
    width: 200%;
    height: 200%;
    opacity: 1;
  }
  100% {
    width: 200%;
    height: 200%;
    opacity: 0;
  }
}

.flash {
  animation: flash 0.5s cubic-bezier(0.11, 0, 0.5, 0) forwards;
}

.camera {
  background: #2a2a2a;
  border-radius: 50%;
  width: 800px;
  height: 800px;
  position: relative;
  box-shadow: 
    0 0 0 8px #353535,
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
  background: #1a1a1a;
  border-radius: 50%;
  box-shadow: 
    0 0 0 8px #404040,
    inset 0 0 40px rgba(0, 0, 0, 0.7);
}

.camera-container {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
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
  position: absolute;
  bottom: 10%;
  left: 50%;
  transform: translateX(-50%);
}

.complete-btn:hover {
  background: #555555;
  transform: translate(-50%, -2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

.modal-enter-active {
  transition: opacity var(--transition-duration) ease;
}

.modal-leave-active {
  transition: opacity var(--transition-duration) ease var(--delay-duration);
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>