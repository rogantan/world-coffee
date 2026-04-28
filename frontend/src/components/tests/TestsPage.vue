<template>
  <div class="mt-2">
    <h2 class="header-container">
      {{ pageTitle }}
    </h2>
    <div class="card">
      <div>
        <ButtonBox title="Создать тест" @click="createTest" />
      </div>

      <TableContent :headers="headers" :data="reportEntries" :showPagination="false">

        <template #testsAvaibale-cell="{ row }">
          <div class="data-block">
            <div class="data-item">
              <span>
                {{ row.testsAvaibale }}
              </span>
              <span>
                <ButtonBox icon="ri-edit-box-line" color="warning" @click="editTest(row.testsEdit)" />
                <ButtonBox icon="ri-delete-back-line" color="danger" @click="deleteTest(row.testsRemove)" />
              </span>
            </div>
          </div>
        </template>
      </TableContent>
      <Notify />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed, ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
// import InputBox from '@/components/fields/InputBox.vue';
import ButtonBox from '../fields/ButtonBox.vue';
import TableContent from '../fields/table/TableContent.vue';
import Notify from '../modals/Notify.vue'
import { notificationService } from '../../api/notify';
import { tests } from '../../api/index'
import { format } from 'date-fns';


const router = useRouter();

const headers = ref({
  testsAvaibale: {
    title: "Тесты",
    key: "testsAvaibale",
    class: "lemon",
    sort: true,
    sortKeys: {
      asc: 'testsAvaibale_asc',
      desc: 'testsAvaibale_desc'
    }
  },
  testsDate: {
    title: "Дата",
    key: "testsDate",
    class: "lemon",
    sort: true,
    sortKeys: {
      asc: 'testsDate_asc',
      desc: 'testsDate_desc'
    }
  },

});
const route = useRoute();
const reportEntries = ref<any>([]);
const pageTitle = computed(() => route.meta.name);

const getAllTests = async () => {
  const response = await tests.getTests();
  if (response.length) {
    reportEntries.value = response.map(test => ({
      testsAvaibale: test.name,
      testsDate: format(test.date_from, 'dd.MM.yyyy') + ' - ' + format(test.date_to, 'dd.MM.yyyy'),
      testsEdit: test.id,
      testsRemove: test.id,
    })
    );
  }
}

// function handleSort(sortKey: string) {
//   // console.log('Новый ключ сортировки:', sortKey);
// }

function createTest() {
  router.push('/tests/create');
}

// const startTest = async (test_id: number) => {
//   router.push({ name: 'TestStarted', query: { test_id: test_id.toString() } });
// }

const editTest = async (test_id: number) => {
  router.push({ name: 'TestEdit', query: { test_id: test_id.toString() } });
}

const deleteTest = async (test_id: number) => {
  const response = await tests.deleteTest(test_id)
  if (response) {
    reportEntries.value = reportEntries.value.filter((test: { testsRemove: number; }) => test.testsRemove !== test_id);
    notificationService.addNotification({
      title: 'Тест успешно удален',
      message: ``,
      type: 'success',
    });
  } else {
    notificationService.addNotification({
      title: 'Ошибка при удалении теста',
      message: ``,
      type: 'error',
    });
  }
}

onMounted(async () => {
  document.title = pageTitle.value as string
  await getAllTests();
});

// onBeforeMount(async () => {
//   const role = await getRole();
//   if (role !== 'admin' && role !== "salesman" && role !== "senior_salesman") {
//     router.push('/access-deny')
//   }
// });
</script>

<style scoped>
.data-block {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background-color: #ffffff;
  padding: 10px;
  border-radius: 5px;
}

.data-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.header-container {
  display: flex;
  align-items: center;
  justify-content: start;
  padding: 10px;
  gap: 20px;
  background-color: #e9ecef;
}
</style>
