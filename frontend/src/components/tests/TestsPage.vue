<template>
  <div class="mt-2">
    <h2 class="header-container">
      {{ pageTitle }}
    </h2>
    <div v-if="showConfirmDialog" class="backdrop" @click="showConfirmDialog = false"></div>
    <div class="card">
      <div v-if="role === 'admin'">
        <ButtonBox title="Создать тест" @click="createTest" />
      </div>
      <div v-if="showConfirmDialog" class="confirmation-dialog">
        <p>Вы уверены, что хотите подтвердить данное действие?</p>
        <div class="button-container">
          <ButtonBox color="success" @click="deleteTest">Да</ButtonBox>
          <ButtonBox color="danger" @click="showConfirmDialog = false">Нет</ButtonBox>
        </div>
      </div>

      <TableContent :headers="headers" :data="reportEntries" :showPagination="false">

        <template #testsAvaibale-cell="{ row }">
          <div class="data-block">
            <div class="data-item">
              <span>
                {{ row.testsAvaibale }}
              </span>
              <span v-if="role == 'admin'">
                <ButtonBox icon="ri-edit-box-line" color="warning" @click="editTest(row.testsEdit)" />
                <ButtonBox icon="ri-delete-back-line" color="danger" @click="setTestId(row.testsRemove)" />
              </span>
              <span>
                <ButtonBox v-if="!row.archived && row.active"
                  title="Начать тест"
                  @click="startTest(row.testsStart)"
                  />
              </span>
              <span>
                <ButtonBox v-if="row.archived"
                  title="Результаты"
                  @click="resultTest(row.testsStart)"
                  />
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
import { useUserStore } from '../../store/user';

const router = useRouter();

const showConfirmDialog = ref(false);

const userStore = useUserStore();
const role = computed(() => userStore.user?.role);

const testId = ref<number | null>(null);

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
      testsStart: test.id,
      active: test.is_active,
      archived: test.was_passed
    })
    );
  }
}

function createTest() {
  router.push('/tests/create');
}

const editTest = async (test_id: number) => {
  router.push({ name: 'TestEdit', query: { test_id: test_id.toString() } });
}

const setTestId = async (test_id: number) => {
  testId.value = test_id;
  showConfirmDialog.value = true;
}

const deleteTest = async () => {
  if (testId.value) {
    const response = await tests.deleteTest(testId.value)
    if (response) {
      reportEntries.value = reportEntries.value.filter((test: { testsRemove: number; }) => test.testsRemove !== testId.value);
      showConfirmDialog.value = false;
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
  
}

const startTest = async(test_id: number) => {
  router.push({ name: 'TestStarted', query: { test_id: test_id.toString() } })
}

const resultTest = async(test_id: number) => {
  router.push({ name: 'TestsShowResult', query: { test_id: test_id.toString() } })
}

onMounted(async () => {
  document.title = pageTitle.value as string
  await getAllTests();
});

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
</style>
