import { apiService } from '../api';
import type { tTestResult, tBestEmployee } from '../../types/testing/user'

export const getTestsResult = async (date_from: string, date_to: string): Promise<tTestResult[]> =>
  await apiService.get<tTestResult[]>(`/test/user/results?date_from=${date_from}&date_to=${date_to}&desc=false`);

export const getFilteredTestsResult = async (
  date_from: string,
  date_to: string,
  order_date: string,
  order_by: string,
  desc: boolean
): Promise<tTestResult[]> =>
  await apiService.get<tTestResult[]>(`/test/user/results?date_from=${date_from}&date_to=${date_to}&order_date=${order_date}&order_by=${order_by}&desc=${desc}`);

export const getBestEmployeeResult = async (date_from: string, date_to: string): Promise<tBestEmployee[]> =>
  await apiService.get<tBestEmployee[]>(`/test/user/best_employee?date_from=${date_from}&date_to=${date_to}`);

export const getFilteredBestEmployeeResult = async (
  date_from: string,
  date_to: string,
  order_date: string,
  order_by: string,
  desc: boolean
): Promise<tBestEmployee[]> => {
  if (order_date) {
    return await apiService.get<tBestEmployee[]>(`/tests/best_employee?date_from=${date_from}&date_to=${date_to}&date_order_by=${order_date}&order_by=${order_by}&desc=${desc}`);
  } else {
    return await apiService.get<tBestEmployee[]>(`/tests/best_employee?date_from=${date_from}&date_to=${date_to}&order_by=${order_by}&desc=${desc}`);
  }
}

export const getResult = async (test_id: number) =>
  await apiService.get(`/test/user/${test_id}`);