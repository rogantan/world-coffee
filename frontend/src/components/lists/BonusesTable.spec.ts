// src/components/lists/BonusesTable.spec.ts
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { mount, flushPromises } from '@vue/test-utils';
import { setActivePinia, createPinia } from 'pinia';
import BonusesTable from './Bonuses.vue';
import { getBonuses, postBonuses, putBonuses } from '../../api/admin/listst';
import { notificationService } from '../../api/notify';

// Моки API
vi.mock('../../api/admin/listst', () => ({
  getBonuses: vi.fn(),
  postBonuses: vi.fn(),
  putBonuses: vi.fn(),
}));

vi.mock('../../api/notify', () => ({
  notificationService: {
    addNotification: vi.fn(),
  },
}));

vi.mock('vue-router', () => ({
  useRoute: () => ({
    meta: {
      name: 'Премии',
    },
  }),
}));

describe('BonusesTable', () => {
  let wrapper: any;

  const mockBonuses = [
    {
      id: 1,
      name: 'Премия А',
      value: 1000,
    },
    {
      id: 2,
      name: 'Премия Б',
      value: 2000,
    },
  ];

  beforeEach(() => {
    vi.clearAllMocks();
    setActivePinia(createPinia());
    
    (getBonuses as any).mockResolvedValue(mockBonuses);
    (postBonuses as any).mockResolvedValue({});
    (putBonuses as any).mockResolvedValue({});
  });

  afterEach(() => {
    if (wrapper) wrapper.unmount();
  });

  describe('Загрузка данных', () => {
    it('getData загружает данные из API', async () => {
      wrapper = mount(BonusesTable);
      
      await wrapper.vm.getData();
      await flushPromises();
      
      expect(getBonuses).toHaveBeenCalled();
      expect(wrapper.vm.data).toHaveLength(2);
      expect(wrapper.vm.data[0].name).toBe('Премия А');
      expect(wrapper.vm.data[0].value).toBe(1000);
      expect(wrapper.vm.data[0].isNewBonus).toBe(false);
      expect(wrapper.vm.data[0].isEditingBonus).toBe(false);
    });
  });

  describe('Добавление премии', () => {
    beforeEach(() => {
      wrapper = mount(BonusesTable);
      wrapper.vm.data = [];
    });

    it('addBonus не добавляет строку, если уже есть незавершенное добавление', () => {
      wrapper.vm.data = [{ isNewBonus: true, name: '', value: 0 }];
      
      wrapper.vm.addBonus();
      
      expect(wrapper.vm.data).toHaveLength(1);
      expect(notificationService.addNotification).toHaveBeenCalledWith({
        title: 'Внимание',
        message: "Сначала сохраните или отмените текущее добавление",
        type: 'warning'
      });
    });
  });

  describe('Отмена добавления', () => {
    it('cancelNewBonus удаляет новую строку', () => {
      wrapper = mount(BonusesTable);
      wrapper.vm.data = [{ id: 123, name: '', value: 0, isNewBonus: true }];
      
      const row = wrapper.vm.data[0];
      wrapper.vm.cancelNewBonus(row);
      
      expect(wrapper.vm.data).toHaveLength(0);
    });
  });

  describe('Сохранение новой премии', () => {
    beforeEach(() => {
      wrapper = mount(BonusesTable);
      wrapper.vm.data = [];
    });

    it('saveRecordBonus показывает ошибку, если поля не заполнены', async () => {
      const row = { name: '', value: 0, isNewBonus: true };
      
      await wrapper.vm.saveRecordBonus(row);
      await flushPromises();
      
      expect(notificationService.addNotification).toHaveBeenCalledWith({
        title: 'Ошибка',
        message: "Не все поля заполнены",
        type: 'error'
      });
      expect(postBonuses).not.toHaveBeenCalled();
    });

    it('saveRecordBonus показывает ошибку, если name пустой', async () => {
      const row = { name: '   ', value: 1000, isNewBonus: true };
      
      await wrapper.vm.saveRecordBonus(row);
      await flushPromises();
      
      expect(notificationService.addNotification).toHaveBeenCalledWith({
        title: 'Ошибка',
        message: "Не все поля заполнены",
        type: 'error'
      });
      expect(postBonuses).not.toHaveBeenCalled();
    });

    it('saveRecordBonus успешно сохраняет новую премию', async () => {
      const row = { name: 'Новая премия', value: 5000, isNewBonus: true };
      
      await wrapper.vm.saveRecordBonus(row);
      await flushPromises();
      
      expect(postBonuses).toHaveBeenCalledWith('Новая премия', 5000);
      expect(row.isNewBonus).toBe(false);
      expect(notificationService.addNotification).toHaveBeenCalledWith({
        title: 'Успех',
        message: "Премия успешно создана",
        type: 'success'
      });
    });

    it('saveRecordBonus обрабатывает ошибку API', async () => {
      (postBonuses as any).mockRejectedValue(new Error('API Error'));
      const row = { name: 'Новая премия', value: 5000, isNewBonus: true };
      
      await wrapper.vm.saveRecordBonus(row);
      await flushPromises();
      
      expect(notificationService.addNotification).toHaveBeenCalledWith({
        title: "Ошибка",
        message: "Не удалось создать премию",
        type: 'error'
      });
    });
  });

  describe('Редактирование премии', () => {
    beforeEach(() => {
      wrapper = mount(BonusesTable);
    });

    it('startEditRecordBonus переводит строку в режим редактирования', () => {
      const row = { 
        id: 1, 
        name: 'Премия А', 
        value: 1000, 
        isEditingBonus: false 
      };
      
      wrapper.vm.startEditRecordBonus(row);
      
      expect(row.isEditingBonus).toBe(true);
      expect(row.name).toBe('Премия А');
      expect(row.value).toBe(1000);
    });

    it('cancelEditRecordBonus отменяет редактирование и восстанавливает данные', () => {
      const row = { 
        id: 1, 
        name: 'Измененное имя', 
        value: 5000, 
        originalName: 'Премия А', 
        originalValue: 1000,
        isEditingBonus: true 
      };
      
      wrapper.vm.cancelEditRecordBonus(row);
      
      expect(row.name).toBe('Премия А');
      expect(row.value).toBe(1000);
      expect(row.isEditingBonus).toBe(false);
      expect(row.originalName).toBeUndefined();
      expect(row.originalValue).toBeUndefined();
    });

    it('editRecordBonus показывает ошибку, если поля пустые', async () => {
      const row = { id: 1, name: '', value: 0, isEditingBonus: true };
      
      await wrapper.vm.editRecordBonus(row);
      await flushPromises();
      
      expect(notificationService.addNotification).toHaveBeenCalledWith({
        title: 'Ошибка',
        message: "Данные не могут быть пустыми",
        type: 'error'
      });
      expect(putBonuses).not.toHaveBeenCalled();
    });

    it('editRecordBonus успешно обновляет премию', async () => {
      const row = { 
        id: 1, 
        name: 'Обновленная премия', 
        value: 3000, 
        isEditingBonus: true,
        originalName: 'Старая премия',
        originalValue: 1000
      };
      
      await wrapper.vm.editRecordBonus(row);
      await flushPromises();
      
      expect(putBonuses).toHaveBeenCalledWith(1, 'Обновленная премия', 3000);
      expect(row.isEditingBonus).toBe(false);
      expect(row.originalName).toBeUndefined();
      expect(row.originalValue).toBeUndefined();
      expect(notificationService.addNotification).toHaveBeenCalledWith({
        title: 'Успех',
        message: "Премия успешно обновлена",
        type: 'success'
      });
    });

    it('editRecordBonus обрабатывает ошибку API', async () => {
      (putBonuses as any).mockRejectedValue(new Error('API Error'));
      const row = { 
        id: 1, 
        name: 'Обновленная премия', 
        value: 3000, 
        isEditingBonus: true 
      };
      
      await wrapper.vm.editRecordBonus(row);
      await flushPromises();
      
      expect(notificationService.addNotification).toHaveBeenCalledWith({
        title: "Ошибка",
        message: "Не удалось обновить премию",
        type: 'error'
      });
    });
  });

  describe('Жизненный цикл', () => {
    it('устанавливает document.title при монтировании', async () => {
      wrapper = mount(BonusesTable);
      
      expect(document.title).toBe('Премии');
    });
  });
});