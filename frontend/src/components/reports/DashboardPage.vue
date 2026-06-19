<template>
  <div class="card mt-2">
    <Loading :active.sync="isLoading" v-bind="loadingOptions" />
    <h2 class="header-container">
      {{ pageTitle }}
      <!-- <DateBox placeholder="" v-model="dashboardStore.dates"/> -->
    </h2>  
    <DashboardBox v-if="dashboardStore.dashboardData" :data="dashboardStore.dashboardData"/>
  </div>
</template>

<script lang="ts" setup>
import { computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import DateBox from '../fields/DateBox.vue';
import DashboardBox from '../fields/DashboardBox.vue';
import { useLoading } from '../../utils/loadingMixin';
import { useDashboardStore } from '../../store/dashboards/dash';
const route = useRoute()

const pageTitle = computed(() => route.meta.name);

const dashboardStore = useDashboardStore();
const { isLoading, loadingOptions } =
  useLoading();

onMounted(async () => {
  document.title = pageTitle.value as string;
  dashboardStore.get();
})
</script>

<style>
.header-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  padding: 20px;
  background-color: #fdd244;
}
</style>