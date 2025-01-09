import axios from '../utils/axios'

export const login = (data) => {
  return axios.post('/auth/login', data)
}

export const register = (data) => {
  return axios.post('/auth/register', data)
}

export const logout = () => {
  return axios.post('/auth/logout')
}

export const getCurrentUser = () => {
  return axios.get('/auth/me')
} 