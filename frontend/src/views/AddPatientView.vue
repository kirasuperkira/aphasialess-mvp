<template>
  <div class="add-patient">
    <h2>Регистрация пациента</h2>
    <p>Многошаговая форма будет подключена на следующем этапе.</p>
    <button @click="$router.push('/dashboard')">← Назад к дашборду</button>
  </div>
</template>

<style scoped>
.add-patient { max-width: 800px; margin: 40px auto; padding: 20px; border: 1px dashed #cbd5e1; border-radius: 8px; text-align: center; }
button { margin-top: 20px; padding: 10px 18px; background: #64748b; color: #fff; border: none; border-radius: 6px; cursor: pointer; }
</style>