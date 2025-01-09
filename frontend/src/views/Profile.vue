<template>
  <div class="max-w-6xl mx-auto">
    <!-- 用户信息 -->
    <div class="bg-gray-800/50 backdrop-blur-sm rounded-lg p-8 border border-gray-700/50">
      <div class="flex items-center space-x-6">
        <img :src="user?.avatar_url || 'https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp'"
             :alt="user?.name"
             class="w-24 h-24 rounded-full">
        <div>
          <h1 class="text-2xl font-bold text-white">{{ user?.name }}</h1>
          <p class="text-gray-400">{{ user?.email }}</p>
        </div>
      </div>
    </div>

    <!-- 标签页 -->
    <div class="mt-8">
      <div class="border-b border-gray-700">
        <nav class="flex space-x-8">
          <button @click="currentTab = 'prompts'"
                  class="px-1 py-4 text-sm font-medium border-b-2 transition-colors"
                  :class="currentTab === 'prompts' ? 'border-primary-500 text-primary-400' : 'border-transparent text-gray-400 hover:text-gray-300 hover:border-gray-300'">
            My Prompts
          </button>
          <button @click="currentTab = 'likes'"
                  class="px-1 py-4 text-sm font-medium border-b-2 transition-colors"
                  :class="currentTab === 'likes' ? 'border-primary-500 text-primary-400' : 'border-transparent text-gray-400 hover:text-gray-300 hover:border-gray-300'">
            Liked Prompts
          </button>
          <button @click="currentTab = 'favorites'"
                  class="px-1 py-4 text-sm font-medium border-b-2 transition-colors"
                  :class="currentTab === 'favorites' ? 'border-primary-500 text-primary-400' : 'border-transparent text-gray-400 hover:text-gray-300 hover:border-gray-300'">
            Favorite Prompts
          </button>
        </nav>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
      </div>

      <!-- 错误状态 -->
      <div v-else-if="error" class="text-red-500 text-center py-12">
        {{ error }}
      </div>

      <!-- 提示词列表 -->
      <div v-else class="mt-6 grid gap-6">
        <PromptCard v-for="prompt in prompts"
                   :key="prompt.id"
                   :prompt="prompt"
                   @like="toggleLike"
                   @favorite="toggleFavorite" />
      </div>

      <!-- 空状态 -->
      <div v-if="!loading && !error && (!prompts || prompts.length === 0)" class="text-center py-12">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-400">No prompts found</h3>
        <p class="mt-1 text-sm text-gray-500">
          {{ getEmptyMessage() }}
        </p>
        <div class="mt-6">
          <router-link v-if="currentTab === 'prompts'"
                      to="/new"
                      class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
            Create a new prompt
          </router-link>
          <router-link v-else
                      to="/"
                      class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
            Explore prompts
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import PromptCard from '../components/PromptCard.vue'

const user = ref(null)
const prompts = ref([])
const currentTab = ref('prompts')
const loading = ref(true)
const error = ref(null)

const fetchUser = async () => {
  try {
    const { data } = await axios.get('/api/v1/user/profile')
    user.value = data.user
  } catch (err) {
    console.error('Failed to fetch user:', err)
    error.value = 'Failed to load user profile'
  }
}

const fetchPrompts = async () => {
  loading.value = true
  error.value = null
  try {
    const { data } = await axios.get(`/api/v1/user/${currentTab.value}`)
    prompts.value = data.prompts
  } catch (err) {
    console.error('Failed to fetch prompts:', err)
    error.value = 'Failed to load prompts'
  } finally {
    loading.value = false
  }
}

const toggleLike = async (promptId) => {
  try {
    const { data } = await axios.post(`/api/v1/prompts/${promptId}/like`)
    const prompt = prompts.value.find(p => p.id === promptId)
    if (prompt) {
      prompt.is_liked = data.is_liked
      prompt.likes_count = data.likes_count
    }
  } catch (err) {
    console.error('Failed to toggle like:', err)
  }
}

const toggleFavorite = async (promptId) => {
  try {
    const { data } = await axios.post(`/api/v1/prompts/${promptId}/favorite`)
    const prompt = prompts.value.find(p => p.id === promptId)
    if (prompt) {
      prompt.is_favorited = data.is_favorited
      prompt.favorites_count = data.favorites_count
    }
  } catch (err) {
    console.error('Failed to toggle favorite:', err)
  }
}

const getEmptyMessage = () => {
  switch (currentTab.value) {
    case 'prompts':
      return "You haven't created any prompts yet"
    case 'likes':
      return "You haven't liked any prompts yet"
    case 'favorites':
      return "You haven't favorited any prompts yet"
    default:
      return "No prompts found"
  }
}

watch(currentTab, () => {
  fetchPrompts()
})

onMounted(async () => {
  await Promise.all([
    fetchUser(),
    fetchPrompts()
  ])
})
</script> 