<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal-content" @click.stop>
      <button class="close-button" @click="$emit('close')">×</button>
      <div class="modal-image">
        <img :src="movie.poster_path" :alt="movie.title" />
      </div>
      <div class="modal-info">
        <h2 class="content__heading">{{ movie.title }}</h2>
        <span class="content__category">{{ movie.genre_ids.join(", ") }}</span>
        <p class="content__description">{{ movie.overview }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

defineProps({
  movie: {
    type: Object,
    required: true
  }
});

defineEmits(['close']);
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  width: 80%;
  max-width: 1000px;
  height: 80%;
  display: flex;
  border-radius: 8px;
  overflow: hidden;
}

.modal-image {
  flex: 0 0 40%;
  overflow: hidden;
}

.modal-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.modal-info {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}

.close-button {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  font-size: 2rem;
  color: white;
  cursor: pointer;
}

/* 나머지 스타일은 기존 코드에서 가져와 필요에 따라 조정 */
</style>