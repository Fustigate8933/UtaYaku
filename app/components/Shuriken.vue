<template>
  <div class="spinner" :style="{ width: size, height: size }">
    <div class="double-bounce1" :style="{ backgroundColor: 'white' }"></div>
    <div class="double-bounce2" :style="{ backgroundColor: 'gray' }"></div>
  </div>
</template>

<script setup lang="ts">
defineProps({
  size: {
    type: String,
    default: "60px",
  },
});
</script>

<style scoped>
.spinner {
  position: relative;
  margin: 100px auto;
}

.double-bounce1,
.double-bounce2 {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  opacity: 0.6;
  position: absolute;
  top: 0;
  left: 0;

  -webkit-animation: sk-bounce 2.0s infinite ease-in-out;
  animation: sk-bounce 2.0s infinite ease-in-out;
}

.double-bounce2 {
  -webkit-animation-delay: -1.0s;
  animation-delay: -1.0s;
}

@-webkit-keyframes sk-bounce {
  0%,
  100% {
    -webkit-transform: scale(0.0);
  }
  50% {
    -webkit-transform: scale(1.0);
  }
}

@keyframes sk-bounce {
  0%,
  100% {
    transform: scale(0.0);
    -webkit-transform: scale(0.0);
  }
  50% {
    transform: scale(1.0);
    -webkit-transform: scale(1.0);
  }
}
</style>

