<template>
  <div class="moda" v-if="notifications.length">
    <div v-for="(notification, index) in notifications" 
      :key="index" 
      class="alert" 
      :class="{'alert-success': notification.type === 'success', 'alert-danger': notification.type === 'error'}">
      <h5>{{ notification.title }}</h5>
      <p>{{ notification.message }}</p>
      <button class="close-btn" @click="removeNotification(index)">X</button>
    </div>
  </div>
</template>

<script lang="ts">
import { notificationService } from '../../api/notify'; // Убедитесь, что путь корректен

export default {
  name: 'Notify',
  setup() {
    const notifications = notificationService.getNotifications();

    const removeNotification = (index: number) => {
      notificationService.removeNotification(index); // Предполагается, что такой метод существует
    };

    return {
      notifications,
      removeNotification,
    };
  },
};
</script>

<style scoped>
.moda {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 2000;
}

.notification-style {
  margin: 0 0 10px;
  padding: 10px;
  border-radius: 5px;
  color: #000000;
}

.success {
  background-color: #d4edda;
}

.error {
  background-color: #f8d7da;
}

.close-btn {
  position: absolute;
  top: 0;
  right: 0;
  border: none;
  background: none;
  color: inherit;
  font-size: 20px;
  cursor: pointer;
}
</style>
