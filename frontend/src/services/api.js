import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000',
})

export const getOverview = () => api.get('/overview')
export const getAnalyze = () => api.get('/analyze')
export const getRecommend = () => api.get('/recommend')
export const getSimulate = () => api.get('/simulate')
export const getForecast = () => api.get('/forecast')

export default api
