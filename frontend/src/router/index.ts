import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('@/views/HomePage.vue')
    },
    {
      path: '/video/:bvid',
      name: 'VideoPlayer',
      component: () => import('@/views/VideoPlayerPage.vue')
    },
    {
      path: '/search',
      name: 'Search',
      component: () => import('@/views/SearchPage.vue')
    },
    {
      path: '/user/:id',
      name: 'UserCenter',
      component: () => import('@/views/UserCenterPage.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/upload',
      name: 'Upload',
      component: () => import('@/views/UploadPage.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/LoginPage.vue')
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/views/RegisterPage.vue')
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('@/views/NotFoundPage.vue')
    }
  ]
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router
