<template>
  <div class="mt-2">
    <h2 class="header-container">
      {{ pageTitle }}
    </h2>
    <div v-if="employeeId && testId">
      <ButtonBox @click="hideTest">Назад</ButtonBox>
      <TestsShowResultByUserPage :employeeId="employeeId" :testId="testId" :employeeName="employeeName" />
    </div>
    <div v-else>
      <ButtonBox @click="goBack">Назад</ButtonBox>
      <TableContent :headers="headers" :data="data">
        <template #finish_date-cell="{ row }">
          {{ row.finish_date.split("T")[0] }}
        </template>

        <template #show-cell="{ row }">
          <ButtonBox icon="ri-eye-line" color="success p-1" @click="showTest(row)">
          </ButtonBox>
        </template>
      </TableContent>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import TableContent from "../fields/table/TableContent.vue";
import ButtonBox from "../fields/ButtonBox.vue";
import TestShowResultByUserPage from "./TestResultByUserPage.vue"

export default defineComponent({
  name: "TestsShowResultTablePage",
  components: {
    ButtonBox,
    TableContent,
    TestShowResultByUserPage,
  },
  props: {
    data: {
      type: Array,
    },
    employeeName: {
      type: String,
    },
  },
  setup(props) {
    const route = useRoute();
    const pageTitle = computed(() => route.meta.name);
    const router = useRouter();

    const headers = {
      name: {
        title: "Название теста",
        key: "name",
        class: "lemon",
      },
      result: {
        title: "Результат",
        key: "result",
        class: "lemon",
      },
      finish_date: {
        title: "Дата прохождения",
        key: "finish_date",
        class: "lemon",
      },
      show: {
        tiitle: "",
        key: "show",
        class: "lemon",
        width: 100,
      },
    };

    const employeeId = ref();
    const testId = ref();

    const showTest = (row: { user_id: any; test_id: any; }) => {
      employeeId.value = row.user_id;
      testId.value = row.test_id;
    };

    const hideTest = () => {
      employeeId.value = undefined;
      testId.value = null;
    };
    const goBack = () => {
      router.push("/tests/result");
    };

    onMounted(async () => {
      // console.log(props.data).
    });

    return {
      pageTitle,
      headers,
      data: props.data,
      showTest,
      hideTest,
      goBack,
      employeeId,
      employeeName: props.employeeName,
      testId,
    };
  },
});
</script>
