import axios from 'axios'

const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const cardiovascularAPI = {
  async predictRisk(patientData) {
    const response = await api.post('/predict', patientData)
    return response.data
  },

  async generateCase() {
    const response = await api.get('/case')
    return response.data
  },

  async analyzeImpact(studyData) {
    const response = await api.post('/study', studyData)
    return response.data
  },

  async chatWithAI(chatData) {
    const response = await api.post('/chat', chatData)
    return response.data
  }
}

export default api