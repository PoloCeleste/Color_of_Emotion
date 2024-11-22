<template>
  <div class="container">
    <Transition name="fade">
      <h1 v-if="showTitle" class="title">{{ typedText }}</h1>
    </Transition>
    <Transition name="fade">
      <RouterView v-if="showRouter" />
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const showTitle = ref(false);
const showRouter = ref(false);
const typedText = ref('');
const fullText = 'Color of Emotion';
const typingSpeed = 150;

const typeText = () => {
  let currentIndex = 0;
  const typing = setInterval(() => {
    if (currentIndex < fullText.length) {
      typedText.value += fullText[currentIndex];
      currentIndex++;
    } else {
      clearInterval(typing);
      // 타이핑이 완료된 후 2초 동안 보여줌
      setTimeout(() => {
        showTitle.value = false;  // 타이틀 페이드아웃 시작
        // 페이드아웃 애니메이션(0.5s) 완료 후 RouterView 표시
        setTimeout(() => {
          showRouter.value = true;
        }, 500);
      }, 2000);
    }
  }, typingSpeed);
};

onMounted(() => {
  setTimeout(() => {
    showTitle.value = true;
    typeText();
  }, 1000);
});
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.title {
  font-family: "Courier New", Courier, monospace;
  font-weight: bold;
  font-size: 5rem;
  text-align: center;
  position: relative;
}

.title::after {
  content: '';
  position: absolute;
  left: 50%;
  bottom: 10px;
  width: 130%;
  height: 10px;
  background: radial-gradient(
    ellipse at center,
    rgba(0, 0, 0, 0.9) 0%,
    rgba(0, 0, 0, 0.4) 50%,
    rgba(0, 0, 0, 0) 100%
  );
  filter: blur(6px);
  transform: translateX(-50%);
  border-radius: 50%;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>