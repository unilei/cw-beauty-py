<template>
  <div class="max-w-4xl mx-auto space-y-8">
    <h1 class="text-2xl font-bold">Create New Prompt</h1>

    <!-- Error Alert -->
    <TransitionRoot appear :show="!!error" as="template">
      <div class="bg-red-500/10 border border-red-500/20 rounded-lg p-4 text-red-400">
        {{ error }}
      </div>
    </TransitionRoot>

    <form @submit.prevent="handleSubmit" class="space-y-6">
      <div>
        <label class="block text-sm font-medium text-gray-400 mb-1">Title</label>
        <input type="text" 
               v-model="form.title"
               required
               class="w-full px-4 py-2 bg-gray-800/50 border border-gray-700/50 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
      </div>

      <div>
        <Listbox v-model="form.language">
          <div class="relative">
            <ListboxLabel class="block text-sm font-medium text-gray-400 mb-1">Language</ListboxLabel>
            <ListboxButton class="relative w-full px-4 py-2 bg-gray-800/50 border border-gray-700/50 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-left">
              <span class="block truncate">
                {{ selectedLanguage ? selectedLanguage.name : 'Select a language' }}
              </span>
              <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
              </span>
            </ListboxButton>

            <Transition
              leave-active-class="transition duration-100 ease-in"
              leave-from-class="opacity-100"
              leave-to-class="opacity-0"
            >
              <ListboxOptions class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-gray-800 py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                <ListboxOption
                  v-for="language in store.languages"
                  :key="language.id"
                  :value="language.id"
                  v-slot="{ active, selected }"
                >
                  <li :class="[
                    active ? 'bg-blue-600 text-white' : 'text-gray-300',
                    'relative cursor-default select-none py-2 pl-10 pr-4'
                  ]">
                    <span :class="[
                      selected ? 'font-medium' : 'font-normal',
                      'block truncate'
                    ]">
                      {{ language.name }}
                    </span>
                    <span v-if="selected" class="absolute inset-y-0 left-0 flex items-center pl-3 text-blue-400">
                      <CheckIcon class="h-5 w-5" aria-hidden="true" />
                    </span>
                  </li>
                </ListboxOption>
              </ListboxOptions>
            </Transition>
          </div>
        </Listbox>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-400 mb-1">Content</label>
        <textarea v-model="form.content"
                  required
                  rows="10"
                  class="w-full px-4 py-2 bg-gray-800/50 border border-gray-700/50 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono"></textarea>
      </div>

      <div class="flex justify-end space-x-4">
        <router-link to="/"
                    class="px-4 py-2 text-gray-400 hover:text-gray-300">
          Cancel
        </router-link>
        <button type="submit"
                :disabled="loading"
                class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-gray-900 disabled:opacity-50 disabled:cursor-not-allowed">
          <span v-if="loading">Creating...</span>
          <span v-else>Create Prompt</span>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Listbox,
  ListboxButton,
  ListboxLabel,
  ListboxOption,
  ListboxOptions,
  TransitionRoot
} from '@headlessui/vue'
import { ChevronUpDownIcon, CheckIcon } from '@heroicons/vue/20/solid'
import axios from '../utils/axios'
import { usePromptsStore } from '../stores/prompts'

const store = usePromptsStore()
const router = useRouter()
const loading = ref(false)
const error = ref(null)
 
const form = ref({
  title: '',
  language: '',
  content: ''
})

const selectedLanguage = computed(() => {
  return store.languages.find(lang => lang.id === form.value.language)
})

const handleSubmit = async () => {
  try {
    loading.value = true
    error.value = null

    const response = await axios.post('/prompts', {
      title: form.value.title,
      language: form.value.language,
      content: form.value.content
    })

    router.push({
      name: 'prompt-detail',
      params: { id: response.data.prompt.id }
    })
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to create prompt'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await store.fetchLanguages()
})
</script> 

<script>
export default {
  name: 'NewPrompt',
  metaInfo: {
    title: 'Create New Prompt',
    meta: [
      { 
        name: 'description', 
        content: 'Create and share your own AI prompts with the community. Help others achieve better results with AI models.' 
      },
      { property: 'og:title', content: 'Create New Prompt | AI Prompt Platform' },
      { 
        property: 'og:description', 
        content: 'Create and share your own AI prompts with the community. Help others achieve better results with AI models.' 
      }
    ]
  }
}
</script> 