import Vue from 'vue'
import VueRouter from 'vue-router'
import InputData from '../views/InputData.vue'
import ShowResult from '../views/ShowResult.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'InputData',
    component: InputData
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
