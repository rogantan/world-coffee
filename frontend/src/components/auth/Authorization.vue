<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import InputBox from '../fields/InputBox.vue';
import { useRoute, useRouter } from 'vue-router';
import type { iModelEntity, iModelEntityErrors, iModelOptions } from '../../models/form_data';
import { auth } from "../../api/index"
import { validateModel } from '../../utils/form_utils';
import { useUserStore } from '../../store/user';
const router = useRouter();
const route = useRoute();
const userStore = useUserStore();

const isPerforming = ref(false);
const showPassword = ref(false);
const entity = reactive({
    username: "",
    password: "",
} as iModelEntity
);

const entity_errors = reactive({
    username: "",
    password: ""
} as iModelEntityErrors);

const validateOptions = reactive({
    username: {
        label: "Логин",
        icon: "ri-login-box-line",
        validate: {
            required: true,
        },
    },
    password: {
        label: "Пароль",
        icon: "ri-fingerprint-line",
        validate: {
            required: true
        },
    },
} as iModelOptions);

const togglePasswordVIsibility = () => {
    showPassword.value = !showPassword.value;
};

const handleLogin = async () => {
    try {
        const { status, errors } = await validateModel(validateOptions, entity);
        Object.assign(entity_errors, errors);
        if (!status) return;
        isPerforming.value = true;

        const response = await auth.login(entity.username, entity.password);
        if (response.access_token) {
            localStorage.setItem("token", response.access_token);
            userStore.get().then(() => {
                router.push("/main")
            })
        }
    } catch (error) {
        const errorText = error instanceof Error ? error.message: "Произошла неизвестная ошибка";
        Object.assign(entity_errors,  { username: errorText });
    } finally {
        isPerforming.value = false;
    }
};

onMounted(() => {
    const setLogin = route.query.setLogin as string || "";
    const setPassword = route.query.setPassword as string || "";
    const fireAuth = route.query.fireAuth === "true";   

    entity.username = setLogin as string;
    entity.password = setPassword as string;

    if (fireAuth) {
        handleLogin();
    }
});
</script>

<template>
  <div class="auth-field">
    <div class="auth-fluid-form-box">
      <h4 class="auth-brand">Вход</h4>
      <p class="">Введите логин и пароль</p>

      <form class="auth-field-right" @submit.prevent="handleLogin">
        <div class="">
          <InputBox v-bind="validateOptions.username" :error="entity_errors.username" :modelValue="entity.username"
          @update:modelValue="(value: any) => (entity.username = value)"></InputBox>
        </div>
        <div class="mt-3 m-auto">
          <div class="row">
            <div class="col-10">
              <InputBox :type="showPassword ? 'text' : 'password'" v-bind="validateOptions.password"
              :error="entity_errors.password" :modelValue="entity.password" @update:modelValue="(value: any) => (entity.password = value)" />
            </div>
            <div class="col-2 align-content-end mt-0">
                <button type="button" class="btn btn-primary" @click="togglePasswordVIsibility">
                    <i :class="[!showPassword ? 'ri-eye-close-line' : 'ri-eye-line',]"></i>
                </button>
            </div>
          </div>
        </div>
        <button class="btn mt-5 w-100 btn-success text-whitr" type="submit">Войти</button>
      </form>
    </div>
  </div>
</template>
