<template>
  <section class="my-10">
    <h2 class="text-3xl text-center text-orange-600 mb-6">Recommendations</h2>
    <section class="carousel-3D-swiper-section">
      <Swiper
        :modules="[EffectCoverflow, Navigation, Pagination]"
        :effect="'coverflow'"
        :grabCursor="true"
        :centeredSlides="true"
        :slidesPerView="3"
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
        :pagination="{ el: '.swiper-pagination' }"
        :loop="false"
      >
        <SwiperSlide v-for="(card, index) in cards" :key="index" @click="openModal(card)">
          <div class="card border rounded-lg shadow-md overflow-hidden transition-transform transform hover:scale-105">
            <div class="image-wrapper aspect-video">
              <img class="aspect-video w-full h-full object-cover" :src="card.image" :alt="card.title">
            </div>
            <div class="details p-4">
              <h3 class="text-xl font-bold">{{ formatCardNumber(index + 1) }}</h3> <!-- 카드 번호 포맷팅 -->
              <span class="text-gray-500">{{ card.subtitle }}</span>
              <p class="text-gray-700">{{ card.description }}</p>
            </div>
          </div>
        </SwiperSlide>

        <!-- 다시하기 카드 -->
        <SwiperSlide>
          <div class="card restart-card border rounded-lg shadow-md overflow-hidden transition-transform transform hover:scale-105">
            <div class="image-wrapper aspect-video">
              <img class="aspect-video w-full h-full object-cover" src="https://picsum.photos/450/800?random=1" alt="Restart">
            </div>
            <div class="details p-4">
              <h3 class="text-xl font-bold">Start Over</h3>
              <button @click="goBackToStart" class="restart-button bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600">다시하기</button>
            </div>
          </div>
        </SwiperSlide>

        <div class="swiper-button-prev"></div>
        <div class="swiper-button-next"></div>
        <div class="swiper-pagination"></div>
      </Swiper>
    </section>
    <CardModal :isOpen="isModalOpen" :cardData="selectedCard" @close="closeModal" />
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
// import { useRouter } from 'vue-router'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { EffectCoverflow, Navigation, Pagination } from 'swiper/modules'
import CardModal from '@/components/CardModal.vue'

// 카드 데이터 상태 관리
const cards = ref([])
const isModalOpen = ref(false)
const selectedCard = ref(null)

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

// 카드 번호를 두 자리로 포맷팅하는 함수
const formatCardNumber = (number) => {
  return String(number).padStart(2, '0');
}

// 모달 열기 및 닫기 함수
const openModal = (card) => {
  selectedCard.value = card
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
}

// 다시 시작하는 함수
const goBackToStart = () => {
  // 다시 시작 로직 추가 (예: 초기화)
}
</script>

<style scoped>
.carousel-3D-swiper-section {
  /* 추가적인 스타일이 필요하다면 여기에 작성 */
}
</style>