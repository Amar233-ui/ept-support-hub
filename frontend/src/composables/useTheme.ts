import { useDark, useToggle } from '@vueuse/core'

/**
 * Light/dark theme bound to the `dark` class on <html>, persisted in localStorage.
 * The storage key is shared with the inline script in index.html (prevents a flash on load).
 */
export function useTheme() {
  const isDark = useDark({ storageKey: 'eptsh-theme', valueDark: 'dark', valueLight: 'light' })
  const toggleTheme = useToggle(isDark)
  return { isDark, toggleTheme }
}
