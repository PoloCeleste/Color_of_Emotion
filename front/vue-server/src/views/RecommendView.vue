<template>
  <div class="animation-container">
    <transition name="fade" mode="out-in">
      <InputAnimation v-if="showInput" @complete="toggleComponent" />
      <FilmAnimation v-else-if="showFilm" @complete="startCurtainEffect" />
    </transition>

    <div class="curtain" :class="{ 'curtain-open': showCard }">
      <div class="rnInner">
        <div class="rnUnit" v-for="i in 10" :key="i"></div>
      </div>
      <CardComponent v-if="showCard" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import FilmAnimation from '@/components/FilmAnimation.vue';
import InputAnimation from '@/components/InputAnimation.vue';
import CardComponent from '@/components/CardComponent.vue';

const showInput = ref(true);
const showFilm = ref(false);
const showCard = ref(false);

function toggleComponent() {
  showInput.value = false;
  showFilm.value = true;
}

function startCurtainEffect() {
  setTimeout(() => {
    showFilm.value = false;
    showCard.value = true;
  }, 3000); // 3초 후에 CardComponent로 전환
}
</script>

<style scoped>
.animation-container {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease; /* 트랜지션 시간을 적절히 설정 */
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.curtain {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.rnInner {
  width: 100%;
  height: 100%;
  position: absolute;
  top: -10%;
  right: 0;
  bottom: 0;
  left: 0;
  margin: auto;
  transform-style: preserve-3d;
  transition: transform 3s ease; /* 커튼 열림 시간을 조정 */
}

.rnUnit {
 width:10vw;height:120vh;background:
 repeating-linear-gradient(to left,hsl(360,80%,50%)4vw,hsl(360,80%,30%)8vw,hsl(360,80%,70%)10vw);background-size:
100%100%;display:inline-block;transform-origin:
00%;transform:
rotate(3deg);animation:
rnUnit2seaseinfinite;}

@keyframes rnUnit { 
50% { 
transform:
rotate(-3deg); 
}
}

.curtain-open .rnInner { 
transform:
scaleX(0); 
}

.rnUnit:nth-child(1) { animation-delay:-0.1s; }
.rnUnit:nth-child(2) { animation-delay:-0.2s; }
.rnUnit:nth-child(3) { animation-delay:-0.3s; }
.rnUnit:nth-child(4) { animation-delay:-0.4s; }
.rnUnit:nth-child(5) { animation-delay:-0.5s; }
.rnUnit:nth-child(6) { animation-delay:-0.6s; }
.rnUnit:nth-child(7) { animation-delay:-0.7s; }
.rnUnit:nth-child(8) { animation-delay:-0.8s; }
.rnUnit:nth-child(9) { animation-delay:-0.9s; }
.rnUnit:nth-child(10) { animation-delay:-1s; }
</style>