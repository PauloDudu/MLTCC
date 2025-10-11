<template>
  <v-container fluid class="metrics-container">
    <PageHeader 
      title="Métricas do Modelo IA" 
      subtitle="Transparência e explicabilidade do algoritmo de predição"
      icon="mdi-chart-box"
    />

    <!-- Visão Geral do Dataset -->
    <v-row>
      <v-col cols="12">
        <v-card elevation="2" class="mb-4">
          <v-card-title class="gradient-bg white--text">
            <v-icon left>mdi-database</v-icon>
            Dataset Cardiovascular
          </v-card-title>
          <v-card-text class="pa-6">
            <v-row>
              <v-col cols="12" md="3">
                <div class="metric-box text-center">
                  <div class="text-h4 primary--text font-weight-bold">68.742</div>
                  <div class="text-body-2">Total de Casos</div>
                </div>
              </v-col>
              <v-col cols="12" md="3">
                <div class="metric-box text-center">
                  <div class="text-h4 success--text font-weight-bold">54.994</div>
                  <div class="text-body-2">Treino (80%)</div>
                </div>
              </v-col>
              <v-col cols="12" md="3">
                <div class="metric-box text-center">
                  <div class="text-h4 info--text font-weight-bold">13.748</div>
                  <div class="text-body-2">Teste (20%)</div>
                </div>
              </v-col>
              <v-col cols="12" md="3">
                <div class="metric-box text-center">
                  <div class="text-h4 warning--text font-weight-bold">11</div>
                  <div class="text-body-2">Variáveis</div>
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Performance do Modelo -->
    <v-row>
      <v-col cols="12" md="6">
        <v-card elevation="2">
          <v-card-title class="bg-success white--text">
            <v-icon left>mdi-target</v-icon>
            Performance do Modelo
          </v-card-title>
          <v-card-text class="pa-4">
            <v-list density="compact">
              <v-list-item>
                <v-list-item-title>Acurácia Geral</v-list-item-title>
                <template v-slot:append>
                  <v-chip color="success" size="small">71.2%</v-chip>
                </template>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Precisão (Classe Positiva)</v-list-item-title>
                <template v-slot:append>
                  <v-chip color="primary" size="small">69.8%</v-chip>
                </template>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Recall (Sensibilidade)</v-list-item-title>
                <template v-slot:append>
                  <v-chip color="info" size="small">74.1%</v-chip>
                </template>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>F1-Score</v-list-item-title>
                <template v-slot:append>
                  <v-chip color="warning" size="small">71.9%</v-chip>
                </template>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card elevation="2">
          <v-card-title class="bg-info white--text">
            <v-icon left>mdi-brain</v-icon>
            Algoritmo Utilizado
          </v-card-title>
          <v-card-text class="pa-4">
            <div class="mb-3">
              <v-chip color="primary" size="large" class="mb-2">
                Random Forest Classifier
              </v-chip>
            </div>
            <v-list density="compact">
              <v-list-item>
                <v-list-item-title>Número de Árvores</v-list-item-title>
                <template v-slot:append>100</template>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Critério de Divisão</v-list-item-title>
                <template v-slot:append>Gini</template>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Seed Aleatória</v-list-item-title>
                <template v-slot:append>42</template>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Variáveis do Modelo -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card elevation="2">
          <v-card-title class="bg-warning white--text">
            <v-icon left>mdi-format-list-bulleted</v-icon>
            Variáveis de Entrada
          </v-card-title>
          <v-card-text class="pa-4">
            <v-row>
              <v-col cols="12" sm="6" md="4" v-for="variable in variables" :key="variable.name">
                <v-card variant="outlined" class="variable-card">
                  <v-card-text class="pa-3">
                    <div class="d-flex align-center mb-2">
                      <v-icon :color="variable.color" class="mr-2">{{ variable.icon }}</v-icon>
                      <span class="font-weight-medium">{{ variable.name }}</span>
                    </div>
                    <div class="text-body-2 text-medium-emphasis">{{ variable.description }}</div>
                    <div class="text-caption mt-1">
                      <strong>Tipo:</strong> {{ variable.type }}
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Processo de Treinamento -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card elevation="2">
          <v-card-title class="gradient-bg white--text">
            <v-icon left>mdi-cog</v-icon>
            Processo de Treinamento
          </v-card-title>
          <v-card-text class="pa-4">
            <v-timeline density="compact">
              <v-timeline-item
                v-for="step in trainingSteps"
                :key="step.title"
                :dot-color="step.color"
                size="small"
              >
                <template v-slot:icon>
                  <v-icon size="small">{{ step.icon }}</v-icon>
                </template>
                <v-card variant="outlined" class="ml-3">
                  <v-card-text class="pa-3">
                    <div class="font-weight-medium mb-1">{{ step.title }}</div>
                    <div class="text-body-2">{{ step.description }}</div>
                  </v-card-text>
                </v-card>
              </v-timeline-item>
            </v-timeline>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Limitações e Considerações -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card elevation="2">
          <v-card-title class="bg-error white--text">
            <v-icon left>mdi-alert-circle</v-icon>
            Limitações e Considerações
          </v-card-title>
          <v-card-text class="pa-4">
            <v-alert type="warning" variant="tonal" class="mb-3">
              <strong>Uso Educacional:</strong> Este modelo foi desenvolvido exclusivamente para fins educacionais e não deve ser usado para diagnósticos médicos reais.
            </v-alert>
            <v-list density="compact">
              <v-list-item>
                <template v-slot:prepend>
                  <v-icon color="error">mdi-minus-circle</v-icon>
                </template>
                <v-list-item-title>Não substitui avaliação médica profissional</v-list-item-title>
              </v-list-item>
              <v-list-item>
                <template v-slot:prepend>
                  <v-icon color="error">mdi-minus-circle</v-icon>
                </template>
                <v-list-item-title>Baseado em dados históricos, pode não refletir casos individuais</v-list-item-title>
              </v-list-item>
              <v-list-item>
                <template v-slot:prepend>
                  <v-icon color="error">mdi-minus-circle</v-icon>
                </template>
                <v-list-item-title>Acurácia de 71% indica margem de erro significativa</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
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
.metrics-container {
  max-width: 1200px;
  margin: 0 auto;
}

.metric-box {
  padding: 16px;
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.02);
}

.v-theme--dark .metric-box {
  background: rgba(255, 255, 255, 0.05);
}

.variable-card {
  height: 100%;
  transition: all 0.3s ease;
}

.variable-card:hover {
  transform: translateY(-2px);
}

@media (max-width: 960px) {
  .v-timeline {
    padding-left: 0;
  }
}
</style>