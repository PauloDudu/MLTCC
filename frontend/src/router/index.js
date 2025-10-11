import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Predict from '../views/Predict.vue'
import ClinicalCases from '../views/ClinicalCases.vue'
import ModelMetrics from '../views/ModelMetrics.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/predict',
    name: 'Predict',
    component: Predict
  },
  {
    path: '/cases',
    name: 'ClinicalCases',
    component: ClinicalCases
  },
  {
    path: '/metrics',
    name: 'ModelMetrics',
    component: ModelMetrics
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router