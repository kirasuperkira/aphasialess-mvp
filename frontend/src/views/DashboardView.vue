<template>
  <div class="dashboard">
    <header class="header">
      <h2>Главная панель / Список пациентов</h2>
      <button class="logout" @click="logout">Выйти</button>
    </header>

    <div class="controls">
      <button class="primary" @click="$router.push('/add-patient')">
        + Добавить пациента
      </button>
    </div>

    <div v-if="loading" class="status">Загрузка данных</div>
    <div v-else-if="error" class="error">Ошибка загрузки: {{ error }}</div>

    <table v-else class="patients-table">
      <thead>
        <tr>
          <th>ФИО</th>
          <th>Тип афазии</th>
          <th>Способ входа</th>
          <th>Дата регистрации</th>
          <th>Действие</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="patient in patients" :key="patient.id">
          <td>{{ patient.full_name }}</td>
          <td>{{ patient.aphasia_type === 'motor' ? 'Моторная' : patient.aphasia_type === 'sensory' ? 'Сенсорная' : 'Смешанная' }}</td>
          <td>{{ patient.auth_method ? (patient.auth_method === 'pin' ? 'ПИН-код' : patient.auth_method === 'biometric' ? 'Биометрия' : 'Ссылка') : '—' }}</td>
          <td>{{ new Date(patient.created_at).toLocaleDateString('ru-RU') }}</td>
          <td>
            <button class="open-btn" @click="openPatient(patient.id)">Открыть</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const patients = ref([])
const loading = ref(false)
const error = ref('')

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

const fetchPatients = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.get(`${API_URL}/patients`)
    patients.value = res.data
  } catch (err) {
    console.error('Ошибка запроса:', err)
    error.value = err.response?.data?.detail || err.message || 'Не удалось загрузить список'
  } finally {
    loading.value = false
  }
}

const openPatient = (id) => {
  router.push(`/patient/${id}`)
}

const logout = () => {
  localStorage.removeItem('doctor_id')
  router.push('/')
}

onMounted(fetchPatients)
</script>

<style scoped>
.dashboard { max-width: 1100px; margin: 40px auto; padding: 0 16px; font-family: system-ui, -apple-system, sans-serif; }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.logout { background: #ef4444; color: #fff; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; }
.controls { margin-bottom: 20px; }
.primary { background: #2563eb; color: #fff; border: none; padding: 10px 18px; border-radius: 6px; cursor: pointer; font-size: 0.95rem; }
.patients-table { width: 100%; border-collapse: collapse; background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border-radius: 8px; overflow: hidden; }
th, td { padding: 12px 16px; text-align: left; border-bottom: 1px solid #e2e8f0; font-size: 0.9rem; }
th { background: #f8fafc; font-weight: 600; color: #475569; }
tr:hover { background: #f8fafc; }
.open-btn { background: #10b981; color: #fff; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-size: 0.85rem; }
.status, .error { padding: 14px; text-align: center; margin: 20px 0; border-radius: 6px; font-size: 0.95rem; }
.status { background: #e0f2fe; color: #0369a1; }
.error { background: #fee2e2; color: #b91c1c; }
</style>