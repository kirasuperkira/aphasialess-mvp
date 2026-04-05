<template>
  <div class="plan-editor">
    <!-- Шапка -->
    <header class="editor-header">
      <button class="back-btn" @click="goBack">← Назад</button>
      <h2>План реабилитации: {{ patientName }}</h2>
      <div class="header-actions">
        <button class="btn-secondary" @click="cancelChanges" :disabled="!hasChanges">
          Отмена
        </button>
        <button class="btn-primary" @click="savePlan" :disabled="!hasChanges || saving">
          {{ saving ? 'Сохранение...' : 'Сохранить и отправить' }}
        </button>
      </div>
    </header>

    <!-- Текущие параметры -->
    <section class="current-params">
      <h3>Текущие параметры плана</h3>
      <div class="params-grid">
        <div class="param-item">
          <label>Частота занятий</label>
          <select v-model="planParams.frequency" @change="markChanged">
            <option value="daily">Ежедневно</option>
            <option value="5days">5 дней в неделю</option>
            <option value="3days">3 дня в неделю</option>
          </select>
        </div>
        <div class="param-item">
          <label>Длительность сессии</label>
          <select v-model="planParams.duration" @change="markChanged">
            <option value="10">10 минут</option>
            <option value="15">15 минут</option>
            <option value="20">20 минут</option>
            <option value="30">30 минут</option>
          </select>
        </div>
        <div class="param-item">
          <label>Режим адаптации</label>
          <select v-model="planParams.adaptationMode" @change="markChanged">
            <option value="auto">Автоматический</option>
            <option value="manual">Ручной</option>
          </select>
        </div>
      </div>
    </section>

    <!-- Типы упражнений -->
    <section class="exercises-section">
      <h3>Типы упражнений</h3>
      <div class="exercises-grid">
        <div 
          v-for="(exercise, index) in exercises" 
          :key="exercise.id" 
          class="exercise-card"
          :class="{ active: exercise.active }"
        >
          <div class="exercise-header">
            <div class="checkbox-wrapper">
              <input 
                type="checkbox" 
                :id="'exercise-' + exercise.id"
                v-model="exercise.active"
                @change="markChanged"
              />
              <label :for="'exercise-' + exercise.id">{{ exercise.title }}</label>
            </div>
            <span class="target-skill" :class="exercise.targetSkill">
              {{ translateSkill(exercise.targetSkill) }}
            </span>
          </div>
          
          <div class="exercise-body">
            <div class="difficulty-control">
              <label>Сложность: {{ exercise.difficulty }}/5</label>
              <input 
                type="range" 
                min="1" 
                max="5" 
                v-model.number="exercise.difficulty"
                @input="markChanged"
                :disabled="!exercise.active"
              />
              <div class="difficulty-labels">
                <span>Низкая</span>
                <span>Высокая</span>
              </div>
            </div>
            
            <div class="exercise-preview">
              <strong>Пример задания:</strong>
              <p>{{ exercise.example }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Предпросмотр изменений -->
    <section class="preview-section" v-if="hasChanges">
      <h3> Предпросмотр изменений</h3>
      <div class="changes-list">
        <div v-for="(change, index) in changesSummary" :key="index" class="change-item">
          <span class="change-icon">✏️</span>
          <span class="change-text">{{ change }}</span>
        </div>
      </div>
    </section>

    <!-- Модальное окно подтверждения -->
    <div v-if="showConfirmModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <div class="modal-header">Подтверждение сохранения</div>
        <div class="modal-body">
          <p>Изменения будут немедленно отправлены пациенту и применены в его приложении.</p>
          <div class="modal-actions">
            <button class="btn-secondary" @click="closeModal">Отмена</button>
            <button class="btn-primary" @click="confirmSave">Применить</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно успеха -->
    <div v-if="showSuccessModal" class="modal-overlay" @click.self="closeSuccessModal">
      <div class="modal success">
        <div class="modal-header">План обновлён</div>
        <div class="modal-body">
          <p>Изменения сохранены и синхронизированы с приложением пациента.</p>
          <button class="btn-primary full-width" @click="closeSuccessModal">Готово</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const patientName = ref('')
const saving = ref(false)
const hasChanges = ref(false)
const showConfirmModal = ref(false)
const showSuccessModal = ref(false)

// Параметры плана
const planParams = reactive({
  frequency: 'daily',
  duration: '15',
  adaptationMode: 'auto'
})

// Упражнения (в MVP — заглушка, в реальности — загрузка с API)
const exercises = ref([
  {
    id: 1,
    title: 'Артикуляция (звук Р)',
    targetSkill: 'phonemic',
    difficulty: 3,
    active: true,
    example: 'Произнесите слова: рак, рот, рука, дорога'
  },
  {
    id: 2,
    title: 'Глаголы (прошедшее время)',
    targetSkill: 'grammar',
    difficulty: 4,
    active: true,
    example: 'Назовите действие: шёл, нёс, пёк, вёз'
  },
  {
    id: 3,
    title: 'Существительные (множественное число)',
    targetSkill: 'grammar',
    difficulty: 2,
    active: true,
    example: 'Образуйте множественное число: дерево → деревья'
  },
  {
    id: 4,
    title: 'Чтение слов',
    targetSkill: 'semantic',
    difficulty: 3,
    active: false,
    example: 'Прочитайте слова вслух: машина, дом, окно'
  },
  {
    id: 5,
    title: 'Письмо под диктовку',
    targetSkill: 'phonemic',
    difficulty: 4,
    active: false,
    example: 'Напишите слово, которое услышите'
  },
  {
    id: 6,
    title: 'Визуальная ассоциация',
    targetSkill: 'semantic',
    difficulty: 2,
    active: true,
    example: 'Выберите картинку, соответствующую слову'
  }
])

// Загрузка данных пациента
const loadPatientData = async () => {
  const patientId = route.params.id
  try {
    const res = await axios.get(`${import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'}/patients`)
    const patient = res.data.find(p => p.id === patientId)
    if (patient) {
      patientName.value = patient.full_name
      // В реальной версии — загрузка текущего плана через GET /treatment-plans/:id
      loadCurrentPlan()
    }
  } catch (err) {
    console.error('Ошибка загрузки:', err)
  }
}

const loadCurrentPlan = () => {
  // Заглушка: загружаем параметры из localStorage или устанавливаем дефолтные
  const saved = localStorage.getItem(`plan_${route.params.id}`)
  if (saved) {
    const parsed = JSON.parse(saved)
    Object.assign(planParams, parsed.params)
    // Обновляем упражнения
    parsed.exercises.forEach(savedEx => {
      const ex = exercises.value.find(e => e.id === savedEx.id)
      if (ex) {
        ex.difficulty = savedEx.difficulty
        ex.active = savedEx.active
      }
    })
  }
}

const markChanged = () => {
  hasChanges.value = true
}

const translateSkill = (skill) => {
  const skills = {
    phonemic: 'Фонематика',
    semantic: 'Семантика',
    grammar: 'Грамматика'
  }
  return skills[skill] || skill
}

const changesSummary = computed(() => {
  const changes = []
  exercises.value.forEach(ex => {
    if (ex.active) {
      changes.push(`${ex.title}: сложность ${ex.difficulty}/5`)
    }
  })
  return changes
})

const goBack = () => {
  if (hasChanges.value) {
    if (confirm('У вас есть несохранённые изменения. Выйти без сохранения?')) {
      router.push(`/patient/${route.params.id}`)
    }
  } else {
    router.push(`/patient/${route.params.id}`)
  }
}

const cancelChanges = () => {
  if (confirm('Отменить все изменения?')) {
    loadCurrentPlan()
    hasChanges.value = false
  }
}

const savePlan = () => {
  showConfirmModal.value = true
}

const confirmSave = async () => {
  saving.value = true
  showConfirmModal.value = false
  
  try {
    const payload = {
      patient_id: route.params.id,
      doctor_id: localStorage.getItem('doctor_id') || 'doctor-mvp-001',
      adaptation_mode: planParams.adaptationMode,
      exercise_schedule: {
        frequency: planParams.frequency,
        duration: parseInt(planParams.duration),
        exercises: exercises.value
          .filter(ex => ex.active)
          .map(ex => ({
            id: ex.id,
            title: ex.title,
            difficulty: ex.difficulty,
            target_skill: ex.targetSkill
          }))
      },
      status: 'active',
      updated_at: new Date().toISOString()
    }
    
    // В MVP сохраняем в localStorage
    localStorage.setItem(`plan_${route.params.id}`, JSON.stringify({
      params: planParams,
      exercises: exercises.value
    }))
    
    // В реальной версии: await axios.put(`/treatment-plans/${planId}`, payload)
    
    await new Promise(resolve => setTimeout(resolve, 800))
    showSuccessModal.value = true
    hasChanges.value = false
  } catch (err) {
    console.error('Ошибка сохранения:', err)
    alert('Ошибка при сохранении плана')
  } finally {
    saving.value = false
  }
}

const closeModal = () => {
  showConfirmModal.value = false
}

const closeSuccessModal = () => {
  showSuccessModal.value = false
  router.push(`/patient/${route.params.id}`)
}

onMounted(loadPatientData)
</script>

<style scoped>
.plan-editor { max-width: 1000px; margin: 0 auto; padding: 24px; }
.editor-header { display: flex; align-items: center; gap: 24px; margin-bottom: 32px; padding: 20px; background: #fff; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.back-btn { background: none; border: none; font-size: 1rem; cursor: pointer; color: #64748b; }
.editor-header h2 { flex: 1; margin: 0; color: #1e293b; }
.header-actions { display: flex; gap: 12px; }
.btn-primary { background: #2563eb; color: #fff; border: none; padding: 10px 18px; border-radius: 6px; cursor: pointer; }
.btn-primary:disabled { background: #93c5fd; cursor: not-allowed; }
.btn-secondary { background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; padding: 10px 18px; border-radius: 6px; cursor: pointer; }
.btn-secondary:disabled { opacity: 0.5; cursor: not-allowed; }

.current-params { background: #fff; padding: 24px; border-radius: 10px; margin-bottom: 32px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.current-params h3 { margin: 0 0 20px; color: #1e293b; }
.params-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.param-item label { display: block; margin-bottom: 8px; font-weight: 500; color: #475569; }
.param-item select { width: 100%; padding: 10px; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 0.95rem; }

.exercises-section { background: #fff; padding: 24px; border-radius: 10px; margin-bottom: 32px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.exercises-section h3 { margin: 0 0 20px; color: #1e293b; }
.exercises-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
.exercise-card { padding: 16px; border: 2px solid #e2e8f0; border-radius: 8px; transition: all 0.2s; }
.exercise-card.active { border-color: #2563eb; background: #eff6ff; }
.exercise-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.checkbox-wrapper { display: flex; align-items: center; gap: 8px; }
.checkbox-wrapper input[type="checkbox"] { width: 18px; height: 18px; cursor: pointer; }
.checkbox-wrapper label { font-weight: 600; color: #1e293b; cursor: pointer; }
.target-skill { padding: 4px 10px; border-radius: 20px; font-size: 0.8rem; font-weight: 500; }
.target-skill.phonemic { background: #dbeafe; color: #1e40af; }
.target-skill.semantic { background: #d1fae5; color: #065f46; }
.target-skill.grammar { background: #fef3c7; color: #92400e; }

.exercise-body { margin-top: 12px; }
.difficulty-control { margin-bottom: 12px; }
.difficulty-control label { display: block; margin-bottom: 6px; font-weight: 500; color: #475569; }
.difficulty-control input[type="range"] { width: 100%; cursor: pointer; }
.difficulty-control input[type="range"]:disabled { opacity: 0.5; cursor: not-allowed; }
.difficulty-labels { display: flex; justify-content: space-between; font-size: 0.8rem; color: #94a3b8; margin-top: 4px; }
.exercise-preview { background: #f8fafc; padding: 10px; border-radius: 6px; font-size: 0.9rem; color: #475569; }
.exercise-preview strong { display: block; margin-bottom: 4px; color: #1e293b; }

.preview-section { background: #fff; padding: 24px; border-radius: 10px; margin-bottom: 32px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border-left: 4px solid #2563eb; }
.preview-section h3 { margin: 0 0 16px; color: #1e293b; }
.changes-list { display: flex; flex-direction: column; gap: 8px; }
.change-item { display: flex; align-items: center; gap: 10px; padding: 8px 12px; background: #f8fafc; border-radius: 6px; }
.change-icon { font-size: 1.2rem; }
.change-text { font-size: 0.95rem; color: #475569; }

.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 100; }
.modal { background: #fff; padding: 24px; border-radius: 10px; width: 90%; max-width: 450px; }
.modal-header { font-size: 1.2rem; font-weight: 600; margin-bottom: 12px; color: #1e293b; }
.modal-body p { margin: 0 0 20px; color: #475569; line-height: 1.6; }
.modal-actions { display: flex; gap: 12px; justify-content: flex-end; }
.modal.success .modal-header { color: #059669; }
.full-width { width: 100%; }
</style>