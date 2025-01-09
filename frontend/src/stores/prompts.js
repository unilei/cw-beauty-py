import { defineStore } from 'pinia'
import axios from '../utils/axios'

export const usePromptsStore = defineStore('prompts', {
  state: () => ({
    prompts: [],
    languages: [],
    currentLanguage: null,
    currentType: 'all',
    loading: false,
    error: null,
    pagination: null,
    stats: {
      total_count: 0,
      language_stats: []
    }
  }),

  getters: {
    totalPrompts: (state) => state.stats.total_count,
    filteredPrompts: (state) => state.pagination?.total || 0,
    hasMore: (state) => state.pagination?.has_next || false,
    currentPage: (state) => state.pagination?.page || 1,
    totalPages: (state) => state.pagination?.total_pages || 1
  },

  actions: {
    async fetchStats() {
      try {
        const { data } = await axios.get('/prompts/stats');
        this.stats = data;
      } catch (error) {
        console.error('Error fetching prompts stats:', error);
      }
    },

    async fetchPrompts({ page = 1, language = null, type = 'all', per_page = 12 } = {}) {
      this.loading = true;
      this.error = null;
      try {
        const params = {
          page,
          type,
          per_page,
          language: language?.slug || null
        };

        const { data } = await axios.get('/prompts', { params });
        this.prompts = data.prompts;
        this.pagination = data.pagination;
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to fetch prompts';
        console.error('Error fetching prompts:', error);
      } finally {
        this.loading = false;
      }
    },

    async fetchLanguages() {
      try {
        const { data } = await axios.get('/languages');
        this.languages = data.languages;
      } catch (error) {
        console.error('Error fetching languages:', error);
      }
    },

    async toggleLike(promptId) {
      try {
        const { data } = await axios.post(`/prompts/${promptId}/like`);
        const prompt = this.prompts.find(p => p.id === promptId);
        if (prompt) {
          prompt.is_liked = data.is_liked;
          prompt.likes_count = data.likes_count;
        }
      } catch (error) {
        console.error('Error toggling like:', error);
      }
    },

    async toggleFavorite(promptId) {
      try {
        const { data } = await axios.post(`/prompts/${promptId}/favorite`);
        const prompt = this.prompts.find(p => p.id === promptId);
        if (prompt) {
          prompt.is_favorited = data.is_favorited;
          prompt.favorites_count = data.favorites_count;
        }
      } catch (error) {
        console.error('Error toggling favorite:', error);
      }
    },

    async updatePrompt(promptId, data) {
      try {
        const response = await axios.put(`/prompts/${promptId}`, data);
        // Update the prompt in the local state
        const index = this.prompts.findIndex(p => p.id === promptId);
        if (index !== -1) {
          this.prompts[index] = response.data.prompt;
        }
        return response.data;
      } catch (error) {
        console.error('Error updating prompt:', error);
        throw error;
      }
    },

    setCurrentLanguage(language) {
      this.currentLanguage = language;
      this.fetchPrompts({ language, type: this.currentType, page: 1 });
    },

    setCurrentType(type) {
      this.currentType = type;
      this.fetchPrompts({ language: this.currentLanguage, type, page: 1 });
    }
  }
})