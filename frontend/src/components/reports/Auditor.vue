<template>
  <div class="mt-2">
    <!-- <Loading :active.sync="isLoading" v-bind="loadingOptions" /> -->
    <h2 class="data-block">
      <div class="data-item">
        <span>
          {{ pageTitle }}
        </span>
        <span>
          <DateBox placeholder="Выберите диапозон дат" v-model="reportStore.dates" />
        </span>
      </div>
    </h2>
    <div class="card">
      <TableContent :data="reportStore.report" :headers="headers" @sort="reportStore.handleSort"
        :sort_key="`${reportStore.sortKey}-${reportStore.sortAsk}`" :staticColumn="true">
        <template #name-cell="{ row }">
          <a :href="row.link">{{ row.name }}</a>
        </template>
        <template #manual_changes-cell="{ row }">
          <div v-if="isEditManual === row.uuid" class="data-item">
            <InputBox type="text" v-model="row.manual_changes" />
            <ButtonBox color="success" icon="ri-save-2-line" @click="handleManualChanges(row)" />
            <ButtonBox color="danger" icon="ri-delete-back-line" @click="isEditManual = null" />
          </div>
          <div v-else class="data-item">
            {{ row.manual_changes }}
            <ButtonBox color="warning" icon="ri-edit-box-line" @click="isEditManual = row.uuid" />
          </div>
        </template>
        <template #date-cell="{ row }">
          {{ format(row.date, 'dd.MM.yyyy') }}
        </template>
        <template #month-cell="{ row }">
          {{ format(row.date, 'dd.MM.yyyy') }}
        </template>
        <!-- <template #link-cell="{ row }">
          <a :href="row.link" target="_blank">{{ row.link.split('id=').pop() }}</a>
        </template> -->
      </TableContent>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed, ref } from 'vue'
import { useRoute } from 'vue-router';
import TableContent from '@/components/table/TableContent.vue'
import DateBox from '@/components/fields/DateBox.vue';
import ButtonBox from '@/components/fields/ButtonBox.vue';
import InputBox from '@/components/fields/InputBox.vue';
import { ApiReport } from '@/api/index'
// import { formatOnlyDate } from '@/utils/date_formatter'
// import { useLoading } from '@/utils/loadingMixin';
import { useAuditorStore } from '@/store/report/auditor';
import { format } from 'date-fns'

const route = useRoute();
const pageTitle = computed(() => route.meta.name as string);
// const { isLoading, loadingOptions, startLoading, stopLoading } = useLoading();
const isEditManual = ref<string | null>(null);

const reportStore = useAuditorStore()
// const dateRange = ref(
//   [new Date(new Date().getFullYear(), new Date().getMonth(), 1),
//   new Date()]
// );

const headers = {
  name: {
    title: "Номер инвента",
    key: "name",
    sort: true,
    class: "lemon",
    width: 100,
    sortKeys: {
      asc: 'name-asc',
      desc: 'name-desc',
    },
  },
  date: {
    title: "Дата",
    key: "date",
    class: "lemon",
    width: 100,
    sort: true,
    sortKeys: {
      asc: 'date-asc',
      desc: 'date-desc',
    },
  },
  salesman_name: {
    title: "Продавец",
    key: "salesman_name",
    class: "lemon",
    sort: true,
    sortKeys: {
      asc: 'salesman_name-asc',
      desc: 'salesman_name-desc',
    },
  },
  retail_store_name: {
    title: "Точка продаж",
    key: "retail_store_name",
    class: "lemon",
    sort: true,
    sortKeys: {
      asc: 'retail_store_name-asc',
      desc: 'retail_store_name-desc',
    },
  },
  loss_sum: {
    title: "Сумма списания",
    key: "loss_sum",
    class: "lemon",
    width: 100,
    sort: true,
    sortKeys: {
      asc: 'loss_sum-asc',
      desc: 'loss_sum-desc',
    },
  },
  enter_sum: {
    title: "Сумма оприхо дования",
    key: "enter_sum",
    class: "lemon",
    width: 100,
    sort: true,
    sortKeys: {
      asc: 'enter_sum-asc',
      desc: 'enter_sum-desc',
    },
  },
  manual_changes: {
    title: "Ручные изменения",
    key: "manual_changes",
    class: "lemon",
    width: 200,
    sort: false,
  },

  retention_sum: {
    title: "Удержание итог",
    key: "retention_sum",
    class: "lemon",
    width: 100,
    sort: true,
    sortKeys: {
      asc: 'retention_sum-asc',
      desc: 'retention_sum-desc',
    },
  },
  month: {
    title: "Дата 2",
    key: "month",
    class: "lemon",
    width: 100,
    sort: true,
    sortKeys: {
      asc: 'month-asc',
      desc: 'month-desc',
    },
  },
}


const handleManualChanges = async (row: any) => {
  const response = await ApiReport.putManualChanges(row.uuid, row.manual_changes)
  if (response) {
    row.retention_sum = response.retention_sum
    isEditManual.value = null;
  }
}

onMounted(async () => {
  document.title = pageTitle.value
  // reportStore.reportName = 'auditor'
  reportStore.get()
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