<template>
  <v-app>
    <!-- Mobile Header -->
    <v-app-bar color="surface" dark elevation="0" height="56" class="mobile-header d-md-none">
      <v-app-bar-title class="text-h6 font-weight-bold">
        <v-icon class="mr-2 pulse-icon" size="default">mdi-heart-pulse</v-icon>
        CardioLearn AI
      </v-app-bar-title>
    </v-app-bar>

    <!-- Desktop Header -->
    <v-app-bar color="surface" dark elevation="0" height="56" class="desktop-header d-none d-md-flex">
      <v-app-bar-title class="text-h6 font-weight-bold">
        <v-icon class="mr-2 pulse-icon" size="default">mdi-heart-pulse</v-icon>
        CardioLearn AI
      </v-app-bar-title>
      
      <v-spacer></v-spacer>
      
      <v-btn to="/" variant="text" class="nav-btn mx-1">
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
      
      <v-btn to="/metrics" variant="text" class="nav-btn mx-1">
        <v-icon left size="small">mdi-chart-box</v-icon>
        <span>Métricas</span>
      </v-btn>
    </v-app-bar>

    <v-main class="main-content">
      <router-view />
    </v-main>

    <!-- Mobile Bottom Navigation -->
    <v-bottom-navigation 
      v-model="activeTab" 
      color="#BB86FC" 
      class="d-md-none mobile-bottom-nav"
      height="64"
      grow
    >
      <v-btn to="/" value="home">
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
      
      <v-btn to="/metrics" value="metrics">
        <v-icon>mdi-chart-box</v-icon>
        <span>Métricas</span>
      </v-btn>
    </v-bottom-navigation>
  </v-app>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      activeTab: 'home'
    }
  },
  watch: {
    $route(to) {
      // Update active tab based on route
      if (to.path === '/') this.activeTab = 'home'
      else if (to.path === '/predict') this.activeTab = 'predict'
      else if (to.path === '/cases') this.activeTab = 'cases'
      else if (to.path === '/metrics') this.activeTab = 'metrics'
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
  background: #000000;
  padding-top: 50px !important;
  min-height: calc(100vh - 120px);
  overflow-y: auto;
}

/* Mobile bottom navigation */
.mobile-bottom-nav {
  background: #121212 !important;
  border-top: 1px solid #1e1e1e !important;
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
</style>