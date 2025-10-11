<template>
  <v-card class="mb-4 page-header gradient-bg" elevation="0">
    <v-card-text class="text-center pa-4 white--text">
      <v-icon size="24" color="white" class="mr-2">{{ icon }}</v-icon>
      <span :class="titleClass" class="font-weight-medium">{{ title }}</span>
      <p v-if="subtitle" class="text-body-2 opacity-90 mb-0 mt-1">{{ subtitle }}</p>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'PageHeader',
  props: {
    title: String,
    subtitle: String,
    icon: String,
    large: Boolean
  },
  computed: {
    iconSize() {
      return this.large ? 48 : 32
    },
    titleClass() {
      return this.large ? 'text-h5' : 'text-h6'
    }
  }
}
</script>

<style scoped>
.page-header {
  border-radius: 4px !important;
  background: #1e1e1e !important;
}
</style>