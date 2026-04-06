// table.ts
// table.ts
import type { ListView } from "../models/api";

export interface iTable<Type> {
    isLoading?: boolean
    isErrored?: boolean
    footer_show?: boolean
    empty_text?: string
    pagination_mode?: 'router' | 'emit'
    context?: object
    headers: iTableHeaders | iTableHeader[]
    data: ListView<Type> | null
}

export type iTableHeaders = Record<string, iTableHeader>

export interface iTableHeader {
    title?: string | number | null
    sort?: boolean
    
    rowspan?: number
    colspan?: number
    key?: string
    
    sortKeys?: {
        asc: string
        desc: string
    }
    classList?: string[] | string
    style?: Record<string, string | number>
    headers?: (iTableHeaders | iTableHeader[])
}

export interface RowData {
    id?: number;
    link?: string;
    [key: string]: any;
}