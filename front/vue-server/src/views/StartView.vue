<template>
  <div class="start-container">
    <div class="content-wrapper">
      <div class="circle-container">
        <div class="circle" :class="[{ 'rainbow-shadow': measurementComplete }]">
          <button 
            v-if="!measurementComplete" 
            class="measure-button" 
            @click="openModal"
          >
            Let's find your emotions
          </button>
          <button 
            v-else 
            class="start-button" 
            @click="goToRecommend"
          >
            START
          </button>
        </div>
      </div>
    </div>
    <!-- 모달 트랜지션 추가 -->
    <transition name="modal-fade">
      <MeasureModal
        v-if="isModalOpen"
        :isOpen="isModalOpen"
        @close="closeModal"
        @complete="completeMeasurement"
      /> 
    </transition>
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
  background-color: whitesmoke;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

/* 모달 트랜지션 효과 */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: all 0.5s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
  transform: scale(0.67);
}

.modal-fade-enter-to,
.modal-fade-leave-from {
  opacity: 1;
  transform: scale(1);
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

/* circle-container 위치 조정 */
.circle-container {
  position: fixed; /* absolute에서 fixed로 변경 */
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 400px;
  height: 400px;
  z-index: 2;
}

.circle {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  background-color: whitesmoke;
  border: 2px solid darkgray;
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
  filter: drop-shadow(0 0 4px rgba(0, 0, 0, 0.5));
  filter: saturate(150%) drop-shadow(0 0 4px rgba(0, 0, 0, 0.3));
  animation: move-shadow 5s linear infinite;
  opacity: 0.8;
}

@keyframes move-shadow {
  0% { filter: drop-shadow(10.00px 0.00px 6px rgba(255, 0, 0, 0.7)) drop-shadow(10.00px 0.00px 7px rgba(255, 0, 0, 0.4)); }
  3.33% { filter: drop-shadow(9.66px 2.59px 6px rgba(255, 102, 0, 0.7)) drop-shadow(9.66px 2.59px 7px rgba(255, 102, 0, 0.4)); }
  6.67% { filter: drop-shadow(8.66px 5.00px 6px rgba(255, 204, 0, 0.7)) drop-shadow(8.66px 5.00px 7px rgba(255, 204, 0, 0.4)); }
  10% { filter: drop-shadow(7.07px 7.07px 6px rgba(255, 255, 0, 0.7)) drop-shadow(7.07px 7.07px 7px rgba(255, 255, 0, 0.4)); }
  13.33% { filter: drop-shadow(5.00px 8.66px 6px rgba(102, 255, 0, 0.7)) drop-shadow(5.00px 8.66px 7px rgba(102, 255, 0, 0.4)); }
  16.67% { filter: drop-shadow(2.59px 9.66px 6px rgba(0, 255, 0, 0.7)) drop-shadow(2.59px 9.66px 7px rgba(0, 255, 0, 0.4)); }
  20% { filter: drop-shadow(0.00px 10.00px 6px rgba(0, 255, 102, 0.7)) drop-shadow(0.00px 10.00px 7px rgba(0, 255, 102, 0.4)); }
  23.33% { filter: drop-shadow(-2.59px 9.66px 6px rgba(0, 255, 204, 0.7)) drop-shadow(-2.59px 9.66px 7px rgba(0, 255, 204, 0.4)); }
  26.67% { filter: drop-shadow(-5.00px 8.66px 6px rgba(0, 255, 255, 0.7)) drop-shadow(-5.00px 8.66px 7px rgba(0, 255, 255, 0.4)); }
  30% { filter: drop-shadow(-7.07px 7.07px 6px rgba(0, 204, 255, 0.7)) drop-shadow(-7.07px 7.07px 7px rgba(0, 204, 255, 0.4)); }
  33.33% { filter: drop-shadow(-8.66px 5.00px 6px rgba(0, 102, 255, 0.7)) drop-shadow(-8.66px 5.00px 7px rgba(0, 102, 255, 0.4)); }
  36.67% { filter: drop-shadow(-9.66px 2.59px 6px rgba(0, 0, 255, 0.7)) drop-shadow(-9.66px 2.59px 7px rgba(0, 0, 255, 0.4)); }
  40% { filter: drop-shadow(-10.00px 0.00px 6px rgba(102, 0, 255, 0.7)) drop-shadow(-10.00px 0.00px 7px rgba(102, 0, 255, 0.4)); }
  43.33% { filter: drop-shadow(-9.66px -2.59px 6px rgba(204, 0, 255, 0.7)) drop-shadow(-9.66px -2.59px 7px rgba(204, 0, 255, 0.4)); }
  46.67% { filter: drop-shadow(-8.66px -5.00px 6px rgba(255, 0, 255, 0.7)) drop-shadow(-8.66px -5.00px 7px rgba(255, 0, 255, 0.4)); }
  50% { filter: drop-shadow(0.00px -10.00px 6px rgba(255, 0, 204, 0.7)) drop-shadow(0.00px -10.00px 7px rgba(255, 0, 204, 0.4)); }
  53.33% { filter: drop-shadow(2.59px -9.66px 6px rgba(255, 0, 102, 0.7)) drop-shadow(2.59px -9.66px 7px rgba(255, 0, 102, 0.4)); }
  56.67% { filter: drop-shadow(5.00px -8.66px 6px rgba(255, 0, 0, 0.7)) drop-shadow(5.00px -8.66px 7px rgba(255, 0, 0, 0.4)); }
  60% { filter: drop-shadow(7.07px -7.07px 6px rgba(255, 51, 0, 0.7)) drop-shadow(7.07px -7.07px 7px rgba(255, 51, 0, 0.4)); }
  63.33% { filter: drop-shadow(8.66px -5.00px 6px rgba(255, 102, 0, 0.7)) drop-shadow(8.66px -5.00px 7px rgba(255, 102, 0, 0.4)); }
  66.67% { filter: drop-shadow(9.66px -2.59px 6px rgba(255, 153, 0, 0.7)) drop-shadow(9.66px -2.59px 7px rgba(255, 153, 0, 0.4)); }
  70% { filter: drop-shadow(10.00px 0.00px 6px rgba(255, 204, 0, 0.7)) drop-shadow(10.00px 0.00px 7px rgba(255, 204, 0, 0.4)); }
  73.33% { filter: drop-shadow(9.66px 2.59px 6px rgba(255, 255, 0, 0.7)) drop-shadow(9.66px 2.59px 7px rgba(255, 255, 0, 0.4)); }
  76.67% { filter: drop-shadow(8.66px 5.00px 6px rgba(255, 204, 0, 0.7)) drop-shadow(8.66px 5.00px 7px rgba(255, 204, 0, 0.4)); }
  80% { filter: drop-shadow(7.07px 7.07px 6px rgba(255, 153, 0, 0.7)) drop-shadow(7.07px 7.07px 7px rgba(255, 153, 0, 0.4)); }
  83.33% { filter: drop-shadow(5.00px 8.66px 6px rgba(255, 102, 0, 0.7)) drop-shadow(5.00px 8.66px 7px rgba(255, 102, 0, 0.4)); }
  86.67% { filter: drop-shadow(2.59px 9.66px 6px rgba(255, 51, 0, 0.7)) drop-shadow(2.59px 9.66px 7px rgba(255, 51, 0, 0.4)); }
  90% { filter: drop-shadow(0.00px 10.00px 6px rgba(255, 25, 0, 0.7)) drop-shadow(0.00px 10.00px 7px rgba(255, 25, 0, 0.4)); }
  93.33% { filter: drop-shadow(-2.59px 9.66px 6px rgba(255, 13, 0, 0.7)) drop-shadow(-2.59px 9.66px 7px rgba(255, 13, 0, 0.4)); }
  96.67% { filter: drop-shadow(-5.00px 8.66px 6px rgba(255, 6, 0, 0.7)) drop-shadow(-5.00px 8.66px 7px rgba(255, 6, 0, 0.4)); }
  100% { filter: drop-shadow(10.00px 0.00px 6px rgba(255, 0, 0, 0.7)) drop-shadow(10.00px 0.00px 7px rgba(255, 0, 0, 0.4)); }
}

.circle:hover {
  transform: scale(1.05);
}

.measure-button {
  padding: 20px 40px;
  font-size: 1.5rem;
  font-weight: bold;
  color: darkgray;
  background: transparent;
  border: none;
  cursor: pointer;
  letter-spacing: 2px;
  overflow: hidden;
  /* 모든 속성에 대해 transition 적용 */
  transition: all 0.3s ease;
}

.measure-button:hover {
  transform: scale(1.1);
  color: #4CAF50;
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

.start-button {
  padding: 20px 40px;
  font-size: 1.5rem;
  font-weight: bold;
  background: transparent;
  border: none;
  cursor: pointer;
  letter-spacing: 2px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  /* 모든 속성에 대해 transition 적용 */
  transition: all 0.3s ease;
}

/* START 버튼일 때의 스타일 */
.rainbow-shadow .start-button {
  animation: text-color-change 5s linear infinite;
}

.start-button:hover {
  transform: scale(1.15);
}

@keyframes text-color-change {
  0% { color: rgba(255, 0, 0, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  3.33% { color: rgba(255, 102, 0, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  6.67% { color: rgba(255, 204, 0, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  10% { color: rgba(255, 255, 0, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  13.33% { color: rgba(102, 255, 0, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  16.67% { color: rgba(0, 255, 0, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  20% { color: rgba(0, 255, 102, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  23.33% { color: rgba(0, 255, 204, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  26.67% { color: rgba(0, 255, 255, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  30% { color: rgba(0, 204, 255, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  33.33% { color: rgba(0, 102, 255, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  36.67% { color: rgba(0, 0, 255, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  40% { color: rgba(102, 0, 255, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  43.33% { color: rgba(204, 0, 255, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  46.67% { color: rgba(255, 0, 255, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  50% { color: rgba(255, 0, 204, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  53.33% { color: rgba(255, 0, 102, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  56.67% { color: rgba(255, 0, 0, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  60% { color: rgba(255, 51, 0, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  63.33% { color: rgba(255, 102, 0, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  66.67% { color: rgba(255, 153, 0, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  70% { color: rgba(255, 204, 0, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  73.33% { color: rgba(255, 255, 0, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  76.67% { color: rgba(255, 204, 0, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  80% { color: rgba(255, 153, 0, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  83.33% { color: rgba(255, 102, 0, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  86.67% { color: rgba(255, 51, 0, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  90% { color: rgba(255, 25, 0, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  93.33% { color: rgba(255, 13, 0, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  96.67% { color: rgba(255, 6, 0, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
  100% { color: rgba(255, 0, 0, 1); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); }
}


</style>