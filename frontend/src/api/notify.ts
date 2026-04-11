// notificationService.ts
import { reactive, readonly } from 'vue';

interface Notification {
  title: string;
  message: string;
  type: 'success' | 'error' | 'warning';
}

class NotificationService {
  private notifications = reactive<Notification[]>([]);

  public addNotification(notification: Notification) {
    this.notifications.push(notification);
    setTimeout(() => this.notifications.shift(), 15000); 
  }

  public removeNotification(index: number) {
    this.notifications.splice(index, 1); // Удаление уведомления по индексу
  }


  public getNotifications() {
    return readonly(this.notifications); // Возвращает реактивное состояние
  }
}

export const notificationService = new NotificationService();
