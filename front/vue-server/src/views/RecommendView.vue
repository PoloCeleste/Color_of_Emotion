<template>
  <div class='recommend-container'>
    <div class="film-container" ref="filmStrip">
      <div class="film-strip-container">
        <div class="film-strip-row">
          <div v-for="movie in firstRow18" :key="movie.id" class="movie-poster flowing">
            <img :src="movie.poster_path" :alt="movie.title" />
          </div>
          <div v-for="movie in firstRow6" :key="movie.id" class="movie-poster static">
            <img :src="movie.poster_path" :alt="movie.title" />
          </div>
        </div>
        <div class="film-strip-row">
          <div v-for="movie in secondRow18" :key="movie.id" class="movie-poster flowing">
            <img :src="movie.poster_path" :alt="movie.title" />
          </div>
          <div v-for="movie in secondRow6" :key="movie.id" class="movie-poster static">
            <img :src="movie.poster_path" :alt="movie.title" />
          </div>
        </div>
      </div>
    </div>
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
const duration = 50000; // 속도제어

const firstRow18 = computed(() => movieStore.recommendedMovies.slice(0, 18));
const firstRow6 = computed(() => movieStore.recommendedMovies.slice(18, 24));
const secondRow18 = computed(() => movieStore.recommendedMovies.slice(24, 42));
const secondRow6 = computed(() => movieStore.recommendedMovies.slice(42, 48));

const isCentered = ref(false);

const checkCentered = () => {
  if (!filmStrip.value) return;
  
  const staticPosters = filmStrip.value.querySelectorAll('.movie-poster.static');
  const firstStaticPoster = staticPosters[0];
  const lastStaticPoster = staticPosters[staticPosters.length - 1];
  
  if (!firstStaticPoster || !lastStaticPoster) return;
  
  const firstPosterRect = firstStaticPoster.getBoundingClientRect();
  const lastPosterRect = lastStaticPoster.getBoundingClientRect();
  const viewportCenter = window.innerWidth / 2;
  const postersCenter = (firstPosterRect.left + lastPosterRect.right) / 2;
  
  const tolerance = 5; // 더 정확한 중앙 정렬을 위해 이 값을 조정하세요
  
  isCentered.value = Math.abs(postersCenter - viewportCenter) < tolerance;
};

const animate = (timestamp) => {
  if (!startTime) startTime = timestamp;
  const elapsed = timestamp - startTime;
  const progress = (elapsed % duration) / duration;
  
  if (filmStrip.value) {
    checkCentered();
    
    let translateX = -progress * 100;
    
    if (isCentered.value) {
      // 정적 포스터를 뷰포트 중앙에 맞추기 위해 위치 조정
      const staticPosters = filmStrip.value.querySelectorAll('.movie-poster.static');
      const firstStaticPoster = staticPosters[0];
      const lastStaticPoster = staticPosters[staticPosters.length - 1];
      const firstPosterRect = firstStaticPoster.getBoundingClientRect();
      const lastPosterRect = lastStaticPoster.getBoundingClientRect();
      const viewportCenter = window.innerWidth / 2;
      const postersCenter = (firstPosterRect.left + lastPosterRect.right) / 2;
      const adjustment = (viewportCenter - postersCenter) / filmStrip.value.offsetWidth * 100;
      translateX += adjustment;

      filmStrip.value.style.transform = `translateX(${translateX}%)`;
      
      // 애니메이션 정지
      cancelAnimationFrame(animationId);
      isAnimating.value = false;

      // flowing 포스터 사라지게 하기
      const flowingPosters = filmStrip.value.querySelectorAll('.movie-poster.flowing');
      flowingPosters.forEach((poster) => {
        poster.style.opacity = '0';
      });

      // flowing 포스터가 완전히 사라진 후 static 포스터 어둡게 하기
      setTimeout(() => {
        staticPosters.forEach((poster) => {
          poster.classList.add('dimmed');
        });
      }, 500); // flowing 포스터가 사라지는 시간(0.5초) 후에 실행
    } else {
      filmStrip.value.style.transform = `translateX(${translateX}%)`;
      filmStrip.value.querySelectorAll('.movie-poster').forEach((poster) => {
        poster.style.transform = 'none';
        if (poster.classList.contains('flowing')) {
          poster.style.opacity = '1';
        }
        if (poster.classList.contains('static')) {
          poster.classList.remove('dimmed');
        }
      });
    }
  }

  if (isAnimating.value) {
    animationId = requestAnimationFrame(animate);
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
  width: 600%;
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
  width: 200%; /* 너비를 늘려 모든 포스터가 표시되도록 함 */
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

.movie-poster.flowing {
  transition: transform 1.2s cubic-bezier(0.25, 0.1, 0.25, 1), 
              opacity 1.2s cubic-bezier(0.25, 0.1, 0.25, 1);
}

.movie-poster.static {
  transition: filter 1.2s cubic-bezier(0.25, 0.1, 0.25, 1);
}

.movie-poster.static.dimmed {
  filter: brightness(0.6);
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