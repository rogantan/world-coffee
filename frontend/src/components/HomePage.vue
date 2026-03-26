<template>
  <div class="card mt-3 p-2">
    <div>Домашняя страница <br>
      Добро пожаловать, {{ userStore?.user?.name }}
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted } from 'vue';
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