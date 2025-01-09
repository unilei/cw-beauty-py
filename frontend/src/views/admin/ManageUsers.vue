<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold">Manage Users</h1>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-500/10 border border-red-500/20 rounded-lg p-4 text-red-400">
      {{ error }}
    </div>

    <!-- Users Table -->
    <div v-else class="bg-gray-800/50 backdrop-blur-sm rounded-lg border border-gray-700/50 overflow-hidden">
      <table class="w-full">
        <thead>
          <tr class="border-b border-gray-700/50">
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">User</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Email</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Role</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Created</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-400 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-700/50">
          <tr v-for="user in users" :key="user.id" class="hover:bg-gray-700/20">
            <td class="px-6 py-4">
              <div class="flex items-center space-x-2">
                <img :src="user.avatar_url" 
                     :alt="user.name"
                     class="w-6 h-6 rounded-full">
                <span>{{ user.name }}</span>
              </div>
            </td>
            <td class="px-6 py-4">{{ user.email }}</td>
            <td class="px-6 py-4">
              <span :class="{
                'px-2 py-1 text-xs rounded-full': true,
                'bg-blue-500/10 text-blue-400': user.role === UserRole.USER,
                'bg-red-500/10 text-red-400': user.role === UserRole.ADMIN
              }">
                {{ user.role }}
              </span>
            </td>
            <td class="px-6 py-4 text-gray-400">
              {{ new Date(user.created_at).toLocaleDateString() }}
            </td>
            <td class="px-6 py-4 text-right space-x-2">
              <button v-if="user.role === UserRole.USER"
                      @click="promoteToAdmin(user.id)"
                      class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700">
                Make Admin
              </button>
              <button v-if="user.role === UserRole.ADMIN && user.id !== currentUser.id"
                      @click="demoteToUser(user.id)"
                      class="px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700">
                Remove Admin
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getUsers, updateUserRole } from '@/api/admin'
import { useUserStore } from '@/stores/user'

// 定义角色枚举
const UserRole = {
  USER: 'USER',
  ADMIN: 'ADMIN'
}

const userStore = useUserStore()
const currentUser = userStore.user

const users = ref([])
const loading = ref(true)
const error = ref(null)

const fetchUsers = async () => {
  try {
    loading.value = true
    const response = await getUsers()
    users.value = response.data.users
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to load users'
  } finally {
    loading.value = false
  }
}

const promoteToAdmin = async (userId) => {
  try {
    await updateUserRole(userId, UserRole.ADMIN)
    await fetchUsers()
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to promote user'
  }
}

const demoteToUser = async (userId) => {
  try {
    await updateUserRole(userId, UserRole.USER)
    await fetchUsers()
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to demote user'
  }
}

onMounted(() => {
  fetchUsers()
})
</script> 