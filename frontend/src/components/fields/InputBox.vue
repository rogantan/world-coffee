<template>
    <label v-if="label" class="form-label" @click="$emit('click', $event)">
        <div v-if="label">
            <i :class="['p-2', `${icon}`]" v-if="icon"></i>
            <span>{{ label }}</span>
        </div>
    </label>
    <div class="login">
        <input
        class="form-control"
        ref="input"
        :step="step"
        :name="name"
        :placeholder="placeholder"
        v-model="valueSetter"
        :type="type"
        :disabled="disabled || silentDisabled"
        :readonly="readonly"
        @focus="$emit('focus')"
        @blur="$emit('blur')"
        @keydown.enter="$emit('keydown:enter', $event)"
        >
    </div>
    <button
    type="button"
    class="ui-field-under-button"
    v-if="underButtonText"
    @click="$emit('underButtonClick')"
    >{{ underButtonText }}</button>
    <div v-show="error" class="alert alert-danger" role="alert">{{ error }}</div>
</template>


<script lang="ts">
import type { PropType } from 'vue';

export default {
    name: "InputBox",
    components: {},
    inheritAttrs: false,
    props: {
        label: {
            type: String,
        },
        step: {
            type: [Number, String],
            default: null,
        },
        name: {
            type: String,
            default: "",
        },
        error: {
            type: String,
        },
        placeholder: {
            type: String,
            default: undefined,
        },
        disabled: {
            type: Boolean,
            default: false,
            },
            silentDisabled: {
            type: Boolean,
            default: false,
            },
            readonly: {
            type: Boolean,
            default: false,
            },
            color: {
            type: String,
            default: "grey",
            validator: (value) => ["white", "grey"].some((r) => r === value),
            },
            modelValue: {
            required: true,
            type: [String, Number] as PropType<string | number>,
            },
            icon: {
            type: String,
            default: undefined,
            },
            text_icon: {},
            type: {
            type: String,
            default: "text",
            validator: (value) =>
                ["text", "number", "password"].some((r) => r === value),
            },
            locale: {
            type: Boolean,
            default: false,
            },
            underButtonText: {
            type: String,
            },
            actions: {
            type: Array as PropType<{ icon: string; key: string }[]>,
            },
        },
   computed: {
    valueSetter: {
      get(): string | number {
        // if (this.type === "number" && typeof this.modelValue === "number") {
        //   return this.modelValue;
        // } else {
        return this.modelValue;
        // }
      },
      set(v: string | number): void {
        this.$emit("update:modelValue", v);
      },
    },
  },
};
</script>