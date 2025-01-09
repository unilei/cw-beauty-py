<template>
  <div class="max-w-3xl mx-auto">
    <div class="bg-gray-800/50 backdrop-blur-sm rounded-lg p-8 border border-gray-700/50">
      <h1 class="text-2xl font-bold text-white mb-6">Settings</h1>

      <form @submit.prevent="saveSettings" class="space-y-8">
        <!-- 基本信息 -->
        <div class="space-y-6">
          <h2 class="text-lg font-medium text-gray-200">Basic Information</h2>
          
          <!-- 头像 -->
          <div class="flex items-center space-x-6">
            <img :src="form.avatar_url || 'https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp'"
                 :alt="form.name"
                 class="w-20 h-20 rounded-full">
            <div>
              <label class="block text-sm font-medium text-gray-300">Profile Photo</label>
              <div class="mt-1 flex items-center space-x-4">
                <button type="button"
                        class="px-4 py-2 bg-gray-700 text-gray-300 rounded-lg hover:bg-gray-600 transition-colors"
                        @click="$refs.fileInput.click()">
                  Change
                </button>
                <button v-if="form.avatar_url"
                        type="button"
                        class="text-gray-400 hover:text-gray-300"
                        @click="removeAvatar">
                  Remove
                </button>
                <input ref="fileInput"
                       type="file"
                       class="hidden"
                       accept="image/*"
                       @change="handleFileChange">
              </div>
            </div>
          </div>

          <!-- 名称 -->
          <div>
            <label for="name" class="block text-sm font-medium text-gray-300">Name</label>
            <input type="text"
                   id="name"
                   v-model="form.name"
                   class="mt-1 block w-full bg-gray-900/50 border border-gray-700 rounded-lg px-4 py-2 text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                   required>
          </div>

          <!-- 邮箱 -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-300">Email</label>
            <input type="email"
                   id="email"
                   v-model="form.email"
                   class="mt-1 block w-full bg-gray-900/50 border border-gray-700 rounded-lg px-4 py-2 text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                   required>
          </div>
        </div>

        <!-- 修改密码 -->
        <div class="space-y-6">
          <h2 class="text-lg font-medium text-gray-200">Change Password</h2>
          
          <div>
            <label for="current_password" class="block text-sm font-medium text-gray-300">Current Password</label>
            <input type="password"
                   id="current_password"
                   v-model="form.current_password"
                   class="mt-1 block w-full bg-gray-900/50 border border-gray-700 rounded-lg px-4 py-2 text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent">
          </div>

          <div>
            <label for="new_password" class="block text-sm font-medium text-gray-300">New Password</label>
            <input type="password"
                   id="new_password"
                   v-model="form.new_password"
                   class="mt-1 block w-full bg-gray-900/50 border border-gray-700 rounded-lg px-4 py-2 text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent">
          </div>

          <div>
            <label for="confirm_password" class="block text-sm font-medium text-gray-300">Confirm New Password</label>
            <input type="password"
                   id="confirm_password"
                   v-model="form.confirm_password"
                   class="mt-1 block w-full bg-gray-900/50 border border-gray-700 rounded-lg px-4 py-2 text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent">
          </div>
        </div>

        <!-- 提交按钮 -->
        <div class="flex justify-end space-x-4">
          <router-link to="/profile"
                      class="px-4 py-2 border border-gray-600 rounded-lg text-gray-300 hover:bg-gray-700 transition-colors">
            Cancel
          </router-link>
          <button type="submit"
                  class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
                  :disabled="loading">
            <span v-if="loading" class="flex items-center space-x-2">
              <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              <span>Saving...</span>
            </span>
            <span v-else>Save Changes</span>
          </button>
        </div>

        <!-- 错误提示 -->
        <div v-if="error" class="text-red-500 text-sm">
          {{ error }}
        </div>

        <!-- 成功提示 -->
        <div v-if="success" class="text-green-500 text-sm">
          {{ success }}
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const form = ref({
  name: '',
  email: '',
  avatar_url: '',
  current_password: '',
  new_password: '',
  confirm_password: ''
})

const loading = ref(false)
const error = ref(null)
const success = ref(null)
const fileInput = ref(null)

const fetchUser = async () => {
  try {
    const { data } = await axios.get('/api/v1/user/profile')
    form.value.name = data.user.name
    form.value.email = data.user.email
    form.value.avatar_url = data.user.avatar_url
  } catch (err) {
    console.error('Failed to fetch user:', err)
    error.value = 'Failed to load user profile'
  }
}

const handleFileChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('avatar', file)

  try {
    loading.value = true
    const { data } = await axios.post('/api/v1/user/avatar', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    form.value.avatar_url = data.avatar_url
    success.value = 'Avatar updated successfully'
  } catch (err) {
    console.error('Failed to upload avatar:', err)
    error.value = err.response?.data?.message || 'Failed to upload avatar'
  } finally {
    loading.value = false
  }
}

const removeAvatar = async () => {
  try {
    loading.value = true
    await axios.delete('/api/v1/user/avatar')
    form.value.avatar_url = null
    success.value = 'Avatar removed successfully'
  } catch (err) {
    console.error('Failed to remove avatar:', err)
    error.value = err.response?.data?.message || 'Failed to remove avatar'
  } finally {
    loading.value = false
  }
}

const saveSettings = async () => {
  // 验证新密码
  if (form.value.new_password && form.value.new_password !== form.value.confirm_password) {
    error.value = 'New passwords do not match'
    return
  }

  loading.value = true
  error.value = null
  success.value = null

  try {
    const { data } = await axios.put('/api/v1/user/settings', {
      name: form.value.name,
      email: form.value.email,
      current_password: form.value.current_password,
      new_password: form.value.new_password
    })
    
    // 清除密码字段
    form.value.current_password = ''
    form.value.new_password = ''
    form.value.confirm_password = ''
    
    success.value = 'Settings updated successfully'
  } catch (err) {
    console.error('Failed to update settings:', err)
    error.value = err.response?.data?.message || 'Failed to update settings'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchUser()
})
</script> 