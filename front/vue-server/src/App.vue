<template>
  <transition name="fade">
    <router-view />
  </transition>
</template>

<script setup>
import { RouterView } from 'vue-router'
</script>

<style scoped>
/* 페이드 효과 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease-in-out;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 전역 스타일 */
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  overflow: hidden; /* 스크롤바 제거 */
}

#app {
  height: 100%; /* 부모 요소가 화면 전체를 채우도록 설정 */
  background-color: whitesmoke; /* 애플리케이션 배경색 */
}
</style>