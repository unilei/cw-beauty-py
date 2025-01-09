<template>
  <div id="app">
    <div class="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 text-gray-100">
      <nav class="bg-gray-900/50 backdrop-blur-lg border-b border-gray-800/50 py-4 sticky top-0 z-50">
        <div class="container mx-auto px-4">
          <div class="flex justify-between items-center">
            <router-link to="/" class="text-2xl font-bold bg-gradient-to-r from-blue-500 to-purple-500 bg-clip-text text-transparent">
              <img src="/logo.svg" alt="cursor.beauty logo" class="h-8 w-8 inline-block mr-2" />
              cursor.beauty
            </router-link>
            <div class="flex-1 max-w-2xl mx-8 hidden md:block">
              <div class="relative">
                <input type="text" 
                       v-model="searchInput"
                       @keydown="handleSearchKeydown"
                       placeholder="Search prompts..." 
                       class="w-full px-4 py-2 bg-gray-800/50 backdrop-blur rounded-lg border border-gray-700/50 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all">
                <button @click="handleSearch"
                        class="absolute right-3 top-1/2 transform -translate-y-1/2 hover:text-gray-200 transition-colors">
                  <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                  </svg>
                </button>
              </div>
            </div>
            <button @click="isMobileMenuOpen = !isMobileMenuOpen" 
                    class="md:hidden p-2">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="!isMobileMenuOpen" 
                      stroke-linecap="round" 
                      stroke-linejoin="round" 
                      stroke-width="2" 
                      d="M4 6h16M4 12h16M4 18h16" />
                <path v-else 
                      stroke-linecap="round" 
                      stroke-linejoin="round" 
                      stroke-width="2" 
                      d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
            <div class="hidden md:flex items-center space-x-4">
              <template v-if="userStore.user">
                <router-link to="/new" class="px-4 py-2 bg-blue-600 rounded hover:bg-blue-700 transition-colors">New Prompt</router-link>
                <div class="relative group">
                  <button @click="isProfileMenuOpen = !isProfileMenuOpen" 
                          class="flex items-center space-x-2 focus:outline-none">
                    <img :src="userStore.user.avatar_url" 
                         :alt="userStore.user.name"
                         class="w-8 h-8 rounded-full">
                    <span>{{ userStore.user.name }}</span>
                    <span v-if="userStore.user.role === 'ADMIN'" 
                          class="ml-2 px-2 py-0.5 text-xs bg-red-500 rounded-full">Admin</span>
                  </button>
                  <div v-if="isProfileMenuOpen" 
                       class="absolute right-0 mt-2 w-48 bg-gray-800 rounded-lg shadow-lg py-2 border border-gray-700">
                    <router-link to="/profile" 
                                class="block px-4 py-2 hover:bg-gray-700">Profile</router-link>
                    <template v-if="userStore.user.role === 'ADMIN'">
                      <div class="border-t border-gray-700 my-1"></div>
                      <router-link to="/admin/prompts" 
                                  class="block px-4 py-2 hover:bg-gray-700">
                        <span class="text-blue-400">Manage Prompts</span>
                      </router-link>
                      <router-link to="/admin/users" 
                                  class="block px-4 py-2 hover:bg-gray-700">
                        <span class="text-blue-400">Manage Users</span>
                      </router-link>
                    </template>
                    <div class="border-t border-gray-700 my-1"></div>
                    <button @click="handleLogout" 
                            class="block w-full text-left px-4 py-2 text-red-400 hover:bg-gray-700">
                      Logout
                    </button>
                  </div>
                </div>
              </template>
              <template v-else>
                <router-link to="/login" class="px-4 py-2 border border-gray-700 rounded hover:bg-gray-800 transition-colors">Login</router-link>
                <router-link to="/register" class="px-4 py-2 bg-blue-600 rounded hover:bg-blue-700 transition-colors">Register</router-link>
              </template>
            </div>
          </div>
          <div class="mt-4 md:hidden">
            <div class="relative">
              <input type="text" 
                     v-model="searchInput"
                     @keydown="handleSearchKeydown"
                     placeholder="Search prompts..." 
                     class="w-full px-4 py-2 bg-gray-800/50 backdrop-blur rounded-lg border border-gray-700/50 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all">
              <button @click="handleSearch"
                      class="absolute right-3 top-1/2 transform -translate-y-1/2 hover:text-gray-200 transition-colors">
                <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                </svg>
              </button>
            </div>
          </div>
          <div v-show="isMobileMenuOpen" 
               class="md:hidden mt-4 bg-gray-800 rounded-lg shadow-lg border border-gray-700">
            <template v-if="userStore.user">
              <div class="p-4 border-b border-gray-700">
                <div class="flex items-center space-x-3">
                  <img :src="userStore.user.avatar_url" 
                       :alt="userStore.user.name"
                       class="w-10 h-10 rounded-full">
                  <div>
                    <div class="font-medium">{{ userStore.user.name }}</div>
                    <span v-if="userStore.user.role === 'ADMIN'" 
                          class="px-2 py-0.5 text-xs bg-red-500 rounded-full">Admin</span>
                  </div>
                </div>
              </div>
              <router-link to="/new" 
                          class="block px-4 py-3 hover:bg-gray-700">New Prompt</router-link>
              <router-link to="/profile" 
                          class="block px-4 py-3 hover:bg-gray-700">Profile</router-link>
              <template v-if="userStore.user.role === 'ADMIN'">
                <div class="border-t border-gray-700"></div>
                <router-link to="/admin/prompts" 
                            class="block px-4 py-3 hover:bg-gray-700 text-blue-400">
                  Manage Prompts
                </router-link>
                <router-link to="/admin/users" 
                            class="block px-4 py-3 hover:bg-gray-700 text-blue-400">
                  Manage Users
                </router-link>
              </template>
              <div class="border-t border-gray-700"></div>
              <button @click="handleLogout" 
                      class="block w-full text-left px-4 py-3 text-red-400 hover:bg-gray-700">
                Logout
              </button>
            </template>
            <template v-else>
              <router-link to="/login" 
                          class="block px-4 py-3 hover:bg-gray-700">Login</router-link>
              <router-link to="/register" 
                          class="block px-4 py-3 hover:bg-gray-700">Register</router-link>
            </template>
          </div>
        </div>
      </nav>

      <main class="container mx-auto px-4 py-8">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { logout, getCurrentUser } from './api/auth'
import { useUserStore } from './stores/user'
import { useSearchStore } from './stores/search'
import { usePromptsStore } from './stores/prompts'
import { useHead } from '@vueuse/head'

const router = useRouter()
const userStore = useUserStore()
const searchStore = useSearchStore()
const isProfileMenuOpen = ref(false)
const isMobileMenuOpen = ref(false)
const searchInput = ref('')

// 处理搜索
const handleSearch = () => {
  searchStore.setSearchQuery(searchInput.value.trim())
  // 如果不在首页，跳转到首页
  if (router.currentRoute.value.path !== '/') {
    router.push('/')
  }
}

// 处理搜索输入框按键事件
const handleSearchKeydown = (event) => {
  if (event.key === 'Enter') {
    handleSearch()
  }
}

// 当路由变化时清除移动端菜单
watch(
  () => router.currentRoute.value,
  () => {
    isMobileMenuOpen.value = false
  }
)

const handleLogout = async () => {
  try {
    await logout()
    localStorage.removeItem('token')
    userStore.clearUser()
    router.push('/login')
  } catch (error) {
    console.error('Logout failed:', error)
  }
}

const fetchCurrentUser = async () => {
  try {
    const token = localStorage.getItem('token')
    if (token) {
      const response = await getCurrentUser()
      userStore.setUser(response.data.user)
    }
  } catch (error) {
    console.error('Failed to fetch current user:', error)
    localStorage.removeItem('token')
    userStore.clearUser()
  }
}

// 添加对搜索输入的监听
watch(searchInput, (newValue) => {
  if (!newValue.trim()) {
    searchStore.clearSearch()
    if (router.currentRoute.value.path === '/') {
      // 如果在首页，重新加载提示
      const promptsStore = usePromptsStore()
      promptsStore.fetchPrompts({ per_page: 10 })
    }
  }
})

onMounted(() => {
  fetchCurrentUser()
})

useHead({
  title: 'cursor.beauty',
  titleTemplate: '%s | cursor.beauty',
  meta: [
    { charset: 'utf-8' },
    { name: 'viewport', content: 'width=device-width, initial-scale=1' },
    { 
      name: 'description', 
      content: 'Discover and share the best Cursor AI editor prompts. Enhance your coding experience with our curated collection of AI prompts for the Cursor editor.' 
    },
    { 
      name: 'keywords', 
      content: 'Cursor AI prompts, Cursor editor prompts, AI coding prompts, Cursor IDE prompts, programming prompts, code generation prompts, AI code assistant' 
    },
    { name: 'robots', content: 'index, follow' },
    { property: 'og:type', content: 'website' },
    { property: 'og:site_name', content: 'cursor.beauty' },
    { property: 'og:title', content: 'cursor.beauty - Cursor AI Editor Prompts Collection' },
    { 
      property: 'og:description', 
      content: 'Find and share the most effective prompts for Cursor AI editor. Boost your coding productivity with community-curated prompts for code generation, refactoring, and documentation.' 
    }
  ],
  link: [
    { rel: 'canonical', href: 'https://cursor.beauty' }
  ]
})
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>