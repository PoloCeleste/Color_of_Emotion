<template>
  <div class="start-container">
    <div class="content-wrapper">
      <h3 class="title">Let's find your emotions</h3>
      <div class="circle-container">
        <div class="circle"  :class="[{ 'rainbow-shadow': measurementComplete }]">
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
  position: relative;
  z-index: 1;
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

.circle-container {
  position: relative;
  width: 300px;
  height: 300px;
  z-index: 2;
  border-radius: 50%;
}

.circle {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  background-color: white;
  border: 2px solid #333;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2;
  transition: transform 0.3s ease;
  overflow: hidden;
}

.circle.rainbow-shadow {
  border: 0px solid transparent;
  background-origin: border-box;
  background-clip: content-box, border-box;
  filter: 
    drop-shadow(0 0 4px #ff0000)
    drop-shadow(0 0 4px #ff7f00)
    drop-shadow(0 0 4px #ffff00)
    drop-shadow(0 0 4px #00ff00)
    drop-shadow(0 0 4px #0000ff)
    drop-shadow(0 0 4px #8b00ff);
  /* background: 
    linear-gradient(white, white) padding-box,
    linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet) border-box; */
  animation: move-shadow 2s linear infinite;
}

@keyframes move-shadow {
  0% { filter: drop-shadow(10.00px 0.00px 4px rgba(255, 0, 0, 0.5)); }
  5% { filter: drop-shadow(9.51px 3.09px 4px rgba(255, 127, 0, 0.5)); }
  10% { filter: drop-shadow(8.09px 5.88px 4px rgba(255, 255, 0, 0.5)); }
  15% { filter: drop-shadow(5.88px 8.09px 4px rgba(0, 255, 0, 0.5)); }
  20% { filter: drop-shadow(3.09px 9.51px 4px rgba(0, 255, 255, 0.5)); }
  25% { filter: drop-shadow(0.00px 10.00px 4px rgba(0, 0, 255, 0.5)); }
  30% { filter: drop-shadow(-3.09px 9.51px 4px rgba(255, 0, 255, 0.5)); }
  35% { filter: drop-shadow(-5.88px 8.09px 4px rgba(255, 0, 127, 0.5)); }
  40% { filter: drop-shadow(-8.09px 5.88px 4px rgba(255, 127, 127, 0.5)); }
  45% { filter: drop-shadow(-9.51px 3.09px 4px rgba(0, 255, 127, 0.5)); }
  50% { filter: drop-shadow(-10.00px 0.00px 4px rgba(127, 0, 255, 0.5)); }
  55% { filter: drop-shadow(-9.51px -3.09px 4px rgba(255, 0, 0, 0.5)); }
  60% { filter: drop-shadow(-8.09px -5.88px 4px rgba(255, 127, 0, 0.5)); }
  65% { filter: drop-shadow(-5.88px -8.09px 4px rgba(255, 255, 0, 0.5)); }
  70% { filter: drop-shadow(-3.09px -9.51px 4px rgba(0, 255, 0, 0.5)); }
  75% { filter: drop-shadow(-0.00px -10.00px 4px rgba(0, 255, 255, 0.5)); }
  80% { filter: drop-shadow(3.09px -9.51px 4px rgba(0, 0, 255, 0.5)); }
  85% { filter: drop-shadow(5.88px -8.09px 4px rgba(255, 0, 255, 0.5)); }
  90% { filter: drop-shadow(8.09px -5.88px 4px rgba(255, 0, 127, 0.5)); }
  95% { filter: drop-shadow(9.51px -3.09px 4px rgba(255, 127, 127, 0.5)); }
  100% { filter: drop-shadow(10.00px -0.00px 4px rgba(255, 0, 0, 0.5)); }
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

.start-button {
  padding: 20px 40px;
  font-size: 1.5rem;
  font-weight: bold;
  color: transparent;
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
</style>