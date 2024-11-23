<template>
  <router-view />
</template>

<script setup>
import { RouterView } from 'vue-router'

</script>

<style scoped>
/* 페이드 효과 개선 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 슬라이드 효과 개선 */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-enter-from {
  transform: translateX(100px);
  opacity: 0;
}

.slide-leave-to {
  transform: translateX(-100px);
  opacity: 0;
}

/* 새로운 줌 효과 추가 */
.zoom-enter-active,
.zoom-leave-active {
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.zoom-enter-from {
  transform: scale(0.95);
  opacity: 0;
}

.zoom-leave-to {
  transform: scale(1.05);
  opacity: 0;
}

html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  overflow: hidden;
}

#app {
  height: 100vh;
  overflow: hidden;
}
</style>