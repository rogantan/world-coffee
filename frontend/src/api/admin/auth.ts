import { apiService } from "../api";
import type { Token } from "../../types/auth";

export const login = async (username: string, password: string): Promise<Token> => {
    const data = new URLSearchParams();
    data.append('username', username);
    data.append('password', password);
    return await apiService.post<Token>('/auth/token', data);
};

export const logout = async (): Promise<null> =>
    await apiService.get<null>('/auth/logout');