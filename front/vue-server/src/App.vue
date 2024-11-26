<template>
  <RouterView v-slot="{ Component, route }">
    <Transition
      :name="$route.meta.transition"
      mode="out-in"
      @before-enter="beforeEnter"
      @after-leave="afterLeave"
    >
      <component :is="Component" :key="route.path" />
    </Transition>
  </RouterView>
</template>

<script setup>
import { RouterView } from "vue-router";
import { onMounted } from "vue";

// 페이지 전환 시 스크롤 초기화
onMounted(() => {
  window.scrollTo(0, 0);
});
</script>

<style>
/* 기본 리셋 스타일 */
html,
body {
  margin: 0;
  padding: 0;
  position: fixed; /* 모바일에서 바운스 효과 방지 */
  width: 100%; /* 가로 스크롤도 방지 */
  height: 100%;
  overflow: hidden;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  height: 100vh;
  overflow: hidden;
  position: relative;
}

/* 페이드 효과 */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  will-change: opacity, transform;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 슬라이드 효과 */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  will-change: transform, opacity;
}

.slide-enter-from {
  transform: translateX(100px);
  opacity: 0;
}

.slide-leave-to {
  transform: translateX(-100px);
  opacity: 0;
}

/* 줌 효과 */
.zoom-enter-active,
.zoom-leave-active {
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  will-change: transform, opacity;
}

.zoom-enter-from {
  transform: scale(0.95);
  opacity: 0;
}

.zoom-leave-to {
  transform: scale(1.05);
  opacity: 0;
}
</style>
