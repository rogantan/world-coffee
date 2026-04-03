<template>
  <div class="card mt-3 p-2">
    <div class="container">
      <h2>Доступ к информации запрещён</h2>
      <div class="container custom-container">
        <button class="btn btn-primary m-2" @click="goHome">На главную</button>
        <button class="btn btn-danger" @click="goLogin">Вход</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { useRouter } from 'vue-router';
import { useUserStore } from '../../store/user';

const router = useRouter();
const userStore = useUserStore();

const goLogin = () => {
  localStorage.removeItem('token');
  router.push("/signin");
  userStore.clear();
}

const goHome = () => {
  router.push("/main");
}
</script>