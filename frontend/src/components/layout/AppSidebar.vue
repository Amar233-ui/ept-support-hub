<script setup lang="ts">
import { computed } from 'vue'

import { navigationFor } from '@/app/navigation'
import { cx } from '@/lib/cx'

defineProps<{ collapsed: boolean }>()

// No session until M2: every entry is visible. Will read the role from the auth store.
const sections = computed(() => navigationFor(null))
</script>

<template>
  <aside
    :class="
      cx(
        'h-full shrink-0 flex-col border-r border-border bg-canvas transition-[width] duration-200 motion-reduce:transition-none',
        collapsed ? 'w-14' : 'w-60',
      )
    "
    aria-label="Navigation principale"
  >
    <div :class="cx('flex h-14 items-center gap-2.5 px-3.5', collapsed && 'justify-center px-0')">
      <img src="/favicon.svg" alt="" class="size-7 shrink-0" />
      <span v-if="!collapsed" class="truncate text-base font-semibold tracking-tight">EPT Support Hub</span>
    </div>

    <nav class="flex-1 overflow-y-auto px-2 pb-4">
      <div v-for="(section, i) in sections" :key="i" class="mt-4 first:mt-1">
        <p
          v-if="section.label && !collapsed"
          class="mb-1 px-2 text-xs font-medium tracking-wide text-fg-subtle uppercase"
        >
          {{ section.label }}
        </p>
        <div v-else-if="section.label" class="mx-2 mb-2 border-t border-border" />
        <ul class="space-y-0.5">
          <li v-for="item in section.items" :key="item.to">
            <span
              v-if="item.upcoming"
              :class="
                cx(
                  'flex h-8 cursor-not-allowed items-center gap-2.5 rounded-md px-2 text-base text-fg-subtle',
                  collapsed && 'justify-center',
                )
              "
              :title="collapsed ? `${item.label} (bientôt)` : 'Bientôt disponible'"
              aria-disabled="true"
            >
              <component :is="item.icon" class="size-4 shrink-0" aria-hidden="true" />
              <span v-if="!collapsed" class="truncate">{{ item.label }}</span>
            </span>
            <RouterLink
              v-else
              :to="item.to"
              :title="collapsed ? item.label : undefined"
              :class="
                cx(
                  'flex h-8 items-center gap-2.5 rounded-md px-2 text-base text-fg-muted transition-colors hover:bg-surface-hover hover:text-fg',
                  collapsed && 'justify-center',
                )
              "
              exact-active-class="!bg-surface-hover !text-fg font-medium"
            >
              <component :is="item.icon" class="size-4 shrink-0" aria-hidden="true" />
              <span v-if="!collapsed" class="truncate">{{ item.label }}</span>
            </RouterLink>
          </li>
        </ul>
      </div>
    </nav>
  </aside>
</template>
