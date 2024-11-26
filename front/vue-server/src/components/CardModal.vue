<template>
  <div class="card-modal" :class="{ 'is-active': isActive }">
    <div class="card-modal__inner" ref="modalInner">
      <div class="card-modal__image">
        <img :src="movie.poster_path" :alt="movie.title" />
      </div>
      <div class="card-modal__content">
        <h2 class="content__heading">{{ movie.title }}</h2>
        <span class="content__category">{{ movie.genre_ids.join(", ") }}</span>
        <p class="content__description">{{ movie.overview }}</p>
        <button class="close-button" @click="closeModal">×</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';
import { ref, watch, onMounted, onUnmounted } from 'vue';
import { gsap } from 'gsap';
import { Flip } from 'gsap/Flip';

gsap.registerPlugin(Flip);

const props = defineProps({
  movie: Object,
  isActive: Boolean,
});

const emit = defineEmits(['close']);

const modalInner = ref(null);

const closeModal = () => {
  emit('close');
};

watch(() => props.isActive, (newValue) => {
  if (newValue) {
    animateOpen();
  } else {
    animateClose();
  }
});

const animateOpen = () => {
  const state = Flip.getState(modalInner.value);
  gsap.set(modalInner.value, { clearProps: 'all' });
  Flip.from(state, {
    duration: 0.7,
    ease: 'power3.inOut',
    scale: true,
    onComplete: () => {
      gsap.to('.card-modal__content', { opacity: 1, y: 0, duration: 0.5, stagger: 0.1 });
    }
  });
};

const animateClose = () => {
  gsap.to('.card-modal__content', { opacity: 0, y: 20, duration: 0.3 });
};

const handleEscape = (e) => {
  if (e.key === 'Escape' && props.isActive) {
    closeModal();
  }
};

onMounted(() => {
  document.addEventListener('keydown', handleEscape);
});

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscape);
});
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
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s, visibility 0.3s;
  z-index: 1000;
}

.card-modal.is-active {
  opacity: 1;
  visibility: visible;
}

.card-modal__inner {
  display: flex;
  width: 90%;
  height: 90%;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
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
  display: flex;
  flex-direction: column;
  justify-content: center;
  opacity: 0;
  transform: translateY(20px);
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
  color: #888888;
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
}
</style>