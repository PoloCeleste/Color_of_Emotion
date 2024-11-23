<template>
  <div class="container">
    <Transition name="fade">
      <h1 v-if="showTitle" class="title">{{ typedText }}</h1>
    </Transition>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { ref, onMounted } from 'vue'

const router = useRouter()
const showTitle = ref(false)
const typedText = ref('')
const fullText = 'Color of Emotion'
const typingSpeed = 150

const typeText = () => {
  let currentIndex = 0
  const typing = setInterval(() => {
    if (currentIndex < fullText.length) {
      typedText.value += fullText[currentIndex]
      currentIndex++
    } else {
      clearInterval(typing)
      setTimeout(() => {
        showTitle.value = false
        router.push('/start')
      }, 2000)
    }
  }, typingSpeed)
}

onMounted(() => {
  setTimeout(() => {
    showTitle.value = true
    typeText()
  }, 1000)
})
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  overflow: hidden;
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