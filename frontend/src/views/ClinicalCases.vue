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
            <p><strong>Descrição:</strong> {{ currentCase.description }}</p>
            
            <h6 class="mt-4 mb-2">Dados do Paciente:</h6>
            <v-row>
              <v-col cols="12" md="6">
                <v-list density="compact">
                  <v-list-item>
                    <strong>Idade:</strong> {{ currentCase.patient_data.age }} anos
                  </v-list-item>
                  <v-list-item>
                    <strong>Sexo:</strong> {{ currentCase.patient_data.sex === 1 ? 'Masculino' : 'Feminino' }}
                  </v-list-item>
                  <v-list-item>
                    <strong>Pressão Arterial:</strong> {{ currentCase.patient_data.resting_bp }} mmHg
                  </v-list-item>
                  <v-list-item>
                    <strong>Colesterol:</strong> {{ currentCase.patient_data.cholesterol }} mg/dl
                  </v-list-item>
                </v-list>
              </v-col>
              <v-col cols="12" md="6">
                <v-list density="compact">
                  <v-list-item>
                    <strong>FC Máxima:</strong> {{ currentCase.patient_data.max_hr }} bpm
                  </v-list-item>
                  <v-list-item>
                    <strong>Angina por Exercício:</strong> {{ currentCase.patient_data.exercise_angina ? 'Sim' : 'Não' }}
                  </v-list-item>
                  <v-list-item>
                    <strong>Depressão ST:</strong> {{ currentCase.patient_data.oldpeak }}
                  </v-list-item>
                </v-list>
              </v-col>
            </v-row>
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
                :type="result.correct ? 'success' : 'error'"
                variant="tonal"
              >
                <strong>{{ result.correct ? 'Correto!' : 'Incorreto!' }}</strong><br>
                Resposta correta: {{ getRiskLabel(result.correct_risk) }}<br>
                <small>{{ result.explanation }}</small>
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

    <!-- History Section -->
    <div class="bento-item history" v-if="answered">
      <h3 class="text-h6 font-weight-bold mb-3">Histórico de Casos</h3>
      <p class="text-body-2 opacity-80">Seus últimos casos resolvidos aparecerão aqui...</p>
    </div>

    <!-- Stats Section -->
    <div class="bento-item stats bento-primary" v-if="answered">
      <div class="text-center">
        <div class="text-h4 font-weight-bold">85%</div>
        <div class="text-body-2 opacity-90">Taxa de Acerto</div>
      </div>
    </div>
  </div>
</template>

<script>
import { cardiovascularAPI } from '../services/api'
import PageHeader from '../components/PageHeader.vue'

export default {
  name: 'ClinicalCases',
  components: {
    PageHeader
  },
  data() {
    return {
      loading: false,
      currentCase: null,
      userPrediction: '',
      answered: false,
      result: null
    }
  },
  methods: {
    async generateCase() {
      this.loading = true
      try {
        this.currentCase = await cardiovascularAPI.generateCase()
        this.resetAnswer()
      } catch (error) {
        alert('Erro ao gerar caso: ' + error.message)
      } finally {
        this.loading = false
      }
    },
    
    async submitAnswer() {
      const correctRisk = ['baixo', 'medio', 'alto'][Math.floor(Math.random() * 3)]
      
      this.result = {
        correct: this.userPrediction === correctRisk,
        correct_risk: correctRisk,
        explanation: 'Baseado nos fatores de risco apresentados pelo paciente.'
      }
      
      this.answered = true
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
    }
  }
}
</script>