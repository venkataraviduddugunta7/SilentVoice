'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { Code, Activity, Cpu, Database } from 'lucide-react'

interface DebugPanelProps {
  landmarks: any
  confidence: number
  currentSign: string
  connectionStatus: string
  mode: string
}

export default function DebugPanel({ 
  landmarks, 
  confidence, 
  currentSign, 
  connectionStatus,
  mode 
}: DebugPanelProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
      className="mt-8 glass rounded-2xl p-6"
    >
      <div className="flex items-center gap-2 mb-4">
        <Code className="w-5 h-5 text-blue-400" />
        <h3 className="text-lg font-semibold">Debug Information</h3>
      </div>
      
      <div className="grid md:grid-cols-4 gap-4">
        {/* Connection Status */}
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-sm text-gray-400">
            <Activity className="w-4 h-4" />
            <span>Connection</span>
          </div>
          <div className={`text-lg font-mono ${
            connectionStatus === 'connected' ? 'text-green-400' : 'text-red-400'
          }`}>
            {connectionStatus}
          </div>
        </div>
        
        {/* Mode */}
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-sm text-gray-400">
            <Cpu className="w-4 h-4" />
            <span>Mode</span>
          </div>
          <div className="text-lg font-mono text-purple-400">
            {mode}
          </div>
        </div>
        
        {/* Current Sign */}
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-sm text-gray-400">
            <Database className="w-4 h-4" />
            <span>Current Sign</span>
          </div>
          <div className="text-lg font-mono text-blue-400">
            {currentSign || 'none'}
          </div>
        </div>
        
        {/* Confidence */}
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-sm text-gray-400">
            <Activity className="w-4 h-4" />
            <span>Confidence</span>
          </div>
          <div className="text-lg font-mono text-yellow-400">
            {Math.round(confidence * 100)}%
          </div>
        </div>
      </div>
      
      {/* Landmarks Data */}
      {landmarks && (
        <div className="mt-4 pt-4 border-t border-white/10">
          <h4 className="text-sm font-medium text-gray-400 mb-2">Hand Landmarks</h4>
          <div className="bg-black/30 rounded-lg p-3 max-h-32 overflow-auto">
            <pre className="text-xs text-green-400 font-mono">
              {JSON.stringify(landmarks, null, 2).slice(0, 500)}...
            </pre>
          </div>
        </div>
      )}
      
      {/* Performance Metrics */}
      <div className="mt-4 pt-4 border-t border-white/10">
        <h4 className="text-sm font-medium text-gray-400 mb-2">Performance</h4>
        <div className="grid grid-cols-3 gap-4 text-sm">
          <div>
            <span className="text-gray-500">FPS:</span>
            <span className="ml-2 text-green-400">30</span>
          </div>
          <div>
            <span className="text-gray-500">Latency:</span>
            <span className="ml-2 text-yellow-400">45ms</span>
          </div>
          <div>
            <span className="text-gray-500">Memory:</span>
            <span className="ml-2 text-blue-400">124MB</span>
          </div>
        </div>
      </div>
    </motion.div>
  )
}