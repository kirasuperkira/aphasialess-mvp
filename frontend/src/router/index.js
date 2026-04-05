import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import AddPatientView from '../views/AddPatientView.vue'
import PatientDetailView from '../views/PatientDetailView.vue'
import TreatmentPlanEditorView from '../views/TreatmentPlanEditorView.vue'

const routes = [
  { path: '/', name: 'Login', component: LoginView },
  { path: '/dashboard', name: 'Dashboard', component: DashboardView },
  { path: '/add-patient', name: 'AddPatient', component: AddPatientView },
  { path: '/patient/:id', name: 'PatientDetail', component: PatientDetailView },
  { path: '/patient/:id/edit-plan', name: 'TreatmentPlanEditor', component: TreatmentPlanEditorView }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})