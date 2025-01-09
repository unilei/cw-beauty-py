import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import NewPrompt from '../views/NewPrompt.vue'
import PromptDetail from '../views/PromptDetail.vue'
import Profile from '../views/Profile.vue'
import ManagePrompts from '../views/admin/ManagePrompts.vue'
import ManageUsers from '../views/admin/ManageUsers.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/register',
      name: 'register',
      component: Register
    },
    {
      path: '/new',
      name: 'new-prompt',
      component: NewPrompt,
      meta: { requiresAuth: true }
    },
    {
      path: '/prompts/:id',
      name: 'prompt-detail',
      component: PromptDetail
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile,
      meta: { requiresAuth: true }
    },
    {
      path: '/admin/prompts',
      name: 'admin-prompts',
      component: ManagePrompts,
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/admin/users',
      name: 'admin-users',
      component: ManageUsers,
      meta: { requiresAuth: true, requiresAdmin: true }
    }
  ]
})

// 导航守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const token = localStorage.getItem('token')

  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.meta.requiresAdmin && (!userStore.user || userStore.user.role !== 'ADMIN')) {
    next('/')
  } else {
    next()
  }
})

export default router 