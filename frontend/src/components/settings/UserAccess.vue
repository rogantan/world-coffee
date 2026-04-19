<template>
  <div class="mt-2">
    <h2>{{ pageTitle }}</h2>
    <div class="card">
      <TableContent :data="employees" :headers="headers">
        <template #resetPwd-cell="{ row }">
          <ButtonBox title="Сбросить пароль" @click="resetPwd(row.uid)" />
        </template>
        <template #salaryCoefficient-cell="{ row }">
          <div v-if="row.salaryCoefficientEdit" class="data-block">
            <div class="data-item">
              <span>
                <InputBox type="number" step="0.1" v-model="row.salaryCoefficient" />
              </span>
              <span>
                <ButtonBox color="success" icon="ri-save-2-line" @click="editSalaryCoefficient(row)" />
                <ButtonBox color="danger" icon="ri-delete-back-line" @click="canselSalaryCoefficient(row)" />
              </span>
            </div>
          </div>
          <div v-else class="data-block">
            <div class="data-item">
              <span>
                {{ row.salaryCoefficient }}
              </span>
              <span>
                <ButtonBox v-if="row.salaryCoefficient" color="warning" icon="ri-edit-box-line"
                  @click="startSalaryCoefficient(row)" />
              </span>
            </div>
          </div>
        </template>

        <template #role-cell="{ row }">
          <SelectBox :values="selectOptionsRole" v-model="row.role"
            @update:model-value="(newValue: string) => onRoleChange(row, newValue)" />
        </template>

        <template v-for="(header) in Object.keys(headers).slice(5)" :key="header" v-slot:[`${header}-cell`]="{ row }">
          <SelectBox :values="getSelectOptions(header)" v-model="row[header]"
            @update:model-value="(newValue: string) => handlePermissionChange(row, header, newValue)" />
          <!-- @change="value => handlePermissionChange(row, header, value)" -->
        </template>
      </TableContent>
      <Notify />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import TableContent from '../fields/table/TableContent.vue';
import { ApiUser } from '../../api';
import { notificationService } from '../../api/notify';
import type { User } from '../../types/admin/user';
import ButtonBox from '../fields/ButtonBox.vue';
import SelectBox from '../fields/SelectBox.vue';
import Notify from '../modals/Notify.vue';

const route = useRoute();
const pageTitle = computed(() => route.meta.name);

interface Header {
  title: string
  key: string
  sort: boolean
  class?: string
  sortKeys?: {
    asc: string
    desc: string
  };
}

type Headers = Record<string, Header>;

interface EmployerRow {
  uid: string
  employeeName: string
  empooyeeEmail: string
  // dateOfEmployment: string
  salaryCoefficient: string
  salaryCoefficientEdit: boolean
  employeeRole: string
  payment?: string
}

interface SelectType {
  value: any;
  title: string;
}
type AccessTypes = SelectType[];

interface SelectTypeRole {
  value: string;
  title: string;
}
type RoleTypes = SelectTypeRole[];
const getSelectOptions = (header: string) => {
  if (header === 'paymentJournal') {
    return selectOptionsEditable.value;
  }
  return selectOptions.value;
};

const selectOptions = ref<AccessTypes>([
  { value: 'hidden', title: 'Нет доступа' },
  { value: 'displayed', title: 'Просмотр' },
]);

const selectOptionsEditable = ref<AccessTypes>([
  { value: 'hidden', title: 'Нет доступа' },
  { value: 'displayed', title: 'Просмотр' },
  { value: 'editable', title: 'Редактирование' },
]);

const selectOptionsRole = ref<RoleTypes>([
  { value: 'admin', title: 'Админ' },
  { value: 'auditor', title: 'Ревизор' },
  { value: 'salesman', title: 'Продавец' },
  { value: 'senior_salesman', title: 'Старший продавец' },
  { value: 'accountant', title: 'Бухгалтер' }
]);

const headers = ref<Headers>({
  name: {
    title: "Сотрудник",
    key: "employeeName",
    class: "lemon",
    sort: false
  },
  email: {
    title: "Email",
    key: "employeeEmail",
    class: "lemon",
    sort: false
  },
  resetPwd: {
    title: "Сбросить пароль",
    key: "resetPwd",
    class: "lemon",
    sort: false
  },
  salaryCoefficient: {
    title: "Коэффициент к окладу",
    key: "salaryCoefficient",
    class: "lemon",
    sort: false,
  },
  role: {
    title: "Роль",
    key: "employeeRole",
    class: "lemon",
    sort: false,
  },
  auditor: {
    title: "Ревизор",
    key: "auditor",
    class: "lemon",
    sort: false,
  },
  salesJournal: {
    title: "Журнал продаж",
    key: "salesJournal",
    class: "lemon",
    sort: false,
  },
  paymentJournal: {
    title: "Журнал платежей",
    key: "paymentJournal",
    class: "lemon",
    sort: false
  }
});

interface tUser extends User {
  resetPwd?: string
}
const employees = ref<tUser[]>([]);


const getPermissions = async () => {
  const response = await ApiUser.getAllUsers();
  if (response && Array.isArray(response)) {
    if (response.length > 0) {
      console.log(response);
    }
    employees.value = response.map((user: tUser) => ({
      uid: user.uid,
        id: user.id,
        name: user.name,
        email: user.email,
        // salaryCoefficient: user. || '',
        // salaryCoefficientEdit: false,
        resetPwd: user.uid || '',
        role: user.role,
        permissions: user.permissions,
        ...user.permissions.reduce((acc, perm) => ({
          ...acc,
          [perm.title]: perm.mode,}),
          {}),
    }))
  }
};

const onRoleChange = async (row: EmployerRow, newValue: string) => {
  const selectedOption = selectOptionsRole.value.find(option => option.value === newValue);
  if (!selectedOption) {
    return;
  }

  try {
    await ApiUser.changeUserRole(row.uid, newValue);
    // toast.success(`Роль пользователя ${row.employeeName} изменена на ${selectedOption.title}`);
    notificationService.addNotification({
      title: 'Роль успешно изменена',
      message: `Роль пользователя ${row.employeeName} изменена на ${selectedOption.title}`,
      type: 'success',
    });
    // row.employeeRole = selectedOption.value;
    await getPermissions()
  } catch (error) {
    notificationService.addNotification({
      title: 'Ошибка изменения роли',
      message: `Не удалось изменить роль пользователя ${row.employeeName}. Попробуйте снова.`,
      type: 'error',
    });
  }
};


const resetPwd = async (uid: string) => {
  try {
    // const response = 
    await ApiUser.resetUserPassword(uid);
    // if (response.status === 200) {
    notificationService.addNotification({
      title: 'Пароль сброшен',
      message: 'Пароль успешно сброшен.',
      type: 'success',
    });
    // }
  } catch (error) {
    notificationService.addNotification({
      title: 'Ошибка сброса пароля',
      message: 'Не удалось сбросить пароль. Попробуйте снова.',
      type: 'error',
    });
  }
};

onMounted(async () => {
  document.title = pageTitle.value as string
  await getPermissions()
  // updateHeaders()
});
</script>