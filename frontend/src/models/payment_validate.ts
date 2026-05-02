// payment_validate.ts

export interface Payment {
    payment_date?: string;
    retail_store_name?: string;
    amount?: number;
    payment_purpose_name?: string;
    user_id?: string;
    accrual_date?: string;
    description?: string;
}

export interface PaymentErrors {
    payment_date?: string;
    retail_store_id?: string;
    amount?: string;
    payment_purpose_id?: string;
    user_id?: string;
    accrual_date?: string;
    description?: string;
}