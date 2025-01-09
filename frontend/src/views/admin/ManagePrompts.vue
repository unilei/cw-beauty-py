<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold">Manage Prompts</h1>
      <div class="flex items-center space-x-4">
        <select
          v-model="statusFilter"
          class="px-4 py-2 bg-gray-800/50 border border-gray-700/50 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="all">All Status</option>
          <option value="PENDING">Pending</option>
          <option value="PUBLISHED">Published</option>
          <option value="REJECTED">Rejected</option>
        </select>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-12">
      <div
        class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"
      ></div>
    </div>

    <!-- Error State -->
    <div
      v-else-if="error"
      class="bg-red-500/10 border border-red-500/20 rounded-lg p-4 text-red-400"
    >
      {{ error }}
    </div>

    <!-- Prompts Table -->
    <div
      v-else
      class="bg-gray-800/50 backdrop-blur-sm rounded-lg border border-gray-700/50 overflow-hidden"
    >
      <table class="w-full">
        <thead>
          <tr class="border-b border-gray-700/50">
            <th
              class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider"
            >
              Title
            </th>
            <th
              class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider"
            >
              Author
            </th>
            <th
              class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider"
            >
              Language
            </th>
            <th
              class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider"
            >
              Status
            </th>
            <th
              class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider"
            >
              Created
            </th>
            <th
              class="px-6 py-3 text-right text-xs font-medium text-gray-400 uppercase tracking-wider"
            >
              Actions
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-700/50">
          <tr
            v-for="prompt in filteredPrompts"
            :key="prompt.id"
            class="hover:bg-gray-700/20"
          >
            <td class="px-6 py-4">
              <router-link
                :to="{ name: 'prompt-detail', params: { id: prompt.id } }"
                class="text-blue-400 hover:text-blue-300"
              >
                {{ prompt.title }}
              </router-link>
            </td>
            <td class="px-6 py-4">
              <div class="flex items-center space-x-2">
                <img
                  :src="prompt.author.avatar_url"
                  :alt="prompt.author.name"
                  class="w-6 h-6 rounded-full"
                />
                <span>{{ prompt.author.name }}</span>
              </div>
            </td>
            <td class="px-6 py-4">{{ prompt.language.name }}</td>
            <td class="px-6 py-4">
              <span
                :class="{
                  'px-2 py-1 text-xs rounded-full': true,
                  'bg-yellow-500/10 text-yellow-400':
                    prompt.status === 'PENDING',
                  'bg-green-500/10 text-green-400':
                    prompt.status === 'PUBLISHED',
                  'bg-red-500/10 text-red-400': prompt.status === 'REJECTED',
                }"
              >
                {{ prompt.status }}
              </span>
            </td>
            <td class="px-6 py-4 text-gray-400">
              {{ new Date(prompt.created_at).toLocaleDateString() }}
            </td>
            <td class="px-6 py-4 text-right space-x-2">
              <button
                v-if="prompt.status === 'PENDING'"
                @click="approvePrompt(prompt.id)"
                class="px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700"
              >
                Approve
              </button>
              <button
                v-if="prompt.status === 'PENDING'"
                @click="rejectPrompt(prompt.id)"
                class="px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700"
              >
                Reject
              </button>
              <button
                @click="confirmDelete(prompt)"
                class="px-3 py-1 bg-gray-600 text-white rounded hover:bg-gray-700"
              >
                Delete
              </button>
              <button
                @click="handleEdit(prompt)"
                class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                Edit
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 编辑对话框 -->
    <EditPromptDialog
      :visible="editDialogVisible"
      :prompt="currentPrompt"
      :languages="store.languages"
      :submitting="submitting"
      title="Edit Prompt"
      description="Update the prompt details below. All fields are required."
      :min-title-length="3"
      :min-content-length="10"
      :max-title-length="100"
      :max-content-length="1000"
      :content-rows="6"
      @submit="handleEditSubmit"
      @close="handleEditClose"
    />

    <!-- 删除确认对话框 -->
    <div
      v-if="showDeleteConfirm"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
    >
      <div class="bg-gray-800 p-6 rounded-lg shadow-lg max-w-md w-full mx-4">
        <h3 class="text-xl font-bold mb-4">Confirm Delete</h3>
        <p class="mb-6">
          Are you sure you want to delete the prompt "{{
            promptToDelete?.title
          }}"? This action cannot be undone.
        </p>
        <div class="flex justify-end space-x-4">
          <button
            @click="showDeleteConfirm = false"
            class="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700"
          >
            Cancel
          </button>
          <button
            @click="handleDelete"
            class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          >
            Delete
          </button>
        </div>
      </div>
    </div>

    <!-- 分页控件 -->
    <div v-if="!loading && !error" class="flex justify-center space-x-2">
      <button
        v-if="pagination.has_prev"
        @click="changePage(currentPage - 1)"
        class="px-3 py-1 bg-gray-700 rounded hover:bg-gray-600"
      >
        Previous
      </button>
      <span class="px-3 py-1">
        Page {{ currentPage }} of {{ pagination.pages }}
      </span>
      <button
        v-if="pagination.has_next"
        @click="changePage(currentPage + 1)"
        class="px-3 py-1 bg-gray-700 rounded hover:bg-gray-600"
      >
        Next
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import EditPromptDialog from "@/components/EditPromptDialog.vue";
import {
  getPrompts,
  updatePromptStatus,
  deletePrompt,
  updatePrompt,
} from "@/api/admin";

import { usePromptsStore } from "@/stores/prompts";

const store = usePromptsStore();
// 定义状态枚举
const PromptStatus = {
  PENDING: "PENDING",
  PUBLISHED: "PUBLISHED",
  REJECTED: "REJECTED",
};

const router = useRouter();
const loading = ref(true);
const error = ref(null);
const prompts = ref([]);
const statusFilter = ref("all");
const currentPage = ref(1);
const pagination = ref({
  page: 1,
  per_page: 20,
  total: 0,
  pages: 0,
  has_next: false,
  has_prev: false,
});

const showDeleteConfirm = ref(false);
const promptToDelete = ref(null);

const editDialogVisible = ref(false);
const submitting = ref(false);
const currentPromptId = ref(null);
const currentPrompt = ref(null);

const editForm = reactive({
  title: "",
  content: "",
  language: "",
});

const formErrors = reactive({
  title: "",
  content: "",
  language: "",
});

const validateForm = () => {
  let isValid = true;
  formErrors.title = "";
  formErrors.content = "";
  formErrors.language = "";

  if (!editForm.title.trim()) {
    formErrors.title = "Title is required";
    isValid = false;
  }

  if (!editForm.content.trim()) {
    formErrors.content = "Content is required";
    isValid = false;
  }

  if (!editForm.language) {
    formErrors.language = "Language is required";
    isValid = false;
  }

  return isValid;
};

const openEditDialog = (prompt) => {
  console.log(prompt);
  currentPromptId.value = prompt.id;
  currentPrompt.value = prompt;
  editForm.title = prompt.title;
  editForm.content = prompt.content;
  editForm.language = prompt.language.id; // Changed from _id to id
  editDialogVisible.value = true;
  formErrors.title = "";
  formErrors.content = "";
  formErrors.language = "";
};

const closeEditDialog = () => {
  editDialogVisible.value = false;
  currentPromptId.value = null;
  currentPrompt.value = null;
  editForm.title = "";
  editForm.content = "";
  editForm.language = "";
  formErrors.title = "";
  formErrors.content = "";
  formErrors.language = "";
};

const submitEdit = async (cleanForm) => {
  if (!validateForm()) return;

  submitting.value = true;
  try {
    await updatePrompt(currentPromptId.value, cleanForm);
    closeEditDialog();
    fetchPrompts();
  } catch (error) {
    console.error("Failed to update prompt:", error);
    // Handle error (show error message to user)
  } finally {
    submitting.value = false;
  }
};

const filteredPrompts = computed(() => {
  if (statusFilter.value === "all") {
    return prompts.value;
  }
  return prompts.value.filter((p) => p.status === statusFilter.value);
});

const fetchPrompts = async () => {
  try {
    loading.value = true;
    const response = await getPrompts({ page: currentPage.value });
    prompts.value = response.data.prompts;
    pagination.value = response.data.pagination;
  } catch (err) {
    error.value = err.response?.data?.message || "Failed to load prompts";
    if (err.response?.status === 403) {
      router.push("/");
    }
  } finally {
    loading.value = false;
  }
};

const changePage = async (page) => {
  currentPage.value = page;
  await fetchPrompts();
};

const approvePrompt = async (promptId) => {
  try {
    await updatePromptStatus(promptId, PromptStatus.PUBLISHED);
    await fetchPrompts();
  } catch (err) {
    error.value = err.response?.data?.message || "Failed to approve prompt";
  }
};

const rejectPrompt = async (promptId) => {
  try {
    await updatePromptStatus(promptId, PromptStatus.REJECTED);
    await fetchPrompts();
  } catch (err) {
    error.value = err.response?.data?.message || "Failed to reject prompt";
  }
};

const confirmDelete = (prompt) => {
  promptToDelete.value = prompt;
  showDeleteConfirm.value = true;
};

const handleDelete = async () => {
  try {
    await deletePrompt(promptToDelete.value.id);
    showDeleteConfirm.value = false;
    promptToDelete.value = null;
    await fetchPrompts();
  } catch (err) {
    error.value = err.response?.data?.message || "Failed to delete prompt";
  }
};

const handleEdit = (prompt) => {
  openEditDialog(prompt);
};

const handleEditSubmit = async (cleanForm) => {
  await submitEdit(cleanForm);
};

const handleEditClose = () => {
  closeEditDialog();
};

onMounted(async () => {
  if (!store.languages.length) {
    await store.fetchLanguages();
  }
  fetchPrompts();
});
</script>

<style scoped>
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
