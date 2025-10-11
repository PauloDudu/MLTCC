<template>
  <v-container fluid class="home-container">
    <PageHeader 
      title="CardioLearn AI" 
      subtitle="Sistema Inteligente para Ensino de Doenças Cardiovasculares"
      icon="mdi-heart-pulse"
      large
    />

    <v-row class="justify-center align-stretch">
      <v-col cols="12" sm="6" lg="4" class="d-flex">
        <FeatureCard
          title="Predição com IA"
          description="Análise inteligente de risco cardiovascular usando machine learning"
          icon="mdi-brain"
          color="primary"
          to="/predict"
          button-text="Iniciar Predição"
        />
      </v-col>

      <v-col cols="12" sm="6" lg="4" class="d-flex">
        <FeatureCard
          title="Casos Clínicos"
          description="Pratique com casos reais e compare com a IA"
          icon="mdi-stethoscope"
          color="secondary"
          to="/cases"
          button-text="Praticar Agora"
        />
      </v-col>

      <v-col cols="12" sm="6" lg="4" class="d-flex">
        <FeatureCard
          title="Métricas da IA"
          description="Veja como o modelo foi treinado e suas limitações"
          icon="mdi-chart-box"
          color="warning"
          to="/metrics"
          button-text="Ver Métricas"
        />
      </v-col>
    </v-row>

    <!-- Seção de estatísticas -->
    <v-row class="mt-8 justify-center">
      <v-col cols="12">
        <v-card class="stats-card gradient-bg" elevation="4">
          <v-card-text class="text-center pa-6 white--text">
            <v-row class="align-center">
              <v-col cols="12" sm="4">
                <div class="stat-item">
                  <div class="text-h4 font-weight-bold">68.742</div>
                  <div class="text-body-1 opacity-90">Casos Analisados</div>
                </div>
              </v-col>
              <v-col cols="12" sm="4">
                <div class="stat-item">
                  <div class="text-h4 font-weight-bold">71%</div>
                  <div class="text-body-1 opacity-90">Precisão da IA</div>
                </div>
              </v-col>
              <v-col cols="12" sm="4">
                <div class="stat-item">
                  <div class="text-h4 font-weight-bold">100%</div>
                  <div class="text-body-1 opacity-90">Educacional</div>
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
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
.home-container {
  max-width: 1200px;
  margin: 0 auto;
}

.stats-card {
  border-radius: 16px !important;
  margin-top: 32px;
}

.stat-item {
  padding: 16px 0;
}

@media (max-width: 960px) {
  .stats-card {
    margin-top: 24px;
  }
  
  .stat-item {
    padding: 8px 0;
  }
  
  .text-h4 {
    font-size: 1.75rem !important;
  }
}

@media (max-width: 600px) {
  .v-row {
    margin: -4px !important;
  }
  
  .v-col {
    padding: 4px !important;
  }
}
</style>