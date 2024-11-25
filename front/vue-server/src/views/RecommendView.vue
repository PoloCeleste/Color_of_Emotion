<template>
  <div class="about">
    <div class="circle-container" v-if="!showFilm">
      <div
        class="circle"
        :class="{
          'rainbow-shadow': measurementComplete,
          'hover-effect': !isModalOpen,
        }"
      >
        <button
          class="start-button"
          @click="startAnimation"
          style="background-color: whitesmoke"
        >
          START
        </button>
      </div>
    </div>
    <FilmAnimation
      v-if="showFilm && recommendedMovies.length > 0"
      :movies="recommendedMovies"
      :emotionData="emotionData"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import FilmAnimation from "@/components/FilmAnimation.vue";
import axios from "axios";

const recommendedMovies = ref([]);
const emotionData = ref(null);
const loading = ref(false);
const error = ref(null);
const showFilm = ref(false);

const URL = process.env.VUE_APP_API_URL;
const api = axios.create({
  baseURL: `http://${URL}`,
  headers: { "Content-Type": "application/json" },
});

const getEmotionId = (emotionName) => {
  const emotionMap = {
    Joy: 1,
    Sadness: 2,
    Anger: 3,
    Embarrassment: 4,
    Anxiety: 5,
    Pain: 6,
    Neutral: 7,
  };
  return emotionMap[emotionName];
};

const getMovieRecommendations = async () => {
  try {
    loading.value = true;
    emotionData.value = JSON.parse(localStorage.getItem("emotionAnalysis"));
    const emotions = [];

    const primaryEmotion = Object.keys(emotionData.value.primary_emotion)[0];
    emotions.push(getEmotionId(primaryEmotion));

    if (emotionData.value.secondary_emotions) {
      emotionData.value.secondary_emotions.slice(0, 2).forEach((emotion) => {
        emotions.push(getEmotionId(Object.keys(emotion)[0]));
      });
    }

    const response = await api.post("/api/v1/recommend_movies/", {
      emotions: emotions,
    });
    recommendedMovies.value = response.data;
  } catch (err) {
    error.value = "영화 추천을 가져오는 중 오류가 발생했습니다.";
    console.error("Error:", err);
  } finally {
    loading.value = false;
  }
};

const startAnimation = () => {
  showFilm.value = true;
};

onMounted(() => {
  getMovieRecommendations();
});
</script>

<style scoped>
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
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
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
  transform: translateY(-5px);
  box-shadow: inset 0 0 60px rgba(0, 0, 0, 0.15), 0 15px 25px rgba(0, 0, 0, 0.3),
    0 0 0 2px rgba(0, 0, 0, 0.1);
}

.about {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.start-button {
  padding: 20px 40px;
  font-size: 50px;
  font-weight: bold;
  border: none;
  cursor: pointer;
  letter-spacing: 2px;
  transform: translateZ(0);
  backface-visibility: hidden;
  -webkit-font-smoothing: antialiased;
  will-change: transform;
  transition: transform 0.3s ease;
}
</style>
