<template>
  <div class="movie-cards">
    <div
      v-for="(movie, idx) in selectedMovies"
      :key="movie.id"
      class="movie-card"
      :class="{ 'is-active': movie.isActive }"
      @click="updateCard(idx)"
      :data-card="true"
    >
      <div class="movie-card__inner" ref="cardInners">
        <div class="movie-card__image">
          <img :src="movie.poster_path" :alt="movie.title" />
        </div>
      </div>
    </div>
    <div class="modal-overlay" v-if="anyCardActive" @click="closeModal"></div>
    <div class="content">
      <div
        v-for="movie in selectedMovies"
        :key="movie.id"
        class="content__group"
        v-show="movie.isActive"
      >
        <div class="modal-content" @click="closeModal">
          <button class="close-button">×</button>
          <div class="modal-info">
            <h2 class="content__heading">{{ movie.title }}</h2>
            <span class="content__category">{{
              movie.genre_ids.join(", ")
            }}</span>
            <p class="content__description">{{ movie.overview }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, defineProps, onMounted } from "vue";
import { useMovieStore } from "@/store/stores";
import { gsap } from "gsap";
import { Flip } from "gsap/Flip";

gsap.registerPlugin(Flip);

const movieStore = useMovieStore();
const cardInners = ref([]);
const isBackgroundAnimationComplete = ref(false);
const props = defineProps({
  isAnimating: Boolean,
});

// 부모 컴포넌트에서 애니메이션 상태 감시
watch(
  () => props.isAnimating,
  (newValue) => {
    if (!newValue) {
      // 애니메이션이 멈추면 0.5초 후에 카드 표시
      setTimeout(() => {
        isBackgroundAnimationComplete.value = true;
      }, 500);
    }
  }
);

const anyCardActive = computed(() => {
  return selectedMovies.value.some((movie) => movie.isActive);
});

const selectedMovies = ref([]);

watch(
  () => movieStore.recommendedMovies,
  (newMovies) => {
    selectedMovies.value = newMovies.slice(0, 3).map((movie) => ({
      ...movie,
      isActive: false,
    }));
  },
  { immediate: true }
);

const updateCard = (idx) => {
  const card = cardInners.value[idx];
  if (Flip.isFlipping(card)) return;

  const cardState = Flip.getState(card, {
    props: "transform,width,height",
  });
  const image = card.querySelector(".movie-card__image");
  const imageState = Flip.getState(image);

  selectedMovies.value[idx].isActive = !selectedMovies.value[idx].isActive;
  const active = selectedMovies.value[idx].isActive;

  const duration = active ? 0.8 : 0.6;
  const ease = "power3.inOut";

  const cardContent = document.querySelectorAll(".content__group")[idx];

  if (active) {
    gsap.fromTo(
      cardContent,
      { opacity: 0, x: 100 },
      {
        duration: 1,
        opacity: 1,
        x: 0,
        ease: "expo.out",
        delay: 0.3,
      }
    );
  } else {
    gsap.to(cardContent, {
      duration: 0.4,
      opacity: 0,
      x: 50,
      ease: "power2.in",
    });
  }

  Flip.from(cardState, {
    duration: active ? 0.8 : 0.6,
    ease: "power3.inOut",
    absolute: true,
    prune: true,
    simple: true,
    onComplete: () => {
      if (active) {
        gsap.to(card, {
          x: 0,
          duration: 0.3,
          ease: "power2.out",
        });
      }
    },
  });

  Flip.from(imageState, {
    duration,
    ease,
    absolute: true,
  });
};

const closeModal = () => {
  selectedMovies.value = selectedMovies.value.map((movie) => ({
    ...movie,
    isActive: false,
  }));
};

// ESC 키로 모달 닫기 추가
onMounted(() => {
  window.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && anyCardActive.value) {
      closeModal();
    }
  });
});
</script>

<style scoped>
/* 기본 카드 레이아웃 */
.movie-cards {
  margin: auto 0;
  width: 90%;
  max-width: 1200px;
  display: flex;
  justify-content: center;
  gap: 2rem;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* 기본 카드 스타일 */
.movie-card {
  cursor: pointer;
  flex: 0 0 auto;
  width: 300px;
  height: 400px;
  margin: 10px;
}
.movie-card__inner {
  width: 100%;
  height: 100%;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  background-color: rgba(255, 255, 255, 0.7);
  border-radius: 8px;
  overflow: hidden;
  will-change: transform;
  transition: border-radius 0.3s ease;
}

.movie-card__image {
  width: 100%;
  height: 100%;
  overflow: hidden;
  position: relative;
  transition: all 0.3s ease;
}

.movie-card__image > img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

/* 모달 오버레이 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.85);
  opacity: 0;
  transition: opacity 0.4s ease;
  animation: fadeIn 0.4s ease forwards;
  z-index: 98;
}

/* 모달 컨텐츠 레이아웃 */
.content {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  pointer-events: none;
  z-index: 101;
}

.content__group {
  opacity: 0;
  position: fixed;
  top: 0;
  right: 0;
  width: 50vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  z-index: 102;
  padding: 4rem;
  color: rgb(38, 38, 40);
  border-radius: 30px 0 0 30px;
  transition: opacity 0.3s ease;
}

.modal-content {
  display: flex;
  width: 100vw;
  height: 100vh;
  background: transparent;
  z-index: 191;
}

/* 모달 이미지 영역 */
.modal-image {
  flex: 0 0 50%;
  height: 100%;
}

.modal-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 모달 정보 영역 */
.modal-info {
  flex: 1;
  padding: 4rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.content__heading {
  font-size: 2.5rem;
  margin-bottom: 1.5rem;
}

.content__description {
  margin-top: 1rem;
  font-size: 1.2rem;
  line-height: 1.8;
  color: rgba(0, 0, 0, 0.9);
}

/* 닫기 버튼 */
.close-button {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 24px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s;
  z-index: 94;
  transition: all 0.3s ease;
  transform: scale(1);
}

.close-button:hover {
  transform: scale(1.1);
  background: rgba(255, 255, 255, 0.4);
}

/* 스크롤바 스타일링 */
.modal-info::-webkit-scrollbar {
  width: 8px;
}

.modal-info::-webkit-scrollbar-track {
  background: transparent;
}

.modal-info::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
}

.movie-card.is-active .movie-card__inner {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 99;
  border-radius: 0;
}

.movie-card.is-active .movie-card__image {
  width: 50vw;
  height: 100vh;
}
</style>
