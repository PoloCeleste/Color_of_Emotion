<template>
  <div
    class="d-flex flex-column justify-content-center align-items-center vh-100"
    @click="skipLoading"
  >
    <!-- 타이핑 텍스트 -->
    <h1 v-if="showTitle" class="typewriter">{{ typedText }}</h1>

    <!-- 로딩 점 애니메이션 -->
    <div v-if="showTitle" class="loading-dots mt-4">
      <span></span>
      <span></span>
      <span></span>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'

// 라우터와 상태 관리
const router = useRouter()
const showTitle = ref(false)
const typedText = ref('')
const fullText = 'Color of Emotion'
const typingSpeed = 200
let typingInterval = null // 타이핑 인터벌 ID

// 텍스트 출력 함수
function typeText() {
  let currentIndex = 0
  typingInterval = setInterval(() => {
    if (currentIndex < fullText.length) {
      typedText.value += fullText[currentIndex]
      currentIndex++
    } else {
      clearInterval(typingInterval)
      setTimeout(() => {
        showTitle.value = false
        router.push('/start') // 타이핑 완료 후 페이지 이동
      }, 2000)
    }
  }, typingSpeed)
}

// 로딩 스킵 함수
function skipLoading() {
  clearInterval(typingInterval) // 타이핑 애니메이션 중단
  router.push('/start') // 즉시 다음 페이지로 이동
}

// 컴포넌트가 마운트될 때 실행
onMounted(() => {
  setTimeout(() => {
    showTitle.value = true
    typeText()
  }, 1000)
})
</script>

<style scoped>
/* 타이틀 스타일 */
.typewriter {
  font-family: "Courier New", Courier, monospace;
  font-size: 3rem;
  color: black;
  white-space: nowrap;
  overflow: hidden;
  border-right: 2px solid black; /* 깜박이는 커서 */
  animation: blink-caret 0.7s step-end infinite; /* 커서 깜박임 */
}

/* 커서 깜박임 애니메이션 */
@keyframes blink-caret {
  from, to {
    border-color: transparent;
  }
  50% {
    border-color: black;
  }
}

/* 로딩 점 애니메이션 */
.loading-dots {
  display: flex;
}

.loading-dots span {
  width: 10px;
  height: 10px;
  margin: 0 5px;
  background-color: black;
  border-radius: 50%;
  animation: bounce-dots 1.5s infinite ease-in-out;
}

.loading-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.loading-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce-dots {
  0%, 80%, 100% {
    transform: scale(0);
    opacity: 0.5;
  }
  
  40% {
    transform: scale(1);
    opacity: 1;
  }
}
</style>