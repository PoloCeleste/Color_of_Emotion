<template>
  <div class="roll-film-container">
    <div class="roll-film" :class="{ 'rotated': isRotated }">
      <div class="top"></div>
      <div class="bottom"></div>
      <div class="side"></div>
			<div class="hat"></div>
			<div class="hat-bottom"></div>
			<div class="hat-side"></div>
    </div>
    <div class="black-overlay" :class="{ 'visible': isRotated, 'expand': isExpanded }"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const isRotated = ref(false);
const isExpanded = ref(false);
const expansionComplete = ref(false)

onMounted(() => {
  setTimeout(() => {
    isRotated.value = true;
  }, 2000);

  setTimeout(() => {
    isExpanded.value = true;
  }, 4000);

	setTimeout(() => {
    expansionComplete.value = true;
  }, 6000); // Adjust this timing based on your transition duration
});
</script>

<style scoped>
.roll-film-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  position: relative;
  overflow: hidden;
}

.roll-film {
  position: relative;
  width: 400px;
  height: 400px;
  transform-style: preserve-3d;
  transition: transform 2s;
}

.roll-film.rotated {
  transform: rotateX(90deg);
}

.top, .bottom {
  position: absolute;
  width: 100%;
  height: 100%;
  background: #1a1a1a;
  border-radius: 50%;
}

.top {
  transform: translateZ(300px);
  border: 20px dashed #f0f0f0;
}

.bottom {
  transform: translateZ(-300px);
}

.side {
  position: absolute;
  width: 100%;
  height: 600px;
  background: #1a1a1a;
  transform: rotateX(90deg) translateZ(0);
  top: calc(50% - 300px);
}

.hat {
	position: absolute;
  width: 20%;
  height: 20%;
	top: 50%;
  left: 50%;
  background: white;
  border-radius: 50%;
	transform: translate(-50%, -50%) translateZ(320px);
	border: #1a1a1a;
}

.hat-bottom {
	position: absolute;
  width: 20%;
  height: 20%;
	top: 50%;
  left: 50%;
  background: white;
  border-radius: 50%;
	transform: translate(-50%, -50%) translateZ(301px);
}

.hat-side {
  position: absolute;
  width: calc(20%);
  height: calc(100px); /* Adjust this value to control the height of the side */
  background: white;
  left: calc(50%);
  transform: translate(-50%, -50%) rotateX(90deg) translateZ(310px);
}

.black-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 20px;
  height: 30px;
  background-color: #1a1a1a;
  transform: translate(-50%, -50%) scale(0);
  transition: all 2s ease-out;
  z-index: 10;
}

.black-overlay.visible {
  transform: translate(-50%, -50%) scale(1);
}

.black-overlay.expand {
  width: 300vw;
  height: 300vw;
}
</style>