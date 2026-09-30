import { onMounted, ref, shallowRef, type Ref, type ShallowRef } from 'vue'

export interface QueryState<T> {
  data: ShallowRef<T | undefined>
  error: ShallowRef<unknown>
  loading: Ref<boolean>
  refresh: () => Promise<void>
}

/** Runs an async loader on mount and exposes its state. Deliberately tiny: no cache. */
export function useQuery<T>(loader: () => Promise<T>): QueryState<T> {
  const data = shallowRef<T>()
  const error = shallowRef<unknown>()
  const loading = ref(true)

  async function refresh() {
    loading.value = true
    error.value = undefined
    try {
      data.value = await loader()
    } catch (e) {
      error.value = e
      data.value = undefined
    } finally {
      loading.value = false
    }
  }

  onMounted(refresh)
  return { data, error, loading, refresh }
}
