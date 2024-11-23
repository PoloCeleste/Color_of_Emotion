<template>
  <Transition name="modal">
    <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
      <div class="camera">
        <div class="lens">
          <CameraComponent />
        </div>
        <div class="controls">
          <button class="complete-btn" @click="completeModal">COMPLETE</button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";
import CameraComponent from "./CameraComponent.vue";

// Props와 Emits 정의
defineProps({
  isOpen: Boolean,
});

const emit = defineEmits(["close", "complete"]);

// 모달 닫기
const closeModal = () => {
  emit("close");
};

// 감정 측정 완료
const completeModal = () => {
  emit("complete");
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.camera {
}

.lens {
}
</style>