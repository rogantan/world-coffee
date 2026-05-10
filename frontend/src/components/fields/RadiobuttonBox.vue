<template>
  <label class="">
    <input
      class="addspace"
      :readonly="readonly"
      :disabled="disabled"
      type="radio"
      :name="name"  
      :value="value"
      :checked="modelValue === value"
      @change="onChange"
    />
    {{ label }}
  </label>
</template>

<script>
export default {
  name: 'RadiobuttonBox',
  props: {
    modelValue: [String, Number],
    value: [String, Number],
    label: String,
    readonly: Boolean,
    disabled: Boolean,
    name: String
  },
  emits: ['update:modelValue'],
  methods: {
    onChange($event) {
      if (!this.readonly && !this.disabled) {
        this.$emit('update:modelValue', this.value);
      }
    }
  }
};
</script>
<style>
.addspace{
  margin-right: 20px !important;
}
</style>