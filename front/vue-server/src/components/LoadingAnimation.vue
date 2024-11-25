<!-- LoadingAnimation.vue -->
<template>
    <div class="loading-container">
      <div class="loading-circle"></div>
      <div class="loading-text">영화를 찾고 있습니다...</div>
    </div>
  </template>
  
  <style scoped>
  .loading-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: #1a1a1a;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 9999;
  }
  
  .loading-circle {
    width: 80px;
    height: 80px;
    border: 8px solid #f3f3f3;
    border-top: 8px solid #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }
  
  .loading-text {
    margin-top: 20px;
    color: white;
    font-size: 1.5rem;
    font-weight: bold;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  </style>