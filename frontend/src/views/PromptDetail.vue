<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" 
         class="bg-red-500/10 border border-red-500/20 rounded-lg p-4 text-red-400">
      {{ error }}
    </div>

    <!-- Prompt Content -->
    <div v-else-if="prompt" class="space-y-6">
      <!-- Header Section -->
      <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
        <div class="space-y-4">
          <h1 class="text-2xl sm:text-3xl font-bold break-words">{{ prompt.title }}</h1>
          
          <!-- Meta Information -->
          <div class="flex flex-wrap items-center gap-2 sm:gap-4 text-sm text-gray-400">
            <div class="flex items-center gap-2">
              <img :src="prompt.author.avatar_url"
                   :alt="prompt.author.name"
                   class="w-6 h-6 rounded-full">
              <span>{{ prompt.author.name }}</span>
            </div>
            <span class="hidden sm:inline">·</span>
            <router-link 
              :to="{ name: 'home', query: { language: prompt.language.slug }}"
              class="hover:text-primary-400 transition-colors"
            >
              {{ prompt.language.name }}
            </router-link>
            <span class="hidden sm:inline">·</span>
            <span>{{ formatDate(prompt.created_at) }}</span>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex items-center gap-2 sm:gap-4 sm:self-start">
          <Menu as="div" class="relative">
            <MenuButton
              @click="handleLike"
              class="flex items-center space-x-2 px-3 sm:px-4 py-2 rounded-lg 
                     hover:bg-gray-800/50 transition-colors"
              :class="{ 'text-red-500': prompt.is_liked }"
            >
              <HeartIcon
                class="h-5 w-5"
                :class="{ 'fill-current': prompt.is_liked }"
                aria-hidden="true"
              />
              <span class="min-w-[1.5rem] text-center">{{ prompt.likes_count }}</span>
            </MenuButton>
          </Menu>

          <Menu as="div" class="relative">
            <MenuButton
              @click="handleFavorite"
              class="flex items-center space-x-2 px-3 sm:px-4 py-2 rounded-lg 
                     hover:bg-gray-800/50 transition-colors"
              :class="{ 'text-yellow-500': prompt.is_favorited }"
            >
              <StarIcon
                class="h-5 w-5"
                :class="{ 'fill-current': prompt.is_favorited }"
                aria-hidden="true"
              />
              <span class="min-w-[1.5rem] text-center">{{ prompt.favorites_count }}</span>
            </MenuButton>
          </Menu>
        </div>
      </div>

      <!-- Content Section -->
      <div class="relative">
        <div class="bg-gray-800/50 backdrop-blur-sm rounded-lg p-4 sm:p-6 
                    border border-gray-700/50 overflow-x-auto">
          <div class="flex justify-between items-start mb-2">
            <span class="text-xs text-gray-400">Prompt Content</span>
            <button
              @click="copyToClipboard"
              class="inline-flex items-center px-2 py-1 sm:px-3 sm:py-1.5 text-xs sm:text-sm 
                     bg-blue-600 text-white rounded-lg hover:bg-blue-700 
                     focus:outline-none focus:ring-2 focus:ring-blue-500 
                     focus:ring-offset-2 focus:ring-offset-gray-900 transition-colors
                     disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <DocumentDuplicateIcon class="w-4 h-4 mr-1.5" />
              <span class="hidden sm:inline">Copy to Clipboard</span>
              <span class="sm:hidden">Copy</span>
            </button>
          </div>
          <pre class="whitespace-pre-wrap font-mono text-sm sm:text-base 
                      overflow-x-auto scrollbar-thin scrollbar-thumb-gray-700 
                      scrollbar-track-transparent">{{ prompt.content }}</pre>
        </div>
        
        <Transition
          enter="transition ease-out duration-200"
          enter-from="opacity-0 translate-y-1"
          enter-to="opacity-100 translate-y-0"
          leave="transition ease-in duration-150"
          leave-from="opacity-100 translate-y-0"
          leave-to="opacity-0 translate-y-1"
        >
          <div v-if="showCopySuccess" 
               class="fixed bottom-4 left-1/2 transform -translate-x-1/2 
                      bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg
                      text-sm flex items-center space-x-2 z-50">
            <CheckCircleIcon class="w-5 h-5" />
            <span>Copied to clipboard!</span>
          </div>
        </Transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Menu, MenuButton } from '@headlessui/vue'
import { 
  HeartIcon, 
  StarIcon,
  DocumentDuplicateIcon,
  CheckCircleIcon
} from '@heroicons/vue/24/outline'
import axios from '../utils/axios'

const route = useRoute()
const router = useRouter()
const prompt = ref(null)
const loading = ref(true)
const error = ref(null)
const showCopySuccess = ref(false)

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const fetchPrompt = async () => {
  try {
    loading.value = true
    const response = await axios.get(`/prompts/${route.params.id}`)
    prompt.value = response.data.prompt
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to load prompt'
    if (err.response?.status === 404) {
      router.push('/')
    }
  } finally {
    loading.value = false
  }
}

const handleLike = async () => {
  try {
    const response = await axios.post(`/prompts/${prompt.value.id}/like`)
    prompt.value.is_liked = response.data.is_liked
    prompt.value.likes_count = response.data.likes_count
  } catch (err) {
    if (err.response?.status === 401) {
      router.push('/login')
    }
  }
}

const handleFavorite = async () => {
  try {
    const response = await axios.post(`/prompts/${prompt.value.id}/favorite`)
    prompt.value.is_favorited = response.data.is_favorited
    prompt.value.favorites_count = response.data.favorites_count
  } catch (err) {
    if (err.response?.status === 401) {
      router.push('/login')
    }
  }
}

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(prompt.value.content)
    showCopySuccess.value = true
    setTimeout(() => {
      showCopySuccess.value = false
    }, 2000)
  } catch (err) {
    console.error('Failed to copy to clipboard:', err)
  }
}

onMounted(() => {
  fetchPrompt()
})
</script>

<style scoped>
/* 自定义滚动条样式 */
.scrollbar-thin::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.scrollbar-thumb-gray-700::-webkit-scrollbar-thumb {
  background-color: rgb(55, 65, 81);
  border-radius: 3px;
}

.scrollbar-track-transparent::-webkit-scrollbar-track {
  background-color: transparent;
}

/* 确保在移动设备上的触摸滚动体验 */
@media (hover: none) {
  .scrollbar-thin {
    -webkit-overflow-scrolling: touch;
  }
}
</style> 