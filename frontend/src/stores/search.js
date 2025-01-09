import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSearchStore = defineStore('search', () => {
  const searchQuery = ref('')
  const isSearching = ref(false)

  function setSearchQuery(query) {
    searchQuery.value = query
  }

  function clearSearch() {
    searchQuery.value = ''
  }

  return {
    searchQuery,
    isSearching,
    setSearchQuery,
    clearSearch
  }
}) 