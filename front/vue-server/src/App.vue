<template>
  <div class="movie-recommendation">
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="recommendedMovies.length" class="movie-list">
      <div
        v-for="movie in recommendedMovies"
        :key="movie.movie_id"
        class="movie-card"
      >
        <img :src="movie.poster_path" :alt="movie.title" />
        <!-- <h3>{{ movie.title }}</h3>
        <p>{{ movie.overview }}</p>
        <div class="movie-info">
          <span>평점: {{ movie.tmdb_vote_average }}</span>
          <span>개봉일: {{ movie.release_date }}</span>
        </div> -->
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const recommendedMovies = ref([]);
const loading = ref(false);
const error = ref(null);
const URL = process.env.VUE_APP_API_URL;
// const URL = "192.168.201.124:8000";

const api = axios.create({
  baseURL: `http://${URL}`,
  headers: {
    "Content-Type": "application/json",
  },
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

    // 로컬 스토리지에서 감정 분석 데이터 가져오기
    const emotionData = JSON.parse(localStorage.getItem("emotionAnalysis"));

    // 감정 ID 배열 생성
    const emotions = [];

    // 주감정 추가
    const primaryEmotion = Object.keys(emotionData.primary_emotion)[0];
    emotions.push(getEmotionId(primaryEmotion));

    // 부감정 추가 (최대 2개)
    if (emotionData.secondary_emotions) {
      emotionData.secondary_emotions.slice(0, 2).forEach((emotion) => {
        emotions.push(getEmotionId(Object.keys(emotion)[0]));
      });
    }
    console.log({ emotions: emotions });
    // Django 서버로 POST 요청
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

onMounted(() => {
  getMovieRecommendations();
});
</script>

<style scoped>
.movie-recommendation {
  padding: 20px;
}

.loading,
.error {
  text-align: center;
  padding: 20px;
}

.movie-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.movie-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s;
}

.movie-card:hover {
  transform: translateY(-5px);
}

.movie-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.movie-card h3 {
  padding: 10px;
  margin: 0;
}

.movie-card p {
  padding: 0 10px;
  font-size: 0.9em;
  color: #666;
}

.movie-info {
  padding: 10px;
  display: flex;
  justify-content: space-between;
  background-color: #f5f5f5;
}

.movie-info span {
  font-size: 0.8em;
  color: #444;
}
</style>
