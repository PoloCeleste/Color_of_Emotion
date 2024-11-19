<template>
  <div>
    <h3>Let's find your emotions</h3>
    <button @click="openModal">MEASURE</button>
    <button v-if="measurementComplete" @click="goToRecommend">START</button>
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

</style>