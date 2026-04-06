import {AxiosError} from "axios";

export type iQuery = Record<string, string | number | boolean | undefined>

export interface Meta {
    count: number
    limit: number
    skip: number
}

export interface ListView<T> {
    rows: Array<T>
    meta: Meta
}

export interface iAxiosError extends AxiosError {
    status: number
    detail: string
}
