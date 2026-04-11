<template>
  <button 
    @click="$emit('click', $event)" 
    tabindex="-1"
    :disabled="disabled"
    :class="['btn', `btn-${ color }`]">
    <slot>
      <i :class="[`${icon}`]" v-if="icon"></i>
      <span v-if="title && typeof title === 'string'">{{ title }}</span>
    </slot>
  </button>
</template>

<script lang="ts">
import type { PropType } from 'vue';

export default {
  name: 'ButtonBox',
  components: {
  },
  inheritAttrs: false,
  props: {
    title: {
      type: [String, Number]
    },
    loading: {
      type: Boolean,
      default: false
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    color: {
      type: String,
      default: 'outline-primary',
    },
    icon: {
      type: String,
      default: ''
    },
    icon_color: {
      type: String,
      default: 'initial'
    },
    mode: {
      type: String as PropType<"mini" | "full">,
      default: 'full',
      validator: (value: string) => (['mini', 'full']).indexOf(value) > -1
    },
  }
}
</script>
