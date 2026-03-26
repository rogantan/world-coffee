<script setup lang="ts">
import { useUserStore } from './store/user';
import { onMounted } from 'vue';

onMounted(() => {
  const userStore = useUserStore();
    userStore.get()
})
</script>

<template>
  <RouterView />
</template>
