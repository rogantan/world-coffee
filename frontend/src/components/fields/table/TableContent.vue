<template>
  <div class="scrollable-horizontal">
    <table class="table table-bordered table-centered mb-0">
      <thead>
        <tr class="custom-head">
          <th v-if="selectable">
            <CheckBoxC v-bind="checkboxProps" v-show="data && DataLoaderPlugin.length > 0 && !isLoading && !isErrored"
              @click="$emit('selectAll')"></CheckBoxC>
          </th>
          <th v-for="(header, key) in headers" :key="key" :class="getHeaderClass(header)" :data-id="key">
            <div v-if="!header.sort" :style="`width: ${header.width || 200}px !important`">
              <span>{{ header.title }}</span>
            </div>
            <div v-else class="flex-container" :style="`width: ${header.width || 200}px !important`" @click="sornEmit(header)">
              <span>{{ header.title }}</span>
              <span v-if="header.sort" :class="['icon-large', getSortIconClass(header.key)]"></span>
            </div>
          </th>
        </tr> 
      </thead>

      <tbody>
        <template v-if="isErrored">
          <tr>
            <td :colspan="thCount">
              Произошла ошибка
            </td>
          </tr>
        </template>
        <template v-else-if="isLoading">
          <tr v-for="item in 2" :key="`item-${item}`">
            <td v-for="(header, key) in headers" :key="item + key" :data:id="key" :class="header.class">
              <div style="animation: loading 2s infinite; height: 50%; width: 70%; border-radius: 5px;"></div>
            </td>
          </tr>
        </template>

        <template v-else-if="!data || data.length === 0">
          <tr>
            <td :colspan="thCount">{{ empty_text }}</td>
          </tr>
        </template>

        <template v-else>
          <slot>
            <tr v-for="row in data" :key="row.uuid || row.link" @click="$emit('click', row)">
              <td v-for="(_, key, index) in headers" :key="`${row.uuid || row.link}-${key}`"
              :class="getCellClass(row, key, index)">
              <slot :name="`${key}-cell`" :row="row">
                <span v-html="row[key]"></span>
              </slot>
              </td>
            </tr>
          </slot>
        </template>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts" setup>
import { computed, toRefs } from 'vue';
import type { iTableHeader } from '../../../models/table';
import CheckBoxC from '../CheckBoxC.vue';
//import iTableHeader

export type Props = {
  isLoading?: boolean,
  isErrored?: boolean,
  headers: any[] | Record<string,any>,
  data: any[],
  sort_key?: string,
  showPagination?: boolean,
  empty_text?: string,
  pagination_mode?: 'router' | 'emit',
  selectable?: boolean,
  selectedIds?: any[],
  staticColumn?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  isLoading: false,
  isErrored: false,
  headers: () => [],
  data: () => [],
  sort_key: '',
  showPagination: true,
  empty_text: 'Нет данных',
  pagination_mode: 'router',
  selectable: false,
  selectedIds: () => [],
  staticColumn: false
})
const emit = defineEmits(['sort', 'selectAll', 'click']);

const {
  headers,
  data,
  selectedIds,
  sort_key,
  selectable,
  isLoading,
  isErrored,
  // showPagination,
  // pagination_mode,
  empty_text,
  staticColumn
} = toRefs(props);

const thCount = computed(() => (headers.value ? Object.keys(headers.value).length : 0) + (selectable.value ? 1 : 0));

const currentSort = computed(() => {
  if (!sort_key.value) {
    return { key: "", direction: "desc" };
  } else {
    const key = sort_key.value
      .replace('+', '')
      .replace('-', '')
      .replace('asc', '')
      .replace('desc', '')
      .trim();
    const direction = sort_key.value[0] === '+' || sort_key.value.includes('asc') ? 'asc' : 'desc';
    return { key, direction };
  }
});

const checkboxProps = computed(() => {
  let allSelected = false;
  if (data.value && data.value.length > 0) {
    allSelected = data.value.every(r => String(r.id) !== undefined && selectedIds.value.includes(Number(r.id)));
  }
  return {
    fixed_icon_name: !allSelected && selectedIds.value.length > 0 ? 'checkbox_partly_filled' : '',
    value: allSelected
  };
});

const sortEmit = (header: iTableHeader) => {
  if (!header.sortKeys) return;
  const currentDirection = currentSort.value.direction;
  const newDirection = currentDirection === 'asc' ? 'desc' : 'asc';
  emit('sort', header.sortKeys[newDirection]);
};

function getHeaderClass(header: any) {
  return `bg-${header.class}-h` || '';
}

const getSortIconClass = (key: any) => {
  if (currentSort.value.key === key) {
    return currentSort.value.direction === 'desc' ? 'ri-sort-desc' : 'ri-sort-asc';
  }
  return 'ri-align-justify';
};


function getCellClass(row: any, key: any, index: any) {
  const classKey = `${key}_class`;

  if (staticColumn.value && index === 0) {
    // console.log(index)
    // console.log(staticColumn.value)
    return 'static-col'
  }
  return `bg-${row[classKey]}` || '';
}
</script>

<style>
.flex-container {
  display: flex;
  justify-content: space-between;
  /* Распределяет элементы так, что один прижат к левому краю, другой к правому */
  align-items: center;
  /* Выравниваем элементы по центру по вертикали */
  width: 100%;
}

/* .scrollable-horizontal {
  overflow: auto;
  position: absolute;
  inset: 0;
} */
.scrollable-horizontal {
  overflow: auto;
  /* -webkit-overflow-scrolling: touch; */
  /* max-height: 75vh; */
  /* height: 100%; */
  /* overflow-y: auto; */
}

.static-col {
  position: sticky !important;
  left: 0px;
  z-index: 2;
  /* --ct-table-border-color: #cfd0d2; */
  --ct-table-bg: #ffffff;
}

.static-col::after {
  content: "";
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 1px;
  /* Ширина границы */
  background: #e9ecef;
  /* Цвет границы */
  z-index: 3;
  /* Убедитесь, что z-index выше, чем у других элементов в таблице */
}

.minh {
  width: 200px !important;
}

.maxh {
  max-width: 20px !important;
}

.custom-head {
  position: sticky !important;
  top: 0px;
  z-index: 3;
}

.bg-archived {
  opacity: 0.5;
  --ct-table-bg: #c7c7c7;
}

.bg-green {
  --ct-table-bg: #d4edda;

}

.bg-red {
  --ct-table-bg: #f8d7da;
  /* light red */
}

.bg-yellow {
  --ct-table-bg: #fff3cd;
  /* light yellow */
}

.bg-lemon {
  --ct-table-bg: #fdd244;
  /*  yellow */
}

.bg-lemon-h {
  background-color: #fdd244 !important;
  /*  yellow */
  --ct-table-bg: #fdd244;
}

.icon-large {
  font-size: 28px;
  /* или другой размер */
}
</style>