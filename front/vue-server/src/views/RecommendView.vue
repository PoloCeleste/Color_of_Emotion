<template>
  <section class="my-10">
    <h2 class="carousel-3D-swiper-title">Recommendations</h2>
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
        :coverflowEffect="useTransition ? {
          rotate: 0,
          stretch: 0,
          depth: 350,
          modifier: 1,
          slideShadows: true
        } : {}"
        :navigation="{
          nextEl: '.swiper-button-next',
          prevEl: '.swiper-button-prev',
        }"
        :pagination="{ el: '.swiper-pagination' }"
        :loop="true"
      >
        <SwiperSlide v-for="(card, index) in cards" :key="index" @click="openModal(card)">
          <CardComponent :card="card" :useTransition="useTransition" />
        </SwiperSlide>
        <!-- 다시하기 카드 -->
        <SwiperSlide>
          <div class="card restart-card" :class="{ 'with-transition': useTransition }">
            <div class="image-wrapper aspect-video">
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
    <CardModal :isOpen="isModalOpen" :card="selectedCard" @close="closeModal" />
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { EffectCoverflow, Navigation, Pagination } from 'swiper/modules'
import CardModal from '@/components/CardModal.vue'  // CardModal 컴포넌트 import
import CardComponent from '@/components/CardComponent.vue'  // 새로운 카드 컴포넌트

import 'swiper/css'
import 'swiper/css/effect-coverflow'
import 'swiper/css/navigation'
import 'swiper/css/pagination'

const router = useRouter()
const cards = ref([])
const isModalOpen = ref(false)
const selectedCard = ref(null)
const useTransition = ref(true)

onMounted(() => {
  // 백엔드에서 데이터를 받아오는 것을 시뮬레이션
  setTimeout(() => {
    cards.value = Array(10).fill().map((_, i) => ({
      title: `Card ${i + 1}`,
      subtitle: 'Recommendation',
      description: `Description for card ${i + 1}`,
      image: `https://picsum.photos/id/${i + 1}/450/800`
    }))
  }, 1000)
})

const goBackToStart = () => {
  router.push('/')
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
  /* 기존 스타일 유지 */
}

.card {
  transition: none;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card.with-transition {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card.with-transition:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.image-wrapper img {
  transition: none;
}

.card.with-transition .image-wrapper img {
  transition: transform 0.3s ease;
}

.card.with-transition:hover .image-wrapper img {
  transform: scale(1.1);
}

.card-transition-enter-active,
.card-transition-leave-active {
  transition: opacity 0.5s ease, transform 0.5s ease;
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