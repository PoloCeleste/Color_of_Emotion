<template>
  <div class="movie-cards">
    <div
      v-for="(movie, index) in selectedMovies"
      :key="index"
      class="movie-card"
      @click="openModal(movie)"
    >
      <div class="movie-card__inner" ref="cardInners">
        <div class="movie-card__image">
          <img :src="movie.poster_path" :alt="movie.title" />
        </div>
      </div>
    </div>
    <CardModal
      v-if="selectedMovie"
      :movie="selectedMovie"
      :isActive="isModalActive"
      @close="closeModal"
    />
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import { useMovieStore } from "@/store/stores";
import CardModal from "./CardModal.vue";

const movieStore = useMovieStore();
const selectedMovies = ref([]);
const selectedMovie = ref(null);
const isModalActive = ref(false);

watch(
  () => movieStore.recommendedMovies,
  (newMovies) => {
    selectedMovies.value = newMovies.slice(48, 51);
  },
  { immediate: true }
);

const openModal = (movie) => {
  selectedMovie.value = movie;
  isModalActive.value = true;
};

const closeModal = () => {
  isModalActive.value = false;
  setTimeout(() => {
    selectedMovie.value = null;
  }, 300); // 애니메이션 종료 후 선택된 영화 초기화
};
</script>

<style scoped>
.movie-cards {
  margin: auto 0;
  width: 90%;
  max-width: 1560px; /* 1200px에서 1800px로 증가 */
  display: flex;
  justify-content: center;
  gap: 3rem; /* 2rem에서 3rem으로 증가하여 카드 간 간격 확대 */
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.movie-card {
  cursor: pointer;
  flex: 0 0 auto;
  width: 390px; /* 300px에서 450px로 1.5배 증가 */
  height: 520px; /* 400px에서 600px로 1.5배 증가 */
  margin: 15px; /* 10px에서 15px로 증가 */
  transition: transform 0.3s ease;
}

.movie-card:hover {
  transform: scale(1.05);
}

.movie-card__inner {
  width: 100%;
  height: 100%;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
  background-color: rgba(255, 255, 255, 0.85);
  border-radius: 8px;
  overflow: hidden;
  will-change: transform;
  transition: border-radius 0.3s ease;
  position: relative;
  border: 2px solid rgba(255, 255, 255, 0.1);
}

.movie-card__inner::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.3);
  z-index: 1;
  transition: opacity 0.3s ease;
}

.movie-card:hover .movie-card__inner::before {
  opacity: 0;
}

.movie-card__image {
  width: 100%;
  height: 100%;
  overflow: hidden;
  position: relative;
  transition: all 0.3s ease;
  z-index: 2;
}

.movie-card__image > img {
  will-change: transform;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  -o-object-fit: cover;
  object-fit: cover;
  -o-object-position: center center;
  object-position: center center;
  transition: transform 0.3s;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.85);
  opacity: 0;
  transition: opacity 0.4s ease;
  animation: fadeIn 0.4s ease forwards;
  z-index: 98;
}

.content {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  pointer-events: none;
  z-index: 101;
}

.content__group {
  opacity: 0;
  position: fixed;
  top: 0;
  right: 0;
  width: 50vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  z-index: 102;
  padding: 4rem;
  color: rgb(38, 38, 40);
  border-radius: 30px 0 0 30px;
  transition: opacity 0.3s ease;
}

.modal-content {
  display: flex;
  width: 100vw;
  height: 100vh;
  background: transparent;
  z-index: 191;
}

.modal-image {
  flex: 0 0 50%;
  height: 100%;
}

.modal-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.modal-info {
  flex: 1;
  padding: 4rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.content__heading {
  font-size: 2.5rem;
  margin-bottom: 1.5rem;
}

.content__description {
  margin-top: 1rem;
  font-size: 1.2rem;
  line-height: 1.8;
  color: rgba(0, 0, 0, 0.9);
}

.close-button {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 24px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s;
  z-index: 94;
  transition: all 0.3s ease;
  transform: scale(1);
}

.close-button:hover {
  transform: scale(1.1);
  background: rgba(255, 255, 255, 0.4);
}

.modal-info::-webkit-scrollbar {
  width: 8px;
}

.modal-info::-webkit-scrollbar-track {
  background: transparent;
}

.modal-info::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
}

.movie-card.is-active .movie-card__inner {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 99;
  border-radius: 0;
}

.movie-card.is-active .movie-card__image {
  width: 50vw;
  height: 100vh;
}
</style>