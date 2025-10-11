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
      loading: false
    }
  },
  mounted() {
    this.messages.push({
      role: 'assistant',
      content: 'Olá! Sou uma IA especializada em cardiologia. Posso explicar melhor o diagnóstico, fatores de risco e responder suas dúvidas sobre este caso. O que gostaria de saber?'
    })
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
          patient_data: this.patientData,
          prediction: this.prediction,
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
