<template>
  <div class="bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700/50 hover:border-gray-600/50 transition-colors">
    

    <!-- 内容区域 -->
    <div class="relative">
      <div :class="{ 'h-[250px] overflow-y-auto': !isExpanded }" 
           class="text-gray-400 pr-8 custom-scrollbar">
        <pre class="whitespace-pre-wrap font-mono text-sm">{{ prompt.content }}</pre>
      </div>
      
      <!-- 未展开时的渐变遮罩 -->
      <div v-if="!isExpanded && shouldShowExpandButton" 
           class="absolute bottom-0 left-0 right-0 h-12 bg-gradient-to-t from-gray-800/50 to-transparent pointer-events-none">
      </div>

      <!-- 复制按钮 -->
      <button @click="copyContent"
              class="absolute top-0 right-0 p-2 text-gray-400 hover:text-primary-400 transition-colors"
              :class="{ 'text-green-400': copied }"
              :title="copied ? '已复制!' : '复制内容'">
        <svg v-if="!copied" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
      </button>
      <button @click="handleLike" 
                class="absolute top-10 right-0 p-2 text-gray-400 hover:text-primary-400 transition-colors"
                :class="{ 'text-red-500': prompt.is_liked, 'animate-pulse': isLiking }"
                :title="prompt.is_liked ? '取消点赞' : '点赞'">
          <svg xmlns="http://www.w3.org/2000/svg"
               class="h-5 w-5"
               :class="{ 'fill-current': prompt.is_liked }"
               fill="none"
               viewBox="0 0 24 24"
               stroke="currentColor">
            <path stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
          </svg>
          <span>{{ prompt.likes_count }}</span>
        </button>
        <button @click="handleFavorite"
                class="absolute top-24 right-0 p-2 text-gray-400 hover:text-primary-400 transition-colors"
                :class="{ 'text-yellow-500': prompt.is_favorited, 'animate-pulse': isFavoriting }"
                :title="prompt.is_favorited ? '取消收藏' : '收藏'">
          <svg xmlns="http://www.w3.org/2000/svg"
               class="h-5 w-5"
               :class="{ 'fill-current': prompt.is_favorited }"
               fill="none"
               viewBox="0 0 24 24"
               stroke="currentColor">
            <path stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
          </svg>
          <span>{{ prompt.favorites_count }}</span>
        </button>

    </div>

    <!-- 查看全部按钮 -->
    <button v-if="shouldShowExpandButton"
            @click="goToDetail"
            class="mt-2 text-primary-400 hover:text-primary-300 transition-colors text-sm">
       Show More
    </button>

    <!-- 标题和元数据区域 -->
    <div class="mt-2">
      <div class="min-w-0 flex-1">
        <div class="group relative">
          <router-link :to="{ name: 'prompt-detail', params: { id: prompt.id }}" 
                      class="text-sm font-[300] hover:text-primary-400 transition-colors block truncate"
                      @click="handleTitleClick"
                      @mouseenter="showFullTitle = true"
                      @mouseleave="showFullTitle = false">
            {{ prompt.title }}
          </router-link>
          <!-- 标题提示框 -->
          <div v-show="showFullTitle && isTitleTruncated"
               class="absolute z-[9999] left-0 bottom-full mt-1 p-2 bg-gray-800 rounded-lg shadow-lg border border-gray-700 max-w-lg break-words">
            {{ prompt.title }}
          </div>
        </div>
        <div class="flex items-center space-x-2 text-xs text-gray-400 mt-2 font-[300]">
          <div class="flex items-center space-x-2">
            <img :src="prompt.author.avatar_url"
                 :alt="prompt.author.name"
                 class="w-4 h-4 rounded-full">
            <span>{{ prompt.author.name }}</span>
          </div>
          <span>·</span>
          <router-link :to="{ name: 'home', query: { language: prompt.language.slug }}"
                      class="hover:text-primary-400 transition-colors">
            {{ prompt.language.name }}
          </router-link>
          <span>·</span>
          <span>{{ new Date(prompt.created_at).toLocaleDateString() }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  prompt: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['like', 'favorite'])
const router = useRouter()

const isExpanded = ref(false)
const copied = ref(false)
const showFullTitle = ref(false)
const isLiking = ref(false)
const isFavoriting = ref(false)

// 计算是否需要显示展开按钮
const shouldShowExpandButton = computed(() => {
  const lines = props.prompt.content.split('\n').length
  return lines > 3
})

// 计算标题是否被截断
const isTitleTruncated = computed(() => {
  const titleElement = document.querySelector('.truncate')
  if (titleElement) {
    return titleElement.scrollWidth > titleElement.clientWidth
  }
  return false
})

const handleTitleClick = (event) => {
  // 在移动端，点击时切换显示状态
  if (window.matchMedia('(hover: none)').matches && isTitleTruncated.value) {
    event.preventDefault() // 阻止路由跳转
    showFullTitle.value = !showFullTitle.value
  }
}

const handleLike = async () => {
  if (!localStorage.getItem('token')) {
    router.push('/login')
    return
  }
  isLiking.value = true
  try {
    await emit('like', props.prompt.id)
  } finally {
    setTimeout(() => {
      isLiking.value = false
    }, 500)
  }
}

const handleFavorite = async () => {
  if (!localStorage.getItem('token')) {
    router.push('/login')
    return
  }
  isFavoriting.value = true
  try {
    await emit('favorite', props.prompt.id)
  } finally {
    setTimeout(() => {
      isFavoriting.value = false
    }, 500)
  }
}

const toggleExpand = () => {
  isExpanded.value = !isExpanded.value
}

const copyContent = async () => {
  try {
    await navigator.clipboard.writeText(props.prompt.content)
    copied.value = true
    triggerHaptic()
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (err) {
    console.error('Failed to copy:', err)
  }
}

const goToDetail = () => {
  router.push({
    name: 'prompt-detail',
    params: { id: props.prompt.id }
  })
}

// 添加触觉反馈（仅在支持的设备上）
const triggerHaptic = () => {
  if ('vibrate' in navigator) {
    navigator.vibrate(50)
  }
}

// 添加触摸事件处理
let touchTimeout = null
const handleTouchStart = () => {
  touchTimeout = setTimeout(() => {
    showFullTitle.value = true
  }, 500)
}

const handleTouchEnd = () => {
  clearTimeout(touchTimeout)
  setTimeout(() => {
    showFullTitle.value = false
  }, 1500)
}

onMounted(() => {
  const titleElement = document.querySelector('.truncate')
  if (titleElement) {
    titleElement.addEventListener('touchstart', handleTouchStart)
    titleElement.addEventListener('touchend', handleTouchEnd)
    titleElement.addEventListener('touchcancel', handleTouchEnd)
  }
})

onUnmounted(() => {
  const titleElement = document.querySelector('.truncate')
  if (titleElement) {
    titleElement.removeEventListener('touchstart', handleTouchStart)
    titleElement.removeEventListener('touchend', handleTouchEnd)
    titleElement.removeEventListener('touchcancel', handleTouchEnd)
  }
})
</script>

<style>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 自定义滚动条样式 */
.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: rgba(156, 163, 175, 0.3) transparent;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.3);
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: rgba(156, 163, 175, 0.5);
}

/* 添加媒体查询来处理移动端的悬停 */
@media (hover: hover) {
  .group:hover .group-hover\:block {
    display: block;
  }
}

@media (hover: none) {
  .group:hover .group-hover\:block {
    display: none;
  }
}
</style> 