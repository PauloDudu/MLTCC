<template>
  <v-container fluid class="pa-4">
    <PageHeader 
      title="Predição de Risco Cardiovascular" 
      icon="mdi-heart-pulse"
    />

    <v-row class="mt-6">
      <v-col cols="12" md="6">
        <v-card flat>
          <v-card-title class="bg-primary white--text">
            <v-icon left>mdi-account-heart</v-icon>
            Dados do Paciente
          </v-card-title>
          <v-card-text>
            <v-form @submit.prevent="predictRisk">
              <v-row>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model.number="patientData.age"
                    label="Idade"
                    type="number"
                    variant="outlined"
                    prepend-inner-icon="mdi-calendar"
                    :rules="[rules.required, rules.ageRange]"
                    hint="30-80 anos"
                    persistent-hint
                  ></v-text-field>
                </v-col>
                
                <v-col cols="12" sm="6">
                  <v-select
                    v-model.number="patientData.gender"
                    :items="genderOptions"
                    label="Gênero"
                    variant="outlined"
                    prepend-inner-icon="mdi-human-male-female"
                  ></v-select>
                </v-col>
                
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model.number="patientData.height"
                    label="Altura"
                    type="number"
                    variant="outlined"
                    prepend-inner-icon="mdi-human-male-height"
                    suffix="cm"
                    hint="150-200 cm"
                    persistent-hint
                  ></v-text-field>
                </v-col>
                
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model.number="patientData.weight"
                    label="Peso"
                    type="number"
                    variant="outlined"
                    prepend-inner-icon="mdi-weight-kilogram"
                    suffix="kg"
                    hint="40-150 kg"
                    persistent-hint
                  ></v-text-field>
                </v-col>
                
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model.number="patientData.ap_hi"
                    label="Pressão Sistólica"
                    type="number"
                    variant="outlined"
                    prepend-inner-icon="mdi-gauge"
                    suffix="mmHg"
                    hint="90-200 mmHg"
                    persistent-hint
                  ></v-text-field>
                </v-col>
                
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model.number="patientData.ap_lo"
                    label="Pressão Diastólica"
                    type="number"
                    variant="outlined"
                    prepend-inner-icon="mdi-gauge-low"
                    suffix="mmHg"
                    hint="60-120 mmHg"
                    persistent-hint
                  ></v-text-field>
                </v-col>
                
                <v-col cols="12" sm="6">
                  <v-select
                    v-model.number="patientData.cholesterol"
                    :items="cholesterolOptions"
                    label="Nível de Colesterol"
                    variant="outlined"
                    prepend-inner-icon="mdi-water"
                  ></v-select>
                </v-col>
                
                <v-col cols="12" sm="6">
                  <v-select
                    v-model.number="patientData.gluc"
                    :items="glucoseOptions"
                    label="Nível de Glicose"
                    variant="outlined"
                    prepend-inner-icon="mdi-diabetes"
                  ></v-select>
                </v-col>
                
                <v-col cols="12" sm="4">
                  <v-select
                    v-model.number="patientData.smoke"
                    :items="binaryOptions"
                    label="Fumante"
                    variant="outlined"
                    prepend-inner-icon="mdi-smoking"
                  ></v-select>
                </v-col>
                
                <v-col cols="12" sm="4">
                  <v-select
                    v-model.number="patientData.alco"
                    :items="binaryOptions"
                    label="Consome Álcool"
                    variant="outlined"
                    prepend-inner-icon="mdi-glass-wine"
                  ></v-select>
                </v-col>
                
                <v-col cols="12" sm="4">
                  <v-select
                    v-model.number="patientData.active"
                    :items="binaryOptions"
                    label="Atividade Física"
                    variant="outlined"
                    prepend-inner-icon="mdi-run"
                  ></v-select>
                </v-col>
              </v-row>
              
              <v-btn
                type="submit"
                color="#9C27B0"
                size="x-large"
                block
                :loading="loading"
                class="mt-6"
              >
                <v-icon left size="large">mdi-brain</v-icon>
                {{ loading ? 'Analisando...' : 'Analisar' }}
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
        
        <AIChat 
          v-if="prediction"
          :patient-data="patientData" 
          :prediction="prediction" 
        />
      </v-col>
      
      <v-col cols="12" md="6" v-if="prediction">
        <v-card flat class="result-card">
          <v-card-title class="bg-success white--text">
            <v-icon left>mdi-chart-donut</v-icon>
            Resultado da IA
          </v-card-title>
          <v-card-text>
            <v-card 
              :color="getRiskColor(prediction.risk_level)"
              class="mb-3 pa-3"
              dark
            >
              <div class="text-center">
                <v-icon size="default" class="mr-2">{{ getRiskIcon(prediction.risk_level) }}</v-icon>
                <span class="text-h6 font-weight-bold">{{ getRiskLabel(prediction.risk_level) }}</span>
                <div class="text-body-1">{{ (prediction.probability * 100).toFixed(1) }}%</div>
              </div>
            </v-card>
            
            <v-card v-if="Object.keys(prediction.factors).length > 0" class="mb-4" flat>
              <v-card-title class="text-subtitle-1">
                <v-icon left color="orange" size="small">mdi-alert</v-icon>
                Fatores de Risco
              </v-card-title>
              <v-card-text class="pa-3">
                <v-chip
                  v-for="(factor, key) in prediction.factors"
                  :key="key"
                  color="orange"
                  size="small"
                  class="ma-1"
                >
                  {{ factor }}
                </v-chip>
              </v-card-text>
            </v-card>
            
            <v-card class="mt-4" flat>
              <v-card-text class="pa-3">
                <div class="text-subtitle-2 mb-2">Recomendação:</div>
                <div class="text-body-2">{{ getRecommendations(prediction.risk_level) }}</div>
              </v-card-text>
            </v-card>
            
            <PredictionExplanation 
              :patient-data="patientData" 
              :prediction="prediction" 
            />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { cardiovascularAPI } from '../services/api'
import Swal from 'sweetalert2'
import PageHeader from '../components/PageHeader.vue'
import PredictionExplanation from '../components/PredictionExplanation.vue'
import AIChat from '../components/AIChat.vue'

export default {
  name: 'Predict',
  components: {
    PageHeader,
    PredictionExplanation,
    AIChat
  },
  data() {
    return {
      loading: false,
      prediction: null,
      patientData: {
        age: 50,
        gender: 1,
        height: 170,
        weight: 70,
        ap_hi: 120,
        ap_lo: 80,
        cholesterol: 1,
        gluc: 1,
        smoke: 0,
        alco: 0,
        active: 1
      },
      rules: {
        required: value => !!value || 'Campo obrigatório',
        ageRange: value => (value >= 18 && value <= 100) || 'Idade deve estar entre 18 e 100 anos'
      },
      genderOptions: [
        { title: 'Feminino', value: 1 },
        { title: 'Masculino', value: 2 }
      ],
      cholesterolOptions: [
        { title: 'Normal', value: 1 },
        { title: 'Acima do Normal', value: 2 },
        { title: 'Muito Acima do Normal', value: 3 }
      ],
      glucoseOptions: [
        { title: 'Normal', value: 1 },
        { title: 'Acima do Normal', value: 2 },
        { title: 'Muito Acima do Normal', value: 3 }
      ],
      binaryOptions: [
        { title: 'Não', value: 0 },
        { title: 'Sim', value: 1 }
      ]
    }
  },
  methods: {
    async predictRisk() {
      this.loading = true
      try {
        this.prediction = await cardiovascularAPI.predictRisk(this.patientData)
        
        Swal.fire({
          title: 'Predição Concluída!',
          text: `Risco ${this.getRiskLabel(this.prediction.risk_level)} detectado`,
          icon: this.getRiskSwalIcon(this.prediction.risk_level),
          confirmButtonText: 'Ver Detalhes'
        })
      } catch (error) {
        Swal.fire({
          title: 'Erro!',
          text: 'Erro ao fazer predição: ' + error.message,
          icon: 'error',
          confirmButtonText: 'Tentar Novamente'
        })
      } finally {
        this.loading = false
      }
    },
    getRiskType(risk) {
      const types = {
        'baixo': 'success',
        'medio': 'warning',
        'alto': 'error'
      }
      return types[risk] || 'info'
    },
    getRiskIcon(risk) {
      const icons = {
        'baixo': 'mdi-check-circle',
        'medio': 'mdi-alert',
        'alto': 'mdi-alert-circle'
      }
      return icons[risk] || 'mdi-information'
    },
    getRiskSwalIcon(risk) {
      const icons = {
        'baixo': 'success',
        'medio': 'warning',
        'alto': 'error'
      }
      return icons[risk] || 'info'
    },
    getRiskLabel(risk) {
      const labels = {
        'baixo': 'BAIXO',
        'medio': 'MÉDIO',
        'alto': 'ALTO'
      }
      return labels[risk] || risk.toUpperCase()
    },
    getRiskColor(risk) {
      const colors = {
        'baixo': 'success',
        'medio': 'warning',
        'alto': 'error'
      }
      return colors[risk] || 'primary'
    },
    getInterpretation(risk, probability) {
      if (risk === 'baixo') {
        return 'Baixa probabilidade de doença cardiovascular. Mantenha hábitos saudáveis.'
      } else if (risk === 'medio') {
        return 'Risco moderado. Recomenda-se acompanhamento médico e mudanças no estilo de vida.'
      } else {
        return 'Alto risco cardiovascular. Procure atendimento médico imediatamente.'
      }
    },
    getRecommendations(risk) {
      if (risk === 'baixo') {
        return 'Exercícios regulares, dieta equilibrada e check-ups anuais.'
      } else if (risk === 'medio') {
        return 'Controle da pressão arterial, redução do colesterol e acompanhamento semestral.'
      } else {
        return 'Avaliação cardiologica urgente, medicação e monitoramento contínuo.'
      }
    }
  }
}
</script>

<style scoped>
.result-card {
  animation: slideInRight 0.3s ease-out;
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>