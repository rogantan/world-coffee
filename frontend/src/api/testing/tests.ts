// tests.ts
import { apiService } from "../api";
import type { tTestResult } from "../../types/testing/user";
import type { Test } from "../../types/testing/tests";

interface Tests {
  name: string;
  questions: Question[];
}

interface Choice {
  id: number;
  text: string;
}

interface Question {
  id: number;
  text: string;
  multiple_answer: boolean;
  choices: Choice[];
}

export const getTests = async (): Promise<tTestResult[]> =>
  await apiService.get<tTestResult[]>("/test/user/list");

export const createTest = async (data: any) =>
  await apiService.post("/test/admin/create", data);

export const getTest = async (test_id: any): Promise<Test> =>
  await apiService.get<Test>(`/test/admin/${test_id}`);

export const getStartedTest = async (test_id: number) =>
  await apiService.get(`/test/admin/${test_id}`, { test_id: test_id });

export const editTest = async (test_id: any, test_data: any): Promise<null> =>
  await apiService.put<null>(`/test/admin/${test_id}/edit`, test_data);

export const deleteTest = async (test_id: number) =>
  await apiService.delete(`/test/admin/${test_id}`);

export const startTest = async (test_id: number): Promise<Tests> =>
  await apiService.get(`/test/passing/${test_id}/starting`);

export const finishTest = async (test_id: number, answers: any) =>
  await apiService.put(`/test/passing/${test_id}/finishing`, answers);

export const getTestsDateResult = async (params: any) =>
  await apiService.get(
    `/test/user/result?date_from=${params.date_from}&date_to=${params.date_to}&order_by=rank&desc=false`
  );

export const getResult = async (test_id: number) =>
  await apiService.get(`/test/passing/${test_id}/result`);

export const getResultByUser = async (test_id: number, user_id: string) =>
  await apiService.get(`/test/admin/${test_id}/result/${user_id}`);

export const getResultByMonth = async (date: string, user_id: string): Promise<any[]> =>
  await apiService.get<any[]>(`test/admin/tests_in_month?date=${date}&user_id=${user_id}`);

