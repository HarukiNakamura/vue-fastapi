import Vue from 'vue'
import VueRouter from 'vue-router'
import InputEle from '@/components/InputEle.vue'
import ShowResult from '@/components/ShowResult.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: InputEle
  },
  {
    path: '/result',
    name: 'result',
    component: ShowResult
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router

