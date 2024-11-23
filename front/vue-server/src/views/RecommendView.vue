<template>
  <section class="my-10">
    <!-- <h2 class="carousel-3D-swiper-title">Recommendations</h2> -->
    <div class="transition-toggle">
      <label>
        <input type="checkbox" v-model="useTransition"> Action On
      </label>
    </div>
    <section class="carousel-3D-swiper-section">
      <Swiper
        :modules="[EffectCoverflow, Navigation, Pagination]"
        :effect="useTransition ? 'coverflow' : 'slide'"
        :grabCursor="true"
        :centeredSlides="true"
        :slidesPerView="3"
        :spaceBetween="20"
        :coverflowEffect="{
          rotate: 0,
          stretch: 0,
          depth: 350,
          modifier: 1,
          slideShadows: true
        }"
        :navigation="{
          nextEl: '.swiper-button-next',
          prevEl: '.swiper-button-prev',
        }"
        :pagination="{
          type: 'progressbar',
          clickable: true,
          dynamicBullets: true,
        }"
        :loop=true
        :keyboard="{
          enabled: true,
          onlyInViewport: true
        }"
        :mousewheel="true"
        :preloadImages="false"
        :watchSlidesProgress="true"
      >
        <SwiperSlide 
          class="swiper-slide"
          v-for="(card, index) in cards" 
          :key="index" 
          @click="openModal(card)"
        >
          <CardComponent 
            v-if="card"
            :card="card" 
            :useTransition="useTransition"
          />
        </SwiperSlide>
        <!-- 다시하기 카드 -->
        <SwiperSlide>
          <div class="card restart-card" :class="{ 'with-transition': useTransition }">
            <div class="image-wrapper aspect-video" @click="goBackToStart">
              <img class="aspect-video" src="https://picsum.photos/450/800?random=1" alt="Restart">
            </div>
            <div class="details">
              <h3>Start Over</h3>
              <button @click="goBackToStart" class="restart-button">다시하기</button>
            </div>
          </div>
        </SwiperSlide>
        <div class="swiper-button-prev"></div>
        <div class="swiper-button-next"></div>
        <div class="swiper-pagination"></div>
      </Swiper>
    </section>
    <CardComponentModal :isOpen="isModalOpen" :card="selectedCard" @close="closeModal" />
  </section>
</template>

<script setup>
// import dummyMovies from '@/data/dummymovies.json'
import axios from 'axios'

import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { EffectCoverflow, Navigation, Pagination } from 'swiper/modules'
import CardComponentModal from '@/components/CardComponentModal.vue'  // CardComponentModal 컴포넌트 import
import CardComponent from '@/components/CardComponent.vue'  // 새로운 카드 컴포넌트

import 'swiper/css'
import 'swiper/css/effect-coverflow'
import 'swiper/css/navigation'
import 'swiper/css/pagination'

const API_URL = process.env.VUE_APP_API_URL

const router = useRouter()
const isModalOpen = ref(false)
const selectedCard = ref(null)
const useTransition = ref(true)

const cards = ref([])

onMounted(async () => {
  
  try {
    const response = await axios.get(`http://${API_URL}/api/v1/movies/`)
    // console.log(response)
    if (!response.data || response.data.length === 0) {
      console.error('데이터가 없습니다')
      return
    } 
    cards.value = response.data
    console.log(cards.value)
  } catch (error) {
    console.error('데이터 로딩 실패:', error)

    if (error.response) {
      // 서버가 응답했지만 2xx 범위가 아닌 경우
      console.error('서버 응답 에러:', error.response.status)
    } else if (error.request) {
      // 요청은 보냈지만 응답을 받지 못한 경우
      console.error('네트워크 에러')
    } else {
      // 요청 설정 중에 문제가 발생한 경우
      console.error('요청 설정 에러')
    }
    
    cards.value = [] // 에러 발생 시 빈 배열로 초기화
  }
})

// onMounted(() => {
//   cards.value = dummyMovies.map(movie => ({
//     genre_ids: movie.genre_ids, 
//     language: movie.original_language,
//     id: movie.movie_id,
//     title: movie.title,
//     original_title: movie.original_title,

//     release_date: movie.release_date,
//     description: movie.overview,
//     image: movie.poster_path,
//     vote_average: movie.tmdb_vote_average,
//     providers: movie.watch_providers,

//     picture_url: movie.picture_url,
//     video_url: movie.video_url,
//     reviews: movie.reviews,
//     watchapedia: movie.watchapedia,
//     poster_palette: movie.poster_palette
//   }))
//   console.log(cards)
//   console.log(cards.value)
// })


const goBackToStart = () => {
  router.push('/start')
}

const openModal = (card) => {
  selectedCard.value = card
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
}
</script>

<style scoped>
.carousel-3D-swiper-section {
  max-width: 100vw;
  overflow: hidden;
}

.swiper-slide {
  width: 300px;  /* 원하는 카드 너비 */
  height: 600px; /* 원하는 카드 높이 */
}

.card {
  width: 100%;
  height: 100%;
  border-radius: 8px;
  overflow: hidden;
}

.card.with-transition {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card.with-transition:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.image-wrapper {
  width: 100%;
  height: 70%;  /* 이미지 영역 비율 조정 */
}

.image-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card.with-transition .image-wrapper img {
  transition: transform 0.3s ease;
}

.card.with-transition:hover .image-wrapper img {
  transform: scale(1.1);
}

.card-transition-enter-from,
.card-transition-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

.details {
  padding: 15px;
  background-color: #fff;
}

.details h3 {
  margin-top: 0;
  font-size: 1.2em;
  color: #333;
}

.details span {
  font-size: 0.9em;
  color: #666;
}

.details p {
  font-size: 0.95em;
  color: #444;
  margin-top: 10px;
}

.restart-button {
  margin-top: 10px;
  padding: 8px 15px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.restart-button:hover {
  background-color: #45a049;
}

.transition-toggle {
  margin-bottom: 15px;
}

.transition-toggle label {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.transition-toggle input[type="checkbox"] {
  margin-right: 8px;
}
</style>