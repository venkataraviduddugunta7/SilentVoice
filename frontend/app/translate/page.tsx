'use client'

import React, { useState, useRef, useEffect, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import dynamic from 'next/dynamic'
import { 
  Camera, 
  Mic, 
  MicOff,
  Settings,
  Activity,
  Brain,
  Hand,
  Volume2,
  VolumeX,
  RefreshCw,
  Info,
  ChevronLeft,
  Eye,
  EyeOff,
  Sparkles,
  Zap
} from 'lucide-react'
import Link from 'next/link'
import WebcamFeed from '@/components/WebcamFeed'
import GestureVisualizer from '@/components/GestureVisualizer'
import SpeechPanel from '@/components/SpeechPanel'
import ConfidenceBar from '@/components/ConfidenceBar'
import DebugPanel from '@/components/DebugPanel'
import { useWebSocket } from '@/hooks/useWebSocket'
import { useSpeechRecognition } from '@/hooks/useSpeechRecognition'
import { useHandTracking } from '@/hooks/useHandTracking'

// Dynamically import 3D avatar to avoid SSR issues
const HumanAvatar3D = dynamic(() => import('@/components/HumanAvatar3D'), {
  ssr: false,
  loading: () => <div className="flex items-center justify-center h-full"><div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div></div>
})

export default function TranslatePage() {
  // State management
  const [mode, setMode] = useState<'sign-to-speech' | 'speech-to-sign'>('sign-to-speech')
  const [isRecording, setIsRecording] = useState(false)
  const [debugMode, setDebugMode] = useState(false)
  const [soundEnabled, setSoundEnabled] = useState(true)
  const [currentSign, setCurrentSign] = useState('')
  const [confidence, setConfidence] = useState(0)
  const [translatedText, setTranslatedText] = useState('')
  const [fingerSpelling, setFingerSpelling] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)
  
  // Refs
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  
  // Custom hooks
  const { 
    sendMessage, 
    lastMessage, 
    connectionStatus 
  } = useWebSocket('ws://localhost:8000/api/v1/ws/sign')
  
  const {
    transcript,
    isListening,
    startListening,
    stopListening,
    resetTranscript
  } = useSpeechRecognition()
  
  const {
    landmarks,
    isTracking,
    startTracking,
    stopTracking
  } = useHandTracking(videoRef, canvasRef)
  
  // Process incoming WebSocket messages
  useEffect(() => {
    if (lastMessage) {
      try {
        const data = JSON.parse(lastMessage)
        
        if (data.type === 'prediction') {
          setCurrentSign(data.sign)
          setConfidence(data.confidence)
          
          // Only update if confidence is above threshold
          if (data.confidence > 0.7) {
            setTranslatedText(prev => prev + ' ' + data.sign)
            
            // Speak if sound is enabled
            if (soundEnabled && mode === 'sign-to-speech') {
              speakText(data.sign)
            }
          }
        } else if (data.type === 'finger_spelling') {
          setFingerSpelling(data.letters)
        }
      } catch (error) {
        console.error('Error processing message:', error)
      }
    }
  }, [lastMessage, soundEnabled, mode])
  
  // Send landmarks when available
  useEffect(() => {
    if (landmarks && mode === 'sign-to-speech') {
      sendMessage(JSON.stringify({
        type: 'landmarks',
        data: landmarks,
        timestamp: Date.now()
      }))
    }
  }, [landmarks, mode, sendMessage])
  
  // Process speech for sign rendering
  useEffect(() => {
    if (transcript && mode === 'speech-to-sign') {
      // Send to backend for sign mapping
      sendMessage(JSON.stringify({
        type: 'speech',
        text: transcript,
        timestamp: Date.now()
      }))
    }
  }, [transcript, mode, sendMessage])
  
  // Text-to-speech function
  const speakText = (text: string) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.rate = 0.9
      utterance.pitch = 1
      speechSynthesis.speak(utterance)
    }
  }
  
  // Toggle recording
  const toggleRecording = useCallback(() => {
    if (mode === 'sign-to-speech') {
      if (isTracking) {
        stopTracking()
      } else {
        startTracking()
      }
    } else {
      if (isListening) {
        stopListening()
      } else {
        startListening()
      }
    }
    setIsRecording(!isRecording)
  }, [mode, isTracking, isListening, startTracking, stopTracking, startListening, stopListening])
  
  // Switch mode
  const switchMode = () => {
    setMode(mode === 'sign-to-speech' ? 'speech-to-sign' : 'sign-to-speech')
    setTranslatedText('')
    setCurrentSign('')
    setFingerSpelling('')
    resetTranscript()
    if (isRecording) {
      toggleRecording()
    }
  }
  
  // Clear all
  const clearAll = () => {
    setTranslatedText('')
    setCurrentSign('')
    setFingerSpelling('')
    setConfidence(0)
    resetTranscript()
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
            <Sparkles className="w-5 h-5 text-yellow-400" />
            <h1 className="text-xl font-bold gradient-text">SilentVoice Translator</h1>
          </div>
          
          <div className="flex items-center gap-3">
            {/* Connection status */}
            <div className={`flex items-center gap-2 px-3 py-1 rounded-full ${
              connectionStatus === 'connected' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
            }`}>
              <div className={`w-2 h-2 rounded-full ${
                connectionStatus === 'connected' ? 'bg-green-400' : 'bg-red-400'
              } animate-pulse`}></div>
              <span className="text-sm">{connectionStatus}</span>
            </div>
            
            {/* Debug toggle */}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setDebugMode(!debugMode)}
              className={`p-2 rounded-lg transition ${
                debugMode ? 'bg-blue-500/20 text-blue-400' : 'glass hover:bg-white/10'
              }`}
              title="Toggle Debug Mode"
            >
              {debugMode ? <Eye className="w-5 h-5" /> : <EyeOff className="w-5 h-5" />}
            </motion.button>
            
            {/* Sound toggle */}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setSoundEnabled(!soundEnabled)}
              className={`p-2 rounded-lg transition ${
                soundEnabled ? 'glass hover:bg-white/10' : 'bg-red-500/20 text-red-400'
              }`}
              title="Toggle Sound"
            >
              {soundEnabled ? <Volume2 className="w-5 h-5" /> : <VolumeX className="w-5 h-5" />}
            </motion.button>
          </div>
        </div>
      </header>
      
      {/* Main Content */}
      <main className="pt-20 px-4 pb-8">
        <div className="max-w-7xl mx-auto">
          {/* Mode Switcher */}
          <div className="flex justify-center mb-6">
            <motion.div 
              className="inline-flex p-1 glass rounded-xl"
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <button
                onClick={() => mode !== 'sign-to-speech' && switchMode()}
                className={`px-6 py-3 rounded-lg font-medium transition ${
                  mode === 'sign-to-speech' 
                    ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white' 
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                <div className="flex items-center gap-2">
                  <Hand className="w-5 h-5" />
                  Sign → Speech
                </div>
              </button>
              <button
                onClick={() => mode !== 'speech-to-sign' && switchMode()}
                className={`px-6 py-3 rounded-lg font-medium transition ${
                  mode === 'speech-to-sign' 
                    ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white' 
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                <div className="flex items-center gap-2">
                  <Mic className="w-5 h-5" />
                  Speech → Sign
                </div>
              </button>
            </motion.div>
          </div>
          
          {/* Main Grid */}
          <div className="grid lg:grid-cols-2 gap-6">
            {/* Input Panel */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="space-y-4"
            >
              {mode === 'sign-to-speech' ? (
                <>
                  {/* Webcam Feed */}
                  <div className="relative aspect-video glass rounded-2xl overflow-hidden">
                    <WebcamFeed
                      ref={videoRef}
                      isActive={isRecording}
                      showLandmarks={debugMode}
                    />
                    <canvas
                      ref={canvasRef}
                      className="absolute inset-0 w-full h-full"
                      style={{ display: debugMode ? 'block' : 'none' }}
                    />
                    
                    {/* Gesture Visualizer Overlay */}
                    {debugMode && landmarks && (
                      <GestureVisualizer
                        landmarks={landmarks}
                        className="absolute inset-0"
                      />
                    )}
                    
                    {/* Recording indicator */}
                    {isRecording && (
                      <div className="absolute top-4 right-4 flex items-center gap-2 px-3 py-1 bg-red-500/20 backdrop-blur-sm rounded-full">
                        <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
                        <span className="text-sm text-red-400">Recording</span>
                      </div>
                    )}
                  </div>
                  
                  {/* Confidence Bar */}
                  <ConfidenceBar confidence={confidence} threshold={0.7} />
                </>
              ) : (
                <>
                  {/* Speech Input Panel */}
                  <SpeechPanel
                    isListening={isListening}
                    transcript={transcript}
                    onToggle={toggleRecording}
                  />
                </>
              )}
              
              {/* Control Buttons */}
              <div className="flex justify-center gap-4">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={toggleRecording}
                  className={`px-6 py-3 rounded-xl font-semibold flex items-center gap-2 transition ${
                    isRecording 
                      ? 'bg-red-500/20 text-red-400 border border-red-500/50' 
                      : 'bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:shadow-2xl hover:shadow-purple-500/25'
                  }`}
                >
                  {mode === 'sign-to-speech' ? (
                    <>
                      <Camera className="w-5 h-5" />
                      {isRecording ? 'Stop Camera' : 'Start Camera'}
                    </>
                  ) : (
                    <>
                      {isListening ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
                      {isListening ? 'Stop Listening' : 'Start Listening'}
                    </>
                  )}
                </motion.button>
                
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={clearAll}
                  className="px-6 py-3 glass border border-white/20 rounded-xl font-semibold flex items-center gap-2 hover:bg-white/10 transition"
                >
                  <RefreshCw className="w-5 h-5" />
                  Clear
                </motion.button>
              </div>
            </motion.div>
            
            {/* Output Panel */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="space-y-4"
            >
              {mode === 'sign-to-speech' ? (
                <>
                  {/* Translated Text Output */}
                  <div className="glass rounded-2xl p-6 min-h-[200px]">
                    <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                      <Brain className="w-5 h-5 text-blue-400" />
                      Translated Text
                    </h3>
                    <div className="space-y-2">
                      {translatedText ? (
                        <p className="text-xl leading-relaxed">{translatedText}</p>
                      ) : (
                        <p className="text-gray-500 italic">Waiting for signs...</p>
                      )}
                      
                      {/* Current sign indicator */}
                      {currentSign && (
                        <motion.div
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          className="pt-4 border-t border-white/10"
                        >
                          <span className="text-sm text-gray-400">Current Sign:</span>
                          <span className="ml-2 text-2xl font-bold gradient-text">{currentSign}</span>
                        </motion.div>
                      )}
                      
                      {/* Finger spelling */}
                      {fingerSpelling && (
                        <motion.div
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          className="flex items-center gap-2 pt-2"
                        >
                          <Zap className="w-4 h-4 text-yellow-400" />
                          <span className="text-sm text-yellow-400">Finger Spelling: {fingerSpelling}</span>
                        </motion.div>
                      )}
                    </div>
                  </div>
                  
                  {/* Sign Dictionary Reference */}
                  <div className="glass rounded-2xl p-6">
                    <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                      <Info className="w-5 h-5 text-purple-400" />
                      Sign Reference
                    </h3>
                    <div className="grid grid-cols-3 gap-3">
                      {['Hello', 'Thank you', 'Please', 'Yes', 'No', 'Help'].map((word) => (
                        <button
                          key={word}
                          className="p-2 glass rounded-lg text-sm hover:bg-white/10 transition"
                          onClick={() => speakText(word)}
                        >
                          {word}
                        </button>
                      ))}
                    </div>
                  </div>
                </>
              ) : (
                <>
                  {/* 3D Avatar */}
                  <div className="aspect-video glass rounded-2xl overflow-hidden">
            <HumanAvatar3D 
              signSequence={currentSign || transcript}
              isAnimating={true}
              useReadyPlayerMe={true}
            />
                  </div>
                  
                  {/* Sign Description */}
                  <div className="glass rounded-2xl p-6">
                    <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                      <Activity className="w-5 h-5 text-green-400" />
                      Sign Description
                    </h3>
                    {currentSign ? (
                      <div className="space-y-2">
                        <p className="text-lg">Current Sign: <span className="font-bold gradient-text">{currentSign}</span></p>
                        <p className="text-sm text-gray-400">
                          The avatar is demonstrating the sign for "{currentSign}" using standard ASL gestures.
                        </p>
                      </div>
                    ) : (
                      <p className="text-gray-500 italic">Speak to see the sign translation...</p>
                    )}
                  </div>
                </>
              )}
            </motion.div>
          </div>
          
          {/* Debug Panel */}
          <AnimatePresence>
            {debugMode && (
              <DebugPanel
                landmarks={landmarks}
                confidence={confidence}
                currentSign={currentSign}
                connectionStatus={connectionStatus}
                mode={mode}
              />
            )}
          </AnimatePresence>
        </div>
      </main>
    </div>
  )
}