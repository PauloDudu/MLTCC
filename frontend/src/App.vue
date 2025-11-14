<template>
  <v-app>
    <!-- Mobile Header -->
    <v-app-bar v-if="showNavigation" color="surface" dark elevation="0" height="56" class="mobile-header d-md-none">
      <v-app-bar-title class="text-h6 font-weight-bold">
        <v-icon class="mr-2 pulse-icon" color="primary" size="default">mdi-heart-pulse</v-icon>
        CardioLearn AI
      </v-app-bar-title>
      
      <v-spacer></v-spacer>
      
      <v-btn v-if="isLoggedIn" @click="drawer = !drawer" variant="text">
        <v-icon>mdi-menu</v-icon>
      </v-btn>
    </v-app-bar>

    <!-- Desktop Header -->
    <v-app-bar v-if="showNavigation" color="surface" dark elevation="0" height="56" class="desktop-header d-none d-md-flex">
      <v-app-bar-title class="text-h6 font-weight-bold">
        <v-icon class="mr-2 pulse-icon" color="primary" size="default">mdi-heart-pulse</v-icon>
        CardioLearn AI
      </v-app-bar-title>
      
      <v-spacer></v-spacer>
      
      <v-btn to="/home" variant="text" class="nav-btn mx-1">
        <v-icon left size="small">mdi-home</v-icon>
        <span>Início</span>
      </v-btn>
      
      <v-btn to="/predict" variant="text" class="nav-btn mx-1">
        <v-icon left size="small">mdi-brain</v-icon>
        <span>Predição</span>
      </v-btn>
      
      <v-btn to="/cases" variant="text" class="nav-btn mx-1">
        <v-icon left size="small">mdi-stethoscope</v-icon>
        <span>Casos</span>
      </v-btn>
      
      <v-btn v-if="isLoggedIn" to="/historico" variant="text" class="nav-btn mx-1">
        <v-icon left size="small">mdi-history</v-icon>
        <span>Histórico</span>
      </v-btn>
      
      <v-btn v-if="isLoggedIn" @click="drawer = !drawer" variant="text" class="nav-btn">
        <v-icon>mdi-menu</v-icon>
      </v-btn>
    </v-app-bar>

    <!-- Sidebar Navigation -->
    <v-navigation-drawer
      v-if="isLoggedIn && showNavigation"
      v-model="drawer"
      temporary
      location="right"
      width="280"
      class="sidebar"
      style="top: 0 !important; height: 100vh !important;"
    >
      <v-list>
        <v-list-item class="user-info">
          <v-list-item-title class="text-h6">Menu</v-list-item-title>
        </v-list-item>
        
        <v-divider></v-divider>
        
        <v-list-item @click="$router.push('/metrics'); drawer = false">
          <template v-slot:prepend>
            <v-icon>mdi-chart-box</v-icon>
          </template>
          <v-list-item-title>Métricas</v-list-item-title>
        </v-list-item>
        
        <v-divider></v-divider>
        
        <v-list-item @click="logout">
          <template v-slot:prepend>
            <v-icon>mdi-logout</v-icon>
          </template>
          <v-list-item-title>Sair</v-list-item-title>
        </v-list-item>
        
        <v-divider></v-divider>
        
        <v-list-item @click="toggleTheme">
          <template v-slot:prepend>
            <v-icon>{{ isDark ? 'mdi-white-balance-sunny' : 'mdi-moon-waning-crescent' }}</v-icon>
          </template>
          <v-list-item-title>{{ isDark ? 'Modo Claro' : 'Modo Escuro' }}</v-list-item-title>
        </v-list-item>
      </v-list>
      
      <template v-slot:append>
        <div class="pa-2">
          <v-btn
            @click="deleteAccount"
            color="error"
            variant="text"
            size="small"
            block
          >
            <v-icon size="small" class="mr-1">mdi-delete</v-icon>
            Apagar Conta
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>

    <v-main :class="['main-content', { 'login-page': $route.path === '/login' }]">
      <router-view />
    </v-main>

    <!-- Mobile Bottom Navigation -->
    <v-bottom-navigation 
      v-if="showNavigation"
      v-model="activeTab" 
      color="#BB86FC" 
      class="d-md-none mobile-bottom-nav"
      height="64"
      grow
    >
      <v-btn to="/home" value="home">
        <v-icon>mdi-home</v-icon>
        <span>Início</span>
      </v-btn>
      
      <v-btn to="/predict" value="predict">
        <v-icon>mdi-brain</v-icon>
        <span>Predição</span>
      </v-btn>
      
      <v-btn to="/cases" value="cases">
        <v-icon>mdi-stethoscope</v-icon>
        <span>Casos</span>
      </v-btn>
      
      <v-btn v-if="isLoggedIn" to="/historico" value="historico">
        <v-icon>mdi-history</v-icon>
        <span>Histórico</span>
      </v-btn>
    </v-bottom-navigation>
  </v-app>
</template>

<script>
import { showConfirm, showSuccess, handleApiError } from '@/utils/alerts'

export default {
  name: 'App',
  data() {
    return {
      activeTab: 'home',
      drawer: false,
      isDark: true,
      loggedIn: !!localStorage.getItem('token')
    }
  },
  mounted() {
    const savedTheme = localStorage.getItem('theme') || 'dark'
    this.isDark = savedTheme === 'dark'
    this.$vuetify.theme.global.name = savedTheme
  },
  computed: {
    isLoggedIn() {
      return this.loggedIn
    },
    showNavigation() {
      return this.$route.path !== '/login'
    }
  },
  methods: {
    toggleTheme() {
      this.isDark = !this.isDark
      const theme = this.isDark ? 'dark' : 'light'
      this.$vuetify.theme.global.name = theme
      localStorage.setItem('theme', theme)
    },
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      this.loggedIn = false
      this.drawer = false
      this.$router.push('/')
    },
    async deleteAccount() {
      const result = await showConfirm(
        'Apagar Conta',
        'Tem certeza que deseja apagar sua conta? Esta ação não pode ser desfeita.',
        'Apagar',
        'Cancelar'
      )
      
      if (result.isConfirmed) {
        try {
          const token = localStorage.getItem('token')
          await fetch(`${process.env.VUE_APP_API_URL}/delete-account`, {
            method: 'DELETE',
            headers: { Authorization: `Bearer ${token}` }
          })
          
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          this.loggedIn = false
          this.drawer = false
          this.$router.push('/')
          showSuccess('Sucesso!', 'Conta apagada com sucesso!')
        } catch (error) {
          handleApiError(error, 'DELETE_ACCOUNT')
        }
      }
    }
  },
  watch: {
    $route(to) {
      this.loggedIn = !!localStorage.getItem('token')
      if (to.path === '/home') this.activeTab = 'home'
      else if (to.path === '/predict') this.activeTab = 'predict'
      else if (to.path === '/cases') this.activeTab = 'cases'
      else if (to.path === '/historico') this.activeTab = 'historico'
      else if (to.path === '/login') this.activeTab = 'login'
    }
  }
}
</script>

<style>
.mobile-header, .desktop-header {
  border-bottom: 1px solid #1e1e1e !important;
}

.nav-btn {
  border-radius: 4px !important;
  margin: 0 4px;
}

.nav-btn:hover {
  background-color: rgba(187, 134, 252, 0.1) !important;
}

.nav-btn.router-link-active {
  background-color: rgba(187, 134, 252, 0.2) !important;
}

.pulse-icon {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* Mobile-first main content */
.main-content {
  background: rgb(var(--v-theme-background));
  padding-top: 50px !important;
  min-height: calc(100vh - 120px);
  overflow-y: auto;
}

/* Login page - full screen */
.main-content.login-page {
  padding-top: 0 !important;
  min-height: 100vh;
}

/* Mobile bottom navigation */
.mobile-bottom-nav {
  background: rgb(var(--v-theme-surface)) !important;
  border-top: 1px solid rgba(var(--v-border-color), var(--v-border-opacity)) !important;
}

.mobile-bottom-nav .v-btn {
  flex-direction: column !important;
  height: 64px !important;
  min-width: 0 !important;
}

.mobile-bottom-nav .v-btn span {
  font-size: 10px !important;
  margin-top: 2px !important;
}

.mobile-bottom-nav .v-btn .v-icon {
  font-size: 20px !important;
}

/* Desktop adjustments */
@media (min-width: 768px) {
  .main-content {
    padding-top: 0 !important;
    min-height: calc(100vh - 56px);
  }
}

/* Sidebar styles */
.sidebar {
  background: rgb(var(--v-theme-surface)) !important;
}

.sidebar .v-list-item {
  border-radius: 0 !important;
  margin: 0 !important;
}

.sidebar .v-list-item:hover {
  background-color: rgba(187, 134, 252, 0.1) !important;
}

.user-info {
  background: rgba(187, 134, 252, 0.1) !important;
  margin-bottom: 8px !important;
}
</style>