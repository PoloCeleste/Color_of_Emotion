<template>
  <div class="animation-container">
    <!-- 인풋 애니메이션 원 -->
    <Transition name="fade">
      <div
        class="circle-container"
        v-show="!animationStarted"
        @click="startAnimation"
      >
        <div class="circle">
          <TypingComponent
            text="START"
            :typing-speed="100"
            @complete="onComplete"
            @skip="skipAnimation"
          />
        </div>
      </div>
    </Transition>
    <Transition name="fade">
      <!-- 필름 애니메이션 -->
      <div class="film-reel-container">
        <div class="film-reel" :class="{ rotated: isRotated }">
          <div class="top"></div>
          <div class="bottom"></div>
          <div class="side" :class="{ expanded: isSideExpanded }"></div>
          <div class="film" :class="{ 'move-right': isSideExpanded }"></div>
        </div>
        <div
          class="black-overlay"
          :class="{ visible: isExpanded, expand: isExpanded }"
        ></div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted, defineProps } from "vue";
import { useRouter } from "vue-router";
// import MovieCard from "@/components/MovieCard.vue";
import { useMovieStore } from "@/store/stores";
import TypingComponent from "@/components/TypingComponent.vue";

const router = useRouter();
const store = useMovieStore();

defineProps({
  movies: {
    type: Array,
    required: true,
  },
});

const animationStarted = ref(false);
const isRotated = ref(false);
const isExpanded = ref(false);
const isSideExpanded = ref(false);
const expansionComplete = ref(false);
const emotionData = ref(null);

// const primaryEmotion = computed(() => {
//   if (emotionData.value && emotionData.value.primary_emotion) {
//     return Object.keys(emotionData.value.primary_emotion)[0];
//   }
//   return "";
// });

// const secondaryEmotions = computed(() => {
//   if (emotionData.value && emotionData.value.secondary_emotions) {
//     return emotionData.value.secondary_emotions.map(
//       (emotion) => Object.keys(emotion)[0]
//     );
//   }
//   return [];
// });

const startAnimation = () => {
  animationStarted.value = true;

  setTimeout(() => {
    isRotated.value = true;
  }, 1500);

  setTimeout(() => {
    isSideExpanded.value = true;
  }, 3000);

  setTimeout(() => {
    isExpanded.value = true;
  }, 4500);

  setTimeout(() => {
    expansionComplete.value = true;
    router.push("/recommend");
  }, 6000);
};

onMounted(() => {
  emotionData.value = JSON.parse(localStorage.getItem("emotionAnalysis"));
  store.setEmotionData(emotionData.value);
});
</script>

<style scoped>
.animation-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

/* 기존 circle 스타일 */
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
  top: -1%;
  left: -1%;
  width: 102%;
  height: 102%;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(145deg, #f0f0f0, #ffffff);
  border: 2px solid darkgray;
  box-shadow: inset 0 0 50px rgba(0, 0, 0, 0.1), 0 10px 20px rgba(0, 0, 0, 0.2);
  transform-style: preserve-3d;
  perspective: 1000px;
  transition: all 0.3s ease;
  color: gray;
  cursor: pointer;
}
.circle:hover {
  transform: scale(1.02);
  color: #222;
  box-shadow: inset 0 0 60px rgba(0, 0, 0, 0.15), 0 15px 25px rgba(0, 0, 0, 0.3),
    0 0 0 2px rgba(0, 0, 0, 0.1);
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

.film-reel-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  position: relative;
  overflow: hidden;
}

.film-reel {
  position: relative;
  width: 400px;
  height: 400px;
  transform-style: preserve-3d;
  transition: transform 1.5s;
}

.film-reel.rotated {
  transform: rotateX(90deg);
}

.top,
.bottom {
  position: absolute;
  width: 100%;
  height: 100%;
  background: #222;
  border-radius: 50%;
}

.top {
  transform: translateZ(50px);
  border: 20px dashed #f0f0f0;
}

.bottom {
  transform: translateZ(-50px);
}

.side {
  position: absolute;
  width: 100%;
  height: 100px;
  background: #222;
  transform: rotateX(90deg) translateZ(0);
  top: calc(50% - 50px);
  right: 0;
  transform-origin: right center;
  z-index: -1;
}

.film {
  position: absolute;
  width: 100%;
  height: 100px;
  transform: rotateX(90deg) translateZ(0);
  top: calc(50% - 50px);
  right: 5;
  z-index: 1;
  opacity: 0;
  transition: opacity 1.5s ease-out;

  /* 필름 스트립 패턴 복원 */
  --s: 8px;
  --c: #222;
  background: conic-gradient(at 50% var(--s), var(--c) 75%, #0000 0) 0 0 /
    calc(2 * var(--s)) calc(100% - var(--s)) padding-box;
  border: var(--s) solid var(--c);
  box-sizing: border-box;
}

.film-reel.rotated .film {
  opacity: 1;
}

@keyframes moveRight {
  0% {
    transform: rotateX(90deg) translateZ(0);
    /* clip-path: polygon(100% 0, 100% 100%, 100% 100%, 100% 0); */
    width: 0%;
  }
  100% {
    transform: rotateX(90deg) translateZ(0) translateX(1200px);
    /* clip-path: polygon(0 0, 100% -100%, 100% 200%, 0 100%); */
    width: 300%;
  }
}

.film.move-right {
  animation: moveRight 1.5s ease-out forwards;
}

.film.move-right {
  animation: moveRight 1.5s ease-out forwards;
}

.black-overlay {
  position: absolute;
  top: 0;
  left: 100%;
  width: 100vw;
  height: 100vh;
  transform: translateX(0);
  transition: transform 1.5s ease-out;
  z-index: 10;
}

.black-overlay.visible {
  transform: translateX(-100%); /* 왼쪽으로 이동하여 화면을 덮음 */
  --s: 20px;
  --c: #222;
  background: conic-gradient(at 50% var(--s), var(--c) 75%, #0000 0) 0 0 /
    calc(2 * var(--s)) calc(100% - var(--s)) padding-box;
  border: var(--s) solid var(--c);
  box-sizing: border-box;
  align-items: center;
  display: flex;
  justify-content: center;
  flex-direction: column;
}

.text-box {
  color: whitesmoke;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.movie-scroll-container {
  width: 100%;
  height: 60vh;
  overflow-y: auto;
  margin-top: 2rem;
  padding: 0 2rem;
}

.movie-scroll-container::-webkit-scrollbar {
  width: 8px;
}

.movie-scroll-container::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.movie-scroll-container::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
}

.movie-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 2rem;
  padding: 1rem;
}
</style>
