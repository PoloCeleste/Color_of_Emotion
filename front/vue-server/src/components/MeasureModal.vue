<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
    <div class="camera">
      <div class="lens">
        <CameraComponent @measurement-complete="handleMeasurementComplete" />
      </div>
      <div class="controls">
        <button class="complete-btn" @click="completeModal">COMPLETE</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, onMounted, onUnmounted, ref } from "vue";
import CameraComponent from "./CameraComponent.vue";

defineProps({
  isOpen: Boolean,
});

const emit = defineEmits(["close", "complete"]);

// CameraComponent에서 측정 완료 이벤트를 받아 처리
const handleMeasurementComplete = (result) => {
  emit("complete", result);
};

const backgroundTransitionDuration = 2000;
const originalColor = ref("");
const originalBodyColor = ref("");

onMounted(() => {
  const startContainer = document.querySelector(".start-container");
  originalColor.value = startContainer.style.backgroundColor;
  originalBodyColor.value = document.body.style.backgroundColor;
});

const updateBackgroundColors = (color) => {
  const startContainer = document.querySelector(".start-container");
  [startContainer, document.body].forEach((el) => {
    el.style.transition = `background-color ${backgroundTransitionDuration}ms ease`;
    el.style.backgroundColor = color;
  });
};

const closeModal = () => {
  updateBackgroundColors(originalColor.value);
  emit("close");
};

const completeModal = () => emit("complete");

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
  background-color: rgba(0, 0, 0, 0.5);
  transition: background-color 0.3s ease;
}

.camera {
  background: linear-gradient(145deg, #2a2a2a, #1a1a1a);
  border-radius: 50%;
  width: 800px;
  height: 800px;
  position: relative;
  box-shadow: 0 0 0 8px #353535, 0 0 0 16px #454545, 0 0 0 24px #555555,
    0 0 100px rgba(0, 0, 0, 0.5);
}

.lens {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 70%;
  height: 70%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(145deg, #1a1a1a, #0a0a0a);
  border-radius: 50%;
  box-shadow: 0 0 0 8px #404040, inset 0 0 40px rgba(0, 0, 0, 0.7);
}

.controls {
  position: absolute;
  bottom: 10%;
  left: 50%;
  transform: translateX(-50%);
}

.complete-btn {
  padding: 12px 24px;
  background: linear-gradient(145deg, #454545, #353535);
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 1.2em;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transform: translateZ(0);
  backface-visibility: hidden;
  -webkit-font-smoothing: antialiased;
  will-change: transform;
}

.complete-btn:hover {
  background: linear-gradient(145deg, #555555, #454545);
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}
</style>
