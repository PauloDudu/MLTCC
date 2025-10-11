<template>
  <v-card 
    height="280" 
    hover 
    class="feature-card fade-in" 
    elevation="2"
    @click="$router.push(to)"
  >
    <v-card-text class="text-center pa-6 d-flex flex-column justify-space-between h-100">
      <div>
        <div class="icon-wrapper mb-4">
          <v-icon :size="48" :color="color" class="feature-icon">{{ icon }}</v-icon>
        </div>
        <h3 class="text-h6 mb-3 font-weight-medium">{{ title }}</h3>
        <p class="text-body-2 mb-4 text-medium-emphasis">{{ description }}</p>
      </div>
      <v-btn 
        :color="color" 
        variant="elevated" 
        size="default"
        block
        class="feature-btn"
      >
        {{ buttonText }}
      </v-btn>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'FeatureCard',
  props: {
    title: String,
    description: String,
    icon: String,
    color: String,
    to: String,
    buttonText: String
  }
}
</script>

<style scoped>
.feature-card {
  cursor: pointer;
  border-radius: 16px !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.feature-card:hover {
  transform: translateY(-4px);
}

.v-theme--light .icon-wrapper {
  background: rgba(198, 40, 40, 0.1);
}

.v-theme--dark .icon-wrapper {
  background: rgba(239, 83, 80, 0.15);
}

.icon-wrapper {
  border-radius: 50%;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  transition: all 0.3s ease;
}

.v-theme--light .feature-card:hover .icon-wrapper {
  background: rgba(198, 40, 40, 0.15);
}

.v-theme--dark .feature-card:hover .icon-wrapper {
  background: rgba(239, 83, 80, 0.25);
}

.feature-card:hover .icon-wrapper {
  transform: scale(1.1);
}

.feature-icon {
  transition: transform 0.3s ease;
}

.feature-card:hover .feature-icon {
  transform: scale(1.1);
}

.feature-btn {
  border-radius: 12px !important;
  font-weight: 500;
}

@media (max-width: 960px) {
  .feature-card {
    height: 240px !important;
  }
  
  .v-card-text {
    padding: 16px !important;
  }
  
  .icon-wrapper {
    width: 64px;
    height: 64px;
  }
  
  .feature-icon {
    font-size: 32px !important;
  }
}
</style>