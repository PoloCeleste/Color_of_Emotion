<template>
  <div class="film-reel-container">
    <div class="film-reel" :class="{ 'rotated': isRotated }">
      <div class="top"></div>
      <div class="bottom"></div>
      <div class="side" :class="{ 'expanded': isSideExpanded }"></div>
      <div class="film" :class="{ 'move-right': isSideExpanded }"></div>
    </div>
    <div class="black-overlay" :class="{ 'visible': isExpanded, 'expand': isExpanded }"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const isRotated = ref(false);
const isExpanded = ref(false);
const isSideExpanded = ref(false);
const expansionComplete = ref(false)


onMounted(() => {
  setTimeout(() => {
    isRotated.value = true;
  }, 1500);

  setTimeout(() => {
    isSideExpanded.value = true;
  }, 3000);

  setTimeout(() => {
    isExpanded.value = true; // 이 시점에 블랙 오버레이가 나타남
  }, 4500);

    setTimeout(() => {
    expansionComplete.value = true;
  }, 6000);
});
</script>

<style scoped>
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

.top, .bottom {
  position: absolute;
  width: 100%;
  height: 100%;
  background: #1a1a1a;
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
  background: #1a1a1a;
  transform: rotateX(90deg) translateZ(0);
  top: calc(50% - 50px);
  right: 0;
  transform-origin: right center;
  z-index: -1;
}

.film {
  position: absolute;
  width: calc(100% + 3px);
  height: 100px;
  transform: rotateX(90deg) translateZ(0);
  top: calc(50% - 50px);
  right: -3px;
  z-index: 1;
  opacity: 0;
  transition: opacity 1.5s ease-out;

  --s: 8px;
  --c: #222;
  background: 
    /* 필름 구멍 패턴 */
    radial-gradient(circle at center, transparent 30%, var(--c) 30%, var(--c) 40%, transparent 40%) 
    0 50%/calc(2*var(--s)) 100% repeat-x,
    /* 필름 스트립 배경 */
    linear-gradient(90deg, 
      var(--c) var(--s), 
      #333 var(--s), 
      #333 calc(100% - var(--s)), 
      var(--c) calc(100% - var(--s))
    );
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

.black-overlay {
  position: absolute;
  top: 0;
  left: 100%;
  width: 100vw;
  height: 100vh;
  transform: translateX(0);
  transition: transform 1.5s ease-out;
  z-index: 10;
  background-color: #1a1a1a;
}


.black-overlay.visible {
  transform: translateX(-100%);
  --s: 32px; /* 더 큰 패턴 */
  --c: #1a1a1a;
  background: 
    /* 필름 구멍 패턴 */
    radial-gradient(circle at center, transparent 30%, var(--c) 30%, var(--c) 40%, transparent 40%) 
    0 50%/calc(2*var(--s)) 100% repeat-x,
    /* 필름 스트립 배경 */
    linear-gradient(90deg, 
      var(--c) var(--s), 
      #222 var(--s), 
      #222 calc(100% - var(--s)), 
      var(--c) calc(100% - var(--s))
    );
  border: var(--s) solid var(--c);
  box-sizing: border-box;
}
</style>