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

              <li class="side-nav-title" v-if="userRole === 'admin'">Отчёты</li>
              <li class="side-nav-item" v-if="userRole === 'admin'" v-for="menuList in menuReports" 
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

const menuTests = ref([
  {
    name: "Прохождение",
    icon: "",
    path: ""
  }
]);

const menuReports = ref([
  {
    name: "",
    path: "",
    icon: ""
  }
])

const navigateTo = (path: string, menuName: string, category: string) => {
  activeMenu.value = {category, name: menuName};
  router.push(path);
}
</script>