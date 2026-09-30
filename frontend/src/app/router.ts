import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

declare module 'vue-router' {
  interface RouteMeta {
    title?: string
    layout?: 'app' | 'blank'
  }
}

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/features/home/HomeView.vue'),
    meta: { title: 'Accueil' },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/features/errors/NotFoundView.vue'),
    meta: { title: 'Page introuvable' },
  },
]

// Internal component catalogue: only bundled in dev builds (tree-shaken in production).
if (import.meta.env.DEV) {
  routes.unshift({
    path: '/dev/ui',
    name: 'dev-ui',
    component: () => import('@/features/dev/DevUiView.vue'),
    meta: { title: 'Catalogue UI' },
  })
}

export const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

router.afterEach((to) => {
  document.title = to.meta.title ? `${to.meta.title} · EPT Support Hub` : 'EPT Support Hub'
})
