<template>
  <div class="bento-grid bento-cases">
    <!-- Header -->
    <div class="bento-item hero bento-hero text-center" v-if="!currentCase">
      <v-icon size="48" class="mb-4">mdi-stethoscope</v-icon>
      <h1 class="text-h4 font-weight-bold mb-4">Casos Clínicos</h1>
      <v-btn 
        @click="generateCase" 
        color="#BB86FC" 
        size="large" 
        :loading="loading"
        block
      >
        {{ loading ? 'Gerando...' : 'Gerar Novo Caso' }}
      </v-btn>
    </div>

    <!-- Case Section -->
    <div class="bento-item case" v-if="currentCase">
      <div class="mb-4">
        <h2 class="text-h5 font-weight-bold mb-2">
          <v-icon left color="#BB86FC">mdi-clipboard-text</v-icon>
          Caso Clínico
        </h2>
      </div>
            <v-card class="mb-4" flat>
              <v-card-title class="text-subtitle-1">
                <v-icon left color="#BB86FC" size="small">mdi-account</v-icon>
                Dados Completos do Paciente
              </v-card-title>
              <v-card-text class="pa-3">
                <v-row>
                  <v-col cols="6" md="3">
                    <div class="text-caption text-medium-emphasis">Idade</div>
                    <div class="text-body-1 font-weight-medium">{{ currentCase.age }} anos</div>
                  </v-col>
                  <v-col cols="6" md="3">
                    <div class="text-caption text-medium-emphasis">Gênero</div>
                    <div class="text-body-1 font-weight-medium">{{ currentCase.gender === 1 ? 'Feminino' : 'Masculino' }}</div>
                  </v-col>
                  <v-col cols="6" md="3">
                    <div class="text-caption text-medium-emphasis">Altura</div>
                    <div class="text-body-1 font-weight-medium">{{ currentCase.height }} cm</div>
                  </v-col>
                  <v-col cols="6" md="3">
                    <div class="text-caption text-medium-emphasis">Peso</div>
                    <div class="text-body-1 font-weight-medium">{{ currentCase.weight }} kg</div>
                  </v-col>
                  <v-col cols="6" md="3">
                    <div class="text-caption text-medium-emphasis">Pressão Sistólica</div>
                    <div class="text-body-1 font-weight-medium">{{ currentCase.ap_hi }} mmHg</div>
                  </v-col>
                  <v-col cols="6" md="3">
                    <div class="text-caption text-medium-emphasis">Pressão Diastólica</div>
                    <div class="text-body-1 font-weight-medium">{{ currentCase.ap_lo }} mmHg</div>
                  </v-col>
                  <v-col cols="6" md="3">
                    <div class="text-caption text-medium-emphasis">Colesterol</div>
                    <div class="text-body-1 font-weight-medium">{{ getCholesterolLabel(currentCase.cholesterol) }}</div>
                  </v-col>
                  <v-col cols="6" md="3">
                    <div class="text-caption text-medium-emphasis">Glicose</div>
                    <div class="text-body-1 font-weight-medium">{{ getGlucoseLabel(currentCase.gluc) }}</div>
                  </v-col>
                  <v-col cols="4" md="2">
                    <div class="text-caption text-medium-emphasis">Fumante</div>
                    <div class="text-body-1 font-weight-medium">{{ currentCase.smoke ? 'Sim' : 'Não' }}</div>
                  </v-col>
                  <v-col cols="4" md="2">
                    <div class="text-caption text-medium-emphasis">Álcool</div>
                    <div class="text-body-1 font-weight-medium">{{ currentCase.alco ? 'Sim' : 'Não' }}</div>
                  </v-col>
                  <v-col cols="4" md="2">
                    <div class="text-caption text-medium-emphasis">Ativo</div>
                    <div class="text-body-1 font-weight-medium">{{ currentCase.active ? 'Sim' : 'Não' }}</div>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
            
            <v-card class="mb-4" color="info" variant="tonal">
              <v-card-text class="pa-3">
                <div class="text-subtitle-2 mb-2">📝 Descrição do Caso:</div>
                <div class="text-body-2">{{ currentCase.description }}</div>
              </v-card-text>
            </v-card>
    </div>

    <!-- Answer Section -->
    <div class="bento-item answer" v-if="currentCase">
      <div class="mb-4">
        <h2 class="text-h5 font-weight-bold mb-2">
          <v-icon left color="#BB86FC">mdi-brain</v-icon>
          Sua Predição
        </h2>
      </div>
            <v-select
              v-model="userPrediction"
              :items="[
                { title: 'Baixo', value: 'baixo' },
                { title: 'Médio', value: 'medio' },
                { title: 'Alto', value: 'alto' }
              ]"
              label="Qual o risco cardiovascular?"
              variant="outlined"
              density="compact"
            ></v-select>
            
            <v-btn 
              @click="submitAnswer" 
              color="success" 
              block
              :disabled="!userPrediction || answered"
              class="mt-3"
            >
              Confirmar
            </v-btn>
            
            <v-card v-if="answered" class="mt-3" flat>
              <v-alert 
                :type="result.correct ? 'success' : (result.close ? 'warning' : 'error')"
                variant="tonal"
              >
                <strong>{{ result.correct ? 'Correto!' : (result.close ? 'Quase acertou!' : 'Incorreto!') }}</strong><br>
                Resposta correta: {{ getRiskLabel(result.correct_risk) }} ({{ result.percentage }}%)<br>
                <small>{{ result.explanation }}</small>
                <div v-if="result.close" class="mt-2">
                  <small class="text-warning">
                    💯 <strong>Observação:</strong> Você estava muito próximo! Com {{ result.percentage }}%, 
                    o risco estava no limite entre {{ result.user_choice }} e {{ result.correct_risk }}. 
                    Seu raciocínio clínico estava correto!
                  </small>
                </div>
              </v-alert>
              
              <v-btn 
                @click="resetCase" 
                color="primary" 
                block
                class="mt-3"
              >
                Novo Caso
              </v-btn>
            </v-card>
    </div>



    <!-- Floating Chat Button -->
    <v-tooltip text="Dúvidas sobre o caso?" location="left">
      <template v-slot:activator="{ props }">
        <v-btn 
          v-if="currentCase" 
          v-bind="props"
          class="floating-chat-btn"
          color="#BB86FC"
          size="large"
          icon
          elevation="8"
          @click="showChat = !showChat"
        >
          <v-icon size="28">mdi-chat-question</v-icon>
        </v-btn>
      </template>
    </v-tooltip>

    <!-- Floating Chat Panel -->
    <v-dialog 
      v-model="showChat" 
      fullscreen 
      hide-overlay 
      transition="dialog-bottom-transition"
      class="chat-dialog"
    >
      <v-card class="chat-card">
        <v-card-title class="d-flex align-center pa-4">
          <v-icon class="mr-2" color="#BB86FC">mdi-robot</v-icon>
          <span>IA - Caso Clínico</span>
          <v-spacer></v-spacer>
          <v-btn icon @click="showChat = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text class="pa-0 chat-container">
          <AIChat 
            ref="aiChat"
            :patient-data="currentCase" 
            :prediction="{ risk_level: 'caso_clinico', probability: 0.5 }" 
          />
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import api from '../services/api'
import AIChat from '../components/AIChat.vue'
import { handleApiError } from '@/utils/alerts'

export default {
  name: 'ClinicalCases',
  components: {
    AIChat
  },
  data() {
    return {
      loading: false,
      currentCase: null,
      userPrediction: '',
      answered: false,
      result: null,
      showChat: false
    }
  },
  methods: {
    async generateCase() {
      this.loading = true
      try {
        // Gerar dados completos do paciente
        const age = Math.floor(Math.random() * 50) + 30 // 30-80 anos
        const gender = Math.floor(Math.random() * 2) + 1 // 1 ou 2
        const height = Math.floor(Math.random() * 50) + 150 // 150-200 cm
        const weight = Math.floor(Math.random() * 60) + 50 // 50-110 kg
        const ap_hi = Math.floor(Math.random() * 80) + 100 // 100-180 mmHg
        const ap_lo = Math.floor(Math.random() * 40) + 60 // 60-100 mmHg
        const cholesterol = Math.floor(Math.random() * 3) + 1 // 1-3
        const gluc = Math.floor(Math.random() * 3) + 1 // 1-3
        const smoke = Math.random() > 0.7 ? 1 : 0
        const alco = Math.random() > 0.8 ? 1 : 0
        const active = Math.random() > 0.3 ? 1 : 0
        
        // Gerar descrição baseada nos dados
        const descriptions = [
          `Paciente de ${age} anos, ${gender === 1 ? 'do sexo feminino' : 'do sexo masculino'}, procura atendimento para avaliação cardiovascular de rotina.`,
          `Paciente apresenta pressão arterial de ${ap_hi}/${ap_lo} mmHg e relata ${smoke ? 'ser fumante' : 'não fumar'}.`,
          `Indivíduo ${active ? 'fisicamente ativo' : 'sedentário'} com IMC de ${(weight / ((height/100)**2)).toFixed(1)} kg/m².`
        ]
        
        this.currentCase = {
          age, gender, height, weight, ap_hi, ap_lo,
          cholesterol, gluc, smoke, alco, active,
          description: descriptions[Math.floor(Math.random() * descriptions.length)]
        }
        
        this.resetAnswer()
      } catch (error) {
        handleApiError(error, 'GENERATE_CASE')
      } finally {
        this.loading = false
      }
    },
    
    async submitAnswer() {
      // Simular cálculo de risco baseado nos dados
      const riskScore = this.calculateRiskScore()
      const percentage = Math.round(riskScore * 100)
      
      let correctRisk
      if (percentage < 35) correctRisk = 'baixo'
      else if (percentage < 65) correctRisk = 'medio'
      else correctRisk = 'alto'
      
      // Verificar se a resposta está próxima
      const isClose = this.isCloseAnswer(this.userPrediction, correctRisk, percentage)
      
      this.result = {
        correct: this.userPrediction === correctRisk,
        close: isClose,
        correct_risk: correctRisk,
        percentage: percentage,
        user_choice: this.userPrediction,
        explanation: this.getExplanation(correctRisk, percentage)
      }
      
      this.answered = true
      
      // Salvar no histórico
      await this.saveToHistory(correctRisk, this.userPrediction, this.result.correct)
    },
    
    resetCase() {
      this.currentCase = null
      this.resetAnswer()
    },
    
    resetAnswer() {
      this.userPrediction = ''
      this.answered = false
      this.result = null
    },
    
    getRiskLabel(risk) {
      const labels = {
        'baixo': 'BAIXO',
        'medio': 'MÉDIO',
        'alto': 'ALTO'
      }
      return labels[risk] || risk.toUpperCase()
    },
    
    getCholesterolLabel(level) {
      const labels = { 1: 'Normal', 2: 'Alto', 3: 'Muito Alto' }
      return labels[level] || 'Desconhecido'
    },
    
    getGlucoseLabel(level) {
      const labels = { 1: 'Normal', 2: 'Alto', 3: 'Muito Alto' }
      return labels[level] || 'Desconhecido'
    },
    
    calculateRiskScore() {
      if (!this.currentCase) return 0.5
      
      let score = 0
      
      // Idade (peso: 0.3)
      if (this.currentCase.age > 60) score += 0.3
      else if (this.currentCase.age > 45) score += 0.15
      
      // Pressão (peso: 0.25)
      if (this.currentCase.ap_hi > 140 || this.currentCase.ap_lo > 90) score += 0.25
      else if (this.currentCase.ap_hi > 120 || this.currentCase.ap_lo > 80) score += 0.1
      
      // Colesterol (peso: 0.15)
      if (this.currentCase.cholesterol > 2) score += 0.15
      else if (this.currentCase.cholesterol > 1) score += 0.05
      
      // Glicose (peso: 0.1)
      if (this.currentCase.gluc > 1) score += 0.1
      
      // Fumo (peso: 0.1)
      if (this.currentCase.smoke) score += 0.1
      
      // Atividade física (peso: -0.05)
      if (!this.currentCase.active) score += 0.05
      
      // IMC (peso: 0.05)
      const bmi = this.currentCase.weight / ((this.currentCase.height/100)**2)
      if (bmi > 30) score += 0.05
      
      return Math.min(Math.max(score, 0), 1)
    },
    
    isCloseAnswer(userAnswer, correctAnswer, percentage) {
      // Considerar "próximo" se:
      // - Usuário escolheu "alto" e correto é "medio" com % > 55
      // - Usuário escolheu "medio" e correto é "alto" com % < 75
      // - Usuário escolheu "medio" e correto é "baixo" com % > 25
      // - Usuário escolheu "baixo" e correto é "medio" com % < 45
      
      if (userAnswer === 'alto' && correctAnswer === 'medio' && percentage > 55) return true
      if (userAnswer === 'medio' && correctAnswer === 'alto' && percentage < 75) return true
      if (userAnswer === 'medio' && correctAnswer === 'baixo' && percentage > 25) return true
      if (userAnswer === 'baixo' && correctAnswer === 'medio' && percentage < 45) return true
      
      return false
    },
    
    getExplanation(risk, percentage) {
      if (risk === 'baixo') {
        return `Com ${percentage}% de risco, o paciente apresenta poucos fatores de risco cardiovascular.`
      } else if (risk === 'medio') {
        return `Com ${percentage}% de risco, o paciente apresenta fatores moderados que requerem atenção.`
      } else {
        return `Com ${percentage}% de risco, o paciente apresenta múltiplos fatores de alto risco cardiovascular.`
      }
    },
    
    async saveToHistory(gabarito, resposta, acertou) {
      try {
        const token = localStorage.getItem('token')
        if (!token) {
          console.log('Token não encontrado')
          return
        }
        
        console.log('Salvando no histórico:', { gabarito, resposta, acertou })
        
        const response = await api.post('/save-caso', {
          caso_dados: this.currentCase,
          gabarito: gabarito,
          resposta: resposta,
          acertou: acertou
        }, {
          headers: { Authorization: `Bearer ${token}` }
        })
        
        console.log('Salvo com sucesso:', response.data)
      } catch (error) {
        console.error('Erro ao salvar no histórico:', error)
        handleApiError(error, 'SAVE_CASE')
      }
    }
  }
}
</script>

<style scoped>
/* Floating Chat Button with Liquid Glass Effect */
.floating-chat-btn {
  position: fixed !important;
  bottom: 80px !important;
  right: 20px !important;
  z-index: 1000 !important;
  background: rgba(187, 134, 252, 0.2) !important;
  backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(187, 134, 252, 0.3) !important;
  animation: float 3s ease-in-out infinite !important;
}

.floating-chat-btn:hover {
  background: rgba(187, 134, 252, 0.3) !important;
  transform: scale(1.1) !important;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

/* Chat Dialog Styles */
.chat-dialog .v-overlay__content {
  margin: 0 !important;
  height: 100% !important;
  width: 100% !important;
}

.chat-card {
  height: 100% !important;
  background: rgb(var(--v-theme-surface)) !important;
  border-radius: 0 !important;
}

.chat-container {
  height: calc(100vh - 64px) !important;
  overflow: hidden !important;
}

@media (min-width: 768px) {
  .floating-chat-btn {
    bottom: 20px !important;
  }
}


</style>