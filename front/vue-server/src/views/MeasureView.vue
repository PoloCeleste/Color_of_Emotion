<template>
  <div class="start-container">
    <div class="content-wrapper">
      <Transition name="button" mode="out-in" appear>
        <div class="circle-container" @click="openModal">
          <div class="circle" :class="{ 'hover-effect': !isModalOpen }">
            <h1 v-if="!measurementComplete" class="measure-button" :disabled="isModalOpen">
              Let's find your emotion
            </h1>
            <Transition name="fade" mode="out-in">
              <h1 v-if="emotionStage > 0" 
                  class="emotion-info typewriter" 
                  :class="emotionClass">
                {{ typedEmotion }}
              </h1>
            </Transition>
          </div>
        </div>
      </Transition>

      <Transition name="camera-body" mode="out-in">
        <div v-if="isModalOpen" class="camera-body">
          <div class="shutter-button" :class="{ pulse: isModalOpen }"></div>
          <div class="flash-window" :class="{ glow: isModalOpen }"></div>
        </div>
      </Transition>
    </div>

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
import MeasureModal from "@/components/MeasureModal.vue";
import { useRouter } from "vue-router";
import { ref, onMounted, nextTick, onBeforeUnmount, computed } from "vue";

// 상수 정의
const TRANSITION_DURATION = 800; // 기본 트랜지션 시간
const DELAY_DURATION = 800; // 지연 시간
const BACKGROUND_TRANSITION = 800; // 배경색 전환 시간

document.documentElement.style.setProperty(
  "--transition-duration",
  `${TRANSITION_DURATION}ms`
);
document.documentElement.style.setProperty(
  "--delay-duration",
  `${DELAY_DURATION}ms`
);

// 상태 관리
const router = useRouter();
const isModalOpen = ref(false);
const measurementComplete = ref(false);
const originalColor = ref("");

// 라우터 핸들러
const goToRecommend = () => {
  setTimeout(() => {
    router.push({
      path: "/animation",
      replace: true,
    });
  }, 800); // 모달 트랜지션 시간과 동일하게 설정
};

// 모달 컨트롤
const openModal = () => {
  isModalOpen.value = true;
  // 모달이 나타나고 나서 배경색과 카메라 몸통이 등장하도록 지연
  setTimeout(() => {
    updateBackgroundColors("#929191");
  }, TRANSITION_DURATION);
};

const updateBackgroundColors = (color) => {
  const startContainer = document.querySelector(".start-container");
  const body = document.body;

  if (startContainer && body) {
    startContainer.style.transition = `background-color ${BACKGROUND_TRANSITION}ms ease`;
    body.style.transition = `background-color ${BACKGROUND_TRANSITION}ms ease`;
    startContainer.style.backgroundColor = color;
    body.style.backgroundColor = color;
  }
};

const closeModal = () => {
  // 배경색 변경과 카메라 몸통 퇴장을 동시에 실행
  updateBackgroundColors(originalColor.value);

  // 배경색 변경과 카메라 몸통 퇴장이 완료된 후 모달 닫기
  setTimeout(() => {
    isModalOpen.value = false;
  }, TRANSITION_DURATION); // 약간의 여유 시간 추가
};

// onMounted 훅 추가
onMounted(() => {
  const startContainer = document.querySelector(".start-container");
  originalColor.value = startContainer.style.backgroundColor;
});

const currentEmotion = ref('');
const typedEmotion = ref('');
const emotionStage = ref(0);
const typingSpeed = 100;
let typingInterval = null;

computed(() => ({
  'primary': emotionStage.value === 1,
  'secondary': emotionStage.value === 2,
  'tertiary': emotionStage.value === 3
}));

const typeEmotion = (emotion) => {
  let currentIndex = 0;
  typedEmotion.value = '';
  clearInterval(typingInterval);
  
  typingInterval = setInterval(() => {
    if (currentIndex < emotion.length) {
      typedEmotion.value += emotion[currentIndex];
      currentIndex++;
    } else {
      clearInterval(typingInterval);
    }
  }, typingSpeed);
};

const showEmotionSequentially = async (emotionData) => {
  const primaryEmotion = Object.keys(emotionData.primary_emotion)[0];
  const secondaryEmotions = emotionData.secondary_emotions.map(emotion => Object.keys(emotion)[0]);

  currentEmotion.value = 'Your emotions';
  typeEmotion('Your emotions');
  emotionStage.value = 0;
  await new Promise(resolve => setTimeout(resolve, 2000));

  emotionStage.value = 1;
  currentEmotion.value = primaryEmotion;
  typeEmotion(primaryEmotion);
  await new Promise(resolve => setTimeout(resolve, 2000));

  if (secondaryEmotions.length > 0) {
    emotionStage.value = 2;
    currentEmotion.value = secondaryEmotions[0];
    typeEmotion(secondaryEmotions[0]);
    await new Promise(resolve => setTimeout(resolve, 2000));
  }

  if (secondaryEmotions.length > 1) {
    emotionStage.value = 3;
    currentEmotion.value = secondaryEmotions[1];
    typeEmotion(secondaryEmotions[1]);
    await new Promise(resolve => setTimeout(resolve, 2000));
  }

  currentEmotion.value = '';
  typedEmotion.value = '';
  emotionStage.value = 0;
};

const completeMeasurement = () => {
  // 1. 플래시 효과 추가
  const flash = document.createElement("div");
  flash.className = "camera-flash";
  document.querySelector(".camera-body").appendChild(flash);

  // 2. 플래시 효과 후 배경색 변경과 카메라 몸통 퇴장
  setTimeout(async () => {
    updateBackgroundColors(originalColor.value);
    flash.remove();

    // 3. 모달창 퇴장과 측정 완료 상태 변경
    setTimeout(async () => {
      isModalOpen.value = false;
      measurementComplete.value = true;

      const emotionData = JSON.parse(localStorage.getItem("emotionAnalysis"));
      if (emotionData && !("error" in emotionData)) {
        await showEmotionSequentially(emotionData);
      }

      await nextTick();

      setTimeout(() => {
        goToRecommend();
      }, TRANSITION_DURATION * 2);
    }, TRANSITION_DURATION);
  }, 300);
};

onBeforeUnmount(() => {
  clearInterval(typingInterval);
});
</script>

<style scoped>
/* 기존 스타일 유지하면서 모달 트랜지션 스타일 수정 */
.modal-enter-active,
.modal-leave-active {
  transition: opacity var(--transition-duration) ease,
    transform var(--transition-duration) cubic-bezier(0.4, 0, 0.2, 1);
}

.modal-enter-from {
  opacity: 0;
  transform: scale(0.95) translateY(10px);
}

.modal-leave-to {
  opacity: 0;
  transform: scale(1.05) translateY(-10px);
}

.modal-enter-to,
.modal-leave-from {
  opacity: 1;
  transform: scale(1) translateY(0);
}

/* 기본 레이아웃 */
.start-container {
  width: 100%;
  height: 100vh;
  background-color: whitesmoke;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  transition: background-color var(--transition-duration) ease
    var(--delay-duration);
}

/* 카메라 몸통 스타일링 */
.camera-body {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 1200px;
  height: 600px;
  background: linear-gradient(145deg, #333333, #1a1a1a);
  border-radius: 20px;
  border: 2px solid #444;
  overflow: hidden;
  box-shadow: inset 0 0 50px rgba(0, 0, 0, 0.5), 0 10px 20px rgba(0, 0, 0, 0.3);
}

/* 카메라 장식 요소 */
.camera-body::before {
  content: "";
  position: absolute;
  top: 20px;
  right: 30px;
  width: 60px;
  height: 60px;
  background: #222;
  border-radius: 50%;
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.8), 0 0 0 2px #444;
}

.camera-body::after {
  content: "";
  position: absolute;
  top: 40px;
  left: 40px;
  width: 100px;
  height: 4px;
  background: #444;
  border-radius: 2px;
}

.camera-body .shutter-button {
  content: "";
  position: absolute;
  top: 30px;
  right: 150px;
  width: 40px;
  height: 40px;
  background: #555;
  border-radius: 50%;
  border: 2px solid #666;
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.5), 0 2px 4px rgba(0, 0, 0, 0.3);
  cursor: pointer;
}

/* 플래시 창 추가 */
.camera-body .flash-window {
  content: "";
  position: absolute;
  top: 25px;
  left: 200px;
  width: 60px;
  height: 30px;
  background: linear-gradient(145deg, #ffffff, #e0e0e0);
  border-radius: 4px;
  border: 2px solid #444;
  box-shadow: inset 0 0 15px rgba(255, 255, 255, 0.8),
    0 2px 4px rgba(0, 0, 0, 0.2);
}

.camera-body-enter-active {
  transition: all var(--transition-duration) ease var(--delay-duration);
}

.camera-body-leave-active {
  transition: all var(--transition-duration) ease;
}

.camera-body-enter-from,
.camera-body-leave-to {
  opacity: 0;
  transform: translate(-50%, -50%) scale(0.8);
}

.camera-flash {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: white;
  opacity: 0;
  animation: flash 0.3s ease-out;
  pointer-events: none;
  z-index: 10;
}

@keyframes flash {
  0% {
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}
/* 원형 렌즈 스타일링 */
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
  top: -1%;
  left: -1%;
  width: 102%;
  height: 102%;
  border-radius: 50%;
  background: linear-gradient(145deg, #f0f0f0, #ffffff);
  border: 2px solid darkgray;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: inset 0 0 50px rgba(0, 0, 0, 0.1), 0 10px 20px rgba(0, 0, 0, 0.2);
  transform-style: preserve-3d;
  perspective: 1000px;
  transition: transform 0.3s ease;
  transition: all 0.3s ease;
}

.circle:hover {
  transform: scale(1.02);
  box-shadow: inset 0 0 60px rgba(0, 0, 0, 0.15), 0 15px 25px rgba(0, 0, 0, 0.3),
    0 0 0 2px rgba(0, 0, 0, 0.1);
}

/* 버튼 스타일링 */
.measure-button {
  padding: 20px 40px;
  font-size: 2rem;
  font-weight: bold;
  color: darkgray;
  background: transparent;
  border: none;
  cursor: pointer;
  letter-spacing: 2px;
  text-align: center;
  transform: scale(1);
  transition: transform 0.3s ease, color 0.3s ease;
  transform: translateZ(0); /* 하드웨어 가속 활성화 */
  backface-visibility: hidden; /* 텍스트 깜빡임 방지 */
  -webkit-font-smoothing: antialiased; /* 폰트 렌더링 개선 */
  will-change: transform; /* 브라우저에 변화 예고 */
}

.measure-button:hover {
  transform: scale(1.1);
  color: #4caf50;
}

.start-button {
  font-size: 50px;
  font-weight: bold;
  background: transparent;
  border: none;
  cursor: pointer;
  letter-spacing: 2px;
  transform: translateZ(0);
  backface-visibility: hidden;
  -webkit-font-smoothing: antialiased;
  will-change: transform;
  transition: transform 0.3s ease;
}

.circle:hover .start-button {
  transform: translateZ(0) scale(1.1);
}

@keyframes gradient-shift {
  0% {
    background-position: 0% center;
  }
  100% {
    background-position: 200% center;
  }
}

/* 트랜지션 효과 */
/* 트랜지션 타이밍 수정 */

/* 기존 스타일 유지하면서 다음 스타일 추가 */

/* 카메라 효과 개선 */
.flash-window.glow {
  animation: glow 3s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

@keyframes glow {
  0% {
    opacity: 0.8;
  }
  50% {
    opacity: 1;
    box-shadow: 0 0 20px rgba(255, 255, 255, 0.8);
  }
  100% {
    opacity: 0.8;
  }
}

/* 버튼 트랜지션 */
.button-enter-active,
.button-leave-active {
  transition: all 0.3s ease;
}

.button-enter-from,
.button-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* 호버 효과 개선 */
.circle.hover-effect:hover {
  transform: translateY(-5px);
  box-shadow: inset 0 0 60px rgba(0, 0, 0, 0.15), 0 15px 25px rgba(0, 0, 0, 0.3),
    0 0 0 2px rgba(0, 0, 0, 0.1);
}

.emotion-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.emotion-info {
  text-align: center;
  color: #333;
  transition: all 0.5s ease;
}

.primary {
  font-size: 2rem;
}

.secondary, .tertiary {
  font-size: 1.5rem;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease, transform 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.typewriter {
  font-family: "Courier New", monospace;
  white-space: nowrap;
  overflow: hidden;
  border-right: 3px solid #2c3e50;
  animation: blink-caret 0.75s step-end infinite;
}

@keyframes blink-caret {
  from, to { border-color: transparent; }
  50% { border-color: #2c3e50; }
}

.emotion-info {
  font-size: 3rem;
  text-align: center;
  color: #333;
  transition: all 0.5s ease;
}

.primary { font-size: 2.5rem; }
.secondary { font-size: 2rem; }
.tertiary { font-size: 1.5rem; }
</style>
