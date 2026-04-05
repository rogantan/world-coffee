<template>
  <div class="leftside-menu menuitem-active">
    <div class="h-100 show" id="leftside-menu-container" data-simplebar="init">
      <div class="simplebar-wrapper">
        <div class="simplebar-offset">
          <div class="simplebar-content-wrapper" role="region" aria-label="scrollable content">
            <div class="simplebar-content">
              <div class="leftbar-user p-3 text-white">
                <a class="d-flex alogn-items-center text-reset">
                  <div class="flex-shrink-0">
                    <img>
                  </div>
                  <div class="flex-grow-1 ms-2">
                    <span class="fw-semibold fs-15 d-block">{{ userName }}</span>
                  </div>
                </a>
              </div>
            </div>

            <ul class="side-nav">
              <li class="side-nav-title" v-if="userRole === 'admin'">Настройки</li>
              <li class="side-nav-item" v-if="userRole === 'admin'" v-for="menuSetting in menuSettings"
              :key="menuSetting.name" @click="navigateTo(menuSetting.path, menuSetting.name, 'settings')" :class="{
                'menuitem-active': activeMenu?.category === 'settings' && activeMenu.name === menuSetting.name,
              }">
              <a class="side-nav-link" :class="{active: activeMenu?.category === 'settings' && activeMenu.name === menuSetting.name}">
                <i :class="menuSetting.icon"></i>
                <span>{{ menuSetting.name }}</span>
              </a>
              </li>

              <li class="side-nav-title" v-if="userRole === 'admin'">Справочники</li>
              <li class="side-nav-item" v-if="userRole === 'admin'" v-for="menuList in menuLists" 
              :key="menuList.name" @click="navigateTo(menuList.path, menuList.name, 'lists')" :class="{
                'menuitem-active': activeMenu?.category === 'lists' && activeMenu.name === menuList.name,
              }">
              <a class="side-nav-link" :class="{active: activeMenu?.category === 'lists' && activeMenu.name === menuList.name}">
                <i :class="menuList.icon"></i>
                <span>{{ menuList.name }}</span>
              </a>
              </li>

              <li class="side-nav-title" v-if="userRole === 'admin'">Тестирование</li>
              <li class="side-nav-item" v-for="menuList in menuTests" 
              :key="menuList.name" @click="navigateTo(menuList.path, menuList.name, 'lists')" :class="{
                'menuitem-active': activeMenu?.category === 'lists' && activeMenu.name === menuList.name,
              }">
              <a class="side-nav-link" :class="{active: activeMenu?.category === 'lists' && activeMenu.name === menuList.name}">
                <i :class="menuList.icon"></i>
                <span>{{ menuList.name }}</span>
              </a>
              </li>

              <li class="side-nav-title" v-if="menuReports.length > 0">Отчёты</li>
              <li class="side-nav-item" v-for="menuList in menuReports" 
              :key="menuList.name" @click="navigateTo(menuList.path, menuList.name, 'reports')" :class="{
                'menuitem-active': activeMenu?.category === 'reports' && activeMenu.name === menuList.name,
              }">
              <a class="side-nav-link" :class="{active: activeMenu?.category === 'reports' && activeMenu.name === menuList.name}">
                <i :class="menuList.icon"></i>
                <span>{{ menuList.name }}</span>
              </a>
              </li>

              <li class="side-nav-title" v-if="userRole === 'admin'">Дашборды</li>
              <li class="side-nav-item" v-if="userRole === 'admin'" v-for="menuList in menuDashboards" 
              :key="menuList.name" @click="navigateTo(menuList.path, menuList.name, 'lists')" :class="{
                'menuitem-active': activeMenu?.category === 'lists' && activeMenu.name === menuList.name,
              }">
              <a class="side-nav-link" :class="{active: activeMenu?.category === 'lists' && activeMenu.name === menuList.name}">
                <i :class="menuList.icon"></i>
                <span>{{ menuList.name }}</span>
              </a>
              </li>

              <li class="side-nav-title" v-if="userRole === 'admin'">Инвентаризации</li>
              <li class="side-nav-item" v-if="userRole === 'admin'" v-for="menuList in menuInventories" 
              :key="menuList.name" @click="navigateTo(menuList.path, menuList.name, 'lists')" :class="{
                'menuitem-active': activeMenu?.category === 'lists' && activeMenu.name === menuList.name,
              }">
              <a class="side-nav-link" :class="{active: activeMenu?.category === 'lists' && activeMenu.name === menuList.name}">
                <i :class="menuList.icon"></i>
                <span>{{ menuList.name }}</span>
              </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <div class="simplebar-track simplebar-vertical" style="visibility: visible">
        <div class="simplebar-scrollbar" style="
            height: 369px;
            display: block;
            transform: translate3d(0px, 0px, 0px);
          "></div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { useRouter } from 'vue-router';
import { useUserStore } from '../../store/user';
import { ref, computed } from 'vue';

const router = useRouter();
const userStore = useUserStore();

const userName = computed(() => userStore.user?.name);
const userRole = computed(() => userStore.user?.role);
const userAccess = computed(() => userStore.user?.permissions || []);

const activeMenu = ref<{category: string; name: string} | null>(null);

const menuSettings = ref([
  {
    name: "Пользователи",
    icon: "ri-tools-line",
    path: "/settings/users"
  },
  {
    name: "Проверка синхронизации",
    icon: "ri-list-check-3",
    path: "/settings/synch"
  }
]);

const menuLists = ref([
  {
    name: "Точки продаж",
    icon: "",
    path: "/lists/retail_stores"
  },
  {
    name: "Премии",
    icon: "",
    path: "/lists/bonuses"
  },
  {
    name: "Назначения платежей",
    icon: "",
    path: "/lists/payment_purposes"
  },
  {
    name: "Оплата за смену",
    icon: "",
    path: "/lists/salary"
  }
]);

const menuTests = computed(() => {
  const baseTests = [];
  if (userRole.value === "admin") {
    baseTests.push({
      name: "Тесты",
      icon: "",
      path:"/tests"
    });
  }

  if (userRole.value === "admin" || userRole.value === "salesman" 
    || userRole.value === "senior_salesman") {
      baseTests.push({
        name: "Результаты тестов",
        icon: "",
        path: "/tests/result"
      });
  }

  if (userRole.value === "salesman") {
    baseTests.push({
      name: "Пройти тест",
      icon: "",
      path: "/tests/start"
    });
  }
  return baseTests;
});

function hasAccess(key: string) {
  return userAccess.value.some(
    (x) => x.title === key && x.mode === "displayed"
  );
}

function hasAccessWrite(key: string) {
  return userAccess.value.some(
    (x) => x.title === key && x.display_name === "editable"
  );
}

const menuReports = computed(() => {
  const baseReports = [];

  if (hasAccess("auditor")) {
    baseReports.push({
      name: "Ревизор",
      icon: "",
      path: "/reports/auditor"
    });
  }
  if (hasAccess("sales_journal")) {
    baseReports.push({
      name: "Журнал продаж",
      icon: "",
      path: "/reports/sales-journal"
    });
  }
  if (hasAccess("cash_journal") || hasAccessWrite("cash_journal")) {
    baseReports.push({
      name: "Журнал платежей",
      icon: "",
      path: "/reports/payment-journal"
    });
  }

  return baseReports;
});

const menuDashboards = ref([
  {
    name: "Точка продаж 1",
    path: "",
    icon: ""
  },
  {
    name: "Точка продаж 2",
    path: "",
    icon: ""
  }
]);

const menuInventories = ref([
  {
    name: "Точка продаж 1",
    path: "",
    icon: ""
  },
  {
    name: "Точка продаж 2",
    path: "",
    icon: ""
  }
]);

const navigateTo = (path: string, menuName: string, category: string) => {
  activeMenu.value = {category, name: menuName};
  router.push(path);
}
</script>