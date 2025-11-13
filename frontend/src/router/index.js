import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Predict from '../views/Predict.vue'
import ClinicalCases from '../views/ClinicalCases.vue'
import ModelMetrics from '../views/ModelMetrics.vue'
import Login from '../views/Login.vue'
import Historico from '../views/Historico.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/predict',
    name: 'Predict',
    component: Predict,
    meta: { requiresAuth: true }
  },
  {
    path: '/cases',
    name: 'ClinicalCases',
    component: ClinicalCases,
    meta: { requiresAuth: true }
  },
  {
    path: '/metrics',
    name: 'ModelMetrics',
    component: ModelMetrics,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/historico',
    name: 'Historico',
    component: Historico,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const token = localStorage.getItem('token')
  
  if (to.meta.requiresAuth) {
    if (!token) {
      next('/login')
      return
    }
    
    try {
      const response = await fetch(`${process.env.VUE_APP_API_URL}/historico`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      
      if (response.status === 401) {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        next('/login')
        return
      }
    } catch (error) {
      console.error('Erro ao verificar token:', error)
    }
  }
  
  if (to.path === '/login' && token) {
    next('/home')
  } else {
    next()
  }
})

export default router