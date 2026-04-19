<template>
  <div class="card mt-3 p-2">
    <h2>{{ pageTitle }}</h2>
    <div>
      <TableContent :data="data" :headers="headers">
        <template #id-cell="{ row }">
          <div class="data-block">
            <div class="data-item">
              <span>
                {{ row.id }}
              </span>
            </div>
          </div>
        </template>
        <template #name-cell="{ row }">
          <div class="data-block">
            <div class="data-item">
              <span>
                {{ row.name }}
              </span>
            </div>
          </div>
        </template>
        <template #archived-cell="{ row }">
          <div class="data-block">
            <div class="data-item">
              <span>
                {{ row.archived }}
              </span>
            </div>
          </div>
        </template>
        <template #salary_per_shift-cell="{ row }">
          <div class="data-block" v-if="row.isEditingSalary">
            <div class="data-item">
              <span>
                <InputBox type="number" v-model="row.salary_per_shift" />
              </span>
              <span>
                <ButtonBox class="p-2" color="success" icon="ri-save-2-line" @click="editBonus(row)"/>
                <ButtonBox class="p-2" color="danger" icon="ri-delete-back-line" @click="cancelEditBonus(row)"/>
              </span>
            </div>
          </div>
          <div v-else class="data-block">
            <div class="data-item">
              <span>
                {{ row.salary_per_shift }}
              </span>
              <span>
                <ButtonBox color="warning" icon="ri-edit-box-line" @click="startEditSalary(row)"/>
              </span>
            </div>
          </div>
        </template>
      </TableContent>
      <Notify />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import TableContent from '../fields/table/TableContent.vue';
import { getRetailStores, putSalary } from '../../api/admin/listst';
import type { tRetailStore } from '../../types/admin/lists';
import InputBox from '../fields/InputBox.vue';
import ButtonBox from '../fields/ButtonBox.vue';
import { notificationService } from '../../api/notify';
import Notify from '../modals/Notify.vue';
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
    title: "Название",
    key: "name",
    class: "lemon",
    sort: false
  },
  archived: {
    title: "Архив",
    key: "archived",
    class: "lemon",
    sort: false
  },
  salary_per_shift: {
    title: "Оплата за смену",
    key: "salary_per_shift",
    class: "lemon",
    sort: false
  }
});

interface RetailStoreItem extends tRetailStore {
  isEditingSalary?: boolean,
  originalSalary?: number
}

const data = ref<RetailStoreItem[]>([]);


const getData = async () => {
  const response = await getRetailStores();

  data.value = response.map((item: tRetailStore) => ({
    id: item.id,
    name: item.name,
    archived: item.archived,
    salary_per_shift: item.salary_per_shift,
    idEditingSalary: false
  }));
};

const startEditSalary = (row: RetailStoreItem) => {
  row.originalSalary = row.salary_per_shift;
  row.isEditingSalary = true;
}

const cancelEditBonus = (row: RetailStoreItem) => {
  row.salary_per_shift = row.originalSalary || 0;
  delete row.originalSalary;
  row.isEditingSalary = false;
};

const editBonus = async(row: RetailStoreItem) => {
  if (!row.salary_per_shift || row.salary_per_shift < 0) {
    notificationService.addNotification({
      title: "Ошибка",
      message: "В данных ошибка!",
      type: 'error'
    });
    return;
  }

  try {
    await putSalary(row.id, row.salary_per_shift);
    delete row.originalSalary;

    row.isEditingSalary = false;

    notificationService.addNotification({
      title: "Успех",
      message: "Оплата за смену успешно изменена",
      type: "success"
    });
  } catch (error) {
    console.log("Ошибка при обновлении", error);
    notificationService.addNotification({
      title: "Ошибка",
      message: "Не удалось изменить оплату за смену",
      type: 'error'
    });
  }
}

onMounted(async () => {
  document.title = pageTitle.value as string
  await getData();
})
</script>

<style scoped>
.data-block {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background-color: #ffffff;
  padding: 0;
  border-radius: 5px;
}

.data-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>