<template>
  <div>
    <h2>Recommendations</h2>
    <!-- 4. 처음으로 돌아가기 버튼 -->
    <button class="retry-button" @click="goToStart">RETRY</button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter()

const goToStart = () => {
  router.push('/')
}
</script>

<style scoped>

</style>