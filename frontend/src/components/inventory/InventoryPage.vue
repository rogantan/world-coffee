<template>
  <div class="card mt-2">
    <h2 class="data-block">
      <div class="data-item">
        {{ pageTitle }}
        <ButtonBox v-if="role === 'admin' || role === 'auditor'" @click="syncWithMS">выгрузить в МойСклад</ButtonBox>
        <ButtonBox v-if="role === 'admin' || role === 'salesman'" @click="showConfirmDialog = true">Очистить</ButtonBox>
        <div v-if="showConfirmDialog" class="backdrop" @click="showConfirmDialog = false"></div>

        <div v-if="showConfirmDialog" class="confirmation-dialog">
          <p>Вы уверены, что хотите подтвердить данное действие?</p>
          <div class="button-container">
            <ButtonBox color="success" @click="clearForm">Да</ButtonBox>
            <ButtonBox color="danger" @click="showConfirmDialog = false">Нет</ButtonBox>
          </div>
        </div>
      </div>
    </h2>
    <TableContent :headers="headers" :data="inventoryStore.inventories">
      <template #sales-cell="{ row }">
        <div v-if="role === 'salesman' || role === 'admin'">
          <InputBox type="number" step=".01" v-model="row.sales" @update:modelValue="(value: any) => handleInputChange(row, 'sales', value)" />
        </div>
        <div v-else>
          {{ row.sales }}
        </div>
      </template>

      <template #actual_balance-cell="{ row }">
        <div v-if="role === 'salesman' || role === 'admin'">
          <InputBox type="number" step=".01" v-model="row.actual_balance" @update:modelValue="(value: any) => handleInputChange(row, 'actual_balance', value)" />
        </div>
        <div v-else>
          {{ row.actual_balance }}
        </div>
      </template>
    </TableContent>
    <Notify />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import ButtonBox from '../fields/ButtonBox.vue';
import InputBox from '../fields/InputBox.vue';
import TableContent from '../fields/table/TableContent.vue';
import Notify from '../modals/Notify.vue';
import { useRoute } from 'vue-router';
import { notificationService } from '../../api/notify';
import { useUserStore } from '../../store/user';
import { useInventoryStore } from '../../store/inventory/inventory';

const route = useRoute();
const pageTitle = computed(() => route.meta.name);
const backUrl = computed(() => route.meta.back_url);
const showConfirmDialog = ref(false);
const role = useUserStore().user?.role;

const inventoryStore = useInventoryStore();

const data = ref([]);

const headers = {
  product_name: {
    title: "Название",
    key: "product_name",
    class: "lemon",
    width: 100,
    sort: false,
  },
  price: {
    title: "Цена",
    key: "price",
    class: "lemon",
    width: 100,
    sort: false,
  },
  actual_balance: {
    title: "Факт остаток",
    key: "actual_balance",
    class: "lemon",
    width: 100,
    sort: false,
  },
  sales: {
    title: "Продажи",
    key: "sales",
    class: "lemon",
    width: 100,
    sort: false,
  },
  closing_balance: {
    title: "Итоговый остаток",
    key: "closing_balance",
    class: "lemon",
    width: 100,
    sort: false,
  },
};

function debounce(fn: any, delay: any) {
  let timeoutId: number | undefined;
  return function (...args: any) {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
    timeoutId = setTimeout(() => {
      fn(...args);
    }, delay);
  };
}

const saveRow = async (row: any) => {
  if (row.actual_balance === "") {
    row.actual_balance = 0;
  }
  if (row.sales === "") {
    row.sales = 0;
  }
  try {
    const response = 1
    if (response) {
      row.closing_balance = response.closing_balance;

    }
  } catch (error: any) {
    if (error.response && error.response.status === 400) {
      notificationService.addNotification({
        title: `Ошибка в поле ${row.product_name}`,
        message: error.response.data.detail,
        type: 'error'
      })
    }
  }
}

const syncWithMS = async () => {

}

const clearForm = async () => {
  
}

const handleInputChange = debounce((row: any, key: string, value: number) => {
  row[key] = value;
  saveRow(row);
}, 500);

onMounted(async () => {
  document.title = pageTitle.value as string;
  inventoryStore.get();
})
</script>

<style>
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

.backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px);
  z-index: 999;
}

.confirmation-dialog {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  padding: 20px;
  border: 1px solid #ccc;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.button-container {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}
</style>