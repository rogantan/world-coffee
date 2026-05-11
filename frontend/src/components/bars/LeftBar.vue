<template>
  <div class="leftside-menu menuitem-active">
    <div class="h-100 show" id="leftside-menu-container" data-simplebar="init">
      <div class="simplebar-wrapper">
        <div class="simplebar-offset">
          <div class="simplebar-content-wrapper" role="region" aria-label="scrollable content">
            <div class="simplebar-content">
              <div class="leftbar-user p-3 text-white">
                <a class="d-flex alogn-items-center text-reset">
                  <div class="flex-grow-1 ms-2">
                    <span class="fw-bold fs-5 text-secondary side-nav-title">{{ userName }}</span>
                  </div>
                </a>
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

              <li class="side-nav-title" v-if="userRole === 'admin' || userRole === 'salesman' || userRole === 'senior_salesman' || 
              userRole === 'accountant'">Тестирование</li>
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

              <li class="side-nav-title" v-if="menuInventories.length > 0">Инвентаризации</li>
              <li class="side-nav-item" v-for="menuList in menuInventories" v-if="userRole === 'admin' || userRole === 'salesman' || userRole === 'auditor'"
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
    icon: "ri-store-line",
    path: "/lists/retail_stores"
  },
  {
    name: "Премии",
    icon: "ri-gift-fill",
    path: "/lists/bonuses"
  },
  {
    name: "Назначения платежей",
    icon: "ri-money-euro-box-line",
    path: "/lists/payment_purposes"
  }
]);

const menuTests = computed(() => {
  const baseTests = [];
  if (userRole.value === "admin" || userRole.value === 'salesman' || userRole.value === 'senior_salesman' ) {
    baseTests.push({
      name: "Тесты",
      icon: "ri-a-b",
      path:"/tests"
    });
  }
  if (userRole.value === "admin" || userRole.value === 'salesman' || userRole.value === 'senior_salesman' || userRole.value === 'accountant' ) {
    baseTests.push({
      name: "Результаты тестов",
      icon: "ri-equal-fill",
      path: "/tests/result"
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
    (x) => x.title === key && x.mode === "editable"
  );
}

const menuReports = computed(() => {
  const baseReports = [];

  if (hasAccess("auditor")) {
    baseReports.push({
      name: "Ревизор",
      icon: "ri-chat-check-line",
      path: "/reports/auditor"
    });
  }
  if (hasAccess("sales_journal")) {
    baseReports.push({
      name: "Журнал продаж",
      icon: "ri-discount-percent-line",
      path: "/reports/sales-journal"
    });
  }
  if (hasAccess("payment_journal") || hasAccessWrite("payment_journal")) {
    baseReports.push({
      name: "Журнал платежей",
      icon: "ri-wallet-line",
      path: "/reports/payment-journal"
    });
  }
  if (hasAccess("revenue_month")) {
    baseReports.push({
      name: "Выручка в месяц",
      icon: "ri-price-tag-3-line",
      path: "/reports/revenue-month"
    });
  }
  if (hasAccess("shift_day")) {
    baseReports.push({
      name: "Подсчёт смен (день)",
      icon: "ri-user-line",
      path: "/reports/shift-day"
    });
  }
  if (hasAccess("shift_month")) {
    baseReports.push({
      name: "Подсчёт смен (месяц)",
      icon: "ri-user-fill",
      path: "/reports/shift-month"
    })
  }
  return baseReports;
});

const menuDashboards = computed(() => {
  const baseDashboards = [];
  if (hasAccess("coffee_point")) {
    baseDashboards.push({
      name: "Coffee Point",
      path: "/dashboard/1",
      icon: "ri-dashboard-3-line"
    });
  }
  if (hasAccess("coffee_enjoy")) {
    baseDashboards.push({
      name: "Coffee Enjoy",
      path: "/dashboard/2",
      icon: "ri-dashboard-3-line"
    })
  }
  return baseDashboards;

});

const menuInventories = computed(() => {
  const baseInventories = [];
  if (userRole.value === "admin" || userRole.value === "auditor" || (userRole.value === "salesman" && hasAccess("coffee_point"))) {
    baseInventories.push({
      name: "Coffee Point",
      path: "/inventory/1",
      icon: "ri-file-list-2-line"
    });
  }
  if (userRole.value === "admin" || userRole.value === "auditor" || (userRole.value === "salesman" && hasAccess("coffee_enjoy"))) {
    baseInventories.push({
      name: "Coffee Enjoy",
      path: "/inventory/2",
      icon: "ri-file-list-2-line"
    });
  }

  return baseInventories;
})

const navigateTo = (path: string, menuName: string, category: string) => {
  activeMenu.value = {category, name: menuName};
  router.push(path);
}
</script>