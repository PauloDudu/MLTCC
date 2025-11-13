import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import './styles/global.css'
import './styles/alerts.css'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'dark',
    themes: {
      dark: {
        dark: true,
        colors: {
          background: '#000000',
          surface: '#121212',
          primary: '#BB86FC',
          secondary: '#03DAC6',
          error: '#CF6679',
          info: '#2196F3',
          success: '#4CAF50',
          warning: '#FB8C00'
        }
      },
      light: {
        dark: false,
        colors: {
          background: '#FFFFFF',
          surface: '#F5F5F5',
          primary: '#6200EA',
          secondary: '#018786',
          error: '#B00020',
          info: '#1976D2',
          success: '#388E3C',
          warning: '#F57C00'
        }
      }
    }
  }
})

createApp(App).use(router).use(vuetify).mount('#app')