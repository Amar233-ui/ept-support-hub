<script setup lang="ts">
import { Inbox, Plus, Trash2 } from '@lucide/vue'

import UiBadge, { type BadgeTone } from '@/components/ui/UiBadge.vue'
import UiButton from '@/components/ui/UiButton.vue'
import UiCard from '@/components/ui/UiCard.vue'
import UiEmptyState from '@/components/ui/UiEmptyState.vue'
import UiKbd from '@/components/ui/UiKbd.vue'
import UiSkeleton from '@/components/ui/UiSkeleton.vue'

// Internal catalogue of the design system (dev builds only). Every new ui/ component
// must be added here with its variants. See docs/design-system.md.

const colorTokens = [
  { name: 'canvas', cls: 'bg-canvas' },
  { name: 'surface', cls: 'bg-surface' },
  { name: 'surface-muted', cls: 'bg-surface-muted' },
  { name: 'surface-hover', cls: 'bg-surface-hover' },
  { name: 'border', cls: 'bg-border' },
  { name: 'border-strong', cls: 'bg-border-strong' },
  { name: 'fg', cls: 'bg-fg' },
  { name: 'fg-muted', cls: 'bg-fg-muted' },
  { name: 'fg-subtle', cls: 'bg-fg-subtle' },
  { name: 'accent', cls: 'bg-accent' },
  { name: 'accent-soft', cls: 'bg-accent-soft' },
  { name: 'success', cls: 'bg-success' },
  { name: 'warning', cls: 'bg-warning' },
  { name: 'danger', cls: 'bg-danger' },
  { name: 'info', cls: 'bg-info' },
]

const typeScale = [
  { cls: 'text-2xl font-semibold tracking-tight', label: 'text-2xl · 30px — titre KPI' },
  { cls: 'text-xl font-semibold tracking-tight', label: 'text-xl · 24px — titre de page' },
  { cls: 'text-lg font-semibold', label: 'text-lg · 20px — titre de section' },
  { cls: 'text-md', label: 'text-md · 16px — texte mis en avant, mobile' },
  { cls: 'text-base', label: 'text-base · 14px — texte courant (UI)' },
  { cls: 'text-sm text-fg-muted', label: 'text-sm · 13px — métadonnées, tableaux' },
  { cls: 'text-xs text-fg-muted', label: 'text-xs · 12px — badges, légendes' },
]

// Planned mapping for ticket status / priority badges (implemented in M3).
const statuses: Array<{ label: string; tone: BadgeTone }> = [
  { label: 'Créé', tone: 'neutral' },
  { label: 'Assigné', tone: 'info' },
  { label: 'En cours', tone: 'accent' },
  { label: 'Escaladé', tone: 'warning' },
  { label: 'Résolu', tone: 'success' },
  { label: 'Rouvert', tone: 'danger' },
  { label: 'Clôturé', tone: 'neutral' },
]
const priorities: Array<{ label: string; tone: BadgeTone }> = [
  { label: 'Basse', tone: 'neutral' },
  { label: 'Moyenne', tone: 'info' },
  { label: 'Haute', tone: 'warning' },
  { label: 'Critique', tone: 'danger' },
]
</script>

<template>
  <div class="space-y-8">
    <header>
      <UiBadge tone="warning">Dev uniquement</UiBadge>
      <h1 class="mt-2 text-xl font-semibold tracking-tight">Catalogue UI</h1>
      <p class="mt-1 text-base text-fg-muted">
        Tokens et composants du design system. Basculez le thème (topbar) pour vérifier le mode sombre.
      </p>
    </header>

    <UiCard title="Couleurs" description="Tokens sémantiques — jamais de couleur en dur dans un composant.">
      <div class="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5">
        <div v-for="t in colorTokens" :key="t.name" class="space-y-1.5">
          <div :class="['h-12 rounded-md border border-border', t.cls]" />
          <code class="text-xs text-fg-muted">{{ t.name }}</code>
        </div>
      </div>
    </UiCard>

    <UiCard title="Typographie" description="Inter Variable — échelle courte.">
      <div class="space-y-3">
        <p v-for="t in typeScale" :key="t.label" :class="t.cls">{{ t.label }}</p>
        <p class="text-lg tabular">1 234 567 · 98,4 % — chiffres tabulaires (<code>tabular</code>)</p>
      </div>
    </UiCard>

    <UiCard title="Boutons">
      <div class="flex flex-wrap items-center gap-2">
        <UiButton variant="primary"><Plus class="size-4" />Primaire</UiButton>
        <UiButton>Secondaire</UiButton>
        <UiButton variant="ghost">Fantôme</UiButton>
        <UiButton variant="danger"><Trash2 class="size-4" />Danger</UiButton>
        <UiButton variant="primary" loading>Chargement</UiButton>
        <UiButton disabled>Désactivé</UiButton>
        <UiButton size="icon" aria-label="Ajouter"><Plus class="size-4" /></UiButton>
      </div>
      <div class="mt-4 flex flex-wrap items-center gap-2">
        <UiButton size="sm">Petit</UiButton>
        <UiButton>Moyen</UiButton>
        <UiButton size="lg" variant="primary">Grand (mobile, vigile)</UiButton>
      </div>
    </UiCard>

    <UiCard title="Badges" description="Statuts et priorités de ticket (mapping prévu pour M3).">
      <div class="space-y-3">
        <div class="flex flex-wrap gap-2">
          <UiBadge v-for="s in statuses" :key="s.label" :tone="s.tone" dot>{{ s.label }}</UiBadge>
        </div>
        <div class="flex flex-wrap gap-2">
          <UiBadge v-for="p in priorities" :key="p.label" :tone="p.tone">{{ p.label }}</UiBadge>
        </div>
      </div>
    </UiCard>

    <div class="grid gap-6 md:grid-cols-2">
      <UiCard title="Skeletons">
        <div class="space-y-2">
          <UiSkeleton class="h-4 w-3/4" />
          <UiSkeleton class="h-4 w-1/2" />
          <UiSkeleton class="h-20 w-full" />
        </div>
      </UiCard>
      <UiCard title="Raccourcis clavier">
        <p class="flex items-center gap-2 text-base">
          Palette de commandes : <UiKbd>Ctrl</UiKbd><UiKbd>K</UiKbd> ou <UiKbd>⌘</UiKbd><UiKbd>K</UiKbd>
        </p>
      </UiCard>
    </div>

    <UiCard title="État vide">
      <UiEmptyState
        :icon="Inbox"
        title="Aucun ticket"
        description="Un état vide explique quoi faire ensuite."
      >
        <UiButton variant="primary">Déclarer un incident</UiButton>
      </UiEmptyState>
    </UiCard>
  </div>
</template>
