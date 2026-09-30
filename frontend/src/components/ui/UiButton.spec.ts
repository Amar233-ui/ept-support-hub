import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import UiButton from './UiButton.vue'

describe('UiButton', () => {
  it('renders its slot and emits click', async () => {
    const wrapper = mount(UiButton, { slots: { default: 'Valider' } })

    await wrapper.trigger('click')

    expect(wrapper.text()).toBe('Valider')
    expect(wrapper.emitted('click')).toHaveLength(1)
  })

  it('is disabled and busy while loading', () => {
    const wrapper = mount(UiButton, { props: { loading: true } })

    expect(wrapper.attributes('disabled')).toBeDefined()
    expect(wrapper.attributes('aria-busy')).toBe('true')
  })

  it('applies the primary variant with accent tokens', () => {
    const wrapper = mount(UiButton, { props: { variant: 'primary' } })

    expect(wrapper.classes()).toContain('bg-accent')
  })
})
