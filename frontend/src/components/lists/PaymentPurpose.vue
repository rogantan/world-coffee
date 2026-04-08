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
import { getPaymentPurpose } from '../../api/admin/listst';
import type { tPaymentPurpose } from '../../types/admin/lists';
const route = useRoute();

const pageTitle = computed(() => route.meta.name);

const headers = ref({
  id: {
    title: "Id",
    key: "id",
    class: "lemon",
    sort: false
  },
  name: {
    title: "Наименование",
    key: "name",
    class: "lemon",
    sort: false
  }
});

const data = ref<{
  id: number,
  name: string
}[]>([]);


const getData = async () => {
  const response = await getPaymentPurpose();

  data.value = response.map((item: tPaymentPurpose) => ({
    id: item.id,
    name: item.name
  }));
};

onMounted(async () => {
  document.title = pageTitle.value as string
  await getData();
})
</script>