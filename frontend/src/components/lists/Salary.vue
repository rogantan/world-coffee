<template>
  <div class="card mt-3 p-2">
    <h2>{{ pageTitle }}</h2>
    <div>
      <TableContent :data="data" :headers="headers">
        <template #retail_store-cell="{ row }">
          <div class="data-block" v-if="row.isEditingSalary">
            <div class="data-item">
              <span>
                <SelectBox :values="retailStores" v-model="editItem.retail_store_id" />
              </span>
            </div>
          </div>
        </template>
      </TableContent>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import TableContent from '../fields/table/TableContent.vue';
import { getRetailStores } from '../../api/admin/listst';
import type { tRetailStore } from '../../types/admin/lists';
import InputBox from '../fields/InputBox.vue';
import SelectBox from '../fields/SelectBox.vue';
import RetailStores from './RetailStores.vue';
const route = useRoute();

const pageTitle = computed(() => route.meta.name);
const retailStores = ref();

const headers = ref({
  retail_store: {
    title: "Точка продаж",
    key: "retail_store",
    class: "lemon",
    sort: false
  },
  salary_per_shift: {
    title: "Значение",
    key: "salary_per_shift",
    class: "lemon",
    sort: false
  }
});

const data = ref<{
  id: string,
  name: string,
  archived: boolean
}[]>([]);


const getData = async () => {
  const response = await getRetailStores();

  RetailStores.value = response.map((item: tRetailStore) => ({
    id: item.id,
    name: item.name
  }));
};

onMounted(async () => {
  document.title = pageTitle.value as string
  await getData();
})
</script>