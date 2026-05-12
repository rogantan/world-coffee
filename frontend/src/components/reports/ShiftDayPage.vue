<template>
  <div class="mt-2">
    <h2 class="data-block">
      <div class="data-item">
        <span>
          {{ pageTitle }}
        </span>
        <span>
          <DateBox placeholder="Выберите диапазон дат"   v-model="shiftStore.dates" @update:modelValue="update"/>
        </span>
      </div>
    </h2>
    <div class="card">
      <TableContent :data="shiftStore.data" :headers="headers" :static-column="true" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { useRoute } from 'vue-router';
import DateBox from '../fields/DateBox.vue';
import { computed, onMounted, reactive } from 'vue';
import TableContent from '../fields/table/TableContent.vue';
import { useShiftStore } from '../../store/reports/shift';

const route = useRoute();
const pageTitle = computed(() => route.meta.name);

const shiftStore = useShiftStore();

const headers = reactive({
  nameEmployee: {
    title: "Имя",
    key: "nameEmployee",
    class: "lemon",
    sort: true,
    sortKeys: {
      asc: 'employee_asc',
      desc: 'employee_desc',
    },
  },
  salePoint: {
    title: "Точка продаж",
    key: "salePoint",
    class: "lemon",
    sort: true,
    sortKeys: {
      asc: 'employee_asc',
      desc: 'employee_desc',
    },
  }
});

const updateHeaders = () => {
  let start = new Date(shiftStore.dates[0]);
  let end = new Date(shiftStore.dates[1]);

  const newHeaders = { ...headers }; // Создаём копию текущих заголовков

  // Очищаем месячные заголовки, чтобы не было дубликатов
  Object.keys(newHeaders).forEach(key => {
    if (key.includes('-')) delete newHeaders[key];
  });

  // Добавляем новые заголовки по месяцам
  while (start <= end) {
    const formattedDate = start.toLocaleDateString('fr-CA', { year: 'numeric', month: '2-digit', day: '2-digit' });
    newHeaders[formattedDate] = {
      title: formattedDate,
      key: formattedDate,
      class: "lemon",
      sort: false,
      sortKeys: false
    };
    start.setDate(start.getDate() + 1);
  }

  for (const key in headers) {
    delete headers[key];
  }
  Object.assign(headers, newHeaders);
};


const update = async () => {
  updateHeaders();
  await shiftStore.get();
};

onMounted(async () => {
  document.title = pageTitle.value as string;
  updateHeaders();
  await shiftStore.get();
})
</script>

<style scoped>
.data-block {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background-color: #e9ecef;
  padding: 10px;
  border-radius: 5px;
}

.data-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
</style>