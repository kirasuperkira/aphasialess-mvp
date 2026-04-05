<template>
  <div class="patient-detail">
    <!-- Шапка профиля -->
    <header class="profile-header">
      <button class="back-btn" @click="$router.push('/dashboard')">← Назад</button>
      <div class="patient-info">
        <h2>{{ patient?.full_name || 'Загрузка...' }}</h2>
        <div class="badges">
          <span class="badge" :class="patient?.aphasia_type">
            {{ translateAphasia(patient?.aphasia_type) }}
          </span>
          <span class="badge status-active">Активен</span>
        </div>
      </div>
      <div class="actions">
        <button class="btn-secondary" @click="downloadReport">Скачать отчёт</button>
        <button class="btn-primary" @click="editPlan">Редактировать план</button>
      </div>
    </header>

    <!-- Быстрая статистика -->
    <section class="stats-grid">
      <div class="stat-card">
        <div class="stat-value">{{ stats.total_sessions }}</div>
        <div class="stat-label">Всего занятий</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ stats.avg_accuracy }}%</div>
        <div class="stat-label">Средняя точность</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ stats.last_session || '—' }}</div>
        <div class="stat-label">Последнее занятие</div>
      </div>
    </section>

    <!-- Графики прогресса -->
    <section class="charts-section">
      <div class="chart-header">
        <h3>Прогресс по точности</h3>
        <select v-model="chartPeriod" @change="loadProgressData">
          <option value="7">7 дней</option>
          <option value="14">14 дней</option>
          <option value="30">30 дней</option>
        </select>
      </div>
      
      <!-- Простая визуализация прогресса (в MVP без Chart.js) -->
      <div class="progress-visualization">
        <div v-for="(day, index) in progressData" :key="index" class="day-bar">
          <div class="bar" :style="{ height: day.accuracy + '%' }" 
               :class="day.accuracy >= 70 ? 'success' : day.accuracy >= 50 ? 'warning' : 'danger'">
          </div>
          <div class="day-label">{{ day.date }}</div>
        </div>
      </div>
    </section>

    <!-- Проблемные зоны -->
    <section class="problem-areas">
      <h3>Проблемные зоны</h3>
      <div class="problems-list">
        <div v-for="(problem, index) in problemAreas" :key="index" class="problem-item">
          <div class="problem-name">{{ problem.exercise }}</div>
          <div class="problem-stats">
            <div class="error-rate">{{ problem.error_rate }}% ошибок</div>
            <div class="progress-bar-mini">
              <div class="fill" :style="{ width: problem.error_rate + '%' }"></div>
            </div>
          </div>
          <div class="problem-details" v-if="problem.expanded">
            <p>Трудные слова: {{ problem.difficult_words.join(', ') }}</p>
          </div>
          <button class="toggle-details" @click="problem.expanded = !problem.expanded">
            {{ problem.expanded ? 'Скрыть' : 'Подробнее' }}
          </button>
        </div>
      </div>
    </section>

    <!-- История занятий -->
    <section class="session-history">
      <h3>История занятий</h3>
      <table class="sessions-table">
        <thead>
          <tr>
            <th>Дата</th>
            <th>Длительность</th>
            <th>Точность</th>
            <th>Статус</th>
            <th>Действие</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="session in sessions" :key="session.id">
            <td>{{ formatDate(session.date) }}</td>
            <td>{{ session.duration }} мин</td>
            <td>{{ session.accuracy }}%</td>
            <td>
              <span class="status-badge" :class="session.status">
                {{ session.status === 'completed' ? 'Выполнено' : 'В процессе' }}
              </span>
            </td>
            <td>
              <button class="btn-small" @click="viewSessionDetails(session)">
                Подробнее
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const patient = ref(null)
const stats = ref({ total_sessions: 0, avg_accuracy: 0, last_session: '' })
const progressData = ref([])
const chartPeriod = ref('7')
const problemAreas = ref([])
const sessions = ref([])

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

// Заглушка данных для MVP (в реальности — запрос к API)
const loadPatientData = async () => {
  const patientId = route.params.id
  
  // Получаем пациента из списка (в MVP)
  try {
    const res = await axios.get(`${API_URL}/patients`)
    const found = res.data.find(p => p.id === patientId)
    if (found) {
      patient.value = found
      // Генерируем тестовые данные
      generateMockData()
    }
  } catch (err) {
    console.error('Ошибка загрузки:', err)
  }
}

const generateMockData = () => {
  // Тестовая статистика
  stats.value = {
    total_sessions: 15,
    avg_accuracy: 78,
    last_session: '2 дня назад'
  }
  
  // Тестовый прогресс (7 дней)
  progressData.value = [
    { date: 'Пн', accuracy: 65 },
    { date: 'Вт', accuracy: 70 },
    { date: 'Ср', accuracy: 68 },
    { date: 'Чт', accuracy: 75 },
    { date: 'Пт', accuracy: 80 },
    { date: 'Сб', accuracy: 72 },
    { date: 'Вс', accuracy: 85 }
  ]
  
  // Проблемные зоны
  problemAreas.value = [
    { 
      exercise: 'Глаголы (прошедшее время)', 
      error_rate: 35, 
      difficult_words: ['шёл', 'нёс', 'пёк'],
      expanded: false 
    },
    { 
      exercise: 'Существительные (множественное число)', 
      error_rate: 25, 
      difficult_words: ['деревья', 'дома', 'окна'],
      expanded: false 
    },
    { 
      exercise: 'Артикуляция звука Р', 
      error_rate: 40, 
      difficult_words: ['рак', 'рот', 'рука'],
      expanded: false 
    }
  ]
  
  // История занятий
  sessions.value = [
    { id: 1, date: '2026-04-03', duration: 18, accuracy: 85, status: 'completed' },
    { id: 2, date: '2026-04-02', duration: 15, accuracy: 72, status: 'completed' },
    { id: 3, date: '2026-04-01', duration: 20, accuracy: 68, status: 'completed' },
    { id: 4, date: '2026-03-31', duration: 12, accuracy: 75, status: 'completed' },
    { id: 5, date: '2026-03-30', duration: 16, accuracy: 80, status: 'completed' }
  ]
}

const translateAphasia = (type) => {
  const types = {
    motor: 'Моторная',
    sensory: 'Сенсорная',
    mixed: 'Смешанная'
  }
  return types[type] || type
}

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleDateString('ru-RU')
}

const downloadReport = () => {
  alert('Отчёт будет сгенерирован в PDF (в ПР-05 интеграция с мед. системами)')
}

const editPlan = () => {
  router.push(`/patient/${route.params.id}/edit-plan`)
}

const viewSessionDetails = (session) => {
  alert(`Занятие от ${session.date}\nТочность: ${session.accuracy}%\nУпражнений выполнено: 8`)
}

const loadProgressData = () => {
  // В реальной версии — запрос к API с периодом
  console.log('Загрузка прогресса за', chartPeriod.value, 'дней')
}

onMounted(loadPatientData)
</script>

<style scoped>
.patient-detail { max-width: 1200px; margin: 0 auto; padding: 24px; }
.profile-header { display: flex; align-items: center; gap: 24px; margin-bottom: 32px; padding: 20px; background: #fff; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.back-btn { background: none; border: none; font-size: 1rem; cursor: pointer; color: #64748b; }
.patient-info { flex: 1; }
.patient-info h2 { margin: 0 0 8px; color: #1e293b; }
.badges { display: flex; gap: 8px; }
.badge { padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 500; }
.badge.motor { background: #dbeafe; color: #1e40af; }
.badge.sensory { background: #fce7f3; color: #9d174d; }
.badge.mixed { background: #fef3c7; color: #92400e; }
.badge.status-active { background: #d1fae5; color: #065f46; }
.actions { display: flex; gap: 12px; }
.btn-primary { background: #2563eb; color: #fff; border: none; padding: 10px 18px; border-radius: 6px; cursor: pointer; }
.btn-secondary { background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; padding: 10px 18px; border-radius: 6px; cursor: pointer; }

.stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 32px; }
.stat-card { background: #fff; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.stat-value { font-size: 2rem; font-weight: 700; color: #2563eb; margin-bottom: 4px; }
.stat-label { color: #64748b; font-size: 0.9rem; }

.charts-section { background: #fff; padding: 24px; border-radius: 10px; margin-bottom: 32px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.chart-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.chart-header h3 { margin: 0; color: #1e293b; }
.chart-header select { padding: 6px 12px; border: 1px solid #cbd5e1; border-radius: 6px; }

.progress-visualization { display: flex; justify-content: space-around; align-items: flex-end; height: 200px; padding: 20px 0; border-bottom: 2px solid #e2e8f0; }
.day-bar { display: flex; flex-direction: column; align-items: center; gap: 8px; }
.bar { width: 40px; border-radius: 4px 4px 0 0; transition: height 0.3s; }
.bar.success { background: #10b981; }
.bar.warning { background: #f59e0b; }
.bar.danger { background: #ef4444; }
.day-label { font-size: 0.8rem; color: #64748b; }

.problem-areas { background: #fff; padding: 24px; border-radius: 10px; margin-bottom: 32px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.problem-areas h3 { margin: 0 0 20px; color: #1e293b; }
.problems-list { display: flex; flex-direction: column; gap: 16px; }
.problem-item { padding: 16px; background: #f8fafc; border-radius: 8px; border-left: 4px solid #ef4444; }
.problem-name { font-weight: 600; color: #1e293b; margin-bottom: 8px; }
.problem-stats { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; }
.error-rate { font-weight: 600; color: #dc2626; min-width: 80px; }
.progress-bar-mini { flex: 1; height: 8px; background: #e2e8f0; border-radius: 4px; overflow: hidden; }
.progress-bar-mini .fill { height: 100%; background: #ef4444; }
.problem-details { margin: 12px 0; padding: 12px; background: #fff; border-radius: 6px; font-size: 0.9rem; color: #475569; }
.toggle-details { background: none; border: none; color: #2563eb; cursor: pointer; font-size: 0.9rem; }

.session-history { background: #fff; padding: 24px; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.session-history h3 { margin: 0 0 20px; color: #1e293b; }
.sessions-table { width: 100%; border-collapse: collapse; }
.sessions-table th, .sessions-table td { padding: 12px; text-align: left; border-bottom: 1px solid #e2e8f0; }
.sessions-table th { background: #f8fafc; font-weight: 600; color: #475569; }
.status-badge { padding: 4px 8px; border-radius: 4px; font-size: 0.85rem; }
.status-badge.completed { background: #d1fae5; color: #065f46; }
.status-badge.in-progress { background: #fef3c7; color: #92400e; }
.btn-small { padding: 6px 12px; background: #e0f2fe; color: #0369a1; border: none; border-radius: 4px; cursor: pointer; font-size: 0.85rem; }
</style>