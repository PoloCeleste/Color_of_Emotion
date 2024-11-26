<template>
  <div>
    <div class="camera-container">
      <div v-if="showIntroMessages" class="camera-display">
        <div class="intro-messages">
          <h2>{{ currentMessage }}</h2>
        </div>
      </div>
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
        width="400"
        height="300"
      ></canvas>

      <div :style="{ display: display_flag ? 'none' : 'block' }">
        <div v-if="showIntroMessages" class="camera-display">
          <div class="intro-messages">
            <h2>{{ currentMessage }}</h2>
          </div>
        </div>

        <div
          class="camera-display"
          v-else
          @click="startStreaming"
          style="margin-bottom: 0px; top: 50% + 7px"
        >
          <img
            v-if="frameData"
            ref="imgElement"
            class="camera-display"
            :src="'data:image/jpeg;base64,' + frameData"
            style="margin-bottom: 0px; top: 50% + 7px"
          />
          <h1 class="button" style="text-align: center">{{ buttonText }}</h1>
          <svg
            class="progress-circle absolute z-10 -rotate-90"
            width="500"
            height="500"
            viewBox="0 0 500 500"
          >
            <circle
              class="progress-circle-bg"
              cx="250"
              cy="250"
              r="240"
              fill="none"
              stroke="#ddd"
              stroke-width="20"
            />
            <circle
              ref="progressCircle"
              class="progress-circle-bar"
              cx="250"
              cy="250"
              r="240"
              fill="none"
              stroke="url(#progressGradient)"
              stroke-width="20"
              :stroke-dasharray="circumference"
              :stroke-dashoffset="dashOffset"
            />
            <defs>
              <linearGradient
                id="progressGradient"
                gradientTransform="rotate(135)"
              >
                <stop offset="0%" stop-color="#1853FF" />
                <stop offset="100%" stop-color="#18FF59" />
              </linearGradient>
            </defs>
          </svg>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineEmits } from "vue";
import { ref, onUnmounted, computed, onMounted } from "vue";

const videoElement = ref(null);
const canvasElement = ref(null);
const imgElement = ref(null);

const radius = 240;
const circumference = computed(() => 2 * Math.PI * radius);
const dashOffset = computed(() => {
  return circumference.value * (1 - measurementProgress.value / 100);
});

const mode = ref(true);
const ws = ref(null);
const intervalId = ref(null);
const frameCount = ref(0);
const frameData = ref("");
const emotions = ref(null);
const buttonText = ref("카메라 시작");
const analyzing = ref(false);
const result = ref(null);
const stopflag = ref(false);

const showIntroMessages = ref(false);
const currentMessage = ref("");

onMounted(() => {
  const startMessage = [
    "지금의 감정을 알아내볼게요.",
    "카메라 정면을 보고 바르게 앉아주세요.",
    "우선 지금의 표정을 볼까요?",
    "",
  ];
  showMessages(startMessage, false);
});

const messages = [
  "오늘 어떤 일이 있었나요?",
  "가장 기억에 남는 일은 무엇인가요?",
  "오늘의 기억을 되돌아보아요.",
  "기억의 감정을 갖고",
  "여러분을 다시 봅시다.",
];
const display_flag = ref(false);

const measurementProgress = ref(0);
const isFaceDetected = ref(false);
// 메세지 보여주기 및 2차 플래그 전송
const showMessages = async (messages, flag) => {
  // currentMessage.value = "준비하세요...";
  showIntroMessages.value = true;
  let messageIndex = 0;

  const messageInterval = setInterval(
    () => {
      if (messageIndex < messages.length) {
        currentMessage.value = messages[messageIndex];
        messageIndex++;
      } else if (flag) {
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
      } else {
        clearInterval(messageInterval);
        showIntroMessages.value = false;
        startStreaming();
      }
    },
    flag ? 1200 : 1500
  );
};

const firstPhaseFrameCount = ref(0); // 1차 촬영 프레임 수
const secondPhaseFrameCount = ref(0); // 2차 촬영 프레임 수
const isSecondPhase = ref(false); // 2차 촬영 진행 여부

const emit = defineEmits(["measurement-complete"]);
import { useMovieStore } from "@/store/stores";

const movieStore = useMovieStore();

// 최종 결과 저장 및 카메라 종료
const handleAnalysisResult = (analysisResult) => {
  // 분석 결과를 localStorage에 저장
  localStorage.setItem("emotionAnalysis", JSON.stringify(analysisResult));
  movieStore.setEmotionData(analysisResult);
  // 스트림 정지
  stopStreaming();
  // 결과 표시
  result.value = analysisResult;
  buttonText.value = "측정 완료";
  emit("measurement-complete", analysisResult);
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
  analyzing.value = !analyzing.value;
  frameCount.value = 0;

  if (!canvasElement.value) {
    console.error("Canvas element not found");
    return;
  }

  const context = canvasElement.value.getContext("2d");
  if (!context) {
    console.error("Failed to get canvas context");
    return;
  }

  if (!mode.value) {
    try {
      buttonText.value = "";

      emotions.value = null;
      result.value = null;
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoElement.value.srcObject = stream;
      videoElement.value.play();
      display_flag.value = true;
      setTimeout(() => {
        display_flag.value = false;
        const delay = 100;
        const jpegQuality = 0.7;

        const URL = process.env.VUE_APP_API_URL;
        // const URL = "192.168.31.207:8000";
        // const URL = "192.168.201.124:8000";

        ws.value = new WebSocket(`ws://${URL}/ws/stream/`);

        ws.value.onopen = () => {
          console.log("WebSocket connected!!!");
          ws.value.send(
            JSON.stringify({
              type: "start_analysis",
            })
          );
          showMessages(messages, true);
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
            !stopflag.value &&
            isSecondPhase.value &&
            secondPhaseFrameCount.value >= firstPhaseFrameCount.value
          ) {
            ws.value.send(
              JSON.stringify({
                type: "stop_analysis",
              })
            );
            stopflag.value = true;
          }
        };

        intervalId.value = setInterval(() => {
          if (!analyzing.value) {
            clearInterval(intervalId.value);
            return;
          }
          const context = canvasElement.value.getContext("2d");
          const width = videoElement.value.width;
          const height = videoElement.value.height;

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
  height: 100%;
  display: flex;
  justify-content: center;
  gap: 20px;
}

.progress-circle {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) rotate(-90deg);
}

.progress-circle-bar {
  transition: stroke-dashoffset 0.3s ease;
}

video,
img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.camera-display {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 500px;
  height: 500px;
  border-radius: 50%;
  border: 2px solid #333;
  background-color: #1a1a1a;
  overflow: hidden;
  display: flex; /* 추가 */
  justify-content: center; /* 추가 */
  align-items: center; /* 추가 */
  color: rgba(255, 245, 238, 0.795);
}

button {
  padding: 8px 16px;
  border: none;
  background-color: #4caf50;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 2; /* 추가 */
}

button:hover {
  transform: scale(1.1);
  color: #4caf50;
}

.emotion-text {
  position: absolute;
  top: 68%;
  left: 41%;
  margin-top: 10px;
  font-size: 1.1em;
  color: #333;
  height: 10px;
  width: 22%;
}

.intro-messages {
  width: 500px;
  height: 500px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f0f0f0;
  border-radius: 8px;
  border: 2px solid #ccc;
}

.intro-messages h2 {
  color: #333;
  text-align: center;
  padding: 20px;
  font-size: 1.5em;
}
</style>
