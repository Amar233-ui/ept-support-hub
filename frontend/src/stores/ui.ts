import { useStorage } from '@vueuse/core'
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUiStore = defineStore('ui', () => {
  const sidebarCollapsed = useStorage('eptsh-sidebar-collapsed', false)
  const mobileNavOpen = ref(false)
  const commandPaletteOpen = ref(false)

  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  return { sidebarCollapsed, mobileNavOpen, commandPaletteOpen, toggleSidebar }
})
