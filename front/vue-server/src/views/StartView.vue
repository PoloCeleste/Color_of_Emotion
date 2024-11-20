<template>
  <div class="start-container">
    <div class="content-wrapper">
      <h3 class="title">Let's find your emotions</h3>
      <div class="circle-container">
        <!-- SVG 애니메이션 추가 -->
        <svg v-if="measurementComplete" class="circle-effect" viewBox="0 0 100 100">
          <circle class="wave" cx="50" cy="50" r="48" />
          <circle class="wave" cx="50" cy="50" r="48" />
          <circle class="wave" cx="50" cy="50" r="48" />
        </svg>
        <div class="circle">
          <button 
            v-if="!measurementComplete" 
            class="measure-button" 
            @click="openModal"
          >
            MEASURE
          </button>
          <button 
            v-else 
            class="measure-button" 
            @click="goToRecommend"
          >
            START
          </button>
        </div>
      </div>
    </div>
    <MeasureModal
      :isOpen="isModalOpen"
      @close="closeModal"
      @complete="completeMeasurement"
    /> 
  </div>
</template>

<script setup>
// 1. start 버튼 누르면 추천으로 넘어가기
import MeasureModal from '@/components/MeasureModal.vue';
import { useRouter } from 'vue-router';
const router = useRouter()

const goToRecommend  = () => {
  router.push('/recommend')
}

// 2. 측정모달 띄우기
import { ref } from 'vue';
const isModalOpen = ref(false)
const measurementComplete = ref(false)

const openModal = () => {
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
}

const completeMeasurement = () => {
  isModalOpen.value = false
  measurementComplete.value = true
}

</script>

<style scoped>
.start-container {
  width: 100%;
  height: 70vh;
  background-color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;  /* 추가 */
  z-index: 1;  /* 추가 */
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

.title {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 2rem;
  font-weight: 500;
}

.circle {
  width: 300px;
  height: 300px;
  background-color: white;
  border: 2px solid #333;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: transform 0.3s ease;
}

.circle:hover {
  transform: scale(1.05);
}

.measure-button {
  padding: 20px 40px;
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: color 0.3s ease;
  letter-spacing: 2px;
}

.measure-button:hover {
  color: #4CAF50;
}

.start-button {
  padding: 20px 40px;
  font-size: 1.5rem;
  font-weight: bold;
  color: #4CAF50;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: 2px;
  z-index: 3;
}

.start-button:hover {
  background-color: #45a049;
  transform: scale(1.05);
}

/* 웨이브 효과 */
.circle-container {
  position: relative;
  width: 300px;
  height: 300px;
  z-index: 2;  /* 수정 */
}

.circle {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: white;
  border: 2px solid #333;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2;
}

.circle-effect {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.wave {
  fill: none;
  stroke-width: 1px;
  stroke-linecap: round;
  animation: wave 3s ease-in-out infinite;
  transform-origin: center; /* 회전 중심점 설정 */
}

.wave:nth-child(1) {
  stroke: rgba(76, 175, 80, 0.3);
  animation-delay: 0s;
}

.wave:nth-child(2) {
  stroke: rgba(76, 175, 80, 0.2);
  animation-delay: 1s;
}

.wave:nth-child(3) {
  stroke: rgba(76, 175, 80, 0.1);
  animation-delay: 2s;
}

@keyframes wave {
  0% {
    transform: rotate(0deg) scale(0.9);
    opacity: 0.3;
  }
  50% {
    transform: rotate(180deg) scale(1.1);
    opacity: 0.5;
  }
  100% {
    transform: rotate(360deg) scale(0.9);
    opacity: 0.3;
  }
}
</style>