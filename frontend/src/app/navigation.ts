import type { Component } from 'vue'
import {
  BarChart3,
  Building2,
  CalendarClock,
  Home,
  Inbox,
  MapPin,
  Mic,
  ScrollText,
  Settings,
  Ticket,
  Users,
} from '@lucide/vue'

export type Role = 'USER' | 'GUARD' | 'TECH_N1' | 'TECH_N2' | 'SERVICE_HEAD' | 'ADMIN'

export interface NavItem {
  label: string
  to: string
  icon: Component
  /** Roles allowed to see the entry. Visibility only: the backend enforces access. */
  roles: Role[]
  /** Route not implemented yet: shown disabled with a "Bientôt" hint. */
  upcoming?: boolean
}

export interface NavSection {
  label?: string
  items: NavItem[]
}

const ALL: Role[] = ['USER', 'GUARD', 'TECH_N1', 'TECH_N2', 'SERVICE_HEAD', 'ADMIN']
const STAFF: Role[] = ['TECH_N1', 'TECH_N2', 'SERVICE_HEAD', 'ADMIN']

export const navigation: NavSection[] = [
  {
    items: [
      { label: 'Accueil', to: '/', icon: Home, roles: ALL },
      { label: 'Mes tickets', to: '/tickets/mine', icon: Ticket, roles: ALL, upcoming: true },
      { label: 'Signalement vocal', to: '/guard', icon: Mic, roles: ['GUARD'], upcoming: true },
      { label: 'Besoins temporaires', to: '/requests', icon: CalendarClock, roles: ALL, upcoming: true },
    ],
  },
  {
    label: 'Service',
    items: [
      { label: 'File de traitement', to: '/queue', icon: Inbox, roles: STAFF, upcoming: true },
      { label: 'Tableau de bord', to: '/dashboard', icon: BarChart3, roles: STAFF, upcoming: true },
    ],
  },
  {
    label: 'Administration',
    items: [
      { label: 'Comptes', to: '/admin/users', icon: Users, roles: ['ADMIN', 'SERVICE_HEAD'], upcoming: true },
      { label: 'Services', to: '/admin/services', icon: Building2, roles: ['ADMIN'], upcoming: true },
      { label: 'Zones', to: '/admin/zones', icon: MapPin, roles: ['ADMIN'], upcoming: true },
      { label: "Journal d'audit", to: '/admin/audit', icon: ScrollText, roles: ['ADMIN'], upcoming: true },
      { label: 'Paramètres', to: '/admin/settings', icon: Settings, roles: ['ADMIN'], upcoming: true },
    ],
  },
]

/** Sections filtered for a role; `null` (no session yet, M0) shows everything. */
export function navigationFor(role: Role | null): NavSection[] {
  if (role === null) return navigation
  return navigation
    .map((section) => ({ ...section, items: section.items.filter((item) => item.roles.includes(role)) }))
    .filter((section) => section.items.length > 0)
}
