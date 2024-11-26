<template>
  <Transition name="modal">
    <div v-if="isActive" class="card-modal">
      <div class="card-modal__inner">
        <div class="card-modal__image">
          <img :src="movie.poster_path" :alt="movie.title" />
        </div>
        <div class="card-modal__content">
          <h2 class="content__heading">{{ movie.title }}</h2>
          <span class="content__description"
            >{{ movie.original_title }} ({{ movie.original_language }})</span
          >
          <span class="content__description"
            >{{ movie.release_date }} / {{ movie.tmdb_vote_average }}</span
          ><br />
          <span class="content__category">{{
            movie.genre_ids.join(", ")
          }}</span>
          
          <p class="content__description">{{ movie.overview }}</p>
          <button class="close-button" @click="closeModal">×</button>

          <div v-if="movie.reviews">
            <h3>리뷰</h3>
            <div v-for="(review, index) in movie.reviews" :key="index">
              <p v-if="showFullReviewIndex !== index && review.length > 100" @click="showFullReview(index)">
                {{ review.substring(0, 100) }}...더보기
              </p>
              <p v-else-if="showFullReviewIndex === index">
                {{ review }}<br>
                <button class="button" @click="hideFullReview(index)">줄이기</button>
              </p>
              <p v-else>{{ review }}</p>
            </div>
          </div>

          <div v-if="movie.picture_url">
            <h3>갤러리</h3>
            <div class="gallery-container">
              <button class="nav-button prev" @click="prevImage">
                &#10094;
              </button>
              <div
                class="gallery-item"
                v-if="currentImageIndex < movie.picture_url.length"
              >
                <img
                  :src="movie.picture_url[currentImageIndex]"
                  alt=""
                  @click="openLightbox(movie.picture_url[currentImageIndex])"
                />
              </div>
              <button class="nav-button next" @click="nextImage">
                &#10095;
              </button>
            </div>
          </div>

          <div v-if="movie.video_url">
            <h3>동영상</h3>
            <div class="video-container">
              <button class="nav-button prev" @click="prevVideo">
                &#10094;
              </button>
              <div
                class="video-item"
                v-if="currentVideoIndex < movie.video_url.length"
              >
                <img
                  :src="getYoutubeThumbnail(movie.video_url[currentVideoIndex])"
                  alt="Video thumbnail"
                  @click="openVideoModal(movie.video_url[currentVideoIndex])"
                />
                <div
                  class="play-button"
                  @click="openVideoModal(movie.video_url[currentVideoIndex])"
                ></div>
              </div>
              <button class="nav-button next" @click="nextVideo">
                &#10095;
              </button>
            </div>
          </div>

          <div v-if="movie.watch_providers">
            <h3>보려면?</h3>
            <div class="provider-container">
              <h4
                v-for="(provider, index) in movie.watch_providers"
                :key="index"
                class="provider-tag"
              >
                <img :src="provider.logo_path" alt="" />
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
import { defineProps, defineEmits, ref } from "vue";

const props = defineProps({
  movie: Object,
  isActive: Boolean,
});

const emit = defineEmits(["close"]);

const showFullReviewIndex = ref(null);

const closeModal = () => {
  emit("close");
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
  const videoId = url.split("/").pop();
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
/* 공통 스타일 */
.card-modal, .lightbox, .video-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.card-modal {
  background-color: rgba(0, 0, 0, 0.8);
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

.card-modal__image, .card-modal__content {
  flex: 1;
  overflow: hidden;
}

.card-modal__content {
  padding: 40px;
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  overflow-y: auto;
  max-height: 90vh;
}

.card-modal__image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 스크롤바 스타일 */
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

/* 컨텐츠 스타일 */
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

/* 버튼 스타일 */
.close-button, .nav-button {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
}

.close-button {
  position: absolute;
  top: 20px;
  right: 20px;
  font-size: 30px;
  z-index: 10;
}

.nav-button {
  background: rgba(255, 255, 255, 0.3);
  font-size: 24px;
  padding: 10px;
  transition: background 0.3s;
}

.nav-button:hover {
  background: rgba(255, 255, 255, 0.5);
}

/* 갤러리 및 비디오 컨테이너 */
.gallery-container, .video-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-top: 10px;
  overflow-x: auto;
  padding: 10px 0;
  scroll-snap-type: x mandatory;
  width: 100%;
  flex-wrap: nowrap;
}

.gallery-item, .video-item {
  flex: 0 0 auto;
  width: calc(100% - 80px);
  aspect-ratio: 16 / 9;
  overflow: hidden;
  cursor: pointer;
  position: relative;
  scroll-snap-align: start;
}

.gallery-item img, .video-item img, .video-item iframe {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 제공자 태그 */
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

/* 추가 정보 링크 */
.more-info {
  margin-top: 20px;
}

.more-info a {
  color: #4caf50;
  text-decoration: none;
}

.more-info a:hover {
  text-decoration: underline;
}

/* 트랜지션 애니메이션 */
.modal-enter-active, .modal-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}

.modal-enter-from, .modal-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

/* 미디어 쿼리 */
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

/* 라이트박스 및 비디오 모달 */
.lightbox, .video-modal {
  background-color: rgba(0, 0, 0, 0.9);
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

/* 1. 리뷰, 갤러리, 동영상, 보려면? 섹션에 효과 추가 */
.card-modal__content h3 {
  font-size: 24px;
  margin-top: 30px;
  margin-bottom: 15px;
  color: #fff;
}

.card-modal__content > div {
  margin-bottom: 20px;
}

/* 2. 갤러리와 동영상의 가로 스크롤 제거 */
.gallery-container, .video-container {
  overflow-x: hidden;
  flex-wrap: nowrap;
  justify-content: center;
}

/* 3. provider 아이콘만 표시 */
.provider-tag {
  background: none;
  padding: 0;
  margin: 5px;
}

.provider-tag img {
  width: 120px; /* 40px에서 120px로 변경 */
  height: 120px; /* 40px에서 120px로 변경 */
  transition: transform 0.3s ease;
}
.provider-tag img:hover {
  transform: scale(1.1);
}

/* 4. 더 알아보기 버튼 매력적으로 꾸미기 */
.more-info {
  margin-top: 30px;
  text-align: center;
}

.more-info a {
  display: inline-block;
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  text-decoration: none;
  border-radius: 25px;
  font-weight: bold;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.more-info a:hover {
  background-color: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
}

.card-modal__content div > p {
  background: rgba(255, 255, 255, 0.05);
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: background 0.3s ease;
  color: #bababa; /* overview와 같은 색상 적용 */
}

.card-modal__content div > p:hover {
  background: rgba(255, 255, 255, 0.1);
}

.button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  padding: 5px 10px;
  margin-top: 5px;
  transition: color 0.3s ease;
}

.button:hover {
  color: #45a049;
}

.gallery-item img,
.video-modal-content iframe {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>