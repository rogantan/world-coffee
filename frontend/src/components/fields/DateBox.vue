<template>
  <div>
    <div v-if="label" class="lbl-size">
      <span>{{ label }}</span>
    </div>
    <DatePicker class=" text-center " v-model:value="model" format="DD.MM.YYYY" :range="single ? false : true"
      confirm="true" :placeholder="placeholder" lang="fr-CA" :disabled-date="disabledBeforeTodayAndAfterAWeek"
      :disabled="disabled" append-to-body>
    </DatePicker>
    <div v-show="error" class="alert alert-danger" role="alert">{{ error }}</div>
  </div>
</template>

<script lang="ts" setup>
import DatePicker from 'vue-datepicker-next';

type Props = {
  placeholder?: string
  label?: string
  single?: boolean
  disabled?: boolean
  future?: boolean
  error?: string
}

const props = defineProps<Props>()
const model = defineModel<Date | Date[]>()


function disabledBeforeTodayAndAfterAWeek(date: Date) {
  if (props.future) return undefined;
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  return date > today;
};
</script>

<style scoped>
.lbl-size {
  font-size: 10px;
}
</style>