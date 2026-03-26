import { watch, ref } from "vue";
import type { User } from "../types/admin/user";
import { defineStore } from 'pinia';
import { ApiUser } from "../api";

export const useUserStore = defineStore('user', () => {
    const user = ref<User>()
    const isOpenMenu = ref(true)

    const get = async (): Promise<User> => {
        if (user.value) return user.value
        try {
            const response = await ApiUser.getUserInfo()
            if (response) {
                user.value = response
                return response
            }
            throw Error("No user data");
        } catch (error) {
            console.log(error)
            throw Error("No user data");
        }
    }

    const toogleMenu = () => {
        isOpenMenu.value = !isOpenMenu.value
    }

    const clear = () => {
        user.value = undefined
    }

    watch(isOpenMenu, (newVal) => {
        document.documentElement.setAttribute("data-sidenav-size", newVal ? "fullscreen": "default");

    });

    return {
        user, 
        isOpenMenu,
        toogleMenu,
        get,
        clear
    }
})