import type { tReports } from "../../types/reports/sales_journal";
import { defineStore } from "pinia";
import { ref } from "vue";
import { sales_journal } from "../../api/index";
import type { ReportFilter } from "../../types/reports/filter";
import { watch } from "vue";
import { formatOnlyDate } from '../../utils/date_formatter';

export const useSalesJournalStore = defineStore("sjournal", () => {
  const sjournal = ref<tReports[]>([]);
  const single = ref<boolean>(false);
  const date = ref<Date>(new Date());
  const dates = ref<Date[]>([new Date(), new Date()]);

  const get = async () => {
    const filters: ReportFilter = {
      report_name: "sales_journal",
      date_from: formatOnlyDate(dates.value[0]),
      date_to: formatOnlyDate(dates.value[1]) || formatOnlyDate(dates.value[0]),
      order_by: "moment",
      desc: false,
    };

    try {
      const resposne = await sales_journal.getReportWithDate(filters);
      if (resposne) {
        sjournal.value = resposne;
      }
    } catch (error) {
      console.log(error);
    }
  };

  watch(dates, () => {
    console.log(dates.value);
    get();
  });

  return {
    sjournal,
    single,
    date,
    dates,
    get
  };
});
