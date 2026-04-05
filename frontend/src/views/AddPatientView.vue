<template>
  <div class="add-patient-container">
    <h2>Регистрация пациента</h2>
    <div class="step-indicator">Шаг {{ currentStep }} из 3</div>

    <div v-if="currentStep === 1" class="form-step">
      <h3>Личные данные</h3>
      <input v-model="form.full_name" placeholder="ФИО пациента *" required />
      <input v-model="form.bot_phone" placeholder="Телефон" />
      <input v-model="form.email" placeholder="Email" />
      <div class="buttons">
        <button class="secondary" @click="$router.push('/dashboard')">Отмена</button>
        <button class="primary" @click="nextStep" :disabled="!form.full_name.trim()">Далее</button>
      </div>
    </div>

    <div v-if="currentStep === 2" class="form-step">
      <h3>Диагноз и доступ</h3>
      <label>Тип афазии *
        <select v-model="form.aphasia_type" required>
          <option disabled value="">Выберите тип</option>
          <option value="motor">Моторная</option>
          <option value="sensory">Сенсорная</option>
          <option value="mixed">Смешанная</option>
        </select>
      </label>
      <label>Способ входа
        <select v-model="form.auth_method">
          <option disabled value="">Не выбрано</option>
          <option value="pin">ПИН-код</option>
          <option value="biometric">Биометрия / FaceID</option>
        </select>
      </label>
      <div class="buttons">
        <button class="secondary" @click="currentStep = 1">Назад</button>
        <button class="primary" @click="nextStep" :disabled="!form.aphasia_type">Далее</button>
      </div>
    </div>

    <div v-if="currentStep === 3" class="form-step">
      <h3>Предпросмотр профиля</h3>
      <div class="preview-card">
        <p><strong>ФИО:</strong> {{ form.full_name }}</p>
        <p><strong>Телефон:</strong> {{ form.bot_phone || '—' }}</p>
        <p><strong>Email:</strong> {{ form.email || '—' }}</p>
        <p><strong>Тип афазии:</strong> {{ translateAphasia(form.aphasia_type) }}</p>
        <p><strong>Способ входа:</strong> {{ translateAuth(form.auth_method) }}</p>
      </div>
      <div class="buttons">
        <button class="secondary" @click="currentStep = 2">Назад</button>
        <button class="primary" @click="submitForm" :disabled="loading">
          {{ loading ? 'Создание...' : 'Создать профиль' }}
        </button>
      </div>
    </div>

    <div v-if="showSuccess" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <div class="modal-header">Профиль успешно создан</div>
        <div class="modal-body">
          <p>Код активации для пациента:</p>
          <div class="code-box">{{ activationCode }}</div>
          <div class="qr-placeholder">[QR-код сгенерируется в ПР-05]</div>
          <button class="primary full-width" @click="closeModal">Готово</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const currentStep = ref(1)
const loading = ref(false)
const showSuccess = ref(false)
const activationCode = ref('')

const form = reactive({
  full_name: '',
  bot_phone: '',
  email: '',
  aphasia_type: '',
  auth_method: ''
})

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

const nextStep = () => {
  if (currentStep.value === 1 && !form.full_name.trim()) return
  if (currentStep.value === 2 && !form.aphasia_type) return
  currentStep.value++
}

const translateAphasia = (type) => ({
  motor: 'Моторная', sensory: 'Сенсорная', mixed: 'Смешанная'
}[type] || '—')

const translateAuth = (method) => ({
  pin: 'ПИН-код', biometric: 'Биометрия'
}[method] || '—')

const submitForm = async () => {
  loading.value = true
  try {
    const payload = {
      full_name: form.full_name.trim(),
      aphasia_type: form.aphasia_type,
      auth_method: form.auth_method || null,
      assigned_doctor_id: localStorage.getItem('doctor_id') || 'doctor-mvp-001',

      bot_phone: form.bot_phone || null,
      crm_external_id: null,
      bpms_process_status: 'pending'
    }
    const res = await axios.post(`${API_URL}/patients`, payload)
    activationCode.value = `APH-${res.data.id.slice(0, 8).toUpperCase()}`
    showSuccess.value = true
  } catch (err) {
    console.error('Ошибка создания:', err)
    alert('Ошибка при создании пациента: ' + (err.response?.data?.detail || err.message))
  } finally {
    loading.value = false
  }
}

const closeModal = () => {
  showSuccess.value = false
  router.push('/dashboard')
}
</script>

<style scoped>
.add-patient-container { max-width: 600px; margin: 40px auto; padding: 24px; background: #fff; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
h2 { margin: 0 0 12px; font-size: 1.4rem; color: #1e293b; }
.step-indicator { display: inline-block; padding: 4px 10px; background: #e0f2fe; color: #0369a1; border-radius: 20px; font-size: 0.85rem; margin-bottom: 20px; }
.form-step h3 { margin: 0 0 16px; color: #334155; }
input, select { width: 100%; padding: 10px 12px; margin: 8px 0 16px; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 0.95rem; box-sizing: border-box; }
input:focus, select:focus { outline: none; border-color: #3b82f6; box-shadow: 0 0 0 2px rgba(59,130,246,0.2); }
.buttons { display: flex; gap: 12px; margin-top: 20px; }
.primary { background: #2563eb; color: #fff; border: none; padding: 10px 18px; border-radius: 6px; cursor: pointer; font-size: 0.95rem; }
.primary:disabled { background: #93c5fd; cursor: not-allowed; }
.secondary { background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; padding: 10px 18px; border-radius: 6px; cursor: pointer; font-size: 0.95rem; }
.preview-card { background: #f8fafc; padding: 16px; border-radius: 8px; margin-bottom: 10px; line-height: 1.6; }
.preview-card p { margin: 6px 0; }
.note { font-size: 0.8rem; color: #64748b; margin-top: 10px; }
.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 100; }
.modal { background: #fff; padding: 24px; border-radius: 10px; width: 90%; max-width: 400px; text-align: center; }
.modal-header { font-size: 1.2rem; font-weight: 600; margin-bottom: 12px; color: #059669; }
.code-box { background: #f1f5f9; padding: 10px; font-family: monospace; font-size: 1.1rem; letter-spacing: 1px; margin: 12px 0; border-radius: 6px; }
.qr-placeholder { background: #e2e8f0; padding: 16px; margin: 12px 0; border-radius: 6px; color: #64748b; font-size: 0.85rem; }
.full-width { width: 100%; }
</style>