import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import AddPatientView from '../views/AddPatientView.vue'

const routes = [
  { path: '/', name: 'Login', component: LoginView },
  { path: '/dashboard', name: 'Dashboard', component: DashboardView },
  { path: '/add-patient', name: 'AddPatient', component: AddPatientView }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})