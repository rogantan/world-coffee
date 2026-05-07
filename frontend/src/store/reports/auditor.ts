import { watch, ref } from "vue";
import type { tReports, ReportFilter } from "../../types/reports/sales_journal";
import { defineStore } from "pinia";
import { auditor } from "../../api";
import { formatOnlyDate } from "../../utils/date_formatter";

export const useAuditorStore = defineStore("auditor", () => {
  const report = ref<tReports[]>([]);
  const dates = ref([
    new Date(new Date().getFullYear(), new Date().getMonth(), 1),
    new Date(),
  ]);
  const sortKey = ref("date");
  const sortAsk = ref<string>("asc");

  const get = async () => {
    const filter: ReportFilter = {
      report_name: "auditor",
      date_from: formatOnlyDate(dates.value[0]),
      date_to: formatOnlyDate(dates.value[1]),
      order_by: sortKey.value,
      desc: sortAsk.value === "desc" ? false : true,
    };
    try {
      const resposne = await auditor.getAuditor(filter);
      if (resposne) {
        report.value.slice(0);
        report.value = [...resposne];
      }
    } catch (error) {
      console.log(error);
    }
  };

  const handleSort = (newKey: string) => {
    console.log(newKey);
    const parts = newKey.split("-");
    sortAsk.value = parts[1];
    sortKey.value = parts[0];
    get();
  };


  watch(dates, () => {
    get();
  });

  return {
    report,
    // reportName,
    dates,
    sortKey,
    sortAsk,
    get,
    handleSort,
  };
});
