<template>
  <div class="card-section">
    <div class="card-grid">
      <div
        v-for="(card, index) in cards"
        :key="index"
        class="card"
        :style="{ animationDelay: `${index * 0.2}s` }"
      >
        <div class="card-inner">
          <div class="card-image">
            <img :src="card.imageUrl" :alt="card.title" />
          </div>
          <div class="card-content">
            <h3>{{ card.title }}</h3>
            <p>{{ card.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from "vue";
defineProps({
  cards: {
    type: Array,
    required: true,
  },
});
</script>
