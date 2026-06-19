// src/components/inventory/InventoryTable.spec.ts
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { mount, flushPromises } from '@vue/test-utils';
import { setActivePinia, createPinia } from 'pinia';
import InventoryTable from './InventoryPage.vue';
import { useUserStore } from '../../store/user';
import { useInventoryStore } from '../../store/inventory/inventory';
import { inventory } from '../../api';
import { notificationService } from '../../api/notify';

// Моки API
vi.mock('../../api', () => ({
  inventory: {
    putInventoryByShop: vi.fn(),
    unloadInventoryByShop: vi.fn(),
    clearItems: vi.fn(),
  },
}));

vi.mock('../../api/notify', () => ({
  notificationService: {
    addNotification: vi.fn(),
  },
}));

vi.mock('vue-router', () => ({
  useRoute: () => ({
    meta: {
      name: 'Инвентаризация',
      back_url: '/shop/123',
    },
  }),
}));

describe('InventoryTable', () => {
  let wrapper: any;
  let userStore: any;
  let inventoryStore: any;

  const mockInventories = [
    {
      id: 1,
      product_name: 'Товар А',
      price: 100,
      actual_balance: 10,
      sales: 2,
      closing_balance: 8,
    },
    {
      id: 2,
      product_name: 'Товар Б',
      price: 200,
      actual_balance: 5,
      sales: 1,
      closing_balance: 4,
    },
  ];

  beforeEach(() => {
    vi.clearAllMocks();
    vi.useFakeTimers();
    
    setActivePinia(createPinia());
    userStore = useUserStore();
    inventoryStore = useInventoryStore();
    inventoryStore.inventories = mockInventories;
    inventoryStore.get = vi.fn().mockResolvedValue(mockInventories);
    
    (inventory.putInventoryByShop as any).mockResolvedValue({ closing_balance: 9 });
    (inventory.unloadInventoryByShop as any).mockResolvedValue(undefined);
    (inventory.clearItems as any).mockResolvedValue(undefined);
  });

  afterEach(() => {
    vi.useRealTimers();
    if (wrapper) wrapper.unmount();
  });

  describe('Сохранение данных', () => {
    beforeEach(() => {
      userStore.user = { role: 'admin' };
      wrapper = mount(InventoryTable);
    });

    it('saveRow вызывает API с правильными параметрами', async () => {
      const row = { ...mockInventories[0] };
      
      await wrapper.vm.saveRow(row);
      await flushPromises();
      
      expect(inventory.putInventoryByShop).toHaveBeenCalledWith(
        '/shop/123',
        row.id,
        row
      );
    });

    it('saveRow обновляет closing_balance из ответа API', async () => {
      const mockResponse = { closing_balance: 15 };
      (inventory.putInventoryByShop as any).mockResolvedValue(mockResponse);
      
      const row = { ...mockInventories[0] };
      await wrapper.vm.saveRow(row);
      await flushPromises();
      
      expect(row.closing_balance).toBe(15);
    });

    it('saveRow показывает уведомление об успехе', async () => {
      const row = { ...mockInventories[0] };
      
      await wrapper.vm.saveRow(row);
      await flushPromises();
      
      expect(notificationService.addNotification).toHaveBeenCalledWith({
        title: "Успех",
        message: "Данные изменены",
        type: 'success'
      });
    });

    it('saveRow нормализует пустые значения в 0', async () => {
      const row = {
        ...mockInventories[0],
        actual_balance: '',
        sales: '',
      };
      
      await wrapper.vm.saveRow(row);
      
      expect(inventory.putInventoryByShop).toHaveBeenCalledWith(
        expect.any(String),
        expect.any(Number),
        expect.objectContaining({
          actual_balance: 0,
          sales: 0,
        })
      );
    });

    it('saveRow обрабатывает ошибку 400', async () => {
      const error = {
        response: {
          status: 400,
          data: { detail: 'Ошибка валидации' },
        },
      };
      (inventory.putInventoryByShop as any).mockRejectedValue(error);
      
      const row = mockInventories[0];
      await wrapper.vm.saveRow(row);
      await flushPromises();
      
      expect(notificationService.addNotification).toHaveBeenCalledWith({
        title: `Ошибка в поле ${row.product_name}`,
        message: 'Ошибка валидации',
        type: 'error'
      });
    });
  });

  describe('Диалог подтверждения', () => {
    beforeEach(() => {
      userStore.user = { role: 'admin' };
      wrapper = mount(InventoryTable);
    });

    it('showConfirmDialog изначально false', () => {
      expect(wrapper.vm.showConfirmDialog).toBe(false);
    });
  });

  describe('Очистка данных', () => {
    beforeEach(() => {
      userStore.user = { role: 'admin' };
      wrapper = mount(InventoryTable);
    });

    it('clearForm вызывает API очистки', async () => {
      await wrapper.vm.clearForm();
      await flushPromises();
      
      expect(inventory.clearItems).toHaveBeenCalledWith('/shop/123');
    });

    it('clearForm закрывает диалог', async () => {
      wrapper.vm.showConfirmDialog = true;
      await wrapper.vm.clearForm();
      
      expect(wrapper.vm.showConfirmDialog).toBe(false);
    });

    it('clearForm показывает уведомление об успехе', async () => {
      await wrapper.vm.clearForm();
      await flushPromises();
      
      expect(notificationService.addNotification).toHaveBeenCalledWith({
        title: "Успех",
        message: "Данные очищены",
        type: 'success'
      });
    });
  });

  describe('Синхронизация с МойСклад', () => {
    beforeEach(() => {
      userStore.user = { role: 'admin' };
      wrapper = mount(InventoryTable);
    });

    it('syncWithMS вызывает API выгрузки', async () => {
      await wrapper.vm.syncWithMS();
      await flushPromises();
      
      expect(inventory.unloadInventoryByShop).toHaveBeenCalledWith('/shop/123');
    });

    it('syncWithMS показывает уведомление об успехе', async () => {
      await wrapper.vm.syncWithMS();
      await flushPromises();
      
      expect(notificationService.addNotification).toHaveBeenCalledWith({
        title: "Успех",
        message: "Инвентаризация выгружена в МойСклад",
        type: 'success'
      });
    });
  });

  describe('Жизненный цикл', () => {
    it('устанавливает document.title при монтировании', async () => {
      userStore.user = { role: 'admin' };
      wrapper = mount(InventoryTable);
      
      expect(document.title).toBe('Инвентаризация');
    });
  });
});