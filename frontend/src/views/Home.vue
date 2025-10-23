<template>
  <div class="bento-grid bento-home">
    <!-- Hero Section -->
    <div class="bento-item hero bento-hero">
      <v-icon size="48" class="mb-4 pulse-icon">mdi-heart-pulse</v-icon>
      <h1 class="text-h3 font-weight-bold mb-2">CardioLearn AI</h1>
      <p class="text-h6 opacity-80">Sistema Inteligente para Ensino de Doenças Cardiovasculares</p>
    </div>

    <!-- Feature Cards -->
    <div class="bento-item feat1 bento-feature" @click="$router.push('/predict')">
      <v-icon size="32" color="#BB86FC" class="mb-3">mdi-brain</v-icon>
      <h3 class="text-h6 font-weight-bold mb-2">Predição com IA</h3>
      <p class="text-body-2 opacity-80 mb-4">Análise inteligente de risco cardiovascular usando machine learning</p>
      <v-btn color="#BB86FC" variant="outlined" size="small">Iniciar Predição</v-btn>
    </div>

    <div class="bento-item feat2 bento-feature" @click="$router.push('/cases')">
      <v-icon size="32" color="#BB86FC" class="mb-3">mdi-stethoscope</v-icon>
      <h3 class="text-h6 font-weight-bold mb-2">Casos Clínicos</h3>
      <p class="text-body-2 opacity-80 mb-4">Pratique com casos reais e compare com a IA</p>
      <v-btn color="#BB86FC" variant="outlined" size="small">Praticar Agora</v-btn>
    </div>

    <div class="bento-item feat3 bento-feature" @click="$router.push('/metrics')">
      <v-icon size="32" color="#BB86FC" class="mb-3">mdi-chart-box</v-icon>
      <h3 class="text-h6 font-weight-bold mb-2">Métricas da IA</h3>
      <p class="text-body-2 opacity-80 mb-4">Veja como o modelo foi treinado e suas limitações</p>
      <v-btn color="#BB86FC" variant="outlined" size="small">Ver Métricas</v-btn>
    </div>

    <!-- Stats Section -->
    <div class="bento-item stats bento-primary">
      <div class="d-flex justify-space-around text-center">
        <div>
          <div class="text-h4 font-weight-bold">68.742</div>
          <div class="text-body-2 opacity-90">Casos Analisados</div>
        </div>
        <div>
          <div class="text-h4 font-weight-bold">71%</div>
          <div class="text-body-2 opacity-90">Precisão da IA</div>
        </div>
        <div>
          <div class="text-h4 font-weight-bold">100%</div>
          <div class="text-body-2 opacity-90">Educacional</div>
        </div>
      </div>
    </div>

    <!-- Info Section -->
    <div class="bento-item info">
      <h4 class="text-h6 font-weight-bold mb-3">Como Funciona</h4>
      <p class="text-body-2 opacity-80">Nossa IA analisa múltiplos fatores de risco cardiovascular para fornecer predições educacionais, ajudando estudantes de medicina a compreender padrões clínicos.</p>
    </div>

    <!-- Chat Preview -->
    <div class="bento-item chat">
      <h4 class="text-h6 font-weight-bold mb-3">IA Explicativa</h4>
      <div class="chat-preview">
        <div class="chat-message mb-2 pa-2" style="background: #1e1e1e; border-radius: 8px;">
          <small class="opacity-60">IA:</small>
          <p class="text-body-2 ma-0">"Baseado na idade e pressão arterial, o risco é moderado..."</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FeatureCard from '../components/FeatureCard.vue'
import PageHeader from '../components/PageHeader.vue'

export default {
  name: 'Home',
  components: {
    FeatureCard,
    PageHeader
  }
}
</script>

<style scoped>
.pulse-icon {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.chat-preview {
  max-height: 120px;
  overflow: hidden;
}

.chat-message {
  border-left: 3px solid #BB86FC;
}
</style>