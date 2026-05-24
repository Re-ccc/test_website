import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './style.css'
import App from './App.vue'
import router from './router'

import {
  VideoPlay, VideoPause, FullScreen, Search, Bell, Message,
  ArrowDown, Star, Check, Coin, Share, Goods,
  Upload, VideoCamera, Delete, Picture,
  User, Loading,
} from '@element-plus/icons-vue'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ElementPlus)

const icons: Record<string, any> = {
  VideoPlay, VideoPause, FullScreen, Search, Bell, Message,
  ArrowDown, Star, Check, Coin, Share, Goods,
  Upload, VideoCamera, Delete, Picture,
  User, Loading,
}
for (const [name, component] of Object.entries(icons)) {
  app.component(name, component)
}

// 注册模板中使用的别名（Element Plus 2.x 图标库中没有这些名字）
app.component('Play', VideoPlay)
app.component('Pause', VideoPause)
app.component('Maximize', FullScreen)
app.component('Minimize', FullScreen)
app.component('ChevronDown', ArrowDown)
app.component('Heart', Star)
app.component('Coins', Coin)
app.component('Share2', Share)
app.component('ThumbsUp', Goods)
app.component('Video', VideoCamera)
app.component('UserPlus', User)

app.mount('#app')
