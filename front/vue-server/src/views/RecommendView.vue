<template>
  <div class="about">
    <Transition name="fade">
      <div class="circle-container" v-if="!showFilm" @click="startAnimation">
        <div class="circle">
          <h1>START</h1>
        </div>
      </div>
    </Transition>
    <Transition name="fade">
      <FilmAnimation
        v-if="showFilm && store.recommendedMovies.length > 0"
        :movies="store.recommendedMovies"
        :emotionData="store.emotionData"
      />
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import FilmAnimation from "@/components/FilmAnimation.vue";
import { useMovieStore } from "@/stores/movieStore";

const showFilm = ref(false);
const store = useMovieStore();

const startAnimation = () => {
  showFilm.value = true;
};

onMounted(() => {
  if (store.emotionData) {
    store.getMovieRecommendations();
  }
});
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 원형 렌즈 스타일링 */
.circle-container {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 400px;
  height: 400px;
  z-index: 2;
}

.circle {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: linear-gradient(145deg, #f0f0f0, #ffffff);
  border: 2px solid darkgray;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: inset 0 0 50px rgba(0, 0, 0, 0.1), 0 10px 20px rgba(0, 0, 0, 0.2);
  transform-style: preserve-3d;
  perspective: 1000px;
  transition: transform 0.3s ease;
  transition: all 0.3s ease;
}

.circle:hover {
  transform: translateY(-5px);
  box-shadow: inset 0 0 60px rgba(0, 0, 0, 0.15), 0 15px 25px rgba(0, 0, 0, 0.3),
    0 0 0 2px rgba(0, 0, 0, 0.1);
}

.about {
  min-height: 100vh;
  display: flex;
  background-color: whitesmoke;
  justify-content: center;
  align-items: center;
}

h1 {
  font-size: 50px;
  font-weight: bold;
  border: none;
  cursor: pointer;
  letter-spacing: 2px;
  transform: translateZ(0);
  backface-visibility: hidden;
  -webkit-font-smoothing: antialiased;
  will-change: transform;
  transition: transform 0.3s ease;
}
</style>
