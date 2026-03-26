export type Permission = {
    title: string,
    display_name: string,
    mode: string
}

export type User = {
    id: string,
    uid: string,
    name: string,
    role: string,
    archived: boolean,
    permissions: Permission[]
}