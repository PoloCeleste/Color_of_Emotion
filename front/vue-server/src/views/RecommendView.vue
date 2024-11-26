<template>
  <div class='recommend-container'>
    <div class="film-container" ref="filmStrip">
      <div class="film-strip-container">
        <div class="film-strip-row">
          <div v-for="movie in firstRow" :key="movie.id" class="movie-poster">
            <img :src="movie.poster_path" :alt="movie.title" />
          </div>
        </div>
        <div class="film-strip-row">
          <div v-for="movie in secondRow" :key="movie.id" class="movie-poster">
            <img :src="movie.poster_path" :alt="movie.title" />
          </div>
        </div>
      </div>
    </div>
    <button @click="toggleAnimation">{{ isAnimating ? '정지' : '시작' }}</button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { useMovieStore } from '@/store/stores';

const movieStore = useMovieStore();
const filmStrip = ref(null);
const isAnimating = ref(true);
let animationId = null;
let startTime = null;
const duration = 60000; // 60초

const firstRow = computed(() => movieStore.recommendedMovies.slice(0, 24));
const secondRow = computed(() => movieStore.recommendedMovies.slice(24, 48));

const animate = (timestamp) => {
  if (!startTime) startTime = timestamp;
  const elapsed = timestamp - startTime;
  const progress = (elapsed % duration) / duration;
  
  if (filmStrip.value) {
    filmStrip.value.style.transform = `translateX(${-progress * 50}%)`;
  }

  if (isAnimating.value) {
    animationId = requestAnimationFrame(animate);
  }
};

const toggleAnimation = () => {
  isAnimating.value = !isAnimating.value;
  if (isAnimating.value) {
    startTime = null;
    animationId = requestAnimationFrame(animate);
  } else {
    cancelAnimationFrame(animationId);
  }
};

onMounted(() => {
  if (movieStore.recommendedMovies.length === 0) {
    movieStore.getMovieRecommendations();
  }
  animationId = requestAnimationFrame(animate);
});

onUnmounted(() => {
  cancelAnimationFrame(animationId);
});

watch(() => movieStore.recommendedMovies, (newMovies) => {
  if (newMovies.length > 0) {
    // 영화 데이터가 로드되면 애니메이션 재시작
    cancelAnimationFrame(animationId);
    startTime = null;
    animationId = requestAnimationFrame(animate);
  }
});
</script>

<style scoped>
.recommend-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

.film-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 200%;
  height: 100%;
  
  --s: 20px;
  --c: #222;
  background: 
    conic-gradient(at 50% var(--s), var(--c) 75%, #0000 0) 0 0 /
    calc(2 * var(--s)) calc(100% - var(--s)) padding-box;
  border: var(--s) solid var(--c);
  box-sizing: border-box;
}

.film-strip-container {
  position: absolute;
  top: 10%;
  left: 0;
  width: 100%;
  height: 80%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}


.film-strip-row {
  width: 100%;
  height: 40vh;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  overflow: hidden;
  margin: 0.25vh;
}

.film-strip-row:first-child {
  top: 10vh; /* 첫 번째 줄 위치 조정 */
}

.film-strip-row:last-child {
  bottom: 10vh; /* 두 번째 줄 위치 조정 */
}

.movie-poster {
  width: calc(40vh * 9 / 16); /* 3:4 비율 유지 */
  height: 40vh;
  flex-shrink: 0;
  box-sizing: border-box;
  overflow: hidden;
  margin: 0.25vh;
}

.movie-poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

button {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  z-index: 10;
}
</style>

