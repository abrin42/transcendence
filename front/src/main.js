import { createApp } from 'vue'
import 'bootstrap/dist/css/bootstrap.css'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import './assets/main.scss';
import i18n from './i18n.js'

const app = createApp(App)

app.use(createPinia())
app.use(i18n)
app.use(router)

app.mount('#app')
