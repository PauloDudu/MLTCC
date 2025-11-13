<template>
  <div class="login-container">
    <v-card class="login-card" max-width="500" width="90%">
      <v-card-title class="text-center">
        <v-icon class="mr-2">mdi-heart-pulse</v-icon>
        CardioLearn AI
      </v-card-title>
      
      <v-card-text>
        <v-form @submit.prevent="isLogin ? login() : register()">
          <v-text-field
            v-model="form.login"
            label="Login"
            prepend-icon="mdi-account"
            required
          />
          
          <v-text-field
            v-if="!isLogin"
            v-model="form.nome"
            label="Nome"
            prepend-icon="mdi-account-circle"
            required
          />
          
          <v-text-field
            v-model="form.senha"
            label="Senha"
            type="password"
            prepend-icon="mdi-lock"
            required
          />
          
          <v-btn
            type="submit"
            color="primary"
            block
            class="mt-4"
            :loading="loading"
          >
            {{ isLogin ? 'Entrar' : 'Cadastrar' }}
          </v-btn>
        </v-form>
        
        <v-btn
          variant="text"
          block
          class="mt-2"
          @click="isLogin = !isLogin"
        >
          {{ isLogin ? 'Criar conta' : 'Já tenho conta' }}
        </v-btn>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import api from '@/services/api'
import { showSuccess, handleApiError } from '@/utils/alerts'

export default {
  data() {
    return {
      isLogin: true,
      loading: false,
      form: {
        login: '',
        nome: '',
        senha: ''
      }
    }
  },
  methods: {
    async login() {
      this.loading = true
      try {
        const response = await api.post('/login', {
          login: this.form.login,
          senha: this.form.senha
        })
        
        localStorage.setItem('token', response.data.token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
        
        this.$router.push('/home')
      } catch (error) {
        handleApiError(error, 'LOGIN')
      }
      this.loading = false
    },
    
    async register() {
      this.loading = true
      try {
        await api.post('/register', this.form)
        await showSuccess('Sucesso!', 'Usuário criado com sucesso!')
        this.isLogin = true
      } catch (error) {
        handleApiError(error, 'CADASTRO')
      }
      this.loading = false
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: rgb(var(--v-theme-background));
  position: relative;
}

.login-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 20% 80%, rgba(187, 134, 252, 0.1) 0%, transparent 50%),
              radial-gradient(circle at 80% 20%, rgba(187, 134, 252, 0.05) 0%, transparent 50%);
}

.login-card {
  background: rgb(var(--v-theme-surface)) !important;
  border: 1px solid rgba(98, 0, 234, 0.2) !important;
  backdrop-filter: blur(10px);
  position: relative;
  z-index: 1;
  border-radius: 16px !important;
  padding: 8px;
}

@media (max-width: 600px) {
  .login-card {
    margin: 16px;
    width: calc(100% - 32px) !important;
    max-width: none !important;
  }
}

.login-card .v-card-title {
  color: rgb(var(--v-theme-primary)) !important;
}

@media (max-width: 768px) {
  .login-card * {
    -webkit-tap-highlight-color: transparent !important;
    -webkit-touch-callout: none !important;
    -webkit-user-select: none !important;
    -moz-user-select: none !important;
    -ms-user-select: none !important;
    user-select: none !important;
  }

  .login-card .v-text-field {
    -webkit-user-select: text !important;
    -moz-user-select: text !important;
    -ms-user-select: text !important;
    user-select: text !important;
  }

  .login-card .v-card-text,
  .login-card .v-card-title {
    pointer-events: none;
  }

  .login-card .v-btn,
  .login-card .v-text-field {
    pointer-events: auto;
  }
}
</style>