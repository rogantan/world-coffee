<template>
  <div>
    <div>
      <div>
        <span>Выручка прошлый месяц</span>
        <span>{{ data.revenue.last_month }}</span>
      </div>
      <div>
        <span>Выручка текущий месяц</span>
        <span>{{ data.revenue.current_month }}</span>
      </div>
      <div>
        <span>LFL</span>
        <span>{{ data.renevue.lfl }}</span>
      </div>
    </div>
    <div>
      <div>
        <span>Количество чеков прошлый месяц</span>
        <span>{{ data.number_of_checks.last_month }}</span>
      </div>
      <div>
        <span>Количество чеков текущий месяц</span>
        <span>{{ data.numer_of_checks.current_month }}</span>
      </div>
      <div>
        <span>LFL</span>
        <span>{{ data.number_of_checks.lfl }}</span>
      </div>
    </div>
    <div>
      <div>
        <span>Средний чек прошлый месяц</span>
        <span>{{ data.avg_check.last_month }}</span>
      </div>
      <div>
        <span>Средний чек текущий месяц</span>
        <span>{{ data.avg_check.current_month }}</span>
      </div>
      <div>
        <span>LFL</span>
        <span>{{ data.avg_check.lfl }}</span>
      </div>
    </div>
    <div>
      <div>
        <span>Средняя выручка за день прошлый месяц</span>
        <span>{{ data.avg_revenue.last_month }}</span>
      </div>
      <div>
        <span>Средняя выручка за день текущий месяц</span>
        <span>{{ data.avg_revenue.current_month }}</span>
      </div>
      <div>
        <span>LFL</span>
        <span>{{ data.avg_revenue.lfl }}</span>
      </div>
    </div>
    <div>
      <div>
        <span>Среднее количество чеков за день прошлый месяц</span>
        <span>{{ data.avg_checks_day. }}</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
</script>