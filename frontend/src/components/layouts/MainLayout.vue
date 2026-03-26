<script setup lang="ts">
import LeftBar from '../bars/LeftBar.vue';
import NavBar from '../bars/NavBar.vue';
import { useUserStore } from '../../store/user';
import { onMounted } from 'vue';

onMounted(() => {
  // const userStore = useUserStore();
  //   userStore.get()
})
</script>

<template>
  <div class="wrapper">
    <NavBar />
    <LeftBar />
    <div v-show="true" class="content-page">
        <RouterView class="content cont" />
    </div>
  </div>
</template>