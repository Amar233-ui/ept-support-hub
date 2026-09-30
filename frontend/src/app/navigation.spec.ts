import { describe, expect, it } from 'vitest'

import { navigationFor } from './navigation'

const labels = (role: Parameters<typeof navigationFor>[0]) =>
  navigationFor(role).flatMap((section) => section.items.map((item) => item.label))

describe('navigationFor', () => {
  it('hides administration entries from a regular user', () => {
    const items = labels('USER')

    expect(items).toContain('Mes tickets')
    expect(items).not.toContain('Comptes')
    expect(items).not.toContain('File de traitement')
  })

  it('shows the voice report entry to guards only', () => {
    expect(labels('GUARD')).toContain('Signalement vocal')
    expect(labels('ADMIN')).not.toContain('Signalement vocal')
  })

  it('drops sections that end up empty', () => {
    const sections = navigationFor('USER')

    expect(sections.every((s) => s.items.length > 0)).toBe(true)
  })
})
