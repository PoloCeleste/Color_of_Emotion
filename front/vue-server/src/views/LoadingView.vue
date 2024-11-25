<template>
  <div
    class="loading-container d-flex flex-column justify-content-center align-items-center vh-100"
    @click="skipLoading"
  >
    <Transition name="fade">
      <h1 v-if="showTitle" class="typewriter">{{ typedText }}</h1>
    </Transition>

    <Transition name="fade">
      <div v-if="showTitle" class="loading-dots mt-4">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import { ref, onMounted, onBeforeUnmount } from "vue";

const router = useRouter();
const showTitle = ref(false);
const typedText = ref("");
const fullText = "Color of Emotion";
const typingSpeed = 150; // 타이핑 속도 최적화

let typingInterval = null;

function typeText() {
  let currentIndex = 0;
  typingInterval = setInterval(() => {
    if (currentIndex < fullText.length) {
      typedText.value += fullText[currentIndex];
      currentIndex++;
    } else {
      clearInterval(typingInterval);
      setTimeout(() => {
        router.push({
          path: "/start",
          query: { transition: "fade" },
        });
      }, 1500);
    }
  }, typingSpeed);
}

function skipLoading() {
  clearInterval(typingInterval);
  router.push("/start");
}

onMounted(() => {
  setTimeout(() => {
    showTitle.value = true;
    typeText();
  }, 800);
});

onBeforeUnmount(() => {
  clearInterval(typingInterval);
});
</script>

<style scoped>
.loading-container {
  /* background: linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%); */
  cursor: pointer;
}

.typewriter {
  font-family: "Courier New", monospace;
  font-size: clamp(2rem, 5vw, 3.5rem);
  color: #2c3e50;
  white-space: nowrap;
  overflow: hidden;
  border-right: 3px solid #2c3e50;
  animation: blink-caret 0.75s step-end infinite;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}

@keyframes blink-caret {
  from,
  to {
    border-color: transparent;
  }
  50% {
    border-color: #2c3e50;
  }
}

.loading-dots {
  display: flex;
  gap: 8px;
}

.loading-dots span {
  width: 12px;
  height: 12px;
  background-color: #2c3e50;
  border-radius: 50%;
  animation: bounce-dots 1.4s cubic-bezier(0.455, 0.03, 0.515, 0.955) infinite;
}

.loading-dots span:nth-child(2) {
  animation-delay: 0.2s;
}
.loading-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce-dots {
  0%,
  80%,
  100% {
    transform: scale(0.3);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
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
