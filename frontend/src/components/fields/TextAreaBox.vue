<template>
    <div class="">
        <div class="" v-if="label">
            <span>{{ label }}</span>
        </div>
        <div class="ui-textarea">
            <textarea 
                :min-height="minHeight"
                class="form-control"
                v-model="valueSetter" 
                @blur="emitBlur" 
                :readonly="readonly" 
                :disabled="disabled">
            </textarea>
        </div>
        <div v-show="error" class="alert alert-danger" role="alert">{{ error }}</div>
    </div>
</template>

<script lang="ts">
import { defineComponent, PropType, computed } from 'vue';

export default defineComponent({
    name: "TextAreaBox",
    props: {
        label: String,
        modelValue: {
            required: true,
            type: String
        },
        disabled: {
            type: Boolean,
            default: false
        },
        color: {
            type: String as PropType<string>,
            validator: (val: string) => ['white', 'grey'].includes(val),
            default: 'grey'
        },
        readonly: {
            type: Boolean,
            default: false
        },
        error: {
            type: String,
        },
        minHeight: {
            type: Number,
            default: 100
        }
    },
    setup(props, { emit }) {
        const valueSetter = computed({
            get: () => props.modelValue, // Тут тоже исправил на modelValue
            set: (newValue: string) => emit('update:modelValue', newValue) // Тут правильно
        });

        const emitBlur = () => emit('blur');

        return { valueSetter, emitBlur };
    }
});
</script>

<style>
.ui-textarea__input {
  resize: none;
}
</style>