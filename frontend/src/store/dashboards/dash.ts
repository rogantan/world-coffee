import { ref, watch } from "vue";
import type { DashboardFilter, tDashboardData } from "../../types/dashboards/dashboard";
import { defineStore } from "pinia";
import { useRoute } from "vue-router";
import { formatOnlyDate } from "../../utils/date_formatter";
import { dashboard } from "../../api";

export const useDashboardStore = defineStore('dashboard', () => {
  const dashboardData = ref<tDashboardData>();
  const dates = ref<Date[]>([new Date(new Date().getFullYear(), new Date().getMonth(), 1), new Date()]);
  const route = useRoute();
  const urls = ["1", "2"]

  const get = async () => {
    const filters: DashboardFilter = {
      report_name: route.meta.back_url as string,
      month_start: formatOnlyDate(dates.value[0])
    };
    try {
      dashboardData.value = await dashboard.getDashboard(filters)
    } catch (error) {
      console.log(error)
    }
  }

  watch(
    () => route.path,
    (newPath, oldPath) => {
      console.log(newPath.split("/")[2])
      console.log(urls)
      if (newPath !== oldPath && urls.includes(newPath.split("/")[2])) {
        document.title = route.meta.back_url as string;
        get();
      }
    },
  );

  watch(dates, () => {
    get();
  })

  return {
    dashboardData,
    dates,
    get
  }
})