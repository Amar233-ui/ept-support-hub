<script setup lang="ts">
import { onKeyStroke } from '@vueuse/core'
import { DialogContent, DialogOverlay, DialogPortal, DialogRoot, DialogTitle } from 'reka-ui'
import { storeToRefs } from 'pinia'
import { watch } from 'vue'
import { useRoute } from 'vue-router'

import AppSidebar from '@/components/layout/AppSidebar.vue'
import AppTopbar from '@/components/layout/AppTopbar.vue'
import CommandPalette from '@/components/layout/CommandPalette.vue'
import { useUiStore } from '@/stores/ui'

const ui = useUiStore()
const { mobileNavOpen, commandPaletteOpen } = storeToRefs(ui)
const route = useRoute()

// Ctrl+K / ⌘K opens the command palette from anywhere.
onKeyStroke('k', (event) => {
  if (event.ctrlKey || event.metaKey) {
    event.preventDefault()
    commandPaletteOpen.value = !commandPaletteOpen.value
  }
})

watch(
  () => route.fullPath,
  () => {
    mobileNavOpen.value = false
  },
)
</script>

<template>
  <div class="flex h-dvh overflow-hidden">
    <a
      href="#main"
      class="sr-only z-50 rounded-md bg-accent px-3 py-2 text-accent-fg focus:not-sr-only focus:absolute focus:top-2 focus:left-2"
    >
      Aller au contenu
    </a>

    <!-- Desktop sidebar -->
    <AppSidebar class="hidden md:flex" :collapsed="ui.sidebarCollapsed" />

    <!-- Mobile drawer -->
    <DialogRoot v-model:open="mobileNavOpen">
      <DialogPortal>
        <DialogOverlay class="fixed inset-0 z-40 bg-black/30 md:hidden" />
        <DialogContent class="fixed inset-y-0 left-0 z-50 flex md:hidden" :aria-describedby="undefined">
          <DialogTitle class="sr-only">Navigation</DialogTitle>
          <AppSidebar class="flex bg-surface" :collapsed="false" />
        </DialogContent>
      </DialogPortal>
    </DialogRoot>

    <div class="flex min-w-0 flex-1 flex-col">
      <AppTopbar />
      <main id="main" class="flex-1 overflow-y-auto" tabindex="-1">
        <div class="mx-auto w-full max-w-6xl px-4 py-6 md:px-8 md:py-8">
          <slot />
        </div>
      </main>
    </div>

    <CommandPalette />
  </div>
</template>
