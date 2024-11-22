<template>
  <div class="modal" v-if="isOpen" @click.self="$emit('close')">
    <div class="modal-content">
      <!-- 영화 기본 정보 -->
      <div class="movie-header">
        <h1>{{ card.title }}</h1>
        <h3>{{ card.original_title }} ({{ card.original_language }})</h3>
        <div class="movie-meta">
          <span>개봉일: {{ card.release_date }}</span>
          <br>
          <span>평점: {{ card.tmdb_vote_average }}</span>
        </div>
      </div>

      <!-- 영화 상세 정보 -->
    <div class="movie-details">
      <p class="overview">{{ card.overview }}</p>

      <!-- 장르 정보 -->
      <div class="genre-list">
        장르 : 
        <span v-for="(genre, index) in card.genre_ids" 
        :key="index" 
        class="genre-tag">
        {{ genre }}
        </span>
      </div>
    </div>
    <div v-if="card.reviews">
    <p>리뷰</p>
    <div v-for="(review, index) in card.reviews" :key="index">
    <p v-if="showFullReviewIndex !== index && review.length > 100">
    {{ review.substring(0, 100) }}...
    <button @click="showFullReview(index)">더보기</button>
    </p>
    <p v-else-if="showFullReviewIndex === index">
    {{ review }}
    <button @click="hideFullReview(index)">줄이기</button>
    </p>
    <p v-else>{{ review }}</p>
    </div>
    </div>

    <div v-if="card.picture_url">
    <p>갤러리</p>
    <div class="gallery-container">
    <div v-for="(picture_url, index) in card.picture_url" :key="index" class="gallery-item">
    <img :src="picture_url" alt="" />
    </div>
    </div>
    </div>

    <div v-if="card.video_url">
    <p>동영상</p>
    <div class="video-container">
    <div v-for="(video_url, index) in card.video_url" :key="index" class="video-item">
    <iframe :src="video_url" frameborder="0"></iframe>
    </div>
    </div>
    </div>

    <div v-if="card.watch_providers">
      <p>보려면?</p>
      <!-- {{ card.providers }} -->
      <h4 v-for="(provider, index) in card.watch_providers" 
        :key="index" 
        class="provider-tag"
      >
      <img :src="provider.logo_path" alt="">
      {{ provider.provider_name }}
      </h4>
    </div>
    <div>
    <a :href="card.watchapedia" target="_blank">더 알아보기</a>
    <!-- {{ card.watchapedia }} -->
    </div>

    <div>
    <!-- o{{ card.title }}<br> -->
    <!-- o{{ card.original_title }}<br> -->
    <!-- {{ card.original_language }}<br> -->
    <!-- {{ card.overview }}<br> -->
    <!-- {{ card.tmdb_vote_average }}<br> -->
    <!-- {{ card.genre_ids }}<br> -->
    <!-- {{ card.release_date }}<br> -->
    <!-- {{ card.description }}<br> -->
    <!-- {{ card.providers }}<br> -->
    <!-- {{ card.picture_url }}<br> -->
    <!-- {{ card.video_url }}<br> -->
    <!-- {{ card.reviews }}<br> -->
    <!-- {{ card.watchapedia }}<br> -->
    </div>

    <!-- 닫기 버튼 -->
    <button 
      class="close-btn" 
      @click="$emit('close')"
      aria-label="모달 닫기"
    >
      닫기
    </button>
    </div>
  </div>
</template>

<script setup>
import { defineProps, ref } from 'vue'

defineProps({
    isOpen: {
    type: Boolean,
    required: true
    },
    card: {
    type: Object,
    required: true
    }
})

const showFullReviewIndex = ref(null)

const showFullReview = (index) => {
    showFullReviewIndex.value = index
}

const hideFullReview = () => {
    showFullReviewIndex.value = null
}
</script>

<style scoped>
.modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal-content {
    background: white;
    padding: 20px;
    border-radius: 8px;
    max-width: 800px; /* 더 넓게 조정 */
    width: 90%;
    max-height: 90vh; /* 높이 증가 */
    overflow-y: auto;
    scrollbar-width: thin; /* 스크롤바 스타일링 */
}

.movie-header {
    margin-bottom: 20px;
}

.movie-meta {
    color: #666;
    font-size: 0.9em;
}

.genre-tag {
    background: #eee;
    padding: 4px 8px;
    border-radius: 4px;
    margin-right: 8px;
    font-size: 0.8em;
}

.close-btn {
    margin-top: 20px;
    padding: 8px 16px;
    background: #333;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.gallery-container, .video-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 10px;
    margin: 10px 0;
}

.gallery-item, .video-item {
    display: inline-block;
    margin-right: 10px;
}

.gallery-item img, .video-item iframe {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 4px;
}
</style>