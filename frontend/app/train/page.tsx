'use client'

import React, { useState, useRef, useEffect, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import dynamic from 'next/dynamic'
import {
  Camera,
  Download,
  Upload,
  Save,
  RefreshCw,
  CheckCircle,
  AlertCircle,
  Info,
  Play,
  Pause,
  SkipForward,
  ChevronLeft,
  Database,
  Brain,
  Zap,
  Target,
  Activity
} from 'lucide-react'
import Link from 'next/link'
import { useMediaPipeHolistic } from '@/hooks/useMediaPipeHolistic'
import { API_ENDPOINTS } from '@/config/api'

// Training data structure
interface TrainingSession {
  id: string
  gesture: string
  frames: any[]
  timestamp: number
  duration: number
}

// ASL gestures to train
const TRAINING_GESTURES = [
  // Basic Greetings
  { id: 'HELLO', name: 'Hello', description: 'Wave hand side to side', category: 'Greetings' },
  { id: 'GOODBYE', name: 'Goodbye', description: 'Wave fingers up and down', category: 'Greetings' },
  { id: 'GOOD_MORNING', name: 'Good Morning', description: 'Good + Morning signs', category: 'Greetings' },
  { id: 'HOW_ARE_YOU', name: 'How are you?', description: 'Point forward with bent fingers', category: 'Greetings' },
  
  // Essential Needs
  { id: 'HELP', name: 'Help', description: 'Fist on flat palm, lift up', category: 'Emergency' },
  { id: 'PLEASE', name: 'Please', description: 'Circular motion on chest', category: 'Polite' },
  { id: 'THANK_YOU', name: 'Thank You', description: 'Touch chin and move forward', category: 'Polite' },
  { id: 'SORRY', name: 'Sorry', description: 'Circular motion on chest with fist', category: 'Polite' },
  
  // Basic Responses
  { id: 'YES', name: 'Yes', description: 'Fist nodding up and down', category: 'Response' },
  { id: 'NO', name: 'No', description: 'Index and middle finger close on thumb', category: 'Response' },
  { id: 'MAYBE', name: 'Maybe', description: 'Flat hands alternating up and down', category: 'Response' },
  { id: 'I_DONT_KNOW', name: "I don't know", description: 'Touch forehead, then shrug', category: 'Response' },
  
  // Emergency
  { id: 'EMERGENCY', name: 'Emergency', description: 'E hand shaking side to side', category: 'Emergency' },
  { id: 'DANGER', name: 'Danger', description: 'Fists alternating up across body', category: 'Emergency' },
  { id: 'SICK', name: 'Sick', description: 'Middle finger to forehead and stomach', category: 'Health' },
  { id: 'HURT', name: 'Hurt', description: 'Index fingers pointing at each other', category: 'Health' },
  
  // Basic Needs
  { id: 'HUNGRY', name: 'Hungry', description: 'C hand moves down chest', category: 'Needs' },
  { id: 'THIRSTY', name: 'Thirsty', description: 'Index finger traces down throat', category: 'Needs' },
  { id: 'WATER', name: 'Water', description: 'W hand taps chin', category: 'Needs' },
  { id: 'FOOD', name: 'Food', description: 'Fingers to mouth repeatedly', category: 'Needs' },
  { id: 'BATHROOM', name: 'Bathroom', description: 'T hand shakes', category: 'Needs' },
  { id: 'SLEEP', name: 'Sleep', description: 'Open hand closes over face', category: 'Needs' },
  
  // Emotions
  { id: 'HAPPY', name: 'Happy', description: 'Flat hand brushes up chest', category: 'Emotions' },
  { id: 'SAD', name: 'Sad', description: 'Hands trace tears down face', category: 'Emotions' },
  { id: 'LOVE', name: 'Love', description: 'Cross arms over chest', category: 'Emotions' },
]

// Group gestures by category
const GESTURE_CATEGORIES = TRAINING_GESTURES.reduce((acc, gesture) => {
  if (!acc[gesture.category]) {
    acc[gesture.category] = []
  }
  acc[gesture.category].push(gesture)
  return acc
}, {} as Record<string, typeof TRAINING_GESTURES>)

export default function TrainPage() {
  // State management
  const [selectedGesture, setSelectedGesture] = useState(TRAINING_GESTURES[0])
  const [isRecording, setIsRecording] = useState(false)
  const [recordingFrames, setRecordingFrames] = useState<any[]>([])
  const [trainingSessions, setTrainingSessions] = useState<TrainingSession[]>([])
  const [recordingDuration, setRecordingDuration] = useState(0)
  const [showInstructions, setShowInstructions] = useState(true)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [trainingStats, setTrainingStats] = useState<Record<string, number>>({})

  // Refs
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const recordingIntervalRef = useRef<NodeJS.Timeout>()
  const recordingStartTimeRef = useRef<number>(0)

  // Use MediaPipe Holistic for comprehensive tracking
  const {
    trackingData,
    isTracking,
    startTracking,
    stopTracking,
    error
  } = useMediaPipeHolistic(videoRef, canvasRef)

  // Start/stop camera
  useEffect(() => {
    startTracking()
    return () => {
      stopTracking()
    }
  }, [])

  // Record tracking data when recording
  useEffect(() => {
    if (isRecording && trackingData) {
      setRecordingFrames(prev => [...prev, {
        ...trackingData,
        timestamp: Date.now()
      }])
    }
  }, [isRecording, trackingData])

  // Update recording duration
  useEffect(() => {
    if (isRecording) {
      recordingStartTimeRef.current = Date.now()
      recordingIntervalRef.current = setInterval(() => {
        setRecordingDuration((Date.now() - recordingStartTimeRef.current) / 1000)
      }, 100)
    } else {
      if (recordingIntervalRef.current) {
        clearInterval(recordingIntervalRef.current)
      }
      setRecordingDuration(0)
    }

    return () => {
      if (recordingIntervalRef.current) {
        clearInterval(recordingIntervalRef.current)
      }
    }
  }, [isRecording])

  // Load existing training stats
  useEffect(() => {
    const savedSessions = localStorage.getItem('trainingSessions')
    if (savedSessions) {
      const sessions = JSON.parse(savedSessions)
      setTrainingSessions(sessions)
      
      // Calculate stats
      const stats: Record<string, number> = {}
      sessions.forEach((session: TrainingSession) => {
        stats[session.gesture] = (stats[session.gesture] || 0) + 1
      })
      setTrainingStats(stats)
    }
  }, [])

  // Start recording
  const startRecording = useCallback(() => {
    if (!isTracking) {
      alert('Please wait for camera to initialize')
      return
    }

    setRecordingFrames([])
    setIsRecording(true)
    setShowInstructions(false)
  }, [isTracking])

  // Stop recording
  const stopRecording = useCallback(() => {
    setIsRecording(false)

    if (recordingFrames.length > 10) {
      const session: TrainingSession = {
        id: `${selectedGesture.id}_${Date.now()}`,
        gesture: selectedGesture.id,
        frames: recordingFrames,
        timestamp: Date.now(),
        duration: recordingDuration
      }

      // Save to local storage
      const updatedSessions = [...trainingSessions, session]
      setTrainingSessions(updatedSessions)
      localStorage.setItem('trainingSessions', JSON.stringify(updatedSessions))

      // Update stats
      setTrainingStats(prev => ({
        ...prev,
        [selectedGesture.id]: (prev[selectedGesture.id] || 0) + 1
      }))

      // Show success message
      alert(`Successfully recorded ${selectedGesture.name}! Total samples: ${trainingStats[selectedGesture.id] || 0 + 1}`)
    } else {
      alert('Recording too short. Please try again with a longer gesture.')
    }

    setRecordingFrames([])
  }, [recordingFrames, selectedGesture, recordingDuration, trainingSessions, trainingStats])

  // Upload training data to backend
  const uploadTrainingData = async () => {
    if (trainingSessions.length === 0) {
      alert('No training data to upload')
      return
    }

    setUploadProgress(0)
    const totalSessions = trainingSessions.length
    let uploaded = 0

    try {
      for (const session of trainingSessions) {
        const response = await fetch(API_ENDPOINTS.trainingUpload, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            gesture: session.gesture,
            frames: session.frames,
            duration: session.duration,
            timestamp: session.timestamp
          })
        })

        if (response.ok) {
          uploaded++
          setUploadProgress((uploaded / totalSessions) * 100)
        }
      }

      if (uploaded === totalSessions) {
        alert(`Successfully uploaded ${uploaded} training sessions!`)
        
        // Clear local storage after successful upload
        localStorage.removeItem('trainingSessions')
        setTrainingSessions([])
        setTrainingStats({})
      } else {
        alert(`Uploaded ${uploaded} out of ${totalSessions} sessions`)
      }
    } catch (error) {
      console.error('Upload error:', error)
      alert('Failed to upload training data. Please check your connection.')
    }

    setUploadProgress(0)
  }

  // Export training data as JSON
  const exportTrainingData = () => {
    if (trainingSessions.length === 0) {
      alert('No training data to export')
      return
    }

    const dataStr = JSON.stringify(trainingSessions, null, 2)
    const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr)
    
    const exportFileDefaultName = `training_data_${Date.now()}.json`
    
    const linkElement = document.createElement('a')
    linkElement.setAttribute('href', dataUri)
    linkElement.setAttribute('download', exportFileDefaultName)
    linkElement.click()
  }

  // Clear all training data
  const clearTrainingData = () => {
    if (confirm('Are you sure you want to clear all training data? This cannot be undone.')) {
      localStorage.removeItem('trainingSessions')
      setTrainingSessions([])
      setTrainingStats({})
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-black">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 glass border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 hover:opacity-80 transition">
            <ChevronLeft className="w-5 h-5" />
            <span className="font-semibold">Back</span>
          </Link>

          <div className="flex items-center gap-2">
            <Brain className="w-5 h-5 text-purple-400" />
            <h1 className="text-xl font-bold gradient-text">Training Studio</h1>
          </div>

          <div className="flex items-center gap-3">
            {/* Training stats */}
            <div className="flex items-center gap-2 px-3 py-1 glass rounded-full">
              <Database className="w-4 h-4 text-blue-400" />
              <span className="text-sm">{trainingSessions.length} samples</span>
            </div>

            {/* Upload progress */}
            {uploadProgress > 0 && (
              <div className="flex items-center gap-2">
                <div className="w-32 h-2 bg-gray-700 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-gradient-to-r from-blue-500 to-purple-500 transition-all"
                    style={{ width: `${uploadProgress}%` }}
                  />
                </div>
                <span className="text-xs text-gray-400">{Math.round(uploadProgress)}%</span>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="pt-20 px-4 pb-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-3 gap-6">
            {/* Gesture Selection Panel */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="lg:col-span-1 space-y-4"
            >
              <div className="glass rounded-2xl p-6">
                <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                  <Target className="w-5 h-5 text-blue-400" />
                  Select Gesture to Train
                </h2>

                <div className="space-y-4 max-h-[600px] overflow-y-auto">
                  {Object.entries(GESTURE_CATEGORIES).map(([category, gestures]) => (
                    <div key={category}>
                      <h3 className="text-sm font-medium text-gray-400 mb-2">{category}</h3>
                      <div className="space-y-2">
                        {gestures.map((gesture) => (
                          <button
                            key={gesture.id}
                            onClick={() => setSelectedGesture(gesture)}
                            className={`w-full text-left p-3 rounded-lg transition ${
                              selectedGesture.id === gesture.id
                                ? 'bg-gradient-to-r from-blue-600/20 to-purple-600/20 border border-blue-500/50'
                                : 'glass hover:bg-white/10'
                            }`}
                          >
                            <div className="flex items-center justify-between">
                              <div>
                                <p className="font-medium">{gesture.name}</p>
                                <p className="text-xs text-gray-400">{gesture.description}</p>
                              </div>
                              {trainingStats[gesture.id] && (
                                <div className="flex items-center gap-1">
                                  <CheckCircle className="w-4 h-4 text-green-400" />
                                  <span className="text-xs text-green-400">{trainingStats[gesture.id]}</span>
                                </div>
                              )}
                            </div>
                          </button>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Data Management */}
              <div className="glass rounded-2xl p-6">
                <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                  <Database className="w-5 h-5 text-purple-400" />
                  Data Management
                </h3>

                <div className="space-y-3">
                  <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={uploadTrainingData}
                    disabled={trainingSessions.length === 0}
                    className="w-full px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-medium flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Upload className="w-4 h-4" />
                    Upload to Server
                  </motion.button>

                  <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={exportTrainingData}
                    disabled={trainingSessions.length === 0}
                    className="w-full px-4 py-2 glass border border-white/20 rounded-lg font-medium flex items-center justify-center gap-2 hover:bg-white/10 transition disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Download className="w-4 h-4" />
                    Export JSON
                  </motion.button>

                  <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={clearTrainingData}
                    disabled={trainingSessions.length === 0}
                    className="w-full px-4 py-2 glass border border-red-500/50 text-red-400 rounded-lg font-medium flex items-center justify-center gap-2 hover:bg-red-500/10 transition disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <RefreshCw className="w-4 h-4" />
                    Clear All Data
                  </motion.button>
                </div>
              </div>
            </motion.div>

            {/* Recording Panel */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="lg:col-span-2 space-y-4"
            >
              {/* Instructions */}
              <AnimatePresence>
                {showInstructions && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    className="glass rounded-2xl p-6 border border-blue-500/30"
                  >
                    <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
                      <Info className="w-5 h-5 text-blue-400" />
                      How to Record: {selectedGesture.name}
                    </h3>
                    <div className="space-y-2 text-sm text-gray-300">
                      <p>1. Position yourself in front of the camera with good lighting</p>
                      <p>2. Make sure your hands are clearly visible</p>
                      <p>3. Click "Start Recording" when ready</p>
                      <p>4. Perform the gesture: <span className="text-white font-medium">{selectedGesture.description}</span></p>
                      <p>5. Hold the gesture for 2-3 seconds for best results</p>
                      <p>6. Click "Stop Recording" when done</p>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>

              {/* Camera Feed */}
              <div className="relative aspect-video glass rounded-2xl overflow-hidden">
                <video
                  ref={videoRef}
                  autoPlay
                  playsInline
                  muted
                  className="w-full h-full object-cover"
                />
                <canvas
                  ref={canvasRef}
                  className="absolute inset-0 w-full h-full"
                />

                {/* Recording Overlay */}
                {isRecording && (
                  <div className="absolute inset-0 pointer-events-none">
                    {/* Recording indicator */}
                    <div className="absolute top-4 right-4 flex items-center gap-2 px-3 py-1 bg-red-500/20 backdrop-blur-sm rounded-full">
                      <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
                      <span className="text-sm text-red-400">Recording</span>
                      <span className="text-sm font-mono text-white">{recordingDuration.toFixed(1)}s</span>
                    </div>

                    {/* Gesture name */}
                    <div className="absolute top-4 left-4 px-3 py-1 bg-black/50 backdrop-blur-sm rounded-lg">
                      <p className="text-sm text-white">Recording: <span className="font-bold">{selectedGesture.name}</span></p>
                    </div>

                    {/* Progress bar */}
                    <div className="absolute bottom-0 left-0 right-0 h-1 bg-gray-800">
                      <div 
                        className="h-full bg-gradient-to-r from-red-500 to-orange-500 transition-all"
                        style={{ width: `${Math.min((recordingDuration / 5) * 100, 100)}%` }}
                      />
                    </div>
                  </div>
                )}

                {/* Tracking status */}
                {trackingData && (
                  <div className="absolute bottom-4 left-4 flex items-center gap-4 text-xs">
                    {trackingData.leftHandLandmarks && (
                      <div className="flex items-center gap-1 px-2 py-1 bg-green-500/20 backdrop-blur-sm rounded">
                        <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                        <span className="text-green-400">Left Hand</span>
                      </div>
                    )}
                    {trackingData.rightHandLandmarks && (
                      <div className="flex items-center gap-1 px-2 py-1 bg-green-500/20 backdrop-blur-sm rounded">
                        <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                        <span className="text-green-400">Right Hand</span>
                      </div>
                    )}
                    {trackingData.faceLandmarks && (
                      <div className="flex items-center gap-1 px-2 py-1 bg-blue-500/20 backdrop-blur-sm rounded">
                        <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
                        <span className="text-blue-400">Face</span>
                      </div>
                    )}
                  </div>
                )}

                {/* Error message */}
                {error && (
                  <div className="absolute inset-0 flex items-center justify-center bg-black/80">
                    <div className="text-center">
                      <AlertCircle className="w-12 h-12 text-red-400 mx-auto mb-2" />
                      <p className="text-red-400">{error}</p>
                    </div>
                  </div>
                )}
              </div>

              {/* Recording Controls */}
              <div className="flex justify-center gap-4">
                {!isRecording ? (
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={startRecording}
                    disabled={!isTracking}
                    className="px-8 py-3 bg-gradient-to-r from-red-600 to-orange-600 text-white rounded-xl font-semibold flex items-center gap-2 hover:shadow-2xl hover:shadow-orange-500/25 transition disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <div className="w-3 h-3 bg-white rounded-full"></div>
                    Start Recording
                  </motion.button>
                ) : (
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={stopRecording}
                    className="px-8 py-3 bg-gray-700 text-white rounded-xl font-semibold flex items-center gap-2 hover:bg-gray-600 transition"
                  >
                    <div className="w-3 h-3 bg-white rounded"></div>
                    Stop Recording
                  </motion.button>
                )}

                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setSelectedGesture(TRAINING_GESTURES[(TRAINING_GESTURES.findIndex(g => g.id === selectedGesture.id) + 1) % TRAINING_GESTURES.length])}
                  className="px-6 py-3 glass border border-white/20 rounded-xl font-semibold flex items-center gap-2 hover:bg-white/10 transition"
                >
                  <SkipForward className="w-5 h-5" />
                  Next Gesture
                </motion.button>
              </div>

              {/* Training Progress */}
              <div className="glass rounded-2xl p-6">
                <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                  <Activity className="w-5 h-5 text-green-400" />
                  Training Progress
                </h3>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center">
                    <p className="text-2xl font-bold gradient-text">{trainingSessions.length}</p>
                    <p className="text-sm text-gray-400">Total Samples</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-blue-400">{Object.keys(trainingStats).length}</p>
                    <p className="text-sm text-gray-400">Unique Gestures</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-green-400">{trainingStats[selectedGesture.id] || 0}</p>
                    <p className="text-sm text-gray-400">Current Gesture</p>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-purple-400">
                      {Math.round((Object.keys(trainingStats).length / TRAINING_GESTURES.length) * 100)}%
                    </p>
                    <p className="text-sm text-gray-400">Completion</p>
                  </div>
                </div>

                {/* Progress bars for each category */}
                <div className="mt-6 space-y-3">
                  {Object.entries(GESTURE_CATEGORIES).map(([category, gestures]) => {
                    const categoryProgress = gestures.filter(g => trainingStats[g.id]).length / gestures.length * 100
                    return (
                      <div key={category}>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-gray-400">{category}</span>
                          <span className="text-gray-400">{Math.round(categoryProgress)}%</span>
                        </div>
                        <div className="w-full h-2 bg-gray-700 rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-gradient-to-r from-blue-500 to-purple-500 transition-all"
                            style={{ width: `${categoryProgress}%` }}
                          />
                        </div>
                      </div>
                    )
                  })}
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </main>
    </div>
  )
}
