<template>
  <TransitionRoot appear :show="visible" as="template">
    <Dialog as="div" @close="handleClose" class="relative z-50">
      <TransitionChild
        as="template"
        enter="duration-300 ease-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="duration-200 ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black/30 backdrop-blur-sm" aria-hidden="true" />
      </TransitionChild>

      <div class="fixed inset-0 flex items-center justify-center p-4">
        <TransitionChild
          as="template"
          enter="duration-300 ease-out"
          enter-from="opacity-0 scale-95"
          enter-to="opacity-100 scale-100"
          leave="duration-200 ease-in"
          leave-from="opacity-100 scale-100"
          leave-to="opacity-0 scale-95"
        >
          <DialogPanel class="w-full max-w-xl bg-white dark:bg-gray-800 rounded-xl shadow-xl">
            <!-- Header -->
            <div class="flex items-center justify-between p-4 border-b dark:border-gray-700">
              <DialogTitle class="text-lg font-semibold dark:text-white">
                {{ title }}
              </DialogTitle>
              <button
                @click="handleClose"
                class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
              >
                <span class="sr-only">Close</span>
                <XMarkIcon class="w-5 h-5" />
              </button>
            </div>

            <!-- Form -->
            <form @submit.prevent="handleSubmit" class="p-4 space-y-4">
              <!-- Title field -->
              <div class="space-y-1">
                <label class="text-sm font-medium dark:text-gray-200">
                  {{ titleLabel }}
                </label>
                <input
                  v-model="form.title"
                  type="text"
                  :placeholder="titlePlaceholder"
                  class="w-full px-3 py-2 rounded-lg border dark:bg-gray-700 dark:border-gray-600 
                         focus:ring-2 focus:ring-blue-500 dark:text-white"
                  :class="{ 'border-red-500': errors.title }"
                />
                <TransitionGroup name="fade">
                  <p v-if="errors.title" class="text-sm text-red-500">
                    {{ errors.title }}
                  </p>
                  <p v-else-if="form.title" class="text-sm text-gray-500">
                    {{ form.title.length }}/{{ maxTitleLength }}
                  </p>
                </TransitionGroup>
              </div>

              <!-- Content field -->
              <div class="space-y-1">
                <label class="text-sm font-medium dark:text-gray-200">
                  {{ contentLabel }}
                </label>
                <textarea
                  v-model="form.content"
                  :rows="5"
                  :placeholder="contentPlaceholder"
                  class="w-full px-3 py-2 rounded-lg border dark:bg-gray-700 dark:border-gray-600 
                         focus:ring-2 focus:ring-blue-500 dark:text-white"
                  :class="{ 'border-red-500': errors.content }"
                ></textarea>
                <TransitionGroup name="fade">
                  <p v-if="errors.content" class="text-sm text-red-500">
                    {{ errors.content }}
                  </p>
                  <p v-else-if="form.content" class="text-sm text-gray-500">
                    {{ form.content.length }}/{{ maxContentLength }}
                  </p>
                </TransitionGroup>
              </div>

              <!-- Language field -->
              <div class="space-y-1">
                <label class="text-sm font-medium dark:text-gray-200">
                  {{ languageLabel }}
                </label>
                <Listbox v-model="form.language">
                  <div class="relative mt-1">
                    <ListboxButton
                      class="relative w-full py-2 pl-3 pr-10 text-left bg-white dark:bg-gray-700 
                             rounded-lg border dark:border-gray-600 cursor-pointer focus:outline-none 
                             focus:ring-2 focus:ring-blue-500"
                      :class="{ 'border-red-500': errors.language }"
                    >
                      <span class="block truncate dark:text-white">
                        {{ selectedLanguageName }}
                      </span>
                      <span class="absolute inset-y-0 right-0 flex items-center pr-2">
                        <ChevronUpDownIcon class="w-5 h-5 text-gray-400" aria-hidden="true" />
                      </span>
                    </ListboxButton>
                    <transition
                      leave-active-class="transition duration-100 ease-in"
                      leave-from-class="opacity-100"
                      leave-to-class="opacity-0"
                    >
                      <ListboxOptions
                        class="absolute w-full py-1 mt-1 overflow-auto text-base bg-white dark:bg-gray-700 
                               rounded-md shadow-lg max-h-60 ring-1 ring-black ring-opacity-5 focus:outline-none 
                               sm:text-sm z-10"
                      >
                        <ListboxOption
                          v-for="language in languages"
                          :key="language.id"
                          :value="language.id"
                          v-slot="{ active, selected }"
                        >
                          <li
                            :class="[
                              active ? 'text-white bg-blue-600' : 'text-gray-900 dark:text-white',
                              'relative cursor-default select-none py-2 pl-10 pr-4'
                            ]"
                          >
                            <span :class="[selected ? 'font-medium' : 'font-normal', 'block truncate']">
                              {{ language.name }}
                            </span>
                            <span
                              v-if="selected"
                              :class="[
                                active ? 'text-white' : 'text-blue-600',
                                'absolute inset-y-0 left-0 flex items-center pl-3'
                              ]"
                            >
                              <CheckIcon class="w-5 h-5" aria-hidden="true" />
                            </span>
                          </li>
                        </ListboxOption>
                      </ListboxOptions>
                    </transition>
                  </div>
                </Listbox>
                <p v-if="errors.language" class="text-sm text-red-500">
                  {{ errors.language }}
                </p>
              </div>

              <!-- Actions -->
              <div class="flex justify-end gap-3 pt-4 border-t dark:border-gray-700">
                <button
                  type="button"
                  @click="handleClose"
                  class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 
                         rounded-lg hover:bg-gray-50 dark:bg-gray-700 dark:text-gray-200 
                         dark:border-gray-600 dark:hover:bg-gray-600"
                  :disabled="submitting"
                >
                  {{ cancelButtonText }}
                </button>
                <button
                  type="submit"
                  :disabled="submitting || !isFormValid || !isFormChanged"
                  class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg 
                         hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {{ submitting ? loadingText : submitButtonText }}
                </button>
              </div>
            </form>
          </DialogPanel>
        </TransitionChild>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { ref, reactive, watch, computed } from 'vue'
import {
  Dialog,
  DialogPanel,
  DialogTitle,
  TransitionRoot,
  TransitionChild,
  Listbox,
  ListboxButton,
  ListboxOptions,
  ListboxOption
} from '@headlessui/vue'
import { XMarkIcon, ChevronUpDownIcon, CheckIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false,
  },
  prompt: {
    type: Object,
    default: () => ({}),
  },
  languages: {
    type: Array,
    default: () => [],
  },
  submitting: {
    type: Boolean,
    default: false,
  },
  title: {
    type: String,
    default: "Edit Prompt",
  },
  description: {
    type: String,
    default: "",
  },
  titleLabel: {
    type: String,
    default: "Title",
  },
  contentLabel: {
    type: String,
    default: "Content",
  },
  languageLabel: {
    type: String,
    default: "Language",
  },
  titlePlaceholder: {
    type: String,
    default: "Enter prompt title",
  },
  contentPlaceholder: {
    type: String,
    default: "Enter prompt content",
  },
  languagePlaceholder: {
    type: String,
    default: "Select a language",
  },
  submitButtonText: {
    type: String,
    default: "Save Changes",
  },
  cancelButtonText: {
    type: String,
    default: "Cancel",
  },
  loadingText: {
    type: String,
    default: "Saving...",
  },
  closeButtonLabel: {
    type: String,
    default: "Close dialog",
  },
  showCancelButton: {
    type: Boolean,
    default: true,
  },
  minTitleLength: {
    type: Number,
    default: 3,
  },
  minContentLength: {
    type: Number,
    default: 10,
  },
  maxTitleLength: {
    type: Number,
    default: 100,
  },
  maxContentLength: {
    type: Number,
    default: 1000,
  },
  contentRows: {
    type: Number,
    default: 5,
  },
});

const emit = defineEmits(["update:visible", "close", "submit"]);

const form = reactive({
  title: "",
  content: "",
  language: "",
});

const errors = reactive({
  title: "",
  content: "",
  language: "",
});

// Watch for changes in prompt prop
watch(
  () => props.prompt,
  (newPrompt) => {
    if (newPrompt) {
      form.title = newPrompt.title ?? '';
      form.content = newPrompt.content ?? '';
      form.language = newPrompt.language?.id ?? '';
      
      console.log('Prompt updated:', {
        newPrompt,
        formState: { ...form }
      });
    }
  },
  { immediate: true, deep: true }
);

const isFormChanged = computed(() => {
  const titleChanged = form.title !== (props.prompt?.title ?? '');
  const contentChanged = form.content !== (props.prompt?.content ?? '');
  const languageChanged = form.language !== (props.prompt?.language?.id ?? '');

  console.log('Checking form changes:', {
    titleChanged: {
      current: form.title,
      original: props.prompt?.title
    },
    contentChanged: {
      current: form.content,
      original: props.prompt?.content
    },
    languageChanged: {
      current: form.language,
      original: props.prompt?.language?.id
    }
  });

  return titleChanged || contentChanged || languageChanged;
});

// 添加实时验证
const validateTitle = (value) => {
  const trimmedValue = value.trim();
  if (!trimmedValue) {
    return "Title is required";
  }
  if (trimmedValue.length < props.minTitleLength) {
    return `Title must be at least ${props.minTitleLength} characters`;
  }
  if (value.length > props.maxTitleLength) {
    return `Title cannot exceed ${props.maxTitleLength} characters`;
  }
  if (/[<>{}[\]\\]/.test(value)) {
    return "Title contains invalid characters";
  }
  return "";
};

const validateContent = (value) => {
  const trimmedValue = value.trim();
  if (!trimmedValue) {
    return "Content is required";
  }
  if (trimmedValue.length < props.minContentLength) {
    return `Content must be at least ${props.minContentLength} characters`;
  }
  if (value.length > props.maxContentLength) {
    return `Content cannot exceed ${props.maxContentLength} characters`;
  }
  if (!value.includes("```") && value.length > 100) {
    return "Consider adding code examples using code blocks (```)";
  }
  return "";
};

const validateLanguage = (value) => {
  if (!value) {
    return "Language is required";
  }
  // 检查是否是有效的语言选项
  if (!props.languages.some((lang) => lang.id === value)) {
    return "Please select a valid language";
  }
  return "";
};

// 添加实时验证的 watch
watch(
  () => form.title,
  (newValue) => {
    errors.title = validateTitle(newValue);
  },
  { immediate: true }
);

watch(
  () => form.content,
  (newValue) => {
    errors.content = validateContent(newValue);
  },
  { immediate: true }
);

watch(
  () => form.language,
  (newValue) => {
    errors.language = validateLanguage(newValue);
  },
  { immediate: true }
);

const validateForm = () => {
  // 同时验证所有字段
  errors.title = validateTitle(form.title);
  errors.content = validateContent(form.content);
  errors.language = validateLanguage(form.language);

  // 检查是否有任何错误
  return !errors.title && !errors.content && !errors.language;
};

const handleSubmit = () => {
  if (validateForm()) {
    const cleanForm = {
      title: form.title,
      content: form.content,
      language: form.language,
    };
    
    console.log('Submitting form:', {
      formData: cleanForm,
      originalPrompt: props.prompt
    });
    
    emit("submit", cleanForm);
  }
};

const handleClose = () => {
  emit("update:visible", false);
  emit("close");

  // Reset form to original values
  form.title = props.prompt?.title || "";
  form.content = props.prompt?.content || "";
  form.language = props.prompt?.language?.id || "";

  // Trigger immediate validation after reset
  validateForm();
};

const isFormValid = computed(() => {
  return !errors.title && !errors.content && !errors.language &&
         form.title.trim() && form.content.trim() && form.language
})

// 添加计算属性用于显示选中的语言名称
const selectedLanguageName = computed(() => {
  const selectedLang = props.languages.find(lang => lang.id === form.language)
  return selectedLang ? selectedLang.name : props.languagePlaceholder
})
</script>

<style scoped>
/* 可以删除现有的 fade transitions，因为我们现在使用 Headless UI 的 TransitionChild */
</style>
