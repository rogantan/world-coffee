<template>
  <label class="form-label">
    <span class="form-text">{{ label }}</span>
    <select class="form-select mt-2" :id="label" v-model="model" :disabled="disabled || isLoading">
      <option v-if="emptyRow" value="">{{ placeholder }}</option>
      <option v-for="val in values" :value="val.value" :key="val.value">
        {{ val.title }}
      </option>
    </select>
    <div v-show="error" class="alert alert-danger" role="alert">{{ error }}</div>
  </label>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';

interface SelectType {
  value: string;
  title: string;
}

defineProps({
  values: {
    type: Array as () => SelectType[],
    default: () => []
  },
  isLoading: Boolean,
  isLoadingErrored: Boolean,
  placeholder: String,
  label: String,
  readonly: Boolean,
  disabled: Boolean,
  error: String,
  emptyRow: Boolean,
});
const model = defineModel()
// };
</script>