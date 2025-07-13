// stores/movieStore.js
import { defineStore } from "pinia";
import axios from "axios";

const URL = process.env.VUE_APP_API_URL;

const api = axios.create({
  baseURL: `https://${URL}`,
  headers: { "Content-Type": "application/json" },
});

const shuffleArray = (array) => {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
};

export const useMovieStore = defineStore("movie", {
  state: () => ({
    recommendedMovies: [],
    emotionData: null,
    emotionsArray: [],
    selectedColors: [],
    loading: false,
    error: null,
    lastAnimationState: null,
  }),

  actions: {
    setEmotionData(data) {
      this.emotionData = data;
      this.selectedColors = [];
      this.getMovieRecommendations();
    },

    async getMovieRecommendations() {
      if (!this.emotionData) return;

      try {
        this.loading = true;
        this.emotionsArray = this.getEmotionsArray();

        const response = await api.post("/api/v1/recommend_movies/", {
          emotions: this.emotionsArray,
        });

        const movies = response.data;
        const staticPart = shuffleArray(movies.slice(0, -10)); // 앞부분 유지
        const shufflePart = shuffleArray([...movies.slice(-10)]);

        this.recommendedMovies = [...staticPart, ...shufflePart];

        // 영화 추천 후 색상 데이터 요청
        if (!this.selectedColors) await this.getEmotionColors();
      } catch (err) {
        this.error = "영화 추천을 가져오는 중 오류가 발생했습니다.";
        console.error("Error:", err);
      } finally {
        this.loading = false;
      }
    },

    async getEmotionColors() {
      try {
        const response = await api.post("/api/v1/emotion-colors/", {
          emotions: this.emotionsArray,
        });

        // 랜덤으로 3개 색상 선택
        const colors = response.data.emotions_color;
        const selectedColors = [];
        while (selectedColors.length < 3) {
          const randomIndex = Math.floor(Math.random() * colors.length);
          const color = colors[randomIndex];
          if (
            !selectedColors.some(
              (selected) =>
                selected[0] === color[0] &&
                selected[1] === color[1] &&
                selected[2] === color[2]
            )
          ) {
            selectedColors.push(color);
          }
        }

        this.selectedColors = selectedColors;
        this.emotionsArray = []; // emotionsArray 초기화
      } catch (err) {
        console.error("Error fetching emotion colors:", err);
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

    setLastAnimationState(state) {
      this.lastAnimationState = state;
    },
  },
});
