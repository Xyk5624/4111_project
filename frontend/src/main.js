import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Element from 'element-plus'
import VueCookies from 'vue3-cookies'
import axios from 'axios'
import 'element-plus/dist/index.css'
import * as ElIconModules from '@element-plus/icons'


axios.defaults.withCredentials = true

const app=createApp(App)
app.use(VueCookies)
app.use(Element)
app.use(router)
router.beforeEach((to, from, next) => {
  /* 路由发生变化修改页面title */
  if (to.meta.title) {
    document.title = to.meta.title
  }
  next()
})
app.mount('#app')

// 统一注册el-icon图标
for (const iconName in ElIconModules) {
  if (Reflect.has(ElIconModules, iconName)) {
      const item = ElIconModules[iconName];
      app.component(iconName, item)
  }
}




