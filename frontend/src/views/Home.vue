<template>
  <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
    <!-- Sidebar -->
    <div class="lg:col-span-3">
      <!-- 移动端的语言选择器切换按钮 -->
      <button 
        @click="showMobileFilter = !showMobileFilter"
        class="w-full mb-4 p-3 bg-gray-800/30 rounded-lg lg:hidden flex items-center justify-between"
      >
        <span>Filter by Language</span>
        <span class="transform transition-transform" :class="{ 'rotate-180': showMobileFilter }">
          ▼
        </span>
      </button>

      <!-- 语言筛选侧边栏 -->
      <div
        :class="{
          'hidden lg:block': !showMobileFilter,
          'block': showMobileFilter
        }"
        class="space-y-2 bg-gray-800/30 backdrop-blur-sm p-4 rounded-lg border border-gray-700/50 lg:sticky lg:top-24 overflow-y-auto max-h-[calc(100vh-10rem)]"
      >
        <h3 class="text-lg font-semibold mb-4 text-gray-300">Categories</h3>
        <button
          @click="store.setCurrentLanguage(null)"
          class="flex justify-between items-center w-full p-2 hover:bg-gray-700/50 rounded-lg transition-all duration-200"
          :class="{
            'bg-blue-500/10 text-blue-400 font-medium': !store.currentLanguage,
          }"
        >
          <span>All</span>
          <span
            class="text-xs px-2 py-1 rounded-full"
            :class="{
              'bg-blue-500/20': !store.currentLanguage,
              'bg-gray-700/50': store.currentLanguage,
            }"
          >
            {{ store.totalPrompts }}
          </span>
        </button>
        <button
          v-for="language in store.languages"
          :key="language.id"
          @click="store.setCurrentLanguage(language)"
          class="flex justify-between items-center w-full p-2 hover:bg-gray-700/50 rounded-lg transition-all duration-200"
          :class="{
            'bg-blue-500/10 text-blue-400 font-medium':
              store.currentLanguage?.id === language.id,
          }"
        >
          <span>{{ language.name }}</span>
          <span
            class="text-xs px-2 py-1 rounded-full"
            :class="{
              'bg-blue-500/20': store.currentLanguage?.id === language.id,
              'bg-gray-700/50': store.currentLanguage?.id !== language.id,
            }"
          >
            {{ language.prompts_count }}
          </span>
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="lg:col-span-9">
      <div class="flex justify-between items-center mb-8 overflow-x-auto">
        <div class="space-x-2 sm:space-x-4 flex-nowrap">
          <button
            @click="store.setCurrentType('all')"
            class="px-4 sm:px-6 py-2 rounded-lg transition-all duration-200 hover:bg-gray-700/50 whitespace-nowrap"
            :class="{ 'bg-gray-800': store.currentType === 'all' }"
          >
            All
          </button>
          <button
            @click="store.setCurrentType('popular')"
            class="px-4 sm:px-6 py-2 rounded-lg transition-all duration-200 hover:bg-gray-700/50 whitespace-nowrap"
            :class="{ 'bg-gray-800': store.currentType === 'popular' }"
          >
            Popular
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="store.loading" class="flex justify-center items-center py-12">
        <div
          class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"
        ></div>
      </div>

      <!-- Error State -->
      <div v-else-if="store.error" class="text-red-500 text-center py-12">
        {{ store.error }}
      </div>

      <!-- Prompts Grid -->
      <div v-if="!store.loading && !store.error" class="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
        <PromptCard
          v-for="prompt in filteredPrompts"
          :key="prompt.id"
          :prompt="prompt"
          @like="store.toggleLike"
          @favorite="store.toggleFavorite"
        />
      </div>

      <!-- Pagination -->
      <div
        v-if="store.pagination"
        class="mt-8 flex justify-center items-center space-x-4"
      >
        <button
          v-if="store.pagination.has_prev"
          @click="loadPage(store.pagination.page - 1)"
          class="px-4 py-2 bg-gray-800 rounded hover:bg-gray-700 transition-colors"
        >
          Previous
        </button>

        <!-- 页码显示 -->
        <div class="flex items-center space-x-2">
          <span class="text-gray-400">
            Page {{ store.pagination.page }} of {{ store.pagination.total_pages }}
          </span>
          <span class="text-gray-500">
            ({{ store.filteredPrompts }} / {{ store.totalPrompts }} items)
          </span>
        </div>

        <button
          v-if="store.pagination.has_next"
          @click="loadPage(store.pagination.page + 1)"
          class="px-4 py-2 bg-gray-800 rounded hover:bg-gray-700 transition-colors"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { onMounted } from "vue";
import { usePromptsStore } from "../stores/prompts";
import PromptCard from "../components/PromptCard.vue";
import { useSearchStore } from '../stores/search'
import { useHead } from '@vueuse/head'

const store = usePromptsStore();
const searchStore = useSearchStore()
const perPage = 10;
const showMobileFilter = ref(false);

const loadPage = (page) => {
  store.fetchPrompts({
    page,
    per_page: perPage,
    language: store.currentLanguage?.slug,
    type: store.currentType,
  });
};

// 根据搜索关键词过滤提示
const filteredPrompts = computed(() => {
  if (!searchStore.searchQuery) {
    return store.prompts || []
  }
  
  const query = searchStore.searchQuery.toLowerCase()
  return store.prompts.filter(prompt => {
    if (!prompt) return false
    
    return (
      (prompt.title && prompt.title.toLowerCase().includes(query)) ||
      (prompt.description && prompt.description.toLowerCase().includes(query)) ||
      (prompt.tags && Array.isArray(prompt.tags) && prompt.tags.some(tag => 
        tag && typeof tag === 'string' && tag.toLowerCase().includes(query)
      ))
    )
  })
})

// 添加对搜索查询的监听
watch(() => searchStore.searchQuery, (newQuery) => {
  if (!newQuery) {
    // 当搜索查询被清空时，重新加载提示
    loadPage(1)
  }
})

onMounted(async () => {
  await Promise.all([
    store.fetchPrompts({ per_page: perPage }),
    store.fetchLanguages(),
    store.fetchStats(),  // 获取统计信息
  ]);
});

useHead({
  title: 'Home',
  meta: [
    { 
      name: 'description', 
      content: 'Browse our collection of community-curated Cursor AI prompts. Find the perfect prompts for code generation, refactoring, and documentation.' 
    },
    { property: 'og:title', content: 'cursor.beauty - Browse Cursor AI Prompts' },
    { 
      property: 'og:description', 
      content: 'Discover trending and popular Cursor AI prompts. Share your own prompts and help others code more efficiently with Cursor AI.' 
    }
  ]
})
</script>
