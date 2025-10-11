<template>
  <v-app>
    <v-app-bar color="surface" dark elevation="0" height="56" class="modern-navbar">
      <v-app-bar-title class="text-h6 font-weight-bold">
        <v-icon class="mr-2 pulse-icon" size="default">mdi-heart-pulse</v-icon>
        CardioLearn AI
      </v-app-bar-title>
      
      <v-spacer></v-spacer>
      
      <v-btn to="/" variant="text" class="nav-btn mx-1">
        <v-icon left size="small">mdi-home</v-icon>
        <span class="d-none d-sm-inline">Início</span>
      </v-btn>
      
      <v-btn to="/predict" variant="text" class="nav-btn mx-1">
        <v-icon left size="small">mdi-brain</v-icon>
        <span class="d-none d-sm-inline">Predição</span>
      </v-btn>
      
      <v-btn to="/cases" variant="text" class="nav-btn mx-1">
        <v-icon left size="small">mdi-stethoscope</v-icon>
        <span class="d-none d-sm-inline">Casos</span>
      </v-btn>
      
      <v-btn to="/metrics" variant="text" class="nav-btn mx-1">
        <v-icon left size="small">mdi-chart-box</v-icon>
        <span class="d-none d-md-inline">Métricas</span>
      </v-btn>
      
    </v-app-bar>

    <v-main class="main-content">
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
.modern-navbar {
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

.main-content {
  background: #000000;
  min-height: calc(100vh - 56px);
}
</style>