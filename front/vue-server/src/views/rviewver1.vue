<template>
  <div class="recommend-view">
    <h1>Recommend View</h1>
    <div class="card-container">
      <div v-for="(card, index) in cards" :key="index" class="card" :class="{ 'done-card': index === cards.length - 1 }">
        <template v-if="index < cards.length - 1">
          <!-- 백엔드에서 데이터를 받아올 카드 -->
          <h3>Card {{ index + 1 }}</h3>
          <p>{{ card.content || 'Loading...' }}</p>
        </template>
        <template v-else>
          <!-- 다시하기 버튼 카드 -->
          <button @click="goBackToStart" class="restart-button">다시하기</button>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const cards = ref([])

onMounted(() => {
  // 백엔드에서 데이터를 받아오는 것을 시뮬레이션
  // 실제로는 여기서 API 호출을 수행해야 합니다
  setTimeout(() => {
    cards.value = Array(10).fill().map((_, i) => ({
      content: `Card ${i + 1} content from backend`
    }))
    // 마지막에 다시하기 버튼용 빈 객체 추가
    cards.value.push({})
  }, 1000) // 1초 후에 데이터가 로드되는 것처럼 시뮬레이션
})

const goBackToStart = () => {
  router.push('/')
}
</script>

<style scoped>
.recommend-view {
  padding: 20px;
}

.card-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.card {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 20px;
  margin: 10px;
  width: calc(33.333% - 20px); /* 3개씩 표시, 마진 고려 */
  box-sizing: border-box;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.done-card {
  background-color: #f9f9f9;
}

.restart-button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
}

.restart-button:hover {
  background-color: #45a049;
}
</style>