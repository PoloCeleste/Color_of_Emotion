<template>
  <div class="typewriter-container" @click="skipAnimation">
    <Transition name="fade">
      <h1 v-if="showText" class="typewriter-text">{{ typedText }}</h1>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, defineEmits, defineProps } from "vue";

const props = defineProps({
  text: {
    type: String,
    required: true,
  },
  typingSpeed: {
    type: Number,
    default: 150,
  },
});

const emit = defineEmits(["complete", "skip"]);

const showText = ref(false);
const typedText = ref("");
let typingInterval = null;

function typeText() {
  let currentIndex = 0;
  typingInterval = setInterval(() => {
    if (currentIndex < props.text.length) {
      typedText.value += props.text[currentIndex];
      currentIndex++;
    } else {
      clearInterval(typingInterval);
      emit("complete");
    }
  }, props.typingSpeed);
}

function skipAnimation() {
  clearInterval(typingInterval);
  typedText.value = props.text;
  emit("skip");
}

onMounted(() => {
  setTimeout(() => {
    showText.value = true;
    typeText();
  }, 800);
});

onBeforeUnmount(() => {
  clearInterval(typingInterval);
});
</script>

<style scoped>
.typewriter-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.typewriter-text {
  font-family: "Courier New", monospace;
  font-size: 50px;
  font-weight: bold;
  letter-spacing: 2px;
  white-space: nowrap;
  overflow: hidden;
  border-right: 3px solid currentColor;
  animation: blink-caret 0.75s step-end infinite;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}

@keyframes blink-caret {
  from,
  to {
    border-color: transparent;
  }
  50% {
    border-color: currentColor;
  }
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
