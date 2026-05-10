<template>
  <div class="mt-2">
    <Loading :active.sync="isLoading" v-bind="loadingOptions" />
    <h2 class="data-block">
      <div class="data-item">
        <span>
          {{ pageTitle }}
        </span>
        <span>
          <DateBox placeholder="Выберите диапозон дат" :modelValue="dateRange" @update:modelValue="handleDateChange" />
        </span>
      </div>
    </h2>
    <div class="card">
      <TableContent :data="data" :headers="headers" @sort="handleSort" :staticColumn="true" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed, ref, reactive, watch } from 'vue';
import { useRoute } from 'vue-router';
import TableContent from '../fields/table/TableContent.vue'
import DateBox from '../fields/DateBox.vue';
import { ApiReport } from "@/api";
import { formatOnlyDate } from '../../utils/date_formatter'
import { processServerData } from '../../utils/response_formatter'
import { useLoading } from '../../utils/loadingMixin';


const route = useRoute();
const pageTitle = computed(() => route.meta.name);
const dateRange = ref([new Date(2022, 0, 1), new Date()]);
const { isLoading, loadingOptions, startLoading, stopLoading } = useLoading();

const headers = reactive({
  columnName: {
    title: "Название",
    key: "columnName",
    sort: false,
    class: "lemon"
  },
});


const updateHeaders = () => {
  let start = new Date(dateRange.value[0]);
  let end = new Date(dateRange.value[1]);

  const newHeaders = { ...headers };

  Object.keys(newHeaders).forEach(key => {
    if (key.includes('-')) delete newHeaders[key];
  });

  while (start <= end) {
    const formattedDate = start.toLocaleDateString('fr-CA', { year: 'numeric', month: '2-digit' });
    const percentKey = `percent_${formattedDate}`; // ключ для процентов

    newHeaders[percentKey] = {
      title: '',
      key: percentKey,
      sort: false,
    };
    newHeaders[formattedDate] = {
      title: formattedDate,
      key: formattedDate,
      class: "lemon",
      sort: false,
    };
    start.setMonth(start.getMonth() + 1);
  }

  for (const key in headers) {
    delete headers[key];
  }
  Object.assign(headers, newHeaders);
};

const data = ref([])

const getData = async () => {
  startLoading();
  const [date_from, date_to] = dateRange.value.map(date => formatOnlyDate(date));
  const response = await ApiReport.getReportWithDate({ report_name: 'revenue_monthly', date_from, date_to })
  if (response.length) {
    const processedData = processServerData(response);
    data.value = processedData;
  }
  stopLoading();
}

const handleDateChange = (newRange: any) => {
  dateRange.value = newRange;
};

const handleSort = () => {

}

watch(dateRange, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    updateHeaders();
    getData();
  }
}, { deep: true });

onMounted(async () => {
  document.title = pageTitle.value as string;
  updateHeaders();
  await getData();
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