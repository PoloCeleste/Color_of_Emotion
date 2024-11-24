<template>
    <div class="circle-container">
      <div class="circle"></div>
    </div>
  </template>
  
  <script setup>
import { onMounted, defineEmits } from 'vue';

const emit = defineEmits(['complete']);

onMounted(() => {
  // 애니메이션이 끝나면 complete 이벤트를 발생시킵니다
  setTimeout(() => {
    emit('complete');
  }, 3000); // 예: 3초 후에 완료
});
  </script>
  
  <style scoped>
  .circle-container {
    position: fixed;
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
    border-radius: 50%;
    background: linear-gradient(145deg, #f0f0f0, #ffffff);
    border: 2px solid darkgray;
    box-shadow: 
      inset 0 0 50px rgba(0, 0, 0, 0.1),
      0 10px 20px rgba(0, 0, 0, 0.2);
    transform-style: preserve-3d;
    perspective: 1000px;
    transition: all 0.3s ease;
  }
  </style>