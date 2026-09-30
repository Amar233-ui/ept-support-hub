<script setup lang="ts">
import { CornerDownLeft, Moon, Search } from '@lucide/vue'
import {
  DialogContent,
  DialogDescription,
  DialogOverlay,
  DialogPortal,
  DialogRoot,
  DialogTitle,
} from 'reka-ui'
import { storeToRefs } from 'pinia'
import { computed, ref, watch, type Component } from 'vue'
import { useRouter } from 'vue-router'

import { navigation } from '@/app/navigation'
import { useTheme } from '@/composables/useTheme'
import { cx } from '@/lib/cx'
import { useUiStore } from '@/stores/ui'

interface Command {
  id: string
  label: string
  group: string
  icon: Component
  run: () => void
}

const { commandPaletteOpen: open } = storeToRefs(useUiStore())
const router = useRouter()
const { toggleTheme } = useTheme()

const query = ref('')
const activeIndex = ref(0)

const commands = computed<Command[]>(() => [
  ...navigation
    .flatMap((s) => s.items)
    .filter((item) => !item.upcoming)
    .map((item) => ({
      id: `nav:${item.to}`,
      label: item.label,
      group: 'Navigation',
      icon: item.icon,
      run: () => router.push(item.to),
    })),
  { id: 'theme', label: 'Basculer le thème clair / sombre', group: 'Actions', icon: Moon, run: toggleTheme },
])

const normalize = (s: string) =>
  s
    .normalize('NFD')
    .replace(/\p{Diacritic}/gu, '')
    .toLowerCase()

const results = computed(() => {
  const q = normalize(query.value.trim())
  return q ? commands.value.filter((c) => normalize(c.label).includes(q)) : commands.value
})

watch(results, () => (activeIndex.value = 0))
watch(open, (isOpen) => {
  if (isOpen) query.value = ''
})

function execute(command: Command | undefined) {
  if (!command) return
  open.value = false
  command.run()
}

function onKeydown(event: KeyboardEvent) {
  const count = results.value.length
  if (!count) return
  if (event.key === 'ArrowDown') {
    event.preventDefault()
    activeIndex.value = (activeIndex.value + 1) % count
  } else if (event.key === 'ArrowUp') {
    event.preventDefault()
    activeIndex.value = (activeIndex.value - 1 + count) % count
  } else if (event.key === 'Enter') {
    event.preventDefault()
    execute(results.value[activeIndex.value])
  }
}
</script>

<template>
  <DialogRoot v-model:open="open">
    <DialogPortal>
      <DialogOverlay class="fixed inset-0 z-50 bg-black/25 backdrop-blur-[1px]" />
      <DialogContent
        class="fixed top-[12vh] left-1/2 z-50 w-[calc(100%-2rem)] max-w-lg -translate-x-1/2 overflow-hidden rounded-lg border border-border bg-surface shadow-overlay"
        @keydown="onKeydown"
      >
        <DialogTitle class="sr-only">Palette de commandes</DialogTitle>
        <DialogDescription class="sr-only">
          Tapez pour filtrer, flèches pour naviguer, Entrée pour exécuter.
        </DialogDescription>
        <div class="flex items-center gap-2 border-b border-border px-3">
          <Search class="size-4 text-fg-subtle" aria-hidden="true" />
          <input
            v-model="query"
            class="h-11 flex-1 bg-transparent text-md outline-none placeholder:text-fg-subtle"
            placeholder="Rechercher une page ou une action…"
            role="combobox"
            aria-expanded="true"
            aria-controls="command-results"
            :aria-activedescendant="results[activeIndex] ? `cmd-${activeIndex}` : undefined"
            autofocus
          />
        </div>
        <ul id="command-results" role="listbox" class="max-h-80 overflow-y-auto p-1.5">
          <li v-if="!results.length" class="px-3 py-6 text-center text-base text-fg-muted">Aucun résultat</li>
          <li
            v-for="(command, i) in results"
            :id="`cmd-${i}`"
            :key="command.id"
            role="option"
            :aria-selected="i === activeIndex"
            :class="
              cx(
                'flex h-9 cursor-pointer items-center gap-2.5 rounded-md px-2.5 text-base',
                i === activeIndex ? 'bg-surface-hover text-fg' : 'text-fg-muted',
              )
            "
            @mousemove="activeIndex = i"
            @click="execute(command)"
          >
            <component :is="command.icon" class="size-4 shrink-0" aria-hidden="true" />
            <span class="flex-1 truncate">{{ command.label }}</span>
            <span class="text-xs text-fg-subtle">{{ command.group }}</span>
            <CornerDownLeft v-if="i === activeIndex" class="size-3.5 text-fg-subtle" aria-hidden="true" />
          </li>
        </ul>
      </DialogContent>
    </DialogPortal>
  </DialogRoot>
</template>
