<template>
  <div class="bento-grid" style="grid-template-columns: repeat(20, 1fr); grid-template-areas: 'hero hero hero hero hero hero hero hero hero hero hero hero hero hero hero hero hero hero hero hero' 'dataset dataset dataset dataset dataset dataset dataset dataset dataset dataset dataset dataset dataset dataset dataset dataset dataset dataset dataset dataset' 'dataset dataset dataset dataset dataset dataset dataset dataset dataset dataset dataset dataset dataset dataset dataset dataset dataset dataset dataset dataset' 'perf perf perf perf perf perf perf perf perf perf algo algo algo algo algo algo algo algo algo algo' 'vars vars vars vars vars vars vars vars vars vars vars vars vars vars vars vars vars vars vars vars' 'train train train train train train train train train train train train train train train train train train train train' 'limits limits limits limits limits limits limits limits limits limits limits limits limits limits limits limits limits limits limits limits'; min-height: 100vh;">
    <!-- Hero Section -->
    <div class="bento-item hero bento-hero text-center">
      <v-icon size="48" class="mb-4">mdi-chart-box</v-icon>
      <h1 class="text-h4 font-weight-bold mb-2">Métricas do Modelo IA</h1>
      <p class="text-body-1 opacity-80">Transparência e explicabilidade do algoritmo de predição</p>
    </div>

    <!-- Dataset Overview -->
    <div class="bento-item dataset bento-primary" style="grid-area: dataset; padding: 24px;">
      <h3 class="text-h5 font-weight-bold mb-6">
        <v-icon left size="32">mdi-database</v-icon>
        Dataset Cardiovascular
      </h3>
      <div class="d-flex justify-space-around text-center mb-4">
        <div>
          <div class="text-h3 font-weight-bold mb-2">68.742</div>
          <div class="text-h6 opacity-90">Total de Casos</div>
          <div class="text-body-2 opacity-70 mt-1">Pacientes únicos</div>
        </div>
        <div>
          <div class="text-h3 font-weight-bold mb-2">54.994</div>
          <div class="text-h6 opacity-90">Treino (80%)</div>
          <div class="text-body-2 opacity-70 mt-1">Para aprendizado</div>
        </div>
        <div>
          <div class="text-h3 font-weight-bold mb-2">13.748</div>
          <div class="text-h6 opacity-90">Teste (20%)</div>
          <div class="text-body-2 opacity-70 mt-1">Para validação</div>
        </div>
        <div>
          <div class="text-h3 font-weight-bold mb-2">11</div>
          <div class="text-h6 opacity-90">Variáveis</div>
          <div class="text-body-2 opacity-70 mt-1">Características</div>
        </div>
      </div>
      <v-divider class="my-4"></v-divider>
      <div class="text-center">
        <v-chip color="success" size="large" class="mr-2">
          <v-icon left>mdi-check-circle</v-icon>
          Balanceado
        </v-chip>
        <v-chip color="info" size="large">
          <v-icon left>mdi-shield-check</v-icon>
          Validado
        </v-chip>
      </div>
    </div>

    <!-- Performance -->
    <div class="bento-item perf" style="grid-area: perf;">
      <h3 class="text-h6 font-weight-bold mb-3">
        <v-icon left color="#BB86FC">mdi-target</v-icon>
        Performance do Modelo
      </h3>
      <div class="d-flex flex-column ga-2">
        <div class="d-flex justify-space-between">
          <span>Acurácia Geral</span>
          <v-chip color="success" size="small">71.2%</v-chip>
        </div>
        <div class="d-flex justify-space-between">
          <span>Precisão</span>
          <v-chip color="primary" size="small">69.8%</v-chip>
        </div>
        <div class="d-flex justify-space-between">
          <span>Recall</span>
          <v-chip color="info" size="small">74.1%</v-chip>
        </div>
        <div class="d-flex justify-space-between">
          <span>F1-Score</span>
          <v-chip color="warning" size="small">71.9%</v-chip>
        </div>
      </div>
    </div>

    <!-- Algorithm -->
    <div class="bento-item algo" style="grid-area: algo;">
      <h3 class="text-h6 font-weight-bold mb-3">
        <v-icon left color="#BB86FC">mdi-brain</v-icon>
        Algoritmo
      </h3>
      <v-chip color="#BB86FC" size="large" class="mb-3">Random Forest</v-chip>
      <div class="d-flex flex-column ga-1">
        <div class="d-flex justify-space-between">
          <span class="text-body-2">Árvores:</span>
          <span class="text-body-2">100</span>
        </div>
        <div class="d-flex justify-space-between">
          <span class="text-body-2">Critério:</span>
          <span class="text-body-2">Gini</span>
        </div>
        <div class="d-flex justify-space-between">
          <span class="text-body-2">Seed:</span>
          <span class="text-body-2">42</span>
        </div>
      </div>
    </div>

    <!-- Variables -->
    <div class="bento-item vars" style="grid-area: vars;">
      <h3 class="text-h6 font-weight-bold mb-3">
        <v-icon left color="#BB86FC">mdi-format-list-bulleted</v-icon>
        Variáveis de Entrada
      </h3>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px;">
        <div v-for="variable in variables.slice(0, 6)" :key="variable.name" class="variable-mini">
          <div class="d-flex align-center mb-1">
            <v-icon :color="variable.color" size="small" class="mr-2">{{ variable.icon }}</v-icon>
            <span class="text-body-2 font-weight-medium">{{ variable.name }}</span>
          </div>
          <div class="text-caption opacity-70">{{ variable.type }}</div>
        </div>
      </div>
    </div>

    <!-- Training Process -->
    <div class="bento-item train" style="grid-area: train;">
      <h3 class="text-h6 font-weight-bold mb-3">
        <v-icon left color="#BB86FC">mdi-cog</v-icon>
        Processo de Treinamento
      </h3>
      <div class="d-flex flex-column ga-3">
        <div v-for="step in trainingSteps.slice(0, 3)" :key="step.title" class="d-flex align-start ga-3">
          <v-icon :color="step.color" size="small">{{ step.icon }}</v-icon>
          <div>
            <div class="text-body-2 font-weight-medium">{{ step.title }}</div>
            <div class="text-caption opacity-70">{{ step.description.substring(0, 60) }}...</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Limitations -->
    <div class="bento-item limits" style="grid-area: limits; border-color: #f44336;">
      <h3 class="text-h6 font-weight-bold mb-3">
        <v-icon left color="error">mdi-alert-circle</v-icon>
        Limitações
      </h3>
      <v-alert type="warning" variant="tonal" class="mb-3" density="compact">
        <strong>Uso Educacional:</strong> Não deve ser usado para diagnósticos reais.
      </v-alert>
      <div class="d-flex flex-column ga-2">
        <div class="d-flex align-start ga-2">
          <v-icon color="error" size="small">mdi-minus-circle</v-icon>
          <span class="text-body-2">Não substitui avaliação médica</span>
        </div>
        <div class="d-flex align-start ga-2">
          <v-icon color="error" size="small">mdi-minus-circle</v-icon>
          <span class="text-body-2">71% de acurácia indica margem de erro</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import PageHeader from '../components/PageHeader.vue'

export default {
  name: 'ModelMetrics',
  components: {
    PageHeader
  },
  data() {
    return {
      variables: [
        {
          name: 'Idade',
          description: 'Idade do paciente em anos (30-80)',
          type: 'Numérica',
          icon: 'mdi-calendar',
          color: 'primary'
        },
        {
          name: 'Gênero',
          description: 'Sexo biológico (1=Feminino, 2=Masculino)',
          type: 'Categórica',
          icon: 'mdi-human-male-female',
          color: 'secondary'
        },
        {
          name: 'Altura',
          description: 'Altura em centímetros (100-250cm)',
          type: 'Numérica',
          icon: 'mdi-human-male-height',
          color: 'info'
        },
        {
          name: 'Peso',
          description: 'Peso corporal em quilogramas (30-200kg)',
          type: 'Numérica',
          icon: 'mdi-weight-kilogram',
          color: 'success'
        },
        {
          name: 'Pressão Sistólica',
          description: 'Pressão arterial sistólica (70-300 mmHg)',
          type: 'Numérica',
          icon: 'mdi-gauge',
          color: 'warning'
        },
        {
          name: 'Pressão Diastólica',
          description: 'Pressão arterial diastólica (40-200 mmHg)',
          type: 'Numérica',
          icon: 'mdi-gauge-low',
          color: 'error'
        },
        {
          name: 'Colesterol',
          description: 'Nível de colesterol (1=Normal, 2=Alto, 3=Muito Alto)',
          type: 'Ordinal',
          icon: 'mdi-water',
          color: 'primary'
        },
        {
          name: 'Glicose',
          description: 'Nível de glicose (1=Normal, 2=Alto, 3=Muito Alto)',
          type: 'Ordinal',
          icon: 'mdi-diabetes',
          color: 'secondary'
        },
        {
          name: 'Fumante',
          description: 'Hábito de fumar (0=Não, 1=Sim)',
          type: 'Binária',
          icon: 'mdi-smoking',
          color: 'error'
        },
        {
          name: 'Álcool',
          description: 'Consumo de álcool (0=Não, 1=Sim)',
          type: 'Binária',
          icon: 'mdi-glass-wine',
          color: 'warning'
        },
        {
          name: 'Atividade Física',
          description: 'Pratica exercícios (0=Não, 1=Sim)',
          type: 'Binária',
          icon: 'mdi-run',
          color: 'success'
        }
      ],
      trainingSteps: [
        {
          title: 'Carregamento dos Dados',
          description: 'Dataset de 68.742 casos reais de doenças cardiovasculares carregado e validado',
          icon: 'mdi-database-import',
          color: 'primary'
        },
        {
          title: 'Limpeza e Pré-processamento',
          description: 'Remoção de outliers extremos e conversão de idade de dias para anos',
          icon: 'mdi-broom',
          color: 'warning'
        },
        {
          title: 'Divisão dos Dados',
          description: 'Separação em 80% para treino (54.994 casos) e 20% para teste (13.748 casos)',
          icon: 'mdi-call-split',
          color: 'info'
        },
        {
          title: 'Treinamento do Modelo',
          description: 'Random Forest com 100 árvores treinado nos dados de treino',
          icon: 'mdi-brain',
          color: 'success'
        },
        {
          title: 'Avaliação e Validação',
          description: 'Teste no conjunto separado resultando em 71.2% de acurácia',
          icon: 'mdi-check-circle',
          color: 'success'
        }
      ]
    }
  }
}
</script>

<style scoped>
.variable-mini {
  padding: 12px;
  background: #1a1a1a;
  border-radius: 8px;
  border: 1px solid #2d2d2d;
  transition: all 0.3s ease;
}

.variable-mini:hover {
  border-color: #BB86FC;
  transform: translateY(-1px);
}
</style>