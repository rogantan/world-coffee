<template>
  <div class="card mt-3 p-2">
    <h2>{{ pageTitle }}</h2>
    <div>
      <ButtonBox title="Создать премию" @click="addBonus()"></ButtonBox>
    </div>
    <div>
      <TableContent :data="data" :headers="headers">
        <template #name-cell="{ row }">
          <div class="data-block" v-if="row.isNewBonus">
            <div class="data-item">
              <span>
                <InputBox type="text" v-model="row.name" />
              </span>
            </div>
          </div>
          <div class="data-block" v-else-if="row.isEditingBonus">
            <div class="data-item">
              <span>
                <InputBox type="text" v-model="row.name" />
              </span>
            </div>
          </div>
          <div class="data-block" v-else>
            <div class="data-item">
              <span>
                {{ row.name }}
              </span>
            </div>
          </div>
        </template>
        <template #value-cell="{ row }">
          <div class="data-block" v-if="row.isNewBonus">
            <div class="data-item">
              <span>
                <InputBox type="text" v-model="row.value" />
              </span>
              <span>
                <ButtonBox class="p-2" color="success" icon="ri-save-2-line" @click="saveRecordBonus(row)" />
                <ButtonBox class="p-2" color="danger" icon="ri-delete-back-line"
                  @click="cancelNewBonus(row)" />
              </span>
            </div>
          </div>
          <div class="data-block" v-else-if="row.isEditingBonus">
            <div class="data-item">
              <span>
                <InputBox type="text" v-model="row.value" />
              </span>
              <span>
                <ButtonBox color="success" icon="ri-save-2-line" @click="editRecordBonus(row)" />
                <ButtonBox color="danger" icon="ri-delete-back-line" @click="cancelEditRecordBonus(row)" />
              </span>
            </div>
          </div>
          <div class="data-block" v-else>
            <div class="data-item">
              <span>
                {{ row.value }}
              </span>
              <span>
                <ButtonBox color="warning" icon="ri-edit-box-line"
                  @click="startEditRecordBonus(row)" />
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
import ButtonBox from '../fields/ButtonBox.vue';
import InputBox from '../fields/InputBox.vue';
import { getBonuses, postBonuses, putBonuses } from '../../api/admin/listst';
import type { tBonus } from '../../types/admin/lists';
import { notificationService } from '../../api/notify';
import Notify from '../modals/Notify.vue';
const route = useRoute();

const pageTitle = computed(() => route.meta.name);

const headers = ref({
  name: {
    title: "Наименование",
    key: "name",
    class: "lemon",
    sort: false
  },
  value: {
    title: "Значение",
    key: "value",
    class: "lemon",
    sort: false
  }
});

interface BonusItem extends tBonus {
  isNewBonus?: boolean;
  isEditingBonus?: boolean;
  originalName?: string;
  originalValue?: number
}

const data = ref<BonusItem[]>([]);


const getData = async () => {
  const response = await getBonuses();

  data.value = response.map((item: tBonus) => ({
    id: item.id,
    name: item.name,
    value: item.value,
    isNewBonus: false,
    isEditingBonus: false
  }));
};

const addBonus = () => {
  const exitstingNewRow = data.value.find(row => row.isNewBonus === true);

  if (exitstingNewRow) {
    notificationService.addNotification({
      title: 'Внимание',
      message: "Сначала сохраните или отмените текущее добавление",
      type: 'warning'
    });
    return;
  }

  data.value.unshift({
    id: Date.now(),
    name: '',
    value: 0,
    isNewBonus: true,
    isEditingBonus: false
  });
};

const cancelNewBonus = (row: BonusItem) => {
  const index = data.value.findIndex(item => item === row);
  if (index !== -1) {
    data.value.splice(index, 1);
  }
};

const saveRecordBonus = async (row: BonusItem) => {
  if (!row.name || row.name.trim() === '' || !row.value) {
    notificationService.addNotification({
      title: 'Ошибка',
      message: "Не все поля заполнены",
      type: 'error'
    });
    return;
  }

  try {
    await postBonuses(row.name.trim(), row.value);
    row.isNewBonus = false;
    notificationService.addNotification({
      title: 'Успех',
      message: "Премия успешно создана",
      type: 'success'
    });
  } catch(error) {
    console.log("Ошибка при сохранении:", error);
    notificationService.addNotification({
      title: "Ошибка",
      message: "Не удалось создать премию",
      type: 'error'
    });
  }
};

const startEditRecordBonus = (row: BonusItem) => {
  row.originalName = row.name;
  row.originalValue = row.value;
  row.isEditingBonus = true;
};

const cancelEditRecordBonus = (row: BonusItem) => {
  row.name = row.originalName || '';
  row.value = row.originalValue || 0;
  delete row.originalName;
  delete row.originalValue;
  row.isEditingBonus = false;
};

const editRecordBonus = async(row: BonusItem) => {
  if (!row.name || row.name.trim() === '' || !row.value) {
    notificationService.addNotification({
      title: 'Ошибка',
      message: "Данные не могут быть пустыми",
      type: 'error'
    });
    return;
  }

  try {
    await putBonuses(row.id, row.name.trim(), row.value);
    delete row.originalName;
    delete row.originalValue;

    row.isEditingBonus = false;

    notificationService.addNotification({
      title: 'Успех',
      message: "Премия успешно обновлена",
      type: 'success'
    });
  } catch (error) {
    console.error("Ошибка при обновлении:", error);
    notificationService.addNotification({
      title: "Ошибка",
      message: "Не удалось обновить премию",
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