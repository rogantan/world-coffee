import type { PaymentJournal } from "../../types/reports/payment_journal";
import { defineStore } from "pinia";
import { reactive, ref } from "vue";
import { payment_journal } from "../../api";
import type { PaymentJournalBody } from "../../api/reports/payment_journal";
import { watch } from "vue";
import { formatOnlyDate } from "../../utils/date_formatter";
import { notificationService } from '../../api/notify';

export const usePaymentJournalStore = defineStore("pjournal", () => {
  const pjournal = reactive<PaymentJournal[]>([]);
  const paymentDates = ref<Date[]>([new Date(2022, 0, 1), new Date()]);
  const accrualDates = ref<Date[]>([new Date(2022, 0, 1), new Date()]);

  const get = async () => {
    const filters: PaymentJournalBody = {
      payment_date_from: formatOnlyDate(paymentDates.value[0]),
      payment_date_to: formatOnlyDate(paymentDates.value[1]),
      accrual_date_from: formatOnlyDate(accrualDates.value[0]),
      accrual_date_to: formatOnlyDate(accrualDates.value[1]),
    };
    try {
      const resposne = await payment_journal.getPaymentJournal(filters);
        pjournal.splice(0)
        console.log(pjournal)
        pjournal.push(...resposne.map((item: any) => ({
          ...item,
          payment_date: new Date(item.payment_date),
          accrual_date: new Date(item.accrual_date),
        })));
    } catch (error) {
      console.log(error);
    }
  };

  const deleteItem = async (id: number) => {
    const response = await payment_journal.deleteSalesJournal(id);
  
    if (response === null) {
      notificationService.addNotification({
        title: 'Запись id',
        message: 'Успешно удалена',
        type: 'success',
      });
      const index = pjournal.findIndex(item => item.id === id);
      pjournal.splice(index, 1);
    }
  }

  const add = () => {
    const newId = -1;
    const newItem = {
      id: newId,
      payment_date: new Date(),
      retail_store_name: "",
      retail_store_id: "",
      amount: 0,
      payment_purpose_name: "",
      payment_purpose_id: "",
      employee_name: "",
      employee_id: "",
      accrual_date: new Date(),
      description: "",
    }
    pjournal.unshift(newItem);
    return newItem

  }

  const clear = () => {
    pjournal.slice(0);
  };

  watch([paymentDates, accrualDates], () => {
    get();
  });

  return {
    pjournal,
    paymentDates,
    accrualDates,
    get,
    add,
    clear,
    deleteItem,
  };
});
