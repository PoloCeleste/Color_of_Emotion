<template>
  <div class="container">
    <Transition name="fade">
      <h1 v-if="showTitle" class="title">Color of Emotion</h1>
    </Transition>
    <Transition name="fade">
      <RouterView v-if="showRouter" />
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const showTitle = ref(false);
const showRouter = ref(false);

onMounted(() => {
  setTimeout(() => {
    showTitle.value = true;
  }, 1000);

  setTimeout(() => {
    showTitle.value = false;
  }, 4000);

  setTimeout(() => {
    showRouter.value = true;
  }, 5000);
});
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.title {
  font-size: 5rem;
  text-align: center;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>