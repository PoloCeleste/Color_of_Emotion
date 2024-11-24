<template>
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h2>{{ currentMessage }}</h2>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  
  const showModal = ref(false);
  const currentMessage = ref("");
  const messages = [
    "카메라를 통해 감정을 측정합니다",
    "편안한 자세로 정면을 바라봐주세요",
    "자연스러운 표정을 지어주세요",
    "잠시 후 카메라가 시작됩니다",
    "준비하세요...",
  ];
  
  const openModal = async () => {
    showModal.value = true;
    let messageIndex = 0;
    const messageInterval = setInterval(() => {
      if (messageIndex < messages.length) {
        currentMessage.value = messages[messageIndex];
        messageIndex++;
      } else {
        clearInterval(messageInterval);
        setTimeout(() => {
          closeModal();
        }, 1000);
      }
    }, 1000);
  };
  
  const closeModal = () => {
    showModal.value = false;
  };
  
  defineExpose({ openModal, closeModal });
  </script>
  
  <style scoped>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .modal-content {
    background-color: #f0f0f0;
    padding: 20px;
    border-radius: 8px;
    border: 2px solid #ccc;
    width: 400px;
    height: 300px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .modal-content h2 {
    color: #333;
    text-align: center;
    font-size: 1.5em;
  }
  </style>