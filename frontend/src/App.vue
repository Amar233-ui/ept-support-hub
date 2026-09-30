<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

import AppShell from '@/layouts/AppShell.vue'

const route = useRoute()
// Pages opt out of the app chrome with `meta: { layout: 'blank' }` (login, pending account…).
const useShell = computed(() => route.meta.layout !== 'blank')
</script>

<template>
  <AppShell v-if="useShell">
    <RouterView />
  </AppShell>
  <RouterView v-else />
</template>
