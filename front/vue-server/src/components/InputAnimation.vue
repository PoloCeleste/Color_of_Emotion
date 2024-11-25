<template>
  <div class="circle-container">
    <div class="circle">
      <button @click="handleClick">START</button>
    </div>
  </div>
</template>

<script setup>
import { defineEmits } from 'vue';

const emit = defineEmits(['complete']);

function handleClick() {
  emit('complete');
}
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