import { ref } from 'vue';

export function useLoading() {
  const isLoading = ref(false);

  const loadingOptions = {
    color: '#bead15',
    width: 100,
    height: 100,
    backgroundColor: '#000000',
    opacity: 0.5,
    loader: 'bars',
    canCancel: true,
    onCancel: () => {
      // console.log('Loading cancelled');
      isLoading.value = false;
    },
    isFullPage: true,
  };

  function startLoading() {
    isLoading.value = true;
  }

  function stopLoading() {
    isLoading.value = false;
  }

  return {
    isLoading,
    loadingOptions,
    startLoading,
    stopLoading,
  };
}
