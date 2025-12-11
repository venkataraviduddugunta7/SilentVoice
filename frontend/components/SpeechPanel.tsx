'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { Mic, MicOff, Volume2 } from 'lucide-react'

interface SpeechPanelProps {
  isListening: boolean
  transcript: string
  onToggle: () => void
}

export default function SpeechPanel({ isListening, transcript, onToggle }: SpeechPanelProps) {
  return (
    <div className="glass rounded-2xl p-8">
      <div className="flex flex-col items-center justify-center space-y-6">
        {/* Microphone Animation */}
        <div className="relative">
          <motion.div
            animate={isListening ? {
              scale: [1, 1.2, 1],
              opacity: [0.3, 0.6, 0.3]
            } : {}}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: "easeInOut"
            }}
            className="absolute inset-0 bg-blue-500 rounded-full blur-xl"
          />
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={onToggle}
            className={`relative z-10 p-8 rounded-full transition ${
              isListening 
                ? 'bg-gradient-to-r from-blue-600 to-purple-600' 
                : 'bg-gray-800 hover:bg-gray-700'
            }`}
          >
            {isListening ? (
              <Mic className="w-12 h-12 text-white" />
            ) : (
              <MicOff className="w-12 h-12 text-gray-400" />
            )}
          </motion.button>
        </div>
        
        {/* Status Text */}
        <div className="text-center">
          {isListening ? (
            <div className="flex items-center gap-2">
              <div className="flex gap-1">
                <span className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                <span className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                <span className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
              </div>
              <span className="text-blue-400">Listening...</span>
            </div>
          ) : (
            <span className="text-gray-500">Click to start speaking</span>
          )}
        </div>
        
        {/* Transcript Display */}
        <div className="w-full min-h-[100px] p-4 bg-black/30 rounded-xl">
          <div className="flex items-start gap-2">
            <Volume2 className="w-5 h-5 text-gray-400 mt-1" />
            <div className="flex-1">
              {transcript ? (
                <p className="text-lg leading-relaxed">{transcript}</p>
              ) : (
                <p className="text-gray-500 italic">Your speech will appear here...</p>
              )}
            </div>
          </div>
        </div>
        
        {/* Speech Tips */}
        <div className="text-xs text-gray-500 text-center max-w-md">
          <p>Speak clearly and at a moderate pace for best results.</p>
          <p className="mt-1">Common phrases: "Hello", "Thank you", "Help", "Please"</p>
        </div>
      </div>
    </div>
  )
}