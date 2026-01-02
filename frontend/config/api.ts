// API Configuration
// Update these values to change the backend endpoint

// Production backend (AWS EC2 instance)
export const BACKEND_URL = 'http://3.239.255.65:8000'
export const WEBSOCKET_URL = 'ws://3.239.255.65:8000/api/v1/ws/sign'

// Local development (commented out)
// export const BACKEND_URL = 'http://localhost:8000'
// export const WEBSOCKET_URL = 'ws://localhost:8000/api/v1/ws/sign'

// API endpoints
export const API_ENDPOINTS = {
  // WebSocket for real-time communication
  websocket: WEBSOCKET_URL,
  
  // REST endpoints
  root: BACKEND_URL,
  docs: `${BACKEND_URL}/docs`,
  
  // Training endpoints
  trainingUpload: `${BACKEND_URL}/api/v1/training/upload`,
  trainingTrain: `${BACKEND_URL}/api/v1/training/train`,
  trainingStatus: `${BACKEND_URL}/api/v1/training/status`,
  
  // Model endpoints
  modelInfo: `${BACKEND_URL}/api/v1/model/info`,
  modelPredict: `${BACKEND_URL}/api/v1/model/predict`,
}

export default {
  BACKEND_URL,
  WEBSOCKET_URL,
  API_ENDPOINTS,
}
