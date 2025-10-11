<template>
  <v-card flat class="explanation-card">
    <v-card-title class="bg-info white--text">
      <v-icon left>mdi-lightbulb</v-icon>
      Explicação da Decisão
    </v-card-title>
    <v-card-text class="pa-4">
      <div class="mb-4">
        <div class="text-subtitle-1 mb-2">Como a IA chegou nesta conclusão:</div>
        <div class="text-body-2 text-medium-emphasis">
          Cada variável contribui positiva ou negativamente para o risco. 
          Barras vermelhas aumentam o risco, barras verdes diminuem.
        </div>
      </div>

      <div class="feature-importance">
        <div 
          v-for="feature in featureImportances" 
          :key="feature.name"
          class="feature-row mb-3"
        >
          <div class="d-flex align-center mb-1">
            <v-icon :color="feature.color" size="small" class="mr-2">{{ feature.icon }}</v-icon>
            <span class="feature-name">{{ feature.name }}</span>
            <v-spacer></v-spacer>
            <span class="feature-value">{{ feature.displayValue }}</span>
          </div>
          
          <div class="impact-bar-container">
            <div class="impact-bar-background">
              <div 
                class="impact-bar"
                :class="feature.impact > 0 ? 'positive-impact' : 'negative-impact'"
                :style="{ width: Math.abs(feature.impact) + '%' }"
              ></div>
            </div>
            <div class="impact-text">
              <span :class="feature.impact > 0 ? 'text-error' : 'text-success'">
                {{ feature.impact > 0 ? '+' : '' }}{{ feature.impact.toFixed(1) }}%
              </span>
              <span class="text-caption ml-2">{{ feature.explanation }}</span>
            </div>
          </div>
        </div>
      </div>

      <v-divider class="my-4"></v-divider>

      <div class="summary-section">
        <div class="text-subtitle-2 mb-2">Resumo da Análise:</div>
        <v-chip 
          v-for="factor in topFactors" 
          :key="factor"
          :color="getFactorColor(factor)"
          size="small"
          class="ma-1"
        >
          {{ factor }}
        </v-chip>
      </div>
      
      <v-card v-if="prediction.ai_explanation" color="info" variant="tonal" class="pa-3 mt-3">
        <div class="text-subtitle-2 mb-2">🤖 Explicação Personalizada:</div>
        <div class="text-body-2">{{ prediction.ai_explanation }}</div>
      </v-card>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'PredictionExplanation',
  props: {
    patientData: {
      type: Object,
      required: true
    },
    prediction: {
      type: Object,
      required: true
    }
  },
  computed: {
    featureImportances() {
      return this.calculateFeatureImportances()
    },
    topFactors() {
      return this.featureImportances
        .filter(f => Math.abs(f.impact) > 5)
        .map(f => f.name)
        .slice(0, 4)
    }
  },
  methods: {
    calculateFeatureImportances() {
      const data = this.patientData
      const features = []

      // Idade - maior impacto
      const ageImpact = this.calculateAgeImpact(data.age)
      features.push({
        name: 'Idade',
        value: data.age,
        displayValue: `${data.age} anos`,
        impact: ageImpact,
        explanation: ageImpact > 0 ? 'Idade avançada aumenta risco' : 'Idade favorável',
        icon: 'mdi-calendar',
        color: ageImpact > 0 ? 'error' : 'success'
      })

      // Pressão Sistólica
      const sysImpact = this.calculatePressureImpact(data.ap_hi, 'systolic')
      features.push({
        name: 'Pressão Sistólica',
        value: data.ap_hi,
        displayValue: `${data.ap_hi} mmHg`,
        impact: sysImpact,
        explanation: sysImpact > 0 ? 'Pressão elevada' : 'Pressão normal',
        icon: 'mdi-gauge',
        color: sysImpact > 0 ? 'error' : 'success'
      })

      // Pressão Diastólica
      const diaImpact = this.calculatePressureImpact(data.ap_lo, 'diastolic')
      features.push({
        name: 'Pressão Diastólica',
        value: data.ap_lo,
        displayValue: `${data.ap_lo} mmHg`,
        impact: diaImpact,
        explanation: diaImpact > 0 ? 'Pressão elevada' : 'Pressão normal',
        icon: 'mdi-gauge-low',
        color: diaImpact > 0 ? 'error' : 'success'
      })

      // Colesterol
      const cholImpact = this.calculateCholesterolImpact(data.cholesterol)
      features.push({
        name: 'Colesterol',
        value: data.cholesterol,
        displayValue: this.getCholesterolLabel(data.cholesterol),
        impact: cholImpact,
        explanation: cholImpact > 0 ? 'Nível elevado' : 'Nível normal',
        icon: 'mdi-water',
        color: cholImpact > 0 ? 'error' : 'success'
      })

      // IMC calculado
      const bmi = data.weight / ((data.height / 100) ** 2)
      const bmiImpact = this.calculateBMIImpact(bmi)
      features.push({
        name: 'IMC',
        value: bmi,
        displayValue: `${bmi.toFixed(1)} kg/m²`,
        impact: bmiImpact,
        explanation: bmiImpact > 0 ? 'Sobrepeso/Obesidade' : 'Peso normal',
        icon: 'mdi-scale-bathroom',
        color: bmiImpact > 0 ? 'warning' : 'success'
      })

      // Fumo
      const smokeImpact = data.smoke === 1 ? 8 : -2
      features.push({
        name: 'Tabagismo',
        value: data.smoke,
        displayValue: data.smoke === 1 ? 'Fumante' : 'Não fumante',
        impact: smokeImpact,
        explanation: data.smoke === 1 ? 'Fator de risco importante' : 'Fator protetor',
        icon: 'mdi-smoking',
        color: data.smoke === 1 ? 'error' : 'success'
      })

      // Atividade física
      const activeImpact = data.active === 1 ? -6 : 4
      features.push({
        name: 'Atividade Física',
        value: data.active,
        displayValue: data.active === 1 ? 'Ativo' : 'Sedentário',
        impact: activeImpact,
        explanation: data.active === 1 ? 'Fator protetor' : 'Sedentarismo aumenta risco',
        icon: 'mdi-run',
        color: data.active === 1 ? 'success' : 'warning'
      })

      return features.sort((a, b) => Math.abs(b.impact) - Math.abs(a.impact))
    },

    calculateAgeImpact(age) {
      if (age < 40) return -5
      if (age < 50) return 0
      if (age < 60) return 8
      if (age < 70) return 15
      return 25
    },

    calculatePressureImpact(pressure, type) {
      const thresholds = type === 'systolic' 
        ? { normal: 120, high: 140, veryHigh: 180 }
        : { normal: 80, high: 90, veryHigh: 110 }
      
      if (pressure < thresholds.normal) return -3
      if (pressure < thresholds.high) return 2
      if (pressure < thresholds.veryHigh) return 12
      return 20
    },

    calculateCholesterolImpact(level) {
      return (level - 1) * 6
    },

    calculateBMIImpact(bmi) {
      if (bmi < 18.5) return 2
      if (bmi < 25) return -2
      if (bmi < 30) return 5
      return 12
    },

    getCholesterolLabel(level) {
      const labels = { 1: 'Normal', 2: 'Alto', 3: 'Muito Alto' }
      return labels[level] || 'Desconhecido'
    },

    getFactorColor(factor) {
      const colors = {
        'Idade': 'error',
        'Pressão Sistólica': 'error',
        'Pressão Diastólica': 'error',
        'Colesterol': 'warning',
        'IMC': 'warning',
        'Tabagismo': 'error',
        'Atividade Física': 'success'
      }
      return colors[factor] || 'primary'
    }
  }
}
</script>

<style scoped>
.explanation-card {
  margin-top: 16px;
}

.feature-row {
  border-left: 3px solid transparent;
  padding-left: 8px;
  transition: all 0.3s ease;
}

.feature-row:hover {
  border-left-color: var(--v-primary-base);
  background: rgba(0, 0, 0, 0.02);
}

.v-theme--dark .feature-row:hover {
  background: rgba(255, 255, 255, 0.05);
}

.feature-name {
  font-weight: 500;
  min-width: 120px;
}

.feature-value {
  font-weight: 600;
  min-width: 80px;
  text-align: right;
}

.impact-bar-container {
  margin-left: 24px;
}

.impact-bar-background {
  height: 8px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  position: relative;
  overflow: hidden;
}

.v-theme--dark .impact-bar-background {
  background: rgba(255, 255, 255, 0.1);
}

.impact-bar {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}

.positive-impact {
  background: linear-gradient(90deg, #FF5252, #F44336);
}

.negative-impact {
  background: linear-gradient(90deg, #4CAF50, #388E3C);
}

.impact-text {
  display: flex;
  align-items: center;
  margin-top: 4px;
  font-size: 0.875rem;
}

.summary-section {
  background: rgba(0, 0, 0, 0.02);
  padding: 12px;
  border-radius: 8px;
}

.v-theme--dark .summary-section {
  background: rgba(255, 255, 255, 0.05);
}
</style>