<template>
  <div class="start-container">
    <div class="content-wrapper">
      <h3 class="title">Let's find your emotions</h3>
      <div class="circle-container">
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
</style>