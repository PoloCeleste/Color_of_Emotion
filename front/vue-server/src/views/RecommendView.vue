<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { EffectCoverflow, Navigation, Pagination } from 'swiper/modules'

import 'swiper/css'
import 'swiper/css/effect-coverflow'
import 'swiper/css/navigation'
import 'swiper/css/pagination'

const router = useRouter()
const cards = ref([])

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
</script>

<template>
  <section class="my-10">
    <h2 class="carousel-3D-swiper-title">Recommendations</h2>
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
        :loop="true"
      >
        <SwiperSlide v-for="(card, index) in cards" :key="index">
          <div class="image-wrapper aspect-video">
            <img class="aspect-video" :src="card.image" :alt="card.title">
          </div>
          <div class="details">
            <h3>{{ card.title }}</h3>
            <span>{{ card.subtitle }}</span>
            <p>{{ card.description }}</p>
          </div>
        </SwiperSlide>
        <SwiperSlide>
          <div class="image-wrapper aspect-video">
            <img class="aspect-video" src="path/to/restart-image.jpg" alt="Restart">
          </div>
          <div class="details">
            <h3>Start Over</h3>
            <button @click="goBackToStart" class="restart-button">다시하기</button>
          </div>
        </SwiperSlide>
        <div class="swiper-button-prev"></div>
        <div class="swiper-button-next"></div>
        <div class="swiper-pagination"></div>
      </Swiper>
    </section>
  </section>
</template>