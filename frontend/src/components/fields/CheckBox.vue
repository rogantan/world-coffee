<template>
  <label>
      <input
        class="addspace"
        :readonly="readonly"
        :disabled="disabled"
        type="checkbox"
        :checked="modelValue"
        @change="onChange"/> 
      {{ label }}
  </label>
</template>

<script lang="ts">
import { defineComponent, ref, watchEffect } from 'vue';

export default defineComponent({
  name: 'CheckBox',
  props: {
    modelValue: Boolean,
    label: String,
    fixedIconName: {
      type: String,
      default: '',
    },
    readonly: Boolean,
    disabled: Boolean,
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const internalValue = ref(props.modelValue);

    const onChange = (event: Event) => {
      const target = event.target as HTMLInputElement;
      if (!props.readonly && !props.disabled) {
        emit('update:modelValue', target.checked);
      }
    }

    watchEffect(() => {
      internalValue.value = props.modelValue;
    });

    return { 
      internalValue,
      onChange 
    };
  },
});
</script>
<style>
.addspace{
  margin-right: 20px !important;
}
.lbl-size{
  font-size: 10px;
}
</style>