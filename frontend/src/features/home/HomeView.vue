<script setup lang="ts">
import { Inbox, Plus } from '@lucide/vue'

import { http } from '@/api/http'
import UiBadge from '@/components/ui/UiBadge.vue'
import UiButton from '@/components/ui/UiButton.vue'
import UiCard from '@/components/ui/UiCard.vue'
import UiEmptyState from '@/components/ui/UiEmptyState.vue'
import UiSkeleton from '@/components/ui/UiSkeleton.vue'
import { useQuery } from '@/composables/useQuery'

interface Health {
  status: string
  version: string
}

const backend = useQuery(() => http<Health>('/health'))
</script>

<template>
  <div class="space-y-8">
    <header class="flex flex-wrap items-end justify-between gap-4">
      <div>
        <h1 class="text-xl font-semibold tracking-tight">Bienvenue sur EPT Support Hub</h1>
        <p class="mt-1 text-base text-fg-muted">
          Signalez un incident, suivez vos demandes et pilotez l'activité des services.
        </p>
      </div>
      <UiButton variant="primary" disabled title="Disponible au milestone M3">
        <Plus class="size-4" aria-hidden="true" />
        Déclarer un incident
      </UiButton>
    </header>

    <UiCard title="Mes tickets" description="Les incidents que vous avez déclarés.">
      <UiEmptyState
        :icon="Inbox"
        title="Aucun ticket pour le moment"
        description="Quand vous déclarerez un incident, vous pourrez suivre son traitement ici, étape par étape."
      />
    </UiCard>

    <footer class="flex items-center gap-2 text-sm text-fg-muted">
      <span>État de l'API :</span>
      <UiSkeleton v-if="backend.loading.value" class="h-5 w-24" />
      <UiBadge v-else-if="backend.data.value" tone="success" dot>
        Opérationnelle · v{{ backend.data.value.version }}
      </UiBadge>
      <UiBadge v-else tone="danger" dot>Injoignable</UiBadge>
    </footer>
  </div>
</template>
