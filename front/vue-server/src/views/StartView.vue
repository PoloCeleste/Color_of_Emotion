<template>
  <div>
    <h3>Let's find your emotions</h3>
    <button @click="openModal">MEASURE</button>
    <button v-if="measurementComplete" @click="goToRecommend">START</button>
    <label>
      <input type="checkbox" v-model="useTransition"> Transition On
    </label>
    <MeasureModal 
      :isOpen="isModalOpen" 
      @close="closeModal"
      @complete="completeMeasurement"
      :useTransition="useTransition"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import MeasureModal from '@/components/MeasureModal.vue'

const router = useRouter()
const isModalOpen = ref(false)
const useTransition = ref(true)
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

const goToRecommend = () => {
  router.push('/recommend')
}
</script>

<style scoped>
button {
  margin: 5px;
  padding: 10px;
  font-size: 16px;
}

label {
  display: block;
  margin-top: 10px;
}
</style>