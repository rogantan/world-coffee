export type Permission = {
    title: string,
    display_name: string,
    mode: string
}

export type User = {
    id: string,
    uid: string,
    name: string,
    email: string,
    role: string,
    archived?: boolean,
    salary_increase: { value: number },
    permissions: Permission[]
}