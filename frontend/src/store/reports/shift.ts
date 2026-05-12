import { shift } from "../../api";
import { format } from 'date-fns';
import { defineStore } from "pinia";
import { reactive, ref } from "vue";

export const useShiftStore = defineStore("shift", () => {
  const data = ref<any[]>([]);
  const dates = reactive<[Date, Date]>([new Date(2026, 0, 1), new Date()]);

  const get = async (by: "day" | "month" = "day") => {
    const [date_from, date_to] = [
      format(dates[0], "yyyy-MM-dd"),
      format(dates[1], "yyyy-MM-dd")
    ];
    try {
      const response = await shift.getShifts(date_from, date_to, by);
      if (response.length) {
        data.value = processServerData(response, by);
      }
    } catch (error) {
      console.log(error);
    }
  };

  const processServerData = (serverData: any[], by: string) => {
    const rows: { nameEmployee: any; salePoint: any; }[] = [];

    serverData.forEach((store) => {
      store.employees.forEach((employee: { employee_name: any; shifts: any[]; }) => {
        const employeeRow = {
          nameEmployee: employee.employee_name,
          salePoint: store.retail_store_name,
        };

        employee.shifts.forEach((shift) => {
          let dateKey: string;
          if (by === "day") {
            dateKey = shift.date.split(".").reverse().join("-");
          } else {
            dateKey = shift.date_from
              .split(".")
              .reverse()
              .slice(0, 2)
              .join("-");
          }
          employeeRow[dateKey] = shift.shift_count;
        });

        rows.push(employeeRow);
      });
    });

    return rows;
  };

  return {
    dates,
    data,
    get
  }
})