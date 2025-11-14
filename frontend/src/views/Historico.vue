<template>
  <div class="historico-container">
    <PageHeader 
      title="Histórico de Casos" 
      subtitle="Acompanhe seu progresso nos casos clínicos"
    />
    
    <v-container>
      <v-row>
        <v-col cols="6" md="6">
          <v-card class="stats-card">
            <v-card-text>
              <div class="text-h4 text-success">{{ acertos }}</div>
              <div class="text-subtitle-1">Acertos</div>
            </v-card-text>
          </v-card>
        </v-col>
        
        <v-col cols="6" md="6">
          <v-card class="stats-card">
            <v-card-text>
              <div class="text-h4 text-error">{{ erros }}</div>
              <div class="text-subtitle-1">Erros</div>
            </v-card-text>
          </v-card>
        </v-col>
        
        <v-col cols="6" md="6">
          <v-card class="stats-card">
            <v-card-text>
              <div class="text-h4 text-primary">{{ total }}</div>
              <div class="text-subtitle-1">Total</div>
            </v-card-text>
          </v-card>
        </v-col>
        
        <v-col cols="6" md="6">
          <v-card class="stats-card">
            <v-card-text>
              <div class="text-h4 text-info">{{ percentual }}%</div>
              <div class="text-subtitle-1">Aproveitamento</div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      
      <v-row class="mt-4">
        <v-col cols="12">
          <v-card>
            <v-card-title>
              Histórico Detalhado
              <v-spacer></v-spacer>
              <v-btn-toggle v-model="filtro" mandatory>
                <v-btn value="todos">Todos</v-btn>
                <v-btn value="acertos">Acertos</v-btn>
                <v-btn value="erros">Erros</v-btn>
              </v-btn-toggle>
            </v-card-title>
            
            <v-card-text>
              <!-- Mobile Cards -->
              <div class="d-md-none">
                <v-card
                  v-for="(item, index) in historicoFiltrado"
                  :key="index"
                  class="mb-3"
                  elevation="1"
                >
                  <v-card-text>
                    <div class="d-flex justify-space-between align-center mb-2">
                      <v-chip
                        :color="item.acertou ? 'success' : 'error'"
                        size="small"
                      >
                        {{ item.acertou ? 'Acerto' : 'Erro' }}
                      </v-chip>
                      <span class="text-caption">{{ item.data }}</span>
                    </div>
                    
                    <div class="mb-2">
                      <div class="text-caption text-medium-emphasis">Gabarito</div>
                      <div class="text-body-2 font-weight-medium">{{ item.gabarito.toUpperCase() }}</div>
                    </div>
                    
                    <div class="mb-3">
                      <div class="text-caption text-medium-emphasis">Sua Resposta</div>
                      <div class="text-body-2 font-weight-medium">{{ item.resposta.toUpperCase() }}</div>
                    </div>
                    
                    <v-btn
                      size="small"
                      color="primary"
                      variant="tonal"
                      block
                      @click="verDetalhes(item)"
                    >
                      Ver Detalhes
                    </v-btn>
                  </v-card-text>
                </v-card>
                
                <div v-if="historicoFiltrado.length === 0" class="text-center py-8">
                  <v-icon size="48" color="grey">mdi-inbox</v-icon>
                  <p class="text-body-2 mt-2">Nenhum caso encontrado</p>
                </div>
              </div>
              
              <!-- Desktop Table -->
              <div class="d-none d-md-block">
                <v-data-table
                  :headers="headers"
                  :items="historicoFiltrado"
                  :items-per-page="10"
                  class="elevation-1"
                >
                  <template v-slot:item.acertou="{ item }">
                    <v-chip
                      :color="item.acertou ? 'success' : 'error'"
                      small
                    >
                      {{ item.acertou ? 'Acerto' : 'Erro' }}
                    </v-chip>
                  </template>
                  
                  <template v-slot:item.actions="{ item }">
                    <v-btn
                      size="small"
                      color="primary"
                      @click="verDetalhes(item)"
                    >
                      Ver Detalhes
                    </v-btn>
                  </template>
                </v-data-table>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    
    <!-- Modal de Detalhes -->
    <v-dialog v-model="showDetalhes" max-width="600">
      <v-card v-if="casoSelecionado">
        <v-card-title class="d-flex align-center">
          <v-icon class="mr-2" color="primary">mdi-clipboard-text</v-icon>
          Detalhes do Caso
          <v-spacer></v-spacer>
          <v-btn icon size="small" @click="showDetalhes = false">
            <v-icon size="20">mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        
        <v-card-text>
          <!-- Dados do Paciente -->
          <div class="mb-4">
            <h3 class="text-subtitle-1 mb-2">Dados do Paciente</h3>
            <v-row>
              <v-col cols="6">
                <strong>Idade:</strong> {{ casoSelecionado.caso_dados.age }} anos
              </v-col>
              <v-col cols="6">
                <strong>Gênero:</strong> {{ casoSelecionado.caso_dados.gender === 1 ? 'Feminino' : 'Masculino' }}
              </v-col>
              <v-col cols="6">
                <strong>Altura:</strong> {{ casoSelecionado.caso_dados.height }} cm
              </v-col>
              <v-col cols="6">
                <strong>Peso:</strong> {{ casoSelecionado.caso_dados.weight }} kg
              </v-col>
              <v-col cols="6">
                <strong>Pressão:</strong> {{ casoSelecionado.caso_dados.ap_hi }}/{{ casoSelecionado.caso_dados.ap_lo }} mmHg
              </v-col>
              <v-col cols="6">
                <strong>Colesterol:</strong> {{ getCholesterolLabel(casoSelecionado.caso_dados.cholesterol) }}
              </v-col>
              <v-col cols="6">
                <strong>Glicose:</strong> {{ getGlucoseLabel(casoSelecionado.caso_dados.gluc) }}
              </v-col>
              <v-col cols="6">
                <strong>Fumante:</strong> {{ casoSelecionado.caso_dados.smoke ? 'Sim' : 'Não' }}
              </v-col>
              <v-col cols="6">
                <strong>Álcool:</strong> {{ casoSelecionado.caso_dados.alco ? 'Sim' : 'Não' }}
              </v-col>
              <v-col cols="6">
                <strong>Ativo:</strong> {{ casoSelecionado.caso_dados.active ? 'Sim' : 'Não' }}
              </v-col>
            </v-row>
          </div>
          
          <!-- Respostas -->
          <v-divider class="mb-4"></v-divider>
          <div class="mb-4">
            <h3 class="text-subtitle-1 mb-2">Resultado</h3>
            <v-row>
              <v-col cols="6">
                <v-chip color="success" variant="tonal">
                  <strong>Correto:</strong> {{ casoSelecionado.gabarito.toUpperCase() }}
                </v-chip>
              </v-col>
              <v-col cols="6">
                <v-chip :color="casoSelecionado.acertou ? 'success' : 'error'" variant="tonal">
                  <strong>Sua resposta:</strong> {{ casoSelecionado.resposta.toUpperCase() }}
                </v-chip>
              </v-col>
            </v-row>
            
            <v-alert 
              :type="casoSelecionado.acertou ? 'success' : 'error'"
              variant="tonal"
              class="mt-3"
            >
              {{ casoSelecionado.acertou ? 'Você acertou!' : 'Você errou.' }}
            </v-alert>
          </div>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn 
            color="primary" 
            variant="tonal"
            @click="abrirChat"
          >
            <v-icon left>mdi-chat-question</v-icon>
            Tirar Dúvidas
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    
    <!-- Chat Dialog -->
    <v-dialog 
      v-model="showChat" 
      fullscreen 
      hide-overlay 
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-card-title class="d-flex align-center pa-4">
          <v-btn icon size="small" @click="showChat = false" class="mr-2">
            <v-icon size="20">mdi-arrow-left</v-icon>
          </v-btn>
          <v-icon size="20" class="mr-2" color="primary">mdi-robot</v-icon>
          <span>IA - Caso do Histórico</span>
        </v-card-title>
        <v-card-text class="pa-0" style="height: calc(100vh - 64px);">
          <AIChat 
            v-if="casoSelecionado"
            :patient-data="casoSelecionado.caso_dados" 
            :prediction="{ 
              risk_level: casoSelecionado.gabarito, 
              probability: 0.5,
              user_answer: casoSelecionado.resposta,
              correct: casoSelecionado.acertou
            }" 
            @close="showChat = false"
          />
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import api from '@/services/api'
import PageHeader from '@/components/PageHeader.vue'
import AIChat from '@/components/AIChat.vue'

export default {
  components: { PageHeader, AIChat },
  data() {
    return {
      historico: [],
      filtro: 'todos',
      showDetalhes: false,
      showChat: false,
      casoSelecionado: null,
      headers: [
        { title: 'Data', key: 'data' },
        { title: 'Gabarito', key: 'gabarito' },
        { title: 'Sua Resposta', key: 'resposta' },
        { title: 'Resultado', key: 'acertou' },
        { title: 'Ações', key: 'actions', sortable: false }
      ]
    }
  },
  computed: {
    historicoFiltrado() {
      if (this.filtro === 'acertos') return this.historico.filter(h => h.acertou)
      if (this.filtro === 'erros') return this.historico.filter(h => !h.acertou)
      return this.historico
    },
    acertos() {
      return this.historico.filter(h => h.acertou).length
    },
    erros() {
      return this.historico.filter(h => !h.acertou).length
    },
    total() {
      return this.historico.length
    },
    percentual() {
      return this.total > 0 ? Math.round((this.acertos / this.total) * 100) : 0
    }
  },
  async mounted() {
    await this.carregarHistorico()
  },
  methods: {
    async carregarHistorico() {
      try {
        const token = localStorage.getItem('token')
        const response = await api.get('/historico', {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.historico = response.data.historico.map(h => ({
          ...h,
          data: new Date(h.data).toLocaleDateString('pt-BR')
        }))
      } catch (error) {
        console.error('Erro ao carregar histórico:', error)
      }
    },
    
    verDetalhes(item) {
      this.casoSelecionado = item
      this.showDetalhes = true
    },
    
    getCholesterolLabel(level) {
      const labels = { 1: 'Normal', 2: 'Alto', 3: 'Muito Alto' }
      return labels[level] || 'Desconhecido'
    },
    
    getGlucoseLabel(level) {
      const labels = { 1: 'Normal', 2: 'Alto', 3: 'Muito Alto' }
      return labels[level] || 'Desconhecido'
    },
    
    abrirChat() {
      this.showDetalhes = false
      this.showChat = true
    }
  }
}
</script>

<style scoped>
.historico-container {
  min-height: 100vh;
  background: rgb(var(--v-theme-background));
}

.stats-card {
  text-align: center;
  background: rgb(var(--v-theme-surface));
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
}
</style>