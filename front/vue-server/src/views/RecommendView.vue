<template>
  <div class='recommend-container'>
  </div>
</template>

<script setup>

</script>

<style scoped>
.recommend-container {
  position: absolute;
  top: 0;
  width: 100vw;
  height: 100vh;

  --s: 20px;
  --c: #222;
  background: conic-gradient(at 50% var(--s), var(--c) 75%, #0000 0) 0 0 /
    calc(2 * var(--s)) calc(100% - var(--s)) padding-box;
  border: var(--s) solid var(--c);
  box-sizing: border-box;
  align-items: center;
  display: flex;
  justify-content: center;
  flex-direction: column;
}
</style>
