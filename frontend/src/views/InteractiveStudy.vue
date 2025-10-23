<template>
  <div class="bento-grid" style="grid-template-columns: repeat(12, 1fr); grid-template-areas: 'hero hero hero hero hero hero hero hero hero hero hero hero' 'controls controls controls controls controls controls result result result result result result' 'chart chart chart chart chart chart analysis analysis analysis analysis analysis analysis';">
    <!-- Hero Section -->
    <div class="bento-item hero bento-hero text-center">
      <v-icon size="48" class="mb-4">mdi-flask</v-icon>
      <h1 class="text-h4 font-weight-bold mb-2">Estudo Interativo</h1>
      <p class="text-body-1 opacity-80">Veja como cada variável impacta o risco cardiovascular em tempo real</p>
    </div>

    <!-- Controls Section -->
    <div class="bento-item controls" style="grid-area: controls;">
      <h3 class="text-h6 font-weight-bold mb-3">
        <v-icon left color="#BB86FC">mdi-tune</v-icon>
        Dados do Paciente
      </h3>
      <div class="d-flex flex-column ga-3">
        <div>
          <label class="text-body-2 mb-1 d-block">Idade: {{ baseData.age }} anos</label>
          <v-slider v-model="baseData.age" min="30" max="80" @update:model-value="updatePrediction" color="#BB86FC" thumb-label></v-slider>
        </div>
        
        <div>
          <label class="text-body-2 mb-1 d-block">Peso: {{ baseData.weight }} kg</label>
          <v-slider v-model="baseData.weight" min="40" max="150" @update:model-value="updatePrediction" color="#BB86FC" thumb-label></v-slider>
        </div>
        
        <div>
          <label class="text-body-2 mb-1 d-block">Pressão Sistólica: {{ baseData.ap_hi }} mmHg</label>
          <v-slider v-model="baseData.ap_hi" min="90" max="200" @update:model-value="updatePrediction" color="#BB86FC" thumb-label></v-slider>
        </div>
        
        <div>
          <label class="text-body-2 mb-1 d-block">Colesterol: {{ getColesterolLabel(baseData.cholesterol) }}</label>
          <v-slider v-model="baseData.cholesterol" min="1" max="3" @update:model-value="updatePrediction" color="#BB86FC" thumb-label></v-slider>
        </div>
      </div>
    </div>

    <!-- Result Section -->
    <div class="bento-item result" style="grid-area: result;">
      <h3 class="text-h6 font-weight-bold mb-3">
        <v-icon left color="#BB86FC">mdi-heart-pulse</v-icon>
        Predição em Tempo Real
      </h3>
      <div v-if="currentPrediction">
        <v-card :color="getRiskColor(currentPrediction.risk_level)" class="mb-3 pa-3" dark>
          <div class="text-center">
            <div class="text-h6 font-weight-bold">{{ getRiskLabel(currentPrediction.risk_level) }}</div>
            <div class="text-body-1">{{ (currentPrediction.probability * 100).toFixed(1) }}%</div>
          </div>
        </v-card>
        
        <div class="text-body-2 opacity-80">
          Ajuste os controles para ver como cada variável afeta o risco cardiovascular.
        </div>
      </div>
    </div>

    <!-- Chart Section -->
    <div class="bento-item chart" style="grid-area: chart;">
      <h3 class="text-h6 font-weight-bold mb-3">
        <v-icon left color="#BB86FC">mdi-chart-line</v-icon>
        Histórico de Risco
      </h3>
      <div class="chart-container">
        <canvas ref="riskChart" width="300" height="150"></canvas>
      </div>
    </div>

    <!-- Analysis Section -->
    <div class="bento-item analysis" style="grid-area: analysis;">
      <h3 class="text-h6 font-weight-bold mb-3">
        <v-icon left color="#BB86FC">mdi-magnify</v-icon>
        Análise de Impacto
      </h3>
      <div v-if="impactAnalysis.length > 0" class="d-flex flex-column ga-2">
        <div v-for="analysis in impactAnalysis" :key="analysis.variable" class="d-flex justify-space-between">
          <span class="text-body-2">{{ analysis.variable }}:</span>
          <span class="text-body-2" :class="analysis.impact > 0 ? 'text-error' : 'text-success'">
            {{ analysis.impact > 0 ? '+' : '' }}{{ (analysis.impact * 100).toFixed(1) }}%
          </span>
        </div>
      </div>
      <div v-else class="text-body-2 opacity-60">
        Ajuste os controles para ver o impacto...
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
    
    getRiskColor(risk) {
      const colors = {
        'baixo': 'success',
        'medio': 'warning',
        'alto': 'error'
      }
      return colors[risk] || 'primary'
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

<style scoped>
.chart-container {
  background: #1a1a1a;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #2d2d2d;
}
</style>