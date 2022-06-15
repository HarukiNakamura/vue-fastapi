import Vue from 'vue'
import VueRouter from 'vue-router'
import InputEle from '../views/InputEle.vue'
import ShowResult from '../views/ShowResult.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'InputEle',
    component: InputEle
  },
  {
    path: '/result',
    name: 'ShowResult',
    component: ShowResult
  },

]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
