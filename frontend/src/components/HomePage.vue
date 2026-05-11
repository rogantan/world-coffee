<template>
  <div class="card mt-3 p-2">
    <div>
      <h2>Главная страница</h2>
      <p>Добро пожаловать, {{ userStore.user?.name }}!</p>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { useUserStore } from '../store/user';

const userStore = useUserStore();
// export default {
//     name: "HomePage",
//     components: {},
//     setup() {
//       

//       onMounted(() => {

//       })
//        return {
//         user:userStore.user
//       }
//     }
// }
</script>