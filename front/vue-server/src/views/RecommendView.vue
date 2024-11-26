<template>
  <div class="about">

      <FilmAnimation />

  </div>
</template>

<script setup>
// import { ref } from 'vue';
import FilmAnimation from '@/components/FilmAnimation.vue'
// import InputAnimation from '@/components/InputAnimation.vue';

// const showInput = ref(true);
// const showFilm = ref(false);

// const onInputComplete = () => {
//   showInput.value = false;
//   setTimeout(() => {
//     showFilm.value = true;
//   }, 300); // 0.3초 후에 FilmAnimation 표시
// };
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
</style>
