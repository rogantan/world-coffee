// response_formatter.ts

export const processServerData = (serverData: any) => {
    const rows: { columnName: any; columnName_class: any; }[] = [];

    serverData.forEach((store: { employees: any[]; }) => {
      let isFirstRow = true;

      store.employees.forEach(employee => {
        const employeeRow = {
          columnName: employee.employee_name,
          columnName_class: isFirstRow ? 'lemon' : 'yellow',
        };

        // Заполнение данных по каждому месяцу
        employee.data.forEach((monthData: { date_from: string; value: any; dynamics: any; color: any; }) => {
          const dateKey = monthData.date_from.split('.').reverse().slice(0, 2).join('-'); // 'год-месяц'
          const percentKey = `percent_${dateKey}`; 

          employeeRow[dateKey] = monthData.value;
          employeeRow[`${dateKey}_class`] = isFirstRow ? 'lemon': '';
          employeeRow[percentKey] = monthData.dynamics;
          employeeRow[`${percentKey}_class`] = monthData.color;
        });

        rows.push(employeeRow);
        isFirstRow = false;

      });
      rows.push({}); 
    });

    return rows;
  };

export const processServerDataShift = (serverData: any[]) => {
    const rows: { nameEmployee: any; salePoint: any; }[] = [];
    serverData.forEach((store) => {
      store.employees.forEach((employee: { employee_name: any; shifts: any[]; }) => {
        const employeeRow = {
          nameEmployee: employee.employee_name,
          salePoint: store.retail_store_name,
        };

        employee.shifts.forEach(shift => {
          const dateKey = shift.date_from.split('.').reverse().slice(0, 2).join('-');
          employeeRow[dateKey] = shift.shift_count;
        });

        rows.push(employeeRow);
      });
    });

    return rows;
  }

