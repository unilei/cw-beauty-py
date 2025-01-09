<template>
  <div class="max-w-md mx-auto">
    <h1 class="text-2xl font-bold mb-6">Login</h1>
    
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <!-- Error Alert -->
      <div v-if="error" class="bg-red-500/10 border border-red-500/20 rounded-lg p-4 text-red-400">
        {{ error }}
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-400 mb-1">Email</label>
        <input type="email" 
               v-model="form.email"
               required
               class="w-full px-3 py-2 bg-gray-800/50 border border-gray-700/50 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-400 mb-1">Password</label>
        <input type="password" 
               v-model="form.password"
               required
               class="w-full px-3 py-2 bg-gray-800/50 border border-gray-700/50 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
      </div>

      <div class="flex items-center">
        <input type="checkbox" 
               id="remember" 
               v-model="form.remember"
               class="rounded bg-gray-800/50 border-gray-700/50 text-blue-500 focus:ring-blue-500">
        <label for="remember" class="ml-2 text-sm text-gray-400">Remember me</label>
      </div>

      <div>
        <button type="submit" 
                :disabled="loading"
                class="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-gray-900 disabled:opacity-50 disabled:cursor-not-allowed">
          <span v-if="loading">Loading...</span>
          <span v-else>Login</span>
        </button>
      </div>

      <div class="text-center text-sm text-gray-400">
        Don't have an account? 
        <router-link to="/register" class="text-blue-400 hover:text-blue-300">Register</router-link>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '@/api/auth'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const error = ref(null)
const form = ref({
  email: '',
  password: '',
  remember: false
})

const handleSubmit = async () => {
  try {
    loading.value = true
    error.value = null
    
    const response = await login(form.value)
    const { token, user } = response.data
    
    // 保存 token
    localStorage.setItem('token', token)
    
    // 更新用户状态
    userStore.setUser(user)
    
    // 根据用户角色重定向
    if (user.role === 'ADMIN') {
      router.push('/admin/prompts')
    } else {
      router.push('/')
    }
  } catch (err) {
    error.value = err.response?.data?.message || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>

<script>
export default {
  name: 'Login',
  metaInfo: {
    title: 'Login',
    meta: [
      { 
        name: 'description', 
        content: 'Login to your AI Prompt Platform account. Create, share and manage your AI prompts.' 
      },
      { property: 'og:title', content: 'Login | AI Prompt Platform' },
      { 
        property: 'og:description', 
        content: 'Login to your AI Prompt Platform account. Create, share and manage your AI prompts.' 
      }
    ]
  }
}
</script> 