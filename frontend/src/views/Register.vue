<template>
  <div class="max-w-md mx-auto">
    <h1 class="text-2xl font-bold mb-6">Register</h1>
    
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <!-- Error Alert -->
      <div v-if="error" class="bg-red-500/10 border border-red-500/20 rounded-lg p-4 text-red-400">
        {{ error }}
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-400 mb-1">Name</label>
        <input type="text" 
               v-model="form.name"
               required
               class="w-full px-3 py-2 bg-gray-800/50 border border-gray-700/50 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
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

      <div>
        <label class="block text-sm font-medium text-gray-400 mb-1">Confirm Password</label>
        <input type="password" 
               v-model="form.confirmPassword"
               required
               class="w-full px-3 py-2 bg-gray-800/50 border border-gray-700/50 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
      </div>

      <div>
        <button type="submit" 
                :disabled="loading || !isFormValid"
                class="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-gray-900 disabled:opacity-50 disabled:cursor-not-allowed">
          <span v-if="loading">Loading...</span>
          <span v-else>Register</span>
        </button>
      </div>

      <div class="text-center text-sm text-gray-400">
        Already have an account? 
        <router-link to="/login" class="text-blue-400 hover:text-blue-300">Login</router-link>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '@/api/auth'

const router = useRouter()
const loading = ref(false)
const error = ref(null)
const form = ref({
  name: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const isFormValid = computed(() => {
  return form.value.password && 
         form.value.password === form.value.confirmPassword &&
         form.value.name &&
         form.value.email
})

const handleSubmit = async () => {
  if (!isFormValid.value) return
  
  try {
    loading.value = true
    error.value = null
    
    const response = await register({
      name: form.value.name,
      email: form.value.email,
      password: form.value.password
    })
    
    const { token, user } = response.data
    
    // 保存 token 和用户信息
    localStorage.setItem('token', token)
    localStorage.setItem('user', JSON.stringify(user))
    
    // 注册成功后重定向到首页
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.message || 'Registration failed'
  } finally {
    loading.value = false
  }
}
</script> 