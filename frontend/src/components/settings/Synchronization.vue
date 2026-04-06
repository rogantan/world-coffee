<template>
  <div class="card mt-3 p-2">
    <h2>{{ pageTitle }}</h2>
    <div>
      <TableContent :data="data" :headers="headers"></TableContent>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import TableContent from '../fields/table/TableContent.vue';
import { getSync } from '../../api/admin/sync';
import type { tSync } from '../../types/admin/sync';
const route = useRoute();

const pageTitle = computed(() => route.meta.name);

const headers = ref({
  startDate: {
    title: "Дата начала",
    key: "startDate",
    class: "lemon",
    sort: false
  },
  endDate: {
    title: "Дата окончания",
    key: "endDate",
    class: "lemon",
    sort: false
  },
  status: {
    title: "Статус",
    key: "status",
    class: "lemon",
    sort: false
  }
});

const data = ref<{
  startDate: string;
  endDate: string;
  status: string;
  status_class: string;
}[]>([]);

function formatDateString(dateString: string) {
  if (!dateString || !dateString.includes('T')) {
    return '';
  }
  const [datePart, timePart] = dateString.split('T');
  const [year, month, day] = datePart.split('-');
  const [hour, minute] = timePart.split(':');

  return `${year}-${month}-${day} ${hour}:${minute}`;
};

const getData = async () => {
  const response = await getSync();

  data.value = response.map((item: tSync) => ({
    startDate: formatDateString(item.start_time),
    endDate: formatDateString(item.finish_time),
    status: item.status,
    status_class: item.color
  }));
};

onMounted(async () => {
  document.title = pageTitle.value as string
  await getData();
})
</script>