// stores/movieStore.js
import { defineStore } from "pinia";
import axios from "axios";

const URL = process.env.VUE_APP_API_URL;

const api = axios.create({
  baseURL: `http://${URL}`,
  headers: { "Content-Type": "application/json" },
});

export const useMovieStore = defineStore("movie", {
  state: () => ({
    recommendedMovies: [],
    emotionData: null,
    loading: false,
    error: null,
  }),

  actions: {
    setEmotionData(data) {
      this.emotionData = data;
      this.getMovieRecommendations();
    },

    async getMovieRecommendations() {
      if (!this.emotionData) return;

      try {
        this.loading = true;
        const emotions = this.getEmotionsArray();

        const response = await api.post("/api/v1/recommend_movies/", {
          emotions: emotions,
        });
        this.recommendedMovies = response.data;
      } catch (err) {
        this.error = "영화 추천을 가져오는 중 오류가 발생했습니다.";
        console.error("Error:", err);
      } finally {
        this.loading = false;
      }
    },

    getEmotionsArray() {
      const emotions = [];
      const primaryEmotion = Object.keys(this.emotionData.primary_emotion)[0];
      emotions.push(this.getEmotionId(primaryEmotion));

      if (this.emotionData.secondary_emotions) {
        this.emotionData.secondary_emotions.slice(0, 2).forEach((emotion) => {
          emotions.push(this.getEmotionId(Object.keys(emotion)[0]));
        });
      }
      return emotions;
    },

    getEmotionId(emotionName) {
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
    },
  },
});
