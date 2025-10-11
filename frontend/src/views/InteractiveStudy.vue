<template>
  <div class="interactive-study">
    <h2>🔬 Estudo Interativo</h2>
    
    <div class="row">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header">
            <h5>Dados Base do Paciente</h5>
          </div>
          <div class="card-body">
            <div class="mb-3">
              <label class="form-label">Idade: {{ baseData.age }}</label>
              <input v-model.number="baseData.age" type="range" class="form-range" min="30" max="80" @input="updatePrediction">
            </div>
            
            <div class="mb-3">
              <label class="form-label">Peso: {{ baseData.weight }} kg</label>
              <input v-model.number="baseData.weight" type="range" class="form-range" min="40" max="150" @input="updatePrediction">
            </div>
            
            <div class="mb-3">
              <label class="form-label">Pressão Sistólica: {{ baseData.ap_hi }} mmHg</label>
              <input v-model.number="baseData.ap_hi" type="range" class="form-range" min="90" max="200" @input="updatePrediction">
            </div>
            
            <div class="mb-3">
              <label class="form-label">Pressão Diastólica: {{ baseData.ap_lo }} mmHg</label>
              <input v-model.number="baseData.ap_lo" type="range" class="form-range" min="60" max="120" @input="updatePrediction">
            </div>
            
            <div class="mb-3">
              <label class="form-label">Colesterol: {{ getColesterolLabel(baseData.cholesterol) }}</label>
              <input v-model.number="baseData.cholesterol" type="range" class="form-range" min="1" max="3" @input="updatePrediction">
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-6">
        <div class="card">
          <div class="card-header">
            <h5>Predição em Tempo Real</h5>
          </div>
          <div class="card-body">
            <div v-if="currentPrediction" class="alert" :class="getRiskClass(currentPrediction.risk_level)">
              <h6>Risco Atual: {{ getRiskLabel(currentPrediction.risk_level) }}</h6>
              <p>Probabilidade: {{ (currentPrediction.probability * 100).toFixed(1) }}%</p>
            </div>
            
            <div v-if="impactAnalysis.length > 0">
              <h6>Análise de Impacto:</h6>
              <div v-for="analysis in impactAnalysis" :key="analysis.variable" class="mb-2">
                <small>
                  <strong>{{ analysis.variable }}:</strong> 
                  <span :class="analysis.impact > 0 ? 'text-danger' : 'text-success'">
                    {{ analysis.impact > 0 ? '+' : '' }}{{ (analysis.impact * 100).toFixed(1) }}%
                  </span>
                </small>
              </div>
            </div>
          </div>
        </div>
        
        <div class="card mt-3">
          <div class="card-header">
            <h5>Gráfico de Risco</h5>
          </div>
          <div class="card-body">
            <canvas ref="riskChart" width="400" height="200"></canvas>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { cardiovascularAPI } from '../services/api'

export default {
  name: 'InteractiveStudy',
  data() {
    return {
      baseData: {
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
      currentPrediction: null,
      impactAnalysis: [],
      riskHistory: []
    }
  },
  mounted() {
    this.updatePrediction()
  },
  methods: {
    async updatePrediction() {
      try {
        this.currentPrediction = await cardiovascularAPI.predictRisk(this.baseData)
        this.riskHistory.push({
          timestamp: new Date(),
          risk: this.currentPrediction.probability
        })
        
        // Manter apenas os últimos 10 pontos
        if (this.riskHistory.length > 10) {
          this.riskHistory.shift()
        }
        
        this.updateChart()
      } catch (error) {
        console.error('Erro ao atualizar predição:', error)
      }
    },
    
    updateChart() {
      // Implementação simplificada do gráfico
      const canvas = this.$refs.riskChart
      if (!canvas) return
      
      const ctx = canvas.getContext('2d')
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      
      // Desenhar linha de risco
      ctx.strokeStyle = '#007bff'
      ctx.lineWidth = 2
      ctx.beginPath()
      
      this.riskHistory.forEach((point, index) => {
        const x = (index / (this.riskHistory.length - 1)) * canvas.width
        const y = canvas.height - (point.risk * canvas.height)
        
        if (index === 0) {
          ctx.moveTo(x, y)
        } else {
          ctx.lineTo(x, y)
        }
      })
      
      ctx.stroke()
    },
    
    getRiskClass(risk) {
      const classes = {
        'baixo': 'alert-success',
        'medio': 'alert-warning',
        'alto': 'alert-danger'
      }
      return classes[risk] || 'alert-info'
    },
    
    getRiskLabel(risk) {
      const labels = {
        'baixo': 'BAIXO',
        'medio': 'MÉDIO',
        'alto': 'ALTO'
      }
      return labels[risk] || risk.toUpperCase()
    },
    
    getColesterolLabel(level) {
      const labels = {
        1: 'Normal',
        2: 'Alto',
        3: 'Muito Alto'
      }
      return labels[level] || level
    }
  }
}
</script>