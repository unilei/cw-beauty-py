import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)

  function setUser(newUser) {
    user.value = newUser
  }

  function clearUser() {
    user.value = null
  }

  return {
    user,
    setUser,
    clearUser
  }
}) 