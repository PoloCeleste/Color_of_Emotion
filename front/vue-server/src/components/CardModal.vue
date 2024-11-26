<template>
  <Transition name="modal">
    <div v-if="isActive" class="card-modal">
      <div class="card-modal__inner">
        <div class="card-modal__image">
          <img :src="movie.poster_path" :alt="movie.title" />
        </div>
        <div class="card-modal__content">
          <h2 class="content__heading">{{ movie.title }}</h2>
          <span class="content__description">{{ movie.original_title }} ({{ movie.original_language }})</span>
          <span class="content__description">{{ movie.release_date }} / {{ movie.tmdb_vote_average }}</span><br>
          <span class="content__category">{{ movie.genre_ids.join(", ") }}</span>
          <p class="content__description">{{ movie.overview }}</p>
          <button class="close-button" @click="closeModal">×</button>
          
          <div v-if="movie.reviews">
            <h3>리뷰</h3>
            <div v-for="(review, index) in movie.reviews" :key="index">
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

          <div v-if="movie.picture_url">
            <h3>갤러리</h3>
            <div class="gallery-container">
              <button class="nav-button prev" @click="prevImage">&#10094;</button>
              <div class="gallery-item" v-if="currentImageIndex < movie.picture_url.length">
                <img :src="movie.picture_url[currentImageIndex]" alt="" @click="openLightbox(movie.picture_url[currentImageIndex])" />
              </div>
              <button class="nav-button next" @click="nextImage">&#10095;</button>
            </div>
          </div>

          <div v-if="movie.video_url">
            <h3>동영상</h3>
            <div class="video-container">
              <button class="nav-button prev" @click="prevVideo">&#10094;</button>
              <div class="video-item" v-if="currentVideoIndex < movie.video_url.length">
                <img :src="getYoutubeThumbnail(movie.video_url[currentVideoIndex])" alt="Video thumbnail" @click="openVideoModal(movie.video_url[currentVideoIndex])" />
                <div class="play-button"></div>
              </div>
              <button class="nav-button next" @click="nextVideo">&#10095;</button>
            </div>
          </div>

          <div v-if="movie.watch_providers">
            <h3>보려면?</h3>
            <div class="provider-container">
              <h4 v-for="(provider, index) in movie.watch_providers" 
                :key="index" 
                class="provider-tag"
              >
                <img :src="provider.logo_path" alt="">
                {{ provider.provider_name }}
              </h4>
            </div>
          </div>
          
          <div class="more-info">
            <a :href="movie.watchapedia" target="_blank">더 알아보기</a>
          </div>
        </div>
      </div>
    </div>
  </Transition>

<!-- Lightbox for images -->
<div v-if="lightboxImage" class="lightbox" @click="closeLightbox">
    <img :src="lightboxImage" alt="" />
  </div>

  <!-- Modal for videos -->
  <div v-if="videoModalUrl" class="video-modal" @click="closeVideoModal">
    <div class="video-modal-content">
      <iframe :src="videoModalUrl" frameborder="0" allowfullscreen></iframe>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref } from 'vue';

const props = defineProps({
  movie: Object,
  isActive: Boolean,
});

const emit = defineEmits(['close']);

const showFullReviewIndex = ref(null);

const closeModal = () => {
  emit('close');
};

const showFullReview = (index) => {
  showFullReviewIndex.value = index;
};

const hideFullReview = () => {
  showFullReviewIndex.value = null;
};

const lightboxImage = ref(null);
const videoModalUrl = ref(null);

const openLightbox = (imageUrl) => {
  lightboxImage.value = imageUrl;
};

const closeLightbox = () => {
  lightboxImage.value = null;
};

const openVideoModal = (videoUrl) => {
  videoModalUrl.value = videoUrl;
};

const closeVideoModal = () => {
  videoModalUrl.value = null;
};

const getYoutubeThumbnail = (url) => {
  const videoId = url.split('v=')[1];
  return `https://img.youtube.com/vi/${videoId}/0.jpg`;
};

const currentImageIndex = ref(0);
const currentVideoIndex = ref(0);

const nextImage = () => {
  if (currentImageIndex.value < props.movie.picture_url.length - 1) {
    currentImageIndex.value++;
  }
};

const prevImage = () => {
  if (currentImageIndex.value > 0) {
    currentImageIndex.value--;
  }
};

const nextVideo = () => {
  if (currentVideoIndex.value < props.movie.video_url.length - 1) {
    currentVideoIndex.value++;
  }
};

const prevVideo = () => {
  if (currentVideoIndex.value > 0) {
    currentVideoIndex.value--;
  }
};
</script>

<style scoped>
.card-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.card-modal__inner {
  display: flex;
  width: 90%;
  height: 90%;
  background-color: transparent;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  border: whitesmoke 1px solid;
}

.card-modal__image {
  flex: 1;
  overflow: hidden;
}

.card-modal__image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-modal__content {
  flex: 1;
  padding: 40px;
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  overflow-y: auto;
  max-height: 90vh;
}

.card-modal__content::-webkit-scrollbar {
  width: 10px;
}

.card-modal__content::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 5px;
}

.card-modal__content::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 5px;
}

.card-modal__content::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

.content__heading {
  font-size: 42px;
  margin-bottom: 10px;
}

.content__category {
  background-color: cadetblue;
  display: inline-block;
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  padding: 0 12px;
  line-height: 30px;
  border-radius: 15px;
  align-self: flex-start;
  margin-top: 8px;
}

.content__description {
  font-size: 17px;
  line-height: 1.5;
  margin-top: 20px;
  color: #bababa;
}

.close-button {
  position: absolute;
  top: 20px;
  right: 20px;
  background: none;
  border: none;
  font-size: 30px;
  color: white;
  cursor: pointer;
  z-index: 10;
}

.gallery-container, .video-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-top: 10px;
}

.gallery-item, .video-item {
  width: calc(100% - 80px);
  aspect-ratio: 16 / 9;
  overflow: hidden;
}

.gallery-item img, .video-item iframe {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.nav-button {
  background: rgba(255, 255, 255, 0.3);
  border: none;
  color: white;
  font-size: 24px;
  padding: 10px;
  cursor: pointer;
  transition: background 0.3s;
}

.nav-button:hover {
  background: rgba(255, 255, 255, 0.5);
}

.provider-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
}

.provider-tag {
  display: inline-flex;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.1);
  padding: 5px 10px;
  border-radius: 15px;
  margin-right: 10px;
  margin-bottom: 10px;
}

.provider-tag img {
  width: 20px;
  height: 20px;
  margin-right: 5px;
}

.more-info {
  margin-top: 20px;
}

.more-info a {
  color: #4CAF50;
  text-decoration: none;
}

.more-info a:hover {
  text-decoration: underline;
}

/* 트랜지션 애니메이션 */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

@media (max-width: 768px) {
  .card-modal__inner {
    flex-direction: column;
  }

  .card-modal__image {
    height: 40vh;
  }

  .card-modal__content {
    padding: 20px;
  }

  .content__heading {
    font-size: 32px;
  }

  .gallery-item, .video-item {
    width: calc(50% - 10px);
  }
}

.gallery-container, .video-container {
  display: flex;
  overflow-x: auto;
  gap: 10px;
  padding: 10px 0;
  scroll-snap-type: x mandatory;
  width: 100%; /* 컨테이너 너비 제한 */
  flex-wrap: nowrap; /* 줄바꿈 방지 */
}

.gallery-item, .video-item {
  flex: 0 0 auto;
  width: 200px;
  height: 150px;
  scroll-snap-align: start;
  cursor: pointer;
  position: relative;
}

.gallery-item img, .video-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-item .play-button {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 0;
  height: 0;
  border-top: 20px solid transparent;
  border-left: 30px solid white;
  border-bottom: 20px solid transparent;
}

.lightbox, .video-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.lightbox img {
  max-width: 90%;
  max-height: 90%;
}

.video-modal-content {
  width: 80%;
  height: 80%;
}

.video-modal-content iframe {
  width: 100%;
  height: 100%;
}
</style>