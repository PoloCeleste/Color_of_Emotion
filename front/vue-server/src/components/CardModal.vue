<template>
  <Transition name="modal">
    <div v-if="isActive" class="card-modal">
      <div class="card-modal__inner">
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
  </Transition>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

defineProps({
  movie: Object,
  isActive: Boolean,
});

const emit = defineEmits(['close']);

const closeModal = () => {
  emit('close');
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
}
</style>