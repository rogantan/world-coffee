<template>
  <!-- {{ employeeName }} -->
  <div v-if="showOne && testId">
    <ButtonBox @click="goBack">Назад</ButtonBox>
    <TestsResultByUserPage :employeeId="employeeId" :testId="testId" :employeeName="employeeName" />
  </div>
  <div v-if="!showOne && data">
    <div class="card">
      <TestsShowResultTablePage :data="data" :employeeName="employeeName" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { tests } from "../../api/index";
import TestsResultByUserPage from "./TestResultByUserPage.vue";
import TestsShowResultTablePage from "./TestShowResultTablePage.vue";
import ButtonBox from "../fields/ButtonBox.vue";

const route = useRoute();
const router = useRouter();
const showOne = ref<boolean>(true);
const data = ref([]);
const employeeId = route.params.id as string;
const employeeName = route.params.name as string;

const date = route.params.date as string;
const testId = ref<number | null>(null);

const getData = async () => {
  const response = await tests.getResultByMonth(date, employeeId);
  data.value = response;

  if (data.value.length === 1) {
    testId.value = response[0].test_id;
  }
};

const goBack = () => {
  router.push("/tests/result");
};

onMounted(async () => {
  await getData();
  if (data.value.length > 1) {
    showOne.value = false;
  }
});

</script>
