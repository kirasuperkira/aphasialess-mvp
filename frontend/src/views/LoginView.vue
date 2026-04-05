<template>
  <div class="login-container">
    <h2>Вход для специалистов</h2>
    <form @submit.prevent="handleLogin">
      <input v-model="form.email" type="email" placeholder="Email" required />
      <input v-model="form.password" type="password" placeholder="Пароль" required />
      <button type="submit" :disabled="loading">
        {{ loading ? 'Вход...' : 'Войти' }}
      </button>
      <a href="#" class="forgot-link">Забыли пароль?</a>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = ref({ email: '', password: '' })
const loading = ref(false)
const error = ref('')

const handleLogin = () => {
  loading.value = true
  error.value = ''
  localStorage.setItem('doctor_id', 'doctor-mvp-001')
  setTimeout(() => {
    loading.value = false
    router.push('/dashboard')
  }, 400)
}
</script>

<style scoped>
.login-container { max-width: 380px; margin: 80px auto; padding: 24px; border: 1px solid #e2e8f0; border-radius: 10px; background: #fff; text-align: center; }
input { width: 100%; padding: 10px; margin: 8px 0; border: 1px solid #cbd5e1; border-radius: 6px; box-sizing: border-box; }
button { width: 100%; padding: 10px; background: #2563eb; color: #fff; border: none; border-radius: 6px; cursor: pointer; margin-top: 8px; }
button:disabled { background: #93c5fd; cursor: not-allowed; }
.forgot-link { display: inline-block; margin-top: 12px; font-size: 0.85rem; color: #2563eb; text-decoration: none; }
.error { color: #dc2626; margin-top: 10px; font-size: 0.9rem; }
</style>