<template>
  <div class="movie-card" :style="{ animationDelay: `${delay}s` }">
    <img :src="movie.poster_path" :alt="movie.title" />
    <div class="movie-info">
      <h3>{{ movie.title }}</h3>
      <div class="rating">⭐ {{ movie.tmdb_vote_average }}</div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from "vue";
defineProps({
  movie: {
    type: Object,
    required: true,
  },
  delay: {
    type: Number,
    required: true,
  },
});
</script>

<style scoped>
.movie-card {
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.5s ease forwards;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  overflow: hidden;
  backdrop-filter: blur(10px);
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.movie-info {
  padding: 1rem;
  color: white;
}

.movie-info h3 {
  margin: 0;
  font-size: 1rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.rating {
  margin-top: 0.5rem;
  font-size: 0.9rem;
}

.movie-card img {
  width: 100%;
  aspect-ratio: 2/3;
  object-fit: cover;
}
</style>
