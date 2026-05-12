<template>
  <div class="grid-container" v-if="data">
    <div class="data-block">
      <div class="data-item">
        <span>Выручка прошлый месяц</span>
        <span class="value">{{ data.revenue.last_month }}</span>
      </div>
      <div class="data-item">
        <span>Выручка текущий месяц</span>
        <span class="value">{{ data.revenue.current_month }}</span>
      </div>
      <div class="data-item">
        <span>LFL</span>
        <span class="value">{{ data.revenue.lfl }}</span>
      </div>
    </div>
    <div class="data-block">
      <div class="data-item">
        <span>Количество чеков прошлый месяц</span>
        <span class="value">{{ data.number_of_checks.last_month }}</span>
      </div>
      <div class="data-item">
        <span>Количество чеков текущий месяц</span>
        <span class="value">{{ data.number_of_checks.current_month }}</span>
      </div>
      <div class="data-item">
        <span>LFL</span>
        <span class="value">{{ data.number_of_checks.lfl }}</span>
      </div>
    </div>
    <div class="data-block">
      <div class="data-item">
        <span>Средний чек прошлый месяц</span>
        <span class="value">{{ data.avg_check.last_month }}</span>
      </div>
      <div class="data-item">
        <span>Средний чек текущий месяц</span>
        <span class="value">{{ data.avg_check.current_month }}</span>
      </div>
      <div class="data-item">
        <span>LFL</span>
        <span class="value">{{ data.avg_check.lfl }}</span>
      </div>
    </div>
    <div class="data-block">
      <div class="data-item">
        <span>Средняя выручка за день прошлый месяц</span>
        <span class="value">{{ data.avg_revenue.last_month }}</span>
      </div>
      <div class="data-item">
        <span>Средняя выручка за день текущий месяц</span>
        <span class="value">{{ data.avg_revenue.current_month }}</span>
      </div>
      <div class="data-item">
        <span>LFL</span>
        <span class="value">{{ data.avg_revenue.lfl }}</span>
      </div>
    </div>
    <div class="data-block">
      <div class="data-item">
        <span>Среднее количество чеков за день прошлый месяц</span>
        <span class="value">{{ data.avg_check.last_month }}</span>
      </div>
      <div class="data-item">
        <span>Среднее количество чеков за день текущий месяц </span>
        <span class="value">{{ data.avg_check.current_month }}</span>
      </div>
      <div class="data-item">
        <span>LFL</span>
        <span class="value">{{ data.avg_check.lfl }}</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import type { tDashboardData } from '../../types/dashboards/dashboard';

type Props = {
  data: tDashboardData
}

const props = defineProps<Props>()

</script>

<style scoped>
.grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-gap: 20px;
  padding: 10px;
}

.data-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.data-block {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background-color: #f3c0c0aa;
  padding: 10px;
  border-radius: 5px;
}

.data-item:last-child {
  margin-bottom: 0;
}

.value {
  flex-grow: 1;
  text-align: right;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 0 10px;
}

@media (max-width: 800px) {
  .grid-container {
    grid-template-columns: 1fr;
    grid-gap: 10px;
    padding: 5px;
  }
}
</style>