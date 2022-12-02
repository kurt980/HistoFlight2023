import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home'
import About from '../views/About'
import Comments from '../views/Comments'
import NotFound from '../views/NotFound'
import Results from '../views/Results.vue'
import MyHisto_login from '../views/MyHisto_login.vue'
import MyHisto_afterlogin from '../views/MyHisto_afterlogin.vue'



Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: Home
  },
  {
    path: '/about',
    component: About
  },
  {
    path: '/comments',
    component: Comments
  },
  {
    path: '/results',
    component: Results
  },
  {
    path: '/login',
    component: MyHisto_login
  },
  {
    path: '/myaccount',
    component: MyHisto_afterlogin
  },
  {
    path: '/*',
    component: NotFound
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
