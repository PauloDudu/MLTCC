<template>
  <v-card class="mb-4 page-header" elevation="0">
    <v-card-text class="text-center pa-4">
      <v-icon size="24" color="primary" class="mr-2">{{ icon }}</v-icon>
      <span :class="titleClass" class="font-weight-medium">{{ title }}</span>
      <p v-if="subtitle" class="text-body-2 mb-0 mt-1" style="opacity: 0.7;">{{ subtitle }}</p>
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
  background: rgb(var(--v-theme-surface)) !important;
}
</style>