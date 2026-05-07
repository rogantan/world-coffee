<template>
  <div class="navbar-custom d-flex">
    <div class="topbar container-fluid">
      <button class="btn" @click="openNavigation">
        <i class="ri-menu-2-fill"></i>
      </button>
    </div>

    <ul class="topbat-menu d-flex align-items-center ms-auto gap-3 list-unstyled">
      <li class="dropdown">
        <a class="nav-link arrow-none nav-user px-2" href="#" role="button">
          <span class="">
            <h5 class="my-0">{{ getUserRole(userStore?.user?.role) }}</h5>
          </span>
        </a>
      </li>
      <li>
        <a class="dropdown-item" @click="Logout">
          <i class="ri-logout-box-line fs-18 align-middle me-1"></i>
          <span>Выйти из аккаунта</span>
        </a>
      </li>
    </ul>
  </div>
</template>

<script lang="ts" setup>
import router from '../../router/index';
import { useUserStore } from '../../store/user';
const userStore = useUserStore();

const Logout = () => {
  localStorage.removeItem('token');
  router.push("/signin");
  userStore.clear();
}

const openNavigation = () => {
  userStore.toogleMenu();
}

const getUserRole = (role_name: string | undefined) => {
  if (role_name === "admin") {
    return "Администратор";
  } else if (role_name === "auditor") {
    return "Ревизор";
  } else if (role_name === "salesman") {
    return "Продавец";
  } else if (role_name === "senior_salesman") {
    return "Старший продавец";
  } else if (role_name === "accountant") {
    return "Бухгалтер";
  }
}
</script>

<style>
.dropdown-item {
  cursor: pointer;
}
</style>