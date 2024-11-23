<template>
  <div>
    <div class="camera-container">
      <video
        ref="videoElement"
        class="camera-display"
        autoplay
        playsinline
        :style="{ display: !display_flag ? 'none' : 'block' }"
        width="400px"
        height="300px"
      ></video>
      <canvas
        ref="canvasElement"
        style="display: none"
        width="400px"
        height="300px"
      ></canvas>
      <div :style="{ display: display_flag ? 'none' : 'block' }">
        <div v-if="showIntroMessages" class="intro-messages">
          <h2>{{ currentMessage }}</h2>
        </div>

        <div
          class="camera-display"
          v-else
          :style="{ width: '400px', height: '300px' }"
          @click="startStreaming"
        >
          <img
            v-if="frameData"
            ref="imgElement"
            class="camera-display"
            :src="'data:image/jpeg;base64,' + frameData"
          />
          <h1 class="button" style="text-align: center">{{ buttonText }}</h1>
        </div>
      </div>
    </div>

    <p
      class="emotion-text"
      :style="{
        color: showIntroMessages ? 'black' : 'white',
      }"
    >
      {{
        showIntroMessages
          ? "측정 준비중"
          : emotions
          ? `측정중 (${Math.round(measurementProgress)}%)`
          : ""
      }}
    </p>

    <div
      v-if="isFaceDetected && !showIntroMessages"
      class="progress-bar"
      style="width: 400px"
    >
      <div
        class="progress"
        :style="{
          width: `${Math.round(measurementProgress)}%`,
          'background-color': 'whitesmoke',
          height: 7,
        }"
      ></div>
    </div>
  </div>
</template>

<script setup>
// import { defineEmits } from "vue";
import { ref, onUnmounted } from "vue";

const videoElement = ref(null);
const canvasElement = ref(null);
const imgElement = ref(null);
const mode = ref(true);
const ws = ref(null);
const intervalId = ref(null);
const frameCount = ref(0);
const frameData = ref("");
const emotions = ref(null);
const buttonText = ref("카메라 시작");
const analyzing = ref(false);
const result = ref(null);

const showIntroMessages = ref(false);
const currentMessage = ref("");
const messages = [
  "카메라를 통해 감정을 측정합니다",
  "편안한 자세로 정면을 바라봐주세요",
  "자연스러운 표정을 지어주세요",
  "잠시 후 카메라가 시작됩니다",
  "준비하세요...",
];
const display_flag = ref(false);

const measurementProgress = ref(0);
const isFaceDetected = ref(false);
// 메세지 보여주기 및 2차 플래그 전송
const showMessages = async () => {
  showIntroMessages.value = true;
  let messageIndex = 0;

  const messageInterval = setInterval(() => {
    if (messageIndex < messages.length) {
      currentMessage.value = messages[messageIndex];
      messageIndex++;
    } else {
      setTimeout(() => {
        if (analyzing.value) {
          isSecondPhase.value = true;
          secondPhaseFrameCount.value = 0;
          ws.value.send(
            JSON.stringify({
              type: "second_phase",
            })
          );
        }
      }, 1000);

      clearInterval(messageInterval);
      showIntroMessages.value = false;
    }
  }, 1000);
};

const firstPhaseFrameCount = ref(0); // 1차 촬영 프레임 수
const secondPhaseFrameCount = ref(0); // 2차 촬영 프레임 수
const isSecondPhase = ref(false); // 2차 촬영 진행 여부

// const emit = defineEmits(["emotion-detected", "auto-close"]);

// 최종 결과 저장 및 카메라 종료
const handleAnalysisResult = (analysisResult) => {
  // 분석 결과를 localStorage에 저장
  localStorage.setItem("emotionAnalysis", JSON.stringify(analysisResult));
  // 스트림 정지
  stopStreaming();
  // 결과 표시
  result.value = analysisResult;
  buttonText.value = "측정 완료";
};

// 진행도 계산 함수
const calculateProgress = () => {
  if (!isSecondPhase.value || firstPhaseFrameCount.value === 0) return 0;
  return Math.min(
    (secondPhaseFrameCount.value / firstPhaseFrameCount.value) * 100,
    100
  );
};

// 재시작 함수
const restartSecondPhase = () => {
  secondPhaseFrameCount.value = 0;
  measurementProgress.value = 0;
  if (ws.value && ws.value.readyState === WebSocket.OPEN) {
    ws.value.send(
      JSON.stringify({
        type: "restart_second_phase",
      })
    );
  }
};

// 스트리밍 시작 함수
const startStreaming = async () => {
  mode.value = !mode.value;
  analyzing.value = true;
  frameCount.value = 0;

  if (!mode.value) {
    try {
      buttonText.value = "카메라 중지";

      emotions.value = null;
      result.value = null;
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoElement.value.srcObject = stream;
      videoElement.value.play();
      display_flag.value = true;
      setTimeout(() => {
        display_flag.value = false;
        const context = canvasElement.value.getContext("2d");
        const width = videoElement.value.width;
        const height = videoElement.value.height;
        const delay = 100;
        const jpegQuality = 0.7;

        // const URL = process.env.VUE_APP_API_URL;
        const URL = "192.168.31.207:8000";

        ws.value = new WebSocket(`ws://${URL}/ws/stream/`);

        ws.value.onopen = () => {
          console.log("WebSocket connected!!!");
          ws.value.send(
            JSON.stringify({
              type: "start_analysis",
            })
          );
          showMessages();
        };

        ws.value.onmessage = (event) => {
          const data = JSON.parse(event.data);
          if (data.type === "analysis_result") {
            handleAnalysisResult(data.result);
          } else {
            frameData.value = data.frame;
            emotions.value = data.emotion;
            if (emotions.value.flag) isFaceDetected.value = true;
          }
          if (isSecondPhase.value && !emotions.value.flag) {
            restartSecondPhase();
          }

          // 2차 촬영 완료시 분석 종료
          if (
            isSecondPhase.value &&
            secondPhaseFrameCount.value >= firstPhaseFrameCount.value
          ) {
            ws.value.send(
              JSON.stringify({
                type: "stop_analysis",
              })
            );
          }
        };

        intervalId.value = setInterval(() => {
          if (!analyzing.value) {
            clearInterval(intervalId.value);
            return;
          }

          frameCount.value++;

          if (frameCount.value % 5 === 4) return;

          if (!isSecondPhase.value) {
            firstPhaseFrameCount.value++;
          } else {
            secondPhaseFrameCount.value++;
            measurementProgress.value = calculateProgress();
          }

          context.drawImage(videoElement.value, 0, 0, width, height);
          const imageData = canvasElement.value.toDataURL(
            "image/jpeg",
            jpegQuality
          );

          if (ws.value.readyState === WebSocket.OPEN) {
            setTimeout(() => {
              if (analyzing.value) {
                ws.value.send(
                  JSON.stringify({
                    type: "frame",
                    data: imageData,
                  })
                );
              }
            });
          }
        }, delay);
      }, 3000);
    } catch (err) {
      console.error("카메라 접근 오류:", err);
      alert("카메라를 시작할 수 없습니다.");
    }
  } else {
    stopStreaming();
  }
};

const stopStreaming = () => {
  // 분석 상태 초기화
  analyzing.value = false;
  mode.value = true;
  frameCount.value = 0;
  buttonText.value = "카메라 시작";
  measurementProgress.value = 0;
  firstPhaseFrameCount.value = 0;
  secondPhaseFrameCount.value = 0;
  isSecondPhase.value = false;
  isFaceDetected.value = false;
  showIntroMessages.value = false;
  emotions.value = null;

  // 웹소켓 종료
  if (ws.value && ws.value.readyState === WebSocket.OPEN) {
    ws.value.close();
    console.log("WebSocket Disconnected!!!");
  }

  // 카메라 스트림 정지
  if (videoElement.value && videoElement.value.srcObject) {
    videoElement.value.srcObject
      .getVideoTracks()
      .forEach((track) => track.stop());
    videoElement.value.srcObject = null;
  }

  // 캔버스 초기화
  if (canvasElement.value) {
    const can = canvasElement.value.getContext("2d");
    can.clearRect(0, 0, 400, 300);
  }

  // 이미지 초기화
  frameData.value = "";

  // 인터벌 정지
  if (intervalId.value) {
    clearInterval(intervalId.value);
    intervalId.value = null;
  }
};

onUnmounted(() => {
  stopStreaming();
});
</script>

<style scoped>
.camera-container {
  position: relative;
  width: 100%;
  height: 300px;
  display: flex;
  justify-content: center;
  gap: 20px;
}

.camera-display {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  max-width: 640px;
  width: 400px;
  height: 300px;
  margin-top: 7px;
  align-items: center;
  border-radius: 8px;
  border: 2px solid #ccc;
  background-color: #f0f0f0;
}

button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  background-color: #4caf50;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

button:hover {
  transform: scale(1.1);
  color: #4caf50;
}

.emotion-text {
  position: absolute;
  top: 70%;
  left: 50%;
  margin-top: 10px;
  font-size: 1.1em;
  color: #333;
  height: 10px;
  width: 100%;
}

.intro-messages {
  width: 400px;
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f0f0f0;
  border-radius: 8px;
  border: 2px solid #ccc;
  margin: 0 auto;
}

.intro-messages h2 {
  color: #333;
  text-align: center;
  padding: 20px;
  font-size: 1.5em;
}
</style>
