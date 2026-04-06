<template>
  <label v-if="label" class="addspace lbl-size">
    <span>
      {{ label }}
    </span>
    <input v-model="model" class="addspace" :readonly="readonly" :disabled="disabled" type="checkbox" />
  </label>
</template>

<script lang="ts" setup>
type Props = {
  label?: string;
  fixedIconName?: string;
  readonly?: boolean;
  disabled?: boolean;
}

withDefaults(defineProps<Props>(), {
  label: '',
  fixedIconName: '',
  readonly: false,
  disabled: false
})
const model = defineModel<boolean>()
</script>
<style>
.addspace {
  display: flex;
  gap: 10px;
  align-items: center;
  justify-content: end;
}

.lbl-size {
  font-size: 10px;
}
</style>