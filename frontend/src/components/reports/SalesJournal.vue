<template>
  <div class="mt-2">
    <h2 class="data-block">
      <div class="data-item">
        <span>
          {{ pageTitle }}
        </span>
        <span>
          <DateBox :single="false" placeholder="Выберите диапозон дат" v-model="saleJournalStore.dates" />
        </span>
      </div>
    </h2>
    <div class="card">
      <TableContent :data="saleJournalStore.sjournal" :headers="headers" @sort="handleSort" :sort_key="currentSort"
        :staticColumn="true" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed, ref } from 'vue'
import { useRoute } from 'vue-router';
import TableContent from '../fields/table/TableContent.vue'
import DateBox from '../fields/DateBox.vue';
import { useSalesJournalStore } from '../../store/reports/sales_journal';


const pageTitle = computed(() => route.meta.name);
const route = useRoute();

const currentSort = ref('');
const saleJournalStore = useSalesJournalStore();

const headersSalesJournal = ref({
  id: {
    title: "ID документа",
    key: "id",
    class: "lemon",
    sort: true,
    sortKeys: {
      asc: 'id-asc',
      desc: 'id-desc',
    },
  },
  name: {
    title: "№ продажи",
    key: "name",
    sort: true,
    class: "lemon",
    sortKeys: {
      asc: 'name-asc',
      desc: 'name-desc',
    },
  },
  moment: {
    title: "Время",
    key: "moment",
    class: "lemon",
    sort: true,
    sortKeys: {
      asc: 'moment-asc',
      desc: 'moment-desc',
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
  agent_name: {
    title: "Контрагент",
    key: "agent_name",
    class: "lemon",
    sort: true,
    sortKeys: {
      asc: 'agent_name-asc',
      desc: 'agent_name-desc',
    },
  },
  organization_name: {
    title: "Организация ",
    key: "organization_name",
    class: "lemon",
    sort: true,
    sortKeys: {
      asc: 'organization_name-asc',
      desc: 'organization_name-desc',
    },
  },
  cash_sum: {
    title: "Сумма нал.",
    key: "cash_sum",
    class: "lemon",
    sort: true,
    sortKeys: {
      asc: 'cash_sum-asc',
      desc: 'cash_sum-desc',
    },
  },
  no_cash_sum: {
    title: "Сумма безна.",
    key: "no_cash_sum",
    class: "lemon",
    sort: true,
    sortKeys: {
      asc: 'no_cash_sum-asc',
      desc: 'no_cash_sum-desc',
    },
  },
  qr_sum: {
    title: "Сумма по QR-коду",
    key: "qr_sum",
    class: "lemon",
    sort: true,
    sortKeys: {
      asc: 'qr_sum-asc',
      desc: 'qr_sum-desc',
    },
  },

  sum: {
    title: "Итого",
    key: "sum",
    class: "lemon",
    sort: true,
    sortKeys: {
      asc: 'sum-asc',
      desc: 'sum-desc',
    },
  },
  discounts: {
    title: "Сумма скидок",
    key: "discounts",
    class: "lemon",
    sort: true,
    sortKeys: {
      asc: 'discounts-asc',
      desc: 'discounts-desc',
    },
  },
  owner_name: {
    title: "Владелец-сотрудник",
    key: "owner_name",
    class: "lemon",
    sort: true,
    sortKeys: {
      asc: 'owner_name-asc',
      desc: 'owner_name-desc',
    },
  },
});

const headers = headersSalesJournal;

const handleSort = (newKey: any) => {
  currentSort.value = newKey;
};

onMounted(() => {
  document.title = pageTitle.value as string
  saleJournalStore.get()
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