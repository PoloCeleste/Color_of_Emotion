<template>
  <div :class="['start-container', backgroundClass]">
    <div class="content-wrapper">
      <!-- 카메라 몸통 -->
      <Transition name="camera-body">
        <div v-if="isModalOpen" class="camera-body">
          <div class="shutter-button"></div>
          <div class="flash-window"></div>
        </div>
      </Transition>

      <!-- 원형 렌즈 -->
      <div class="circle-container">
        <div class="circle" :class="{ 'rainbow-shadow': measurementComplete }">
          <!-- 감정 측정 버튼 -->
          <button v-if="!measurementComplete" class="measure-button" @click="openModal">
            Let's find your emotion
          </button>
          <!-- 시작 버튼 -->
          <button v-else class="start-button" @click="goToRecommend">
            START
          </button>
        </div>
      </div>
    </div>

    <!-- 모달 -->
    <Transition name="modal">
      <MeasureModal
        v-if="isModalOpen"
        :isOpen="isModalOpen"
        @close="closeModal"
        @complete="completeMeasurement"
      />
    </Transition>
  </div>
</template>

<script setup>
import MeasureModal from '@/components/MeasureModal.vue'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

// 상태 관리
const router = useRouter()
const isModalOpen = ref(false)
const measurementComplete = ref(false)
const backgroundClass = ref('default-background')

// 모달 열기
const openModal = () => {
  isModalOpen.value = true
  backgroundClass.value = 'dark-background'
}

// 모달 닫기
const closeModal = () => {
  isModalOpen.value = false
  backgroundClass.value = 'default-background'
}

// 감정 측정 완료
const completeMeasurement = () => {
  isModalOpen.value = false
  measurementComplete.value = true
}

// 추천 페이지로 이동
const goToRecommend = () => {
  router.push('/recommend')
}
</script>

<style scoped>
/* 기본 레이아웃 */
.start-container {
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.default-background {
  background-color: whitesmoke;
}

.dark-background {
  background-color: #929191;
}

/* 카메라 몸통 */
.camera-body {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 1200px;
  height: 600px;
}

/* 원형 렌즈 */
.circle-container {
  position: absolute;
  top: calc(50% + 300px);
  left: calc(50%);
  transform: translate(-50%, -50%);
}

.circle {
  width: 400px;
  height: 400px;
}

/* 버튼 스타일 */
.measure-button,
.start-button {
  padding: 20px;
}
</style>