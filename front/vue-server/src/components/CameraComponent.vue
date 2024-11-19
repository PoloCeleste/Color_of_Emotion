<template>
  <div>
    <video
      ref="videoElement"
      :width="400"
      :height="300"
      style="display: none"
    ></video>
    <canvas
      ref="canvasElement"
      :width="400"
      :height="300"
      style="display: none"
    ></canvas>
    <img
      ref="imgElement"
      id="client"
      :width="400"
      :height="300"
      :src="'data:image/jpeg;base64,' + frameData"
    /><br />
    <button @click="startStreaming">{{ buttonText }}</button>
    <br />
    <p v-if="emotions">{{ emotions.emotion }}</p>
  </div>
</template>

<script setup>
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
const buttonText = ref("Start Streaming");

const startStreaming = async () => {
  mode.value = !mode.value;

  if (!mode.value) {
    try {
      buttonText.value = "Stop Streaming";
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoElement.value.srcObject = stream;
      videoElement.value.play();

      const context = canvasElement.value.getContext("2d");
      const width = videoElement.value.width;
      const height = videoElement.value.height;
      const delay = 100; // 원래 딜레이 유지
      const jpegQuality = 0.7;

      ws.value = new WebSocket("ws://192.168.201.124:8000/ws/stream/");

      ws.value.onopen = () => {
        console.log("WebSocket connected!!!");
      };

      ws.value.onmessage = (event) => {
        const data = JSON.parse(event.data);
        frameData.value = data.frame;
        emotions.value = data.emotion;
        // console.log(emotions);
        // imgElement.value.src = `data:image/jpeg;base64,${event.data}`;
      };

      // const startTime = Date.now();

      intervalId.value = setInterval(() => {
        // if (Date.now() - startTime >= 5000) {
        //   // 5초 후 중지
        //   stopStreaming();
        //   return;
        // }

        if (frameCount.value % 5 !== 4) {
          // 5프레임 중 4프레임만 전송 (1프레임 스킵)
          context.drawImage(videoElement.value, 0, 0, width, height);
          canvasElement.value.toBlob(
            (blob) => {
              if (ws.value.readyState === WebSocket.OPEN) {
                ws.value.send(mode.value ? new Uint8Array([]) : blob);
              }
            },
            "image/jpeg",
            jpegQuality
          );
        }

        frameCount.value++;
      }, delay);
    } catch (error) {
      console.error("Error accessing media devices", error);
    }
  } else {
    stopStreaming();
  }
};

const stopStreaming = () => {
  // Stop video and WebSocket
  videoElement.value.pause();
  videoElement.value.srcObject.getVideoTracks()[0].stop();
  videoElement.value.srcObject = null;
  canvasElement.value.srcObject = null;
  imgElement.value.src = null; // 기본값 사진 넣기
  const can = canvasElement.value.getContext("2d");
  can.clearRect(0, 0, 400, 300);

  if (ws.value) {
    ws.value.close();
  }

  clearInterval(intervalId.value);
  mode.value = true;
  frameCount.value = 0;
  buttonText.value = "Start Streaming";
};

onUnmounted(() => {
  if (ws.value) {
    ws.value.close();
  }
  clearInterval(intervalId.value);
  buttonText.value = "Start Streaming";
});
</script>

<style scoped>
img {
  border-radius: 40%;
  border: lightgray 2px solid;
  background-color: #c0c0c0;
}
button {
  border: solid 1px dodgerblue;
  color: white;
  background-color: dodgerblue;
  border-radius: 5px;
  padding: 5px 15px;
  margin-top: 10px;
}
div {
  text-align: center;
}
</style>
<style>
body {
  background-color: whitesmoke;
}
</style>