<template>
    <div class="card" :class="{ 'with-transition': useTransition }">
      <div class="image-wrapper aspect-video">
        <img class="aspect-video" :src="card.poster_path" :alt="card.title">
      </div>
    </div>
  </template>
  
  <script setup>
  import { defineProps } from 'vue';
  defineProps({
    card: {
      type: Object,
      required: true
    },
    useTransition: {
      type: Boolean,
      default: true
    }
  })
  </script>
  
  <style scoped>
  .card {
    width: 100%;
    height: 100%;
    border-radius: 8px;
    overflow: hidden;
  }
  
  .image-wrapper {
    width: 100%;
    height: 100%;
    position: relative;
  }
  
  .image-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
  }
  
  .with-transition:hover .image-wrapper img {
    transform: scale(1.1);
  }
  </style>