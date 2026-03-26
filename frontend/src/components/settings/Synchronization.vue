<template>
  <div>
    <h2>{{ pageTitle }}</h2>
    <div>
      <table></table>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const pageTitle = computed(() => route.meta.name)
</script>