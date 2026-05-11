<template>
  <div class="mt-2">
    <Loading :active.sync="isLoading" v-bind="loadingOptions" />
    <h2 class="data-block">
      <div class="data-item">
        <span>
          {{ pageTitle }}
        </span>
        <span>
          <DateBox label="Дата оплаты" placeholder="Выберите диапазон дат для оплат"
            v-model="paymentJournalStore.paymentDates" />
        </span>
        <span>
          <DateBox label="Дата фактическая" placeholder="Выберите диапазон дат фактический"
            v-model="paymentJournalStore.accrualDates" />
        </span>
      </div>
    </h2>
    <div class="card">
      <div>
        <ButtonBox v-if="!recordIsEdit" title="Добавить запись" @click="addRecord" />
      </div>
      <TableContent :data="paymentJournalStore.pjournal" :headers="headers" @sort="handleSort" :sort_key="currentSort"
        :staticColumn="true">
        <template #payment_date-cell="{ row }">
          <div v-if="editItem.id === row.id">
            <DateBox placeholder="" :single="true" :disabled-date="false" v-model="(editItem.payment_date as Date)" />
          </div>
          <div v-else>
            {{ format(row.payment_date, 'dd.MM.yyyy') }}
          </div>
        </template>

        <template #retail_store_name-cell="{ row }">
          <div v-if="editItem.id === row.id">
            <SelectBox :values="retailStores" v-model="editItem.retail_store_id" />
            <!-- @change="(value) => editItem.retail_store_id = value"  -->
          </div>
          <div v-else>
            {{ row.retail_store_name }}
          </div>
        </template>

        <template #amount-cell="{ row }">
          <div v-if="editItem.id === row.id">
            <InputBox type="number" v-model="editItem.amount" />
          </div>
          <div v-else>
            {{ row.amount }}
          </div>
        </template>

        <template #payment_purpose_name-cell="{ row }">
          <div v-if="editItem.id === row.id">
            <SelectBox :values="paymentPurposes" v-model="editItem.payment_purpose_id" />
            <!-- @change="(value: any) => editItem.payment_purpose_id = value"  -->
          </div>
          <div v-else>
            {{ row.payment_purpose_name }}
          </div>
        </template>


        <template #employee_name-cell="{ row }">
          <div v-if="editItem.id === row.id">
            <SelectBox :values="employees" v-model="editItem.employee_id" />
            <!-- @change="(value) => editItem.employee_id = value"  -->
          </div>
          <div v-else>
            {{ row.employee_name }}
          </div>
        </template>

        <template #description-cell="{ row }">
          <div v-if="editItem.id === row.id">
            <InputBox placeholder="Описание" v-model="editItem.description"
              @update:modelValue="(value: any) => editItem.description = value" />
          </div>
          <div v-else>
            {{ row.description }}
          </div>
        </template>

        <template #accrual_date-cell="{ row }">
          <div v-if="editItem.id === row.id">
            <DateBox placeholder="" :single="true" :disabled-date="false" v-model="(editItem.accrual_date as Date)" />
          </div>
          <div v-else>
            {{ format(row.accrual_date, 'dd.MM.yyyy') }}
          </div>
        </template>

        <template #edit-cell="{ row }">
          <ButtonBox v-if="row.id === -1" color="success" icon="ri-save-2-line" @click="createRecord()" />
          <ButtonBox v-else color="success" icon="ri-save-2-line" @click="addEditedRecord()" />
          <ButtonBox color="warning" icon="ri-edit-box-line" @click="editRecord(row)" />
          <ButtonBox v-if="editItem.id === row.id" color="danger" icon="ri-delete-back-line" @click="editItem.id = 0" />
          <ButtonBox v-else color="danger" icon="ri-delete-back-line" @click="paymentJournalStore.deleteItem(row.id)" />
        </template>

      </TableContent>
      <Notify />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, reactive, computed } from 'vue'
import { useRoute } from 'vue-router';
import TableContent from '../fields/table/TableContent.vue'

import DateBox from '../fields/DateBox.vue'
import ButtonBox from '../fields/ButtonBox.vue'
import InputBox from '../fields/InputBox.vue';
import SelectBox from '../fields/SelectBox.vue'
import Notify from '../modals/Notify.vue'
import { notificationService } from '../../api/notify';
// import { getPermission } from '@utils/permission';
import { lists, payment_journal } from '../../api/index'
import { formatOnlyDate } from '../../utils/date_formatter'
import type { PaymentErrors } from '../../models/payment_validate'
import { useLoading } from '../../utils/loadingMixin';
import { usePaymentJournalStore } from '../../store/reports/payment_journal';
import type { PaymentJournal } from '../../types/reports/payment_journal';
import { format } from 'date-fns';


const route = useRoute();
const pageTitle = computed(() => route.meta.name as string);
const recordIsEdit = ref(false)
const { isLoading, loadingOptions, startLoading, stopLoading } = useLoading();

const employees = ref();
const retailStores = ref();
const paymentPurposes = ref();
const headersPaymentJournal = ref({
  payment_date: {
    title: "Дата оплаты",
    key: "payment_date",
    width: 100,
    class: "lemon",
    sort: true,
    sortKeys: {
      asc: 'payment_date-asc',
      desc: 'payment_date-desc'
    }
  },
  retail_store_name: {
    title: "Точка продаж",
    key: "retail_store_name",
    class: "lemon",
    sort: true,
    sortKeys: {
      asc: 'retail_store_name-asc',
      desc: 'retail_store_name-desc'
    }
  },
  amount: {
    title: "Сумма",
    key: "amount",
    class: "lemon",
    width: 100,
    sort: true,
    sortKeys: {
      asc: 'amount_asc',
      desc: 'amount_desc'
    }
  },
  payment_purpose_name: {
    title: "Назначение",
    key: "payment_purpose_name",
    class: "lemon",
    sort: false,
    sortKeys: {
      asc: 'payment_purpose_name-asc',
      desc: 'payment_purpose_name-desc'
    }
  },
  employee_name: {
    title: "Сотрудник",
    key: "employee_name",
    class: "lemon",
    sort: true,
    sortKeys: {
      asc: 'employee_name-asc',
      desc: 'employee_name-desc'
    }
  },
  accrual_date: {
    title: "Дата начисления",
    key: "accrual_date",
    class: "lemon",
    width: 100,
    sort: true,
    sortKeys: {
      asc: 'accrual_date-asc',
      desc: 'accrual_date-desc'
    }
  },
  description: {
    title: "Комментарий",
    key: "description",
    class: "lemon",
    sort: false,
  },
  edit: {
    title: "",
    key: "edit",
    class: "lemon",
    sort: false,
  },
})
const headers = headersPaymentJournal;
const data = ref();
const currentSort = ref('');



const editItem = reactive<PaymentJournal>({
  id: 0,
  payment_date: '',
  accrual_date: '',
  description: '',
  amount: 0,
  payment_purpose_id: '',
  employee_id: '',
  retail_store_id: '',
  payment_purpose_name: '',
  employee_name: '',
  retail_store_name: ''
})

const paymentJournalStore = usePaymentJournalStore()

const entityErrors = reactive<{ [key: number]: PaymentErrors }>({});

const handleSingleDateChange = (rows: any, dateIdentifier: any, newValue: any) => {
  if (dateIdentifier === 'payment') {
    rows.paymentDate = [newValue];
    rows.payment_date = formatOnlyDate(newValue);
    entityErrors[rows.id].payment_date = '';
  } else if (dateIdentifier === 'actual') {
    rows.accrualDate = [newValue];
    rows.accrual_date = formatOnlyDate(newValue)
    entityErrors[rows.id].accrual_date = '';
  }
};

const getDir = async () => {
  const promises = [
    lists.getEmployees(),
    lists.getRetailStores(),
    lists.getPaymentPurpose()
  ]
  const responses = await Promise.all(promises);
  if (responses.every((response: string | any[]) => response.length)) {
    employees.value = responses[0].map((item: { id: any; name: any; }) => ({
      value: item.id,
      title: item.name
    }));
    retailStores.value = responses[1].map((item: { id: any; name: any; }) => ({
      value: item.id,
      title: item.name
    }));
    paymentPurposes.value = responses[2].map((item: { id: any; name: any; }) => ({
      value: item.id,
      title: item.name
    }));
  }
}


const newRecord = async (data: { payment_date: string; retail_store_id: string; amount: number; payment_purpose_id: any; user_id: string; accrual_date: string; description: any; }) => {
  const response = await payment_journal.newSalesJournal(data);
  if (response === null) {
    notificationService.addNotification({
      title: 'Запись',
      message: 'Успешно добавлена',
      type: 'success',
    });
    editItem.id = 0
    paymentJournalStore.get()
  }
}

const addEditedRecord = async () => {
  const { id, retail_store_id, amount, payment_date, payment_purpose_id, employee_id, accrual_date, description } = editItem;
  const data = {
    payment_date: format(payment_date, 'yyyy-MM-dd'),
    retail_store_id: retail_store_id,
    amount: amount,
    payment_purpose_id: payment_purpose_id,
    user_id: employee_id,
    accrual_date: format(accrual_date, 'yyyy-MM-dd'),
    description: description
  }
  
  const response = await payment_journal.editSalesJournal(Number(id), data);
  if (response === null) {
    notificationService.addNotification({
      title: 'Запись id',
      message: 'Успешно изменена',
      type: 'success',
    });
    
    // Обновляем данные в сторе
    await paymentJournalStore.get(); // Просто перезагружаем все данные
    
    editItem.id = 0;
    recordIsEdit.value = false;
  }
}

const addRecord = async () => {
  Object.assign(editItem, paymentJournalStore.add())

  recordIsEdit.value = true;
}

const editRecord = (row: any) => {
  const retailStore = retailStores.value?.find((store: any) => store.title === row.retail_store_name);
  const paymentPurpose = paymentPurposes.value?.find((purpose: any) => String(purpose.title).trim() === String(row.payment_purpose_name).trim());
  const employee = employees.value?.find((emp: any) => emp.title === row.employee_name);
  
  Object.assign(editItem, {
    ...row,
    retail_store_id: retailStore?.value || '',
    payment_purpose_id: paymentPurpose?.value || '',
    employee_id: employee?.value || '',
    payment_date: row.payment_date ? new Date(row.payment_date) : '',
    accrual_date: row.accrual_date ? new Date(row.accrual_date) : ''
  })
  
  console.log('editItem после заполнения:', editItem)
}

const createRecord = async () => {
  const { payment_date, retail_store_id, amount, payment_purpose_id, employee_id, accrual_date, description } = editItem
  const data = {
    payment_date: format(payment_date, 'yyyy-MM-dd'),
    retail_store_id: retail_store_id,
    amount: amount,
    payment_purpose_id: payment_purpose_id,
    user_id: employee_id,
    accrual_date: format(accrual_date, 'yyyy-MM-dd'),
    description: description
  }
  try {
    await newRecord(data);
    recordIsEdit.value = false;
    paymentJournalStore.get()
  } catch (error) {
    console.error("Ошибка при создании записи:", error);
  }
}


const handleSort = (newKey: any) => {
  currentSort.value = newKey;
}

const onStoreChange = (row: any, newValue: string) => {
  const selectedOption = retailStores.value.find((option: { value: any; }) => String(option.value) === String(newValue));
  if (!selectedOption) {
    return;
  }
  row.retail_store_id = selectedOption.value;
  entityErrors[row.id].retail_store_id = '';
}

const onEmploeeChange = (row: any, newValue: any) => {
  const selectedOption = employees.value.find((option: { value: any; }) => String(option.value) === String(newValue));
  if (!selectedOption) {
    return;
  }
  row.user_id = selectedOption.value;
  entityErrors[row.id].user_id = '';
}

const onPurposeChange = (row: any, newValue: any) => {
  const selectedOption = paymentPurposes.value.find((option: { value: any; }) => String(option.value) === String(newValue));
  if (!selectedOption) {
    return;
  }
  row.payment_purpose_id = selectedOption.value
  entityErrors[row.id].payment_purpose_id = '';
}


onMounted(async () => {
  document.title = pageTitle.value
  await getDir();
  paymentJournalStore.get()
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