import { apiService } from "../api";
import type { User } from "../../types/admin/user";

export const getUserInfo = async (): Promise<User> => 
    await apiService.get<User>('/user/me');

export const getAllUsers = async (): Promise<User[]> => 
    await apiService.get<User[]>("/user/list?archived=false");

export const resetUserPassword = async (user_id: string): Promise<null> => 
    await apiService.post<null>(`/user/${user_id}/reset_password`);

export const changeUserRole = async (user_id: string, new_role: string): Promise<null> => 
    await apiService.put<null>(`/user/${user_id}/role`, {"role": new_role});