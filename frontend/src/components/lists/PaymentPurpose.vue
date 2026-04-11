<template>
  <div class="card mt-3 p-2">
    <h2>{{ pageTitle }}</h2>
    <div>
      <ButtonBox title="Создать назначение платежа" @click="addPurposePayment" />
    </div>
    <div>
      <TableContent :data="data" :headers="headers">
        <template #name-cell="{ row }">
          <div class="data-block" v-if="row.isNewPayment">
            <div class="data-item">
              <span>
                <InputBox type="text" v-model="row.name" />
              </span>
              <span>
                <ButtonBox class="p-2" color="success" icon="ri-save-2-line" @click="saveRecordPayment(row)" />
                <ButtonBox class="p-2" color="danger" icon="ri-delete-back-line"
                  @click="cancelNewPayment(row)" />
              </span>
            </div>
          </div>
          <div class="data-block" v-else-if="row.isEditingPayment">
            <div class="data-item">
              <span>
                <InputBox type="text" v-model="row.name" />
              </span>
              <span>
                <ButtonBox color="success" icon="ri-save-2-line" @click="editRecordPayment(row)" />
                <ButtonBox color="danger" icon="ri-delete-back-line" @click="cancelEditRecordPayment(row)" />
              </span>
            </div>
          </div>
          <div v-else class="data-block">
            <div class="data-item">
              <span>
                {{ row.name }}
              </span>
              <span>
                <ButtonBox v-if="row.name" color="warning" icon="ri-edit-box-line"
                  @click="startEditRecordPayment(row)" />
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
import { getPaymentPurpose, postPaymentPurpose, putPaymentPurpose } from '../../api/admin/listst';
import type { tPaymentPurpose } from '../../types/admin/lists';
import ButtonBox from '../fields/ButtonBox.vue';
import InputBox from '../fields/InputBox.vue';
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
  }
});

// Расширяем тип для добавления служебных полей
interface PaymentPurposeItem extends tPaymentPurpose {
  isNewPayment?: boolean;
  isEditingPayment?: boolean;
  originalName?: string;
}

const data = ref<PaymentPurposeItem[]>([]);

const getData = async () => {
  const response = await getPaymentPurpose();

  data.value = response.map((item: tPaymentPurpose) => ({
    id: item.id,
    name: item.name,
    isNewPayment: false,
    isEditingPayment: false
  }));
};

// Добавление нового назначения платежа
const addPurposePayment = () => {
  // Проверяем, есть ли уже строка в режиме добавления
  const existingNewRow = data.value.find(row => row.isNewPayment === true);
  
  if (existingNewRow) {
    notificationService.addNotification({
      title: 'Внимание',
      message: 'Сначала сохраните или отмените текущее добавление',
      type: 'warning',
    });
    return;
  }
  
  // Добавляем новую временную запись
  data.value.unshift({
    id: Date.now(), // временный ID
    name: '',
    isNewPayment: true,
    isEditingPayment: false
  });
};

// Отмена добавления
const cancelNewPayment = (row: PaymentPurposeItem) => {
  const index = data.value.findIndex(item => item === row);
  if (index !== -1) {
    data.value.splice(index, 1);
  }
};

// Сохранение новой записи
const saveRecordPayment = async (row: PaymentPurposeItem) => {
  if (!row.name || row.name.trim() === '') {
    notificationService.addNotification({
      title: 'Ошибка',
      message: 'Назначение платежа не может быть пустым',
      type: 'error',
    });
    return;
  }
  
  try {
    await postPaymentPurpose(row.name.trim());
    row.isNewPayment = false;
    notificationService.addNotification({
      title: 'Успех',
      message: 'Назначение платежа успешно создано',
      type: 'success',
    });
  } catch (error) {
    console.error('Ошибка при сохранении:', error);
    notificationService.addNotification({
      title: 'Ошибка',
      message: 'Не удалось создать назначение платежа',
      type: 'error',
    });
  }
};

// Редактирование существующей записи
const startEditRecordPayment = (row: PaymentPurposeItem) => {
  row.originalName = row.name;
  row.isEditingPayment = true;
};

const cancelEditRecordPayment = (row: PaymentPurposeItem) => {
  row.name = row.originalName || '';
  delete row.originalName;
  row.isEditingPayment = false;
};

const editRecordPayment = async (row: PaymentPurposeItem) => {
  if (!row.name || row.name.trim() === '') {
    notificationService.addNotification({
      title: 'Ошибка',
      message: 'Назначение платежа не может быть пустым',
      type: 'error',
    });
    return;
  }
  
  try {
    await putPaymentPurpose(row.id, row.name.trim());
    delete row.originalName;
    row.isEditingPayment = false;
    
    notificationService.addNotification({
      title: 'Успех',
      message: 'Назначение платежа успешно обновлено',
      type: 'success',
    });
  } catch (error) {
    console.error('Ошибка при обновлении:', error);
    notificationService.addNotification({
      title: 'Ошибка',
      message: 'Не удалось обновить назначение платежа',
      type: 'error',
    });
  }
};

onMounted(async () => {
  document.title = pageTitle.value as string;
  await getData();
});
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