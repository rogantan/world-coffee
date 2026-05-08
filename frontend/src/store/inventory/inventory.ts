import { ref, watch } from "vue";
import type { Inventory } from "../../types/inventory/inventory";
import { defineStore } from "pinia";
import { useRoute } from "vue-router";
import { inventory } from "../../api";

export const useInventoryStore = defineStore('inventory', () => {
  const inventories = ref<Inventory[]>([]);
  const route = useRoute();
  const urls = ["1", "2"]

  const get = async (): Promise<Inventory[]> => {
    try {
      const response = await inventory.getInventoryByShop(route.meta.back_url as string)
      if (response) {
        inventories.value.slice(0);
        inventories.value = [...response]
        return response
      }
    } catch (error) {
      console.log(error);
    }
  }

  watch(
    () => route.path,
    (newPath, oldPath) => {
      if (newPath !== oldPath && urls.includes(newPath.split("/")[2])) {
        document.title = route.meta.back_url as string;
        get();
      }
    }
  )

  return {
    inventories,
    get
  }
})