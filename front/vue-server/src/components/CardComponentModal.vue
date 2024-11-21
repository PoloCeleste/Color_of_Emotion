<template>
  <div class="modal" v-if="isOpen">
    <div class="modal-content">
      <!-- 영화 기본 정보 -->
      <div class="movie-header">
        <h1>{{ card.title }}</h1>
        <h3>원제 : {{ card.original_title }}({{ card.language }})</h3>
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
          <span v-for="genreId in card.genre_ids" 
                :key="genreId" 
                class="genre-tag">
            {{ getGenreName(genreId) }}
          </span>
        </div>
      </div>
      <div v-if="card.reviews">
        <p>리뷰</p>
        <p v-for="(review, index) in card.reviews" :key="index">{{ review }}</p>
      </div>

      <div v-if="card.picture_url">
        <p>갤러리</p>
        <p v-for="(picture_url, index) in card.picture_url" :key="index">
          <img :src="picture_url" alt="">
        </p>
        <!-- {{ card.picture_url }} -->
      </div>

      <div v-if="card.video_url">
        <p>동영상</p>
        <p v-for="(video_url, index) in card.video_url" :key="index">
          <iframe :src= "video_url" frameborder="0"></iframe>
        </p>
        <!-- {{ card.video_url }} -->
      </div>
      
      <div v-if="card.providers">
        <p>보려면?</p>
        <!-- {{ card.providers }} -->
        <h4 v-for="providerId in card.providers" 
              :key="providerId" 
              class="provider-tag">
          {{ getProviderName(providerId) }}
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
import { defineProps } from 'vue'
import genres from '@/data/genres.json'
import providers from '@/data/providers.json'

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
const getGenreName = (genreId) => {
  const genre = genres.find(g => g.id === genreId)
  return genre ? genre.name : ''
}

const getProviderName = (providerId) => {
  console.log(providerId)
  const provider = providers.find(p => p.provider_id === providerId)
  console.log(provider)
  return provider ? provider.provider_name : ''
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
</style>