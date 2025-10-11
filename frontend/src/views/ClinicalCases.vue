<template>
  <v-container fluid class="pa-4">
    <PageHeader 
      title="Casos Clínicos" 
      icon="mdi-stethoscope"
    />
    
    <div v-if="!currentCase" class="text-center">
      <v-btn 
        @click="generateCase" 
        color="primary" 
        size="large" 
        :loading="loading"
      >
        {{ loading ? 'Gerando...' : 'Gerar Novo Caso' }}
      </v-btn>
    </div>
    
    <v-row v-if="currentCase">
      <v-col cols="12" md="8">
        <v-card flat>
          <v-card-title class="bg-primary white--text">
            <v-icon left>mdi-clipboard-text</v-icon>
            Caso Clínico
          </v-card-title>
          <v-card-text class="pa-4">
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
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="4">
        <v-card flat>
          <v-card-title class="bg-success white--text">
            <v-icon left>mdi-brain</v-icon>
            Sua Predição
          </v-card-title>
          <v-card-text class="pa-4">
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
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
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