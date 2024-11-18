<template>
  <transition name="modal">
    <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <button @click="closeModal" class="close-button">&times;</button>
        <h2>{{ cardData.title }}</h2>
        <img :src="cardData.image" :alt="cardData.title" class="modal-image">
        <p>{{ cardData.description }}</p>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';
defineProps({
  isOpen: Boolean,
  cardData: Object
})

const emit = defineEmits(['close'])

const closeModal = () => {
  emit('close')
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
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  max-width: 500px;
  position: relative;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 24px;
  cursor: pointer;
  background: none;
  border: none;
  color: #333;
}

.modal-image {
  width: 100%;
  max-height: 300px;
  object-fit: cover;
  border-radius: 5px;
  margin-bottom: 10px;
}

/* 트랜지션 효과 */
.modal-enter-active, .modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from, .modal-leave-to {
  opacity: 0;
}
</style>