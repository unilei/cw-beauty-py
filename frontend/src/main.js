import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createHead } from '@vueuse/head'
import router from './router'
import App from './App.vue'
import './style.css'

// Create app instance
const app = createApp(App)
const head = createHead()

// Use plugins
app.use(createPinia())
app.use(router)
app.use(head)

// Mount app
app.mount('#app')
