import axios from '../utils/axios'

// 获取所有提示词
export const getPrompts = ({ page = 1, per_page = 20 } = {}) => {
  return axios.get('/admin/prompts', {
    params: { page, per_page }
  })
}

// 更新提示词状态
export const updatePromptStatus = (promptId, status) => {
  return axios.put(`/admin/prompts/${promptId}/status`, { status })
}

// 删除提示词
export const deletePrompt = (promptId) => {
  return axios.delete(`/admin/prompts/${promptId}`)
}

// 编辑提示词
/**
 * 更新提示词（管理员）
 * @param {string} promptId - 提示词ID
 * @param {Object} data - 提示词数据
 * @returns {Promise}
 */
export function updatePrompt(promptId, data) {
  return axios.put(`/admin/prompts/${promptId}`, data)
}

// 获取所有用户
export const getUsers = () => {
  return axios.get('/admin/users')
}

// 更新用户角色
export const updateUserRole = (userId, role) => {
  return axios.put(`/admin/users/${userId}/role`, { role })
}