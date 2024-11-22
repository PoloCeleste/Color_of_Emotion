﻿<template>
<div class="modal" v-if="isOpen">
<div class="modal-content">
<!-- 영화 기본 정보 -->
<div class="movie-header">
<h1>{{ card.title }}</h1>
<h3>{{ card.original_title }} ({{ card.language }})</h3>
<div class="movie-meta">
<span>개봉일: {{ card.release_date }}</span>
<br>
<span>평점: {{ card.vote_average }}</span>
</div>
</div>

<!-- 영화 상세 정보 -->
<div class="movie-details">
<p class="overview">{{ card.description }}</p>

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

<div v-if="card.providers">
<p>보려면?</p>
<!-- {{ card.providers }} -->
<h4 v-for="(provider, index) in card.providers" 
:key="index" 
class="provider-tag">
{{ provider }}
</h4>
</div>
<div>
<a :href="card.watchapedia" target="_blank">더 알아보기</a>
<!-- {{ card.watchapedia }} -->
</div>

<div>
<!-- {{ card.title }}<br> -->
<!-- {{ card.original_title }}<br> -->
<!-- {{ card.language }}<br> -->
<!-- {{ card.description }}<br> -->
<!-- {{ card.vote_average }}<br> -->
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
<button class="close-btn" @click="$emit('close')">닫기</button>
</div>
</div>
</template>

<script setup>
import { defineProps, ref } from 'vue'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  card: {
    type: Object,
    required: true
  }
})
console.log(props.card)

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
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
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
  overflow-x: auto;
  white-space: nowrap;
}

.gallery-item, .video-item {
  display: inline-block;
  margin-right: 10px;
}

.gallery-item img, .video-item iframe {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
</style>