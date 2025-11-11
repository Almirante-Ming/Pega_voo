<template>
  <div class="page-container">
    <div class="example-card">
      <h1>Exemplo de Input de Código</h1>
      
      <div class="example-section">
        <h2>Código de 6 dígitos</h2>
        <InputConfirmation 
          :length="6"
          @complete="handleComplete"
          @change="handleChange"
        />
        <p class="result">Código digitado: {{ code6 }}</p>
        <p v-if="isComplete6" class="success">✓ Código completo!</p>
      </div>

      <div class="example-section">
        <h2>Código de 4 dígitos</h2>
        <InputConfirmation 
          :length="4"
          @complete="handleComplete4"
          @change="handleChange4"
        />
        <p class="result">Código digitado: {{ code4 }}</p>
        <p v-if="isComplete4" class="success">✓ Código completo!</p>
      </div>

      <div class="example-section">
        <h2>Com controle externo</h2>
        <InputConfirmation 
          ref="codeInputRef"
          :length="6"
          @complete="handleCompleteWithAction"
        />
        <div class="button-group">
          <button @click="clearCode">Limpar</button>
          <button @click="focusCode">Focar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const code6 = ref('')
const isComplete6 = ref(false)
const code4 = ref('')
const isComplete4 = ref(false)
const codeInputRef = ref<any>(null)

const handleComplete = (code: string) => {
  console.log('Código completo (6 dígitos):', code)
  isComplete6.value = true
  // Aqui você pode fazer a validação do código
}

const handleChange = (code: string) => {
  code6.value = code
  isComplete6.value = false
}

const handleComplete4 = (code: string) => {
  console.log('Código completo (4 dígitos):', code)
  isComplete4.value = true
}

const handleChange4 = (code: string) => {
  code4.value = code
  isComplete4.value = false
}

const handleCompleteWithAction = (code: string) => {
  console.log('Código completo com ação:', code)
  alert(`Código verificado: ${code}`)
}

const clearCode = () => {
  codeInputRef.value?.clear()
}

const focusCode = () => {
  codeInputRef.value?.focus()
}
</script>

<style scoped>
.page-container {
  min-height: 100vh;
  padding: 2rem;
  background-color: #f9fafb;
}

.example-card {
  max-width: 800px;
  margin: 0 auto;
  background-color: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

h1 {
  font-size: 2rem;
  font-weight: bold;
  color: #1f2937;
  margin-bottom: 2rem;
  text-align: center;
}

.example-section {
  margin-bottom: 3rem;
  padding: 1.5rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
}

h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 1rem;
}

.result {
  margin-top: 1rem;
  font-size: 0.875rem;
  color: #6b7280;
  text-align: center;
}

.success {
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: #10b981;
  font-weight: 600;
  text-align: center;
}

.button-group {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1rem;
}

button {
  padding: 0.5rem 1rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #2563eb;
}

button:active {
  background-color: #1d4ed8;
}
</style>
