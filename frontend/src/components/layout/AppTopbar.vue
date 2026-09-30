<script setup lang="ts">
import { Menu, Moon, PanelLeft, Search, Sun } from '@lucide/vue'

import UiButton from '@/components/ui/UiButton.vue'
import UiKbd from '@/components/ui/UiKbd.vue'
import { useTheme } from '@/composables/useTheme'
import { useUiStore } from '@/stores/ui'

const ui = useUiStore()
const { isDark, toggleTheme } = useTheme()
const isMac = typeof navigator !== 'undefined' && /Mac|iPhone|iPad/.test(navigator.platform)
</script>

<template>
  <header class="flex h-14 shrink-0 items-center gap-2 border-b border-border bg-canvas px-3 md:px-4">
    <UiButton
      variant="ghost"
      size="icon"
      class="md:hidden"
      aria-label="Ouvrir la navigation"
      @click="ui.mobileNavOpen = true"
    >
      <Menu class="size-4" />
    </UiButton>
    <UiButton
      variant="ghost"
      size="icon"
      class="hidden md:inline-flex"
      :aria-label="ui.sidebarCollapsed ? 'Déplier la barre latérale' : 'Replier la barre latérale'"
      :aria-pressed="!ui.sidebarCollapsed"
      @click="ui.toggleSidebar()"
    >
      <PanelLeft class="size-4" />
    </UiButton>

    <button
      type="button"
      class="flex h-8 w-full max-w-md items-center gap-2 rounded-md border border-border bg-surface px-2.5 text-base text-fg-subtle transition-colors hover:border-border-strong"
      @click="ui.commandPaletteOpen = true"
    >
      <Search class="size-4 shrink-0" aria-hidden="true" />
      <span class="flex-1 truncate text-left">Rechercher ou aller à…</span>
      <span class="hidden items-center gap-0.5 sm:flex">
        <UiKbd>{{ isMac ? '⌘' : 'Ctrl' }}</UiKbd
        ><UiKbd>K</UiKbd>
      </span>
    </button>

    <div class="ml-auto flex items-center gap-1">
      <UiButton
        variant="ghost"
        size="icon"
        :aria-label="isDark ? 'Passer en mode clair' : 'Passer en mode sombre'"
        @click="toggleTheme()"
      >
        <Sun v-if="isDark" class="size-4" />
        <Moon v-else class="size-4" />
      </UiButton>
      <div
        class="ml-1 flex size-8 items-center justify-center rounded-full bg-accent-soft text-sm font-semibold text-accent"
        aria-label="Profil (non connecté)"
        role="img"
      >
        ?
      </div>
    </div>
  </header>
</template>
