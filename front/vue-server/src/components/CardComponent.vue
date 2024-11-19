<template>
  <div class="card" :class="{ 'with-transition': useTransition }">
    <div class="image-wrapper aspect-video">
      <img class="aspect-video" :src="card.image" :alt="card.title">
    </div>
    <div class="details">
      <h3>{{ card.title }}</h3>
      <span>{{ card.subtitle }}</span>
      <p>{{ card.description }}</p>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
defineProps({
  card: Object,
  useTransition: Boolean
})
</script>

<style scoped>
.card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card.with-transition:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.image-wrapper img {
  transition: transform 0.3s ease;
}

.card.with-transition:hover .image-wrapper img {
  transform: scale(1.1);
}

/* ... (기타 필요한 스타일) */
</style>