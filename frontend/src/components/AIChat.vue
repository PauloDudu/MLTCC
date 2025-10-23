<template>
  <v-card flat class="chat-card mt-4">
    <v-card-title class="bg-secondary text-white">
      <v-icon left>mdi-chat</v-icon>
      Chat com IA - Tire suas dúvidas
    </v-card-title>
    <v-card-text class="pa-0">
      <div class="chat-messages pa-3" ref="messagesContainer">
        <div v-for="(msg, index) in messages" :key="index" class="message mb-3">
          <v-card 
            :color="msg.role === 'user' ? 'primary' : 'surface'"
            :class="msg.role === 'user' ? 'ml-auto' : 'mr-auto'"
            class="message-card"
            elevation="0"
          >
            <v-card-text class="pa-2">
              <div class="text-caption mb-1">
                {{ msg.role === 'user' ? '👤 Você' : '🤖 IA Médica' }}
              </div>
              <div class="text-body-2" v-html="formatMessage(msg.content)"></div>
            </v-card-text>
          </v-card>
        </div>
        <div v-if="loading" class="text-center">
          <v-progress-circular indeterminate color="primary" size="24"></v-progress-circular>
        </div>
      </div>
      
      <v-divider></v-divider>
      
      <div class="chat-input pa-3">
        <v-text-field
          v-model="userMessage"
          placeholder="Pergunte sobre o diagnóstico, fatores de risco, recomendações..."
          variant="outlined"
          density="compact"
          hide-details
          @keyup.enter="sendMessage"
        >
          <template v-slot:append-inner>
            <v-btn 
              icon 
              size="small" 
              color="primary" 
              @click="sendMessage"
              :disabled="!userMessage.trim() || loading"
            >
              <v-icon>mdi-send</v-icon>
            </v-btn>
          </template>
        </v-text-field>
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
import { cardiovascularAPI } from '../services/api'
import { marked } from 'marked'

export default {
  name: 'AIChat',
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
  data() {
    return {
      messages: [],
      userMessage: '',
      loading: false,
      contextData: null,
      contextPrediction: null
    }
  },
  mounted() {
    this.initializeContext()
  },
  watch: {
    patientData: {
      handler() {
        this.initializeContext()
      },
      deep: true
    },
    prediction: {
      handler() {
        this.initializeContext()
      },
      deep: true
    }
  },
  methods: {
    async sendMessage() {
      if (!this.userMessage.trim() || this.loading) return
      
      const message = this.userMessage.trim()
      this.messages.push({
        role: 'user',
        content: message
      })
      
      this.userMessage = ''
      this.loading = true
      
      try {
        const response = await cardiovascularAPI.chatWithAI({
          message,
          patient_data: this.contextData,
          prediction: this.contextPrediction,
          chat_history: this.messages.slice(-6)
        })
        
        this.messages.push({
          role: 'assistant',
          content: response.response
        })
      } catch (error) {
        this.messages.push({
          role: 'assistant',
          content: 'Desculpe, ocorreu um erro. Tente novamente.'
        })
      } finally {
        this.loading = false
        this.$nextTick(() => {
          this.scrollToBottom()
        })
      }
    },
    
    scrollToBottom() {
      const container = this.$refs.messagesContainer
      if (container) {
        container.scrollTop = container.scrollHeight
      }
    },
    
    formatMessage(content) {
      return marked(content, { breaks: true })
    },
    
    getRiskLabel(risk) {
      const labels = {
        'baixo': 'BAIXO',
        'medio': 'MÉDIO', 
        'alto': 'ALTO'
      }
      return labels[risk] || risk.toUpperCase()
    },
    
    initializeContext() {
      if (!this.contextData || !this.contextPrediction) {
        this.contextData = JSON.parse(JSON.stringify(this.patientData))
        this.contextPrediction = JSON.parse(JSON.stringify(this.prediction))
        
        this.messages = [{
          role: 'assistant',
          content: `Olá! Analisei o caso com os seguintes dados:\n\n**Paciente:** ${this.contextData.age} anos, ${this.contextData.gender === 1 ? 'Feminino' : 'Masculino'}\n**Risco:** ${this.getRiskLabel(this.contextPrediction.risk_level)} (${(this.contextPrediction.probability * 100).toFixed(1)}%)\n\nPosso explicar melhor o diagnóstico, fatores de risco e responder suas dúvidas sobre este caso específico. O que gostaria de saber?`
        }]
      }
    },
    
    resetContext() {
      this.contextData = null
      this.contextPrediction = null
      this.messages = []
    }
  }
}
</script>

<style scoped>
.chat-messages {
  height: 300px;
  overflow-y: auto;
  background: #000000;
}

.message-card {
  max-width: 80%;
  border-radius: 8px !important;
}

.chat-input {
  background: #121212;
}

.text-body-2 >>> strong {
  color: #BB86FC;
  font-weight: 600;
}

.text-body-2 >>> p {
  margin: 0;
  line-height: 1.5;
}

.text-body-2 >>> ul {
  margin: 4px 0;
  padding-left: 20px;
}
</style>
