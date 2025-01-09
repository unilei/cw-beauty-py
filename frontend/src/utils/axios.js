import axios from 'axios'
import router from '../router'
import { API_BASE_URL } from '../config/api'
 console.log(API_BASE_URL)
// 创建axios实例
const instance = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  timeout: 30000, // 减少超时时间到10秒
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: true,
  // 添加重试配置
  retry: 3,
  retryDelay: 1000
})

// 请求拦截器
instance.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 添加重试逻辑的辅助函数
const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// 响应拦截器
instance.interceptors.response.use(
  response => response,
  async error => {
    const config = error.config;

    // 如果配置了重试，并且是网络错误或5xx错误
    if (config && config.retry && (
      error.code === 'ECONNABORTED' || 
      error.message === 'Network Error' ||
      (error.response && error.response.status >= 500)
    )) {
      config.__retryCount = config.__retryCount || 0;

      if (config.__retryCount < config.retry) {
        config.__retryCount += 1;
        await wait(config.retryDelay || 1000);
        return instance(config);
      }
    }

    if (error.code === 'ECONNABORTED' || error.message === 'Network Error') {
      console.error('Network timeout or error:', error)
      return Promise.reject({
        response: {
          data: {
            message: 'Network timeout or error. Please try again.'
          }
        }
      })
    }

    if (error.response) {
      switch (error.response.status) {
        case 401:
          // 未授权，清除 token 并跳转到登录页面
          localStorage.removeItem('token')
          router.push('/login')
          break
        case 403:
          // 权限不足
          console.error('Permission denied')
          break
        case 500:
          // 服务器错误
          console.error('Server error')
          break
        default:
          console.error(error.response.data.message || 'Error')
      }
    }
    return Promise.reject(error)
  }
)

// 添加请求取消功能
export const createCancelToken = () => {
  return axios.CancelToken.source();
}

export default instance 