<template>
  <div class="dashboard">
    <header class="header">
      <h2>Главная панель</h2>
      <button class="logout" @click="logout">Выйти</button>
    </header>
    <main>
      <p>Список пациентов будет загружен с бэкенда на следующем шаге.</p>
      <button class="primary" @click="$router.push('/add-patient')">
        + Добавить пациента
      </button>
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
const logout = () => {
  localStorage.removeItem('doctor_id')
  router.push('/')
}
</script>

<style scoped>
.dashboard { max-width: 900px; margin: 40px auto; padding: 0 16px; }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.logout { background: #ef4444; color: #fff; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; }
.primary { background: #10b981; color: #fff; border: none; padding: 12px 20px; border-radius: 6px; font-size: 1rem; cursor: pointer; }
</style>