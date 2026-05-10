<template>
  <div class="mt-2">
    <h2 class="header-container">
      {{ pageTitle }}
      <DateBox placeholder="" :modelValue="dateRange" @update:modelValue="handleDateChange" />
    </h2>
    <div class="card">
      <TableContent :headers="headers" :data="data" @sort="handleSort" :sort_key="currentSort" :staticColumn="true">
        <template class="" v-for="item in templateName" #[`points_${item}-cell`]="{ row }">
          <div class="data-block">
            <div class="data-item">
              <span>
                {{ row[`points_${item}`] }}
              </span>

              <ButtonBox v-if="
                row.employee_name !== ' ' &&
                row[`points_${item}`] != null &&
                role !== 'salesman'
              " icon="ri-eye-line" color="success p-1" @click="
                handleShowDetail(
                  item,
                  row.employee_id,
                  row[`employee_name_${item}`]
                )
                ">
              </ButtonBox>
            </div>
          </div>
        </template>
      </TableContent>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onBeforeMount, onMounted, watch, reactive, computed, ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import TableContent from "../fields/table/TableContent.vue";
import ButtonBox from "../fields/ButtonBox.vue";
import DateBox from "../fields/DateBox.vue";
import { test_user } from "../../api/index";
import { formatOnlyDate } from "../../utils/date_formatter";
import type { tTestResult } from "../../types/testing/user";
import { useUserStore } from "../../store/user";

const route = useRoute();
const router = useRouter();
const role = useUserStore().user?.role;
const dateRange = ref([new Date(2026, 0, 1), new Date()]);
const templateName = ref<any[]>([]);

const currentSort = ref("");
const pageTitle = computed(() => route.meta.name);

const headers: any = reactive({});

const updateHeaders = () => {
  let start = new Date(dateRange.value[0]);
  let end = new Date(dateRange.value[1]);

  for (const key in headers) {
    delete headers[key];
  }

  const newHeaders: any = {};

  while (start <= end) {
    const formattedKey = start.toLocaleDateString("fr-CA", {
      year: "numeric",
      month: "2-digit",
    });
    const formattedDate = formattedKey.replace(/-/g, "_");

    newHeaders[`employee_name_${formattedDate}`] = {
      title: "Имя",
      key: `employee_name_${formattedDate}`,
      class: "lemon",
      sort: true,
      sortKeys: {
        asc: `employee_name&${formattedDate}-asc`,
        desc: `employee_name&${formattedDate}-desc`,
      },
    };
    newHeaders[`employee_email_${formattedDate}`] = {
      title: "Email",
      key: `employee_email_${formattedDate}`,
      class: "lemon",
      sort: true,
      sortKeys: {
        asc: `employee_email&${formattedDate}-asc`,
        desc: `employee_email&${formattedDate}-desc`,
      },
    };
    newHeaders[`points_${formattedDate}`] = {
      title: "Результат",
      key: `points_${formattedDate}`,
      class: "lemon",
      sort: true,
      sortKeys: {
        asc: `points&${formattedDate}_asc`,
        desc: `points&${formattedDate}_desc`,
      },
    };
    newHeaders[`rank_${formattedDate}`] = {
      title: "Место",
      key: `rank_${formattedDate}`,
      class: "lemon",
      sort: true,
      sortKeys: {
        asc: `rank&${formattedDate}_asc`,
        desc: `rank&${formattedDate}_desc`,
      },
    };

    start.setMonth(start.getMonth() + 1);
    start.setDate(1);
  }
  Object.assign(headers, newHeaders);
};

const data = ref<any[]>([]);

const getData = async (
  order_date: string = "",
  order_by: string = "",
  desc: boolean = false
) => {
  const [date_from, date_to] = dateRange.value.map((date) =>
    formatOnlyDate(date)
  );
  let response: tTestResult[];
  if (order_by) {
    response = await test_user.getFilteredTestsResult(
      date_from,
      date_to,
      order_date,
      order_by,
      desc
    );
  } else {
    response = await test_user.getTestsResult(date_from, date_to);
  }

  if (response.length) {
    const aggregatedData: any = {};
    const initialRow: any = {
      employee_name: " ",
    };

    let startDate = new Date(dateRange.value[0]);
    let endDate = new Date(dateRange.value[1]);
    while (startDate <= endDate) {
      const formattedDate = `${startDate.getFullYear()}_${(
        startDate.getMonth() + 1
      )
        .toString()
        .padStart(2, "0")}`;
      initialRow[`points_${formattedDate}`] = startDate.toLocaleDateString("fr-CA");
      initialRow[`rank_${formattedDate}`] = " ";
      templateName.value.push(`${formattedDate}`);
      // console.log(templateName.value)
      startDate.setMonth(startDate.getMonth() + 1);
      startDate.setDate(1);
    }

    response.forEach((item: any) => {
      // let isFirstRow = true;
      item.rows.forEach((row: any) => {
        // console.log(row.points)
        const [year, month] = row.date.split("-");
        const formattedDate = `${year}_${month}`;

        if (!aggregatedData[item.employee_name]) {
          aggregatedData[item.employee_name] = {};
        }
        // Заполняем данные сотрудника для конкретной даты
        aggregatedData[item.employee_name][
          `employee_name_${formattedDate}`
        ] = item.employee_name;
        aggregatedData[item.employee_name][
          `employee_email_${formattedDate}`
        ] = item.employee_email;
        aggregatedData[item.employee_name][`points_${formattedDate}`] =
          row.points;
        aggregatedData[item.employee_name][`rank_${formattedDate}`] =
          row.rank;
        aggregatedData[item.employee_name][`employee_id`] =
          item.employee_id;
      });
    });

    // Обновляем data.value.rows одним объектом с данными по всем пользователям
    const newData = [initialRow, ...Object.values(aggregatedData)];
    data.value = newData;
  }
  // console.log(data.value)
};

const handleSort = (newKey: string) => {
  currentSort.value = newKey;
  const parts = currentSort.value.split("-");
  const order_type = parts[1] === "desc" ? false : true;
  const partsTwo = parts[0].split("&");
  const date =
    partsTwo[0] !== "employee_name"
      ? partsTwo[1].replace(/_/g, "-") + "-01"
      : "";

  getData(date, partsTwo[0], order_type);
};

const handleDateChange = (newRange: any) => {
  dateRange.value = newRange;
};

const handleShowDetail = (item: any, employee_id: string, employee_name: string) => {
  const date = item.replace(/_/g, "-") + "-01";
  const employeeId = employee_id;
  const employeeName = employee_name;
  console.log(employeeName);
  router.push({
    name: "TestPreshowPage",
    params: {
      id: employeeId,
      date: date,
      name: employeeName,
    },
  });
};

watch(
  dateRange,
  (newVal, oldVal) => {
    if (newVal !== oldVal) {
      updateHeaders();
      getData();
    }
  },
  { deep: true }
);

onMounted(async () => {
  document.title = pageTitle.value as string;
  updateHeaders();
  await getData();
});

onBeforeMount(() => {
  const curRole = useUserStore().user?.role;
  if (
    curRole !== "admin" &&
    curRole !== "salesman" &&
    curRole !== "senior_salesman"
  ) {
    router.push("/access-deny");
  }
  // role.value = curRole;
});
</script>

<style scoped>
.header-container {
  display: flex;
  align-items: center;
  justify-content: start;
  padding: 10px;
  gap: 20px;
  background-color: #e9ecef;
}

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
  margin: 0;
}
</style>