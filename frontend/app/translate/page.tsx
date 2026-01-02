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
import { useMediaPipeHolistic } from '@/hooks/useMediaPipeHolistic'

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
  const [lastSpokenSign, setLastSpokenSign] = useState('')
  const [lastSignTime, setLastSignTime] = useState(0)
  const [signBuffer, setSignBuffer] = useState<{sign: string, count: number}>({sign: '', count: 0})
  const [confidenceThreshold, setConfidenceThreshold] = useState(0.75)
  const [showSettings, setShowSettings] = useState(false)
  const [sentenceMode, setSentenceMode] = useState(true)
  const [currentSentence, setCurrentSentence] = useState<string[]>([])
  const [sentenceTimer, setSentenceTimer] = useState<NodeJS.Timeout | null>(null)
  const [gestureMetadata, setGestureMetadata] = useState<any>(null)

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
    trackingData,
    isTracking,
    startTracking,
    stopTracking,
    error: trackingError
  } = useMediaPipeHolistic(videoRef, canvasRef)

  // Process incoming WebSocket messages with improved filtering
  useEffect(() => {
    if (lastMessage) {
      try {
        const data = JSON.parse(lastMessage)

        if (data.type === 'prediction') {
          const currentTime = Date.now()
          
          // Update confidence display
          setConfidence(data.confidence)
          
          // Filter out low confidence and "Unknown" predictions
          if (data.sign && data.sign !== 'Unknown' && data.confidence > confidenceThreshold) {
            // Buffer the sign to ensure consistency
            if (signBuffer.sign === data.sign) {
              setSignBuffer(prev => ({ ...prev, count: prev.count + 1 }))
            } else {
              setSignBuffer({ sign: data.sign, count: 1 })
            }
            
            // Only accept sign if it appears consistently (at least 3 times)
            if (signBuffer.count >= 3) {
              // Check if this is a new sign (not the same as last spoken)
              // or if enough time has passed (3 seconds) to repeat the same sign
              const isNewSign = data.sign !== lastSpokenSign
              const enoughTimePassed = currentTime - lastSignTime > 3000
              
              if (isNewSign || enoughTimePassed) {
                setCurrentSign(data.sign)
                
                // Handle sentence mode
                if (sentenceMode) {
                  // Add to current sentence
                  setCurrentSentence(prev => {
                    // Avoid immediate duplicates in sentence
                    if (prev[prev.length - 1] !== data.sign) {
                      return [...prev, data.sign]
                    }
                    return prev
                  })
                  
                  // Clear any existing timer
                  if (sentenceTimer) {
                    clearTimeout(sentenceTimer)
                  }
                  
                  // Set new timer to speak sentence after 2 seconds of no new signs
                  const timer = setTimeout(() => {
                    setCurrentSentence(prevSentence => {
                      if (prevSentence.length > 0) {
                        const sentence = buildSentence(prevSentence)
                        setTranslatedText(prev => prev + ' ' + sentence + '.')
                        
                        if (soundEnabled && mode === 'sign-to-speech') {
                          speakText(sentence)
                        }
                        
                        // Return empty array to clear sentence
                        return []
                      }
                      return prevSentence
                    })
                  }, 2000)
                  
                  setSentenceTimer(timer)
                } else {
                  // Original word-by-word mode
                  setTranslatedText(prev => {
                    const words = prev.trim().split(' ')
                    if (words[words.length - 1] !== data.sign) {
                      return prev + ' ' + data.sign
                    }
                    return prev
                  })
                  
                  if (soundEnabled && mode === 'sign-to-speech') {
                    speakText(data.sign)
                  }
                }
                
                setLastSpokenSign(data.sign)
                setLastSignTime(currentTime)
                
                // Reset buffer after successful recognition
                setSignBuffer({ sign: '', count: 0 })
              }
            }
          } else if (data.confidence < 0.5) {
            // Reset buffer if confidence drops too low
            setSignBuffer({ sign: '', count: 0 })
          }
        } else if (data.type === 'gesture_metadata') {
          // Handle gesture metadata for better visualization
          setGestureMetadata({
            hand: data.hand,
            isMotion: data.is_motion,
            duration: data.duration,
            frames: data.frames
          })
        } else if (data.type === 'signs') {
          // Handle speech to sign response
          if (data.signs && data.signs.length > 0) {
            setCurrentSign(data.signs.join(' → '))
          }
        } else if (data.type === 'finger_spelling') {
          setFingerSpelling(data.letters)
        }
      } catch (error) {
        console.error('Error processing message:', error)
      }
    }
  }, [lastMessage, soundEnabled, mode, signBuffer, lastSpokenSign, lastSignTime])

  // Send tracking data when available
  useEffect(() => {
    if (trackingData && mode === 'sign-to-speech' && isRecording) {
      // Send holistic tracking data
      sendMessage(JSON.stringify({
        type: 'holistic',
        data: trackingData,
        timestamp: trackingData.timestamp
      }))
    }
  }, [trackingData, mode, isRecording, sendMessage])

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
  
  // Build grammatically correct sentence from signs
  const buildSentence = (signs: string[]) => {
    // Convert sign names to proper words and build sentence
    const words = signs.map(sign => {
      // Convert sign format to readable text
      const word = sign.toLowerCase().replace(/_/g, ' ')
      
      // Handle special cases
      switch(sign.toUpperCase()) {
        case 'I_LOVE_YOU': return 'I love you'
        case 'THANK_YOU': return 'thank you'
        case 'HOW_ARE_YOU': return 'how are you'
        case 'I_NEED_HELP': return 'I need help'
        case 'GOOD_MORNING': return 'good morning'
        case 'GOOD': return 'good'
        case 'BAD': return 'bad'
        case 'YES': return 'yes'
        case 'NO': return 'no'
        case 'HELLO': return 'hello'
        case 'HELP': return 'help'
        case 'PLEASE': return 'please'
        case 'SORRY': return 'sorry'
        case 'HUNGRY': return 'hungry'
        case 'THIRSTY': return 'thirsty'
        case 'WATER': return 'water'
        case 'FOOD': return 'food'
        case 'BATHROOM': return 'bathroom'
        case 'ONE': return 'one'
        case 'TWO': return 'two'
        case 'THREE': return 'three'
        case 'FOUR': return 'four'
        case 'FIVE': return 'five'
        default: return word
      }
    })
    
    // Build sentence with basic grammar rules
    let sentence = words.join(' ')
    
    // Add "I am" for states
    if (words.includes('hungry') || words.includes('thirsty') || words.includes('tired') || words.includes('happy') || words.includes('sad')) {
      if (!words.includes('i') && !words.includes('you')) {
        sentence = 'I am ' + sentence
      }
    }
    
    // Add "I need" for needs
    if (words.includes('help') || words.includes('water') || words.includes('food') || words.includes('bathroom')) {
      if (!words.includes('i') && !words.includes('need')) {
        sentence = 'I need ' + sentence
      }
    }
    
    // Capitalize first letter
    sentence = sentence.charAt(0).toUpperCase() + sentence.slice(1)
    
    return sentence
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
    setLastSpokenSign('')
    setLastSignTime(0)
    setSignBuffer({ sign: '', count: 0 })
    setCurrentSentence([])
    if (sentenceTimer) {
      clearTimeout(sentenceTimer)
      setSentenceTimer(null)
    }
    resetTranscript()
    // Stop any ongoing speech
    if ('speechSynthesis' in window) {
      speechSynthesis.cancel()
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-black">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 glass border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-1 md:gap-2 hover:opacity-80 transition">
            <ChevronLeft className="w-5 h-5" />
            <span className="font-semibold hidden sm:inline">Back</span>
          </Link>

          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-yellow-400" />
            <h1 className="text-xl font-bold gradient-text">SilentVoice Translator</h1>
          </div>

          <div className="flex items-center gap-3">
            {/* Connection status */}
            <div className={`flex items-center gap-2 px-2 md:px-3 py-1 rounded-full ${connectionStatus === 'connected' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
              }`}>
              <div className={`w-2 h-2 rounded-full ${connectionStatus === 'connected' ? 'bg-green-400' : 'bg-red-400'
                } animate-pulse`}></div>
              <span className="text-xs md:text-sm">{connectionStatus}</span>
            </div>

            {/* Debug toggle */}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setDebugMode(!debugMode)}
              className={`p-2 rounded-lg transition ${debugMode ? 'bg-blue-500/20 text-blue-400' : 'glass hover:bg-white/10'
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
              className={`p-2 rounded-lg transition ${soundEnabled ? 'glass hover:bg-white/10' : 'bg-red-500/20 text-red-400'
                }`}
              title="Toggle Sound"
            >
              {soundEnabled ? <Volume2 className="w-5 h-5" /> : <VolumeX className="w-5 h-5" />}
            </motion.button>
            
            {/* Settings toggle */}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setShowSettings(!showSettings)}
              className={`p-2 rounded-lg transition ${showSettings ? 'bg-blue-500/20 text-blue-400' : 'glass hover:bg-white/10'
                }`}
              title="Settings"
            >
              <Settings className="w-5 h-5" />
            </motion.button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="pt-20 px-4 pb-8">
        <div className="max-w-7xl mx-auto">
          {/* Settings Panel */}
          <AnimatePresence>
            {showSettings && (
              <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="mb-6 glass rounded-2xl p-6"
              >
                <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                  <Settings className="w-5 h-5 text-blue-400" />
                  Recognition Settings
                </h3>
                
                <div className="grid md:grid-cols-2 gap-6">
                  {/* Confidence Threshold */}
                  <div>
                    <label className="block text-sm font-medium text-gray-400 mb-2">
                      Confidence Threshold: {Math.round(confidenceThreshold * 100)}%
                    </label>
                    <input
                      type="range"
                      min="50"
                      max="95"
                      value={confidenceThreshold * 100}
                      onChange={(e) => setConfidenceThreshold(parseInt(e.target.value) / 100)}
                      className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
                    />
                    <div className="flex justify-between text-xs text-gray-500 mt-1">
                      <span>Less Strict</span>
                      <span>More Strict</span>
                    </div>
                    <p className="text-xs text-gray-400 mt-2">
                      Higher values reduce false positives but may miss some signs
                    </p>
                  </div>
                  
                  {/* Sentence Mode */}
                  <div>
                    <label className="block text-sm font-medium text-gray-400 mb-2">
                      Sentence Mode
                    </label>
                    <div className="flex items-center gap-3">
                      <button
                        onClick={() => setSentenceMode(!sentenceMode)}
                        className={`relative inline-flex h-6 w-11 items-center rounded-full transition ${
                          sentenceMode ? 'bg-blue-600' : 'bg-gray-600'
                        }`}
                      >
                        <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                          sentenceMode ? 'translate-x-6' : 'translate-x-1'
                        }`} />
                      </button>
                      <span className="text-sm text-gray-300">
                        {sentenceMode ? 'Build sentences' : 'Word by word'}
                      </span>
                    </div>
                    <p className="text-xs text-gray-400 mt-2">
                      {sentenceMode 
                        ? 'Groups signs into sentences before speaking'
                        : 'Speaks each sign immediately'}
                    </p>
                  </div>
                </div>
                
                <div className="mt-4 pt-4 border-t border-white/10">
                  <p className="text-sm text-gray-400">
                    Tips for better recognition:
                  </p>
                  <ul className="text-xs text-gray-500 mt-2 space-y-1">
                    <li>• Ensure good lighting with no backlight</li>
                    <li>• Keep hands clearly visible in frame</li>
                    <li>• Hold signs steady for 1-2 seconds</li>
                    <li>• Make deliberate, clear movements</li>
                  </ul>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
          {/* Mode Switcher */}
          <div className="flex justify-center mb-6">
            <motion.div
              className="inline-flex p-1 glass rounded-xl"
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <button
                onClick={() => mode !== 'sign-to-speech' && switchMode()}
                className={`px-4 md:px-6 py-3 rounded-lg font-medium transition text-sm md:text-base ${mode === 'sign-to-speech'
                    ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white'
                    : 'text-gray-400 hover:text-white'
                  }`}
              >
                <div className="flex items-center gap-2">
                  <Hand className="w-5 h-5" />
                  Sign
                </div>
              </button>
              <button
                onClick={() => mode !== 'speech-to-sign' && switchMode()}
                className={`px-4 md:px-6 py-3 rounded-lg font-medium transition text-sm md:text-base ${mode === 'speech-to-sign'
                    ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white'
                    : 'text-gray-400 hover:text-white'
                  }`}
              >
                <div className="flex items-center gap-2">
                  <Mic className="w-5 h-5" />
                  Speech
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
                    {debugMode && trackingData && (
                      <GestureVisualizer
                        landmarks={trackingData.rightHandLandmarks || trackingData.leftHandLandmarks}
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
                  <ConfidenceBar confidence={confidence} threshold={0.75} />

                  {/* Recognition Status */}
                  <div className="glass rounded-xl p-4">
                    <div className="space-y-3">
                      {/* Tracking Status */}
                      {trackingData && (
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-gray-400">Tracking:</span>
                          <div className="flex gap-2">
                            {trackingData.leftHandLandmarks && (
                              <span className="px-2 py-1 bg-green-500/20 text-green-400 rounded text-xs">Left Hand</span>
                            )}
                            {trackingData.rightHandLandmarks && (
                              <span className="px-2 py-1 bg-green-500/20 text-green-400 rounded text-xs">Right Hand</span>
                            )}
                            {trackingData.faceLandmarks && (
                              <span className="px-2 py-1 bg-blue-500/20 text-blue-400 rounded text-xs">Face</span>
                            )}
                          </div>
                        </div>
                      )}
                      
                      {/* Recognition Buffer Status */}
                      {signBuffer.sign && signBuffer.count > 0 && (
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-gray-400">Detecting:</span>
                          <div className="flex items-center gap-2">
                            <span className="text-sm text-yellow-400">{signBuffer.sign}</span>
                            <div className="flex gap-1">
                              {[1, 2, 3].map((i) => (
                                <div
                                  key={i}
                                  className={`w-2 h-2 rounded-full ${
                                    i <= signBuffer.count 
                                      ? 'bg-yellow-400' 
                                      : 'bg-gray-600'
                                  }`}
                                />
                              ))}
                            </div>
                          </div>
                        </div>
                      )}
                      
                      {/* Last Recognized Sign */}
                      {lastSpokenSign && (
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-gray-400">Last Sign:</span>
                          <span className="text-sm text-green-400">{lastSpokenSign}</span>
                        </div>
                      )}
                      
                      {/* Gesture Metadata */}
                      {gestureMetadata && (
                        <div className="mt-2 pt-2 border-t border-white/10">
                          <div className="grid grid-cols-2 gap-2 text-sm">
                            <div className="flex items-center justify-between">
                              <span className="text-gray-400">Hand:</span>
                              <span className="text-blue-400">{gestureMetadata.hand}</span>
                            </div>
                            <div className="flex items-center justify-between">
                              <span className="text-gray-400">Type:</span>
                              <span className={`${gestureMetadata.isMotion ? 'text-yellow-400' : 'text-green-400'}`}>
                                {gestureMetadata.isMotion ? 'Dynamic' : 'Static'}
                              </span>
                            </div>
                            {gestureMetadata.duration && (
                              <div className="flex items-center justify-between">
                                <span className="text-gray-400">Duration:</span>
                                <span className="text-gray-300">{gestureMetadata.duration.toFixed(1)}s</span>
                              </div>
                            )}
                            {gestureMetadata.frames && (
                              <div className="flex items-center justify-between">
                                <span className="text-gray-400">Frames:</span>
                                <span className="text-gray-300">{gestureMetadata.frames}</span>
                              </div>
                            )}
                          </div>
                        </div>
                      )}
                      
                      {/* Current Sentence Being Built */}
                      {sentenceMode && currentSentence.length > 0 && (
                        <div className="mt-2 pt-2 border-t border-white/10">
                          <span className="text-sm text-gray-400">Building sentence:</span>
                          <div className="mt-1 flex flex-wrap gap-2">
                            {currentSentence.map((word, index) => (
                              <span 
                                key={index}
                                className="px-2 py-1 bg-blue-500/20 text-blue-400 rounded text-sm"
                              >
                                {word.toLowerCase()}
                              </span>
                            ))}
                            <span className="animate-pulse text-gray-500">...</span>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
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
                  className={`px-6 py-3 rounded-xl font-semibold flex items-center gap-2 transition ${isRecording
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
                    
                    {/* Speak Sentence Button (only in sentence mode) */}
                    {sentenceMode && currentSentence.length > 0 && (
                      <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => {
                          const sentence = buildSentence(currentSentence)
                          setTranslatedText(prev => prev + ' ' + sentence + '.')
                          if (soundEnabled) {
                            speakText(sentence)
                          }
                          setCurrentSentence([])
                          if (sentenceTimer) {
                            clearTimeout(sentenceTimer)
                            setSentenceTimer(null)
                          }
                        }}
                        className="px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-xl font-semibold flex items-center gap-2 hover:shadow-2xl hover:shadow-green-500/25 transition"
                      >
                        <Volume2 className="w-5 h-5" />
                        Speak Sentence
                      </motion.button>
                    )}
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
                  <div className="md:aspect-video aspect-[3/4] glass rounded-2xl overflow-hidden min-h-[400px]">
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
                landmarks={trackingData ? [
                  ...(trackingData.leftHandLandmarks || []),
                  ...(trackingData.rightHandLandmarks || [])
                ] : null}
                confidence={confidence}
                currentSign={currentSign}
                connectionStatus={connectionStatus}
                mode={mode}
                trackingData={trackingData}
              />
            )}
          </AnimatePresence>
        </div>
      </main>
    </div>
  )
}