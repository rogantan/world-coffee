import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'
import router from './router'
// import './assets/css/app.css'
import './assets/css/index.css'
import 'vue-datepicker-next/index.css';
import 'vue-datepicker-next/locale/ru.js';

const app = createApp(App)

const pinia = createPinia()

app.use(pinia) 
app.use(router)
app.mount('#app')