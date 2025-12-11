'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { TrendingUp, AlertCircle, CheckCircle } from 'lucide-react'

interface ConfidenceBarProps {
  confidence: number
  threshold: number
}

export default function ConfidenceBar({ confidence, threshold }: ConfidenceBarProps) {
  const percentage = Math.round(confidence * 100)
  const isAboveThreshold = confidence >= threshold
  
  const getColorClass = () => {
    if (confidence >= 0.8) return 'from-green-500 to-emerald-500'
    if (confidence >= 0.6) return 'from-yellow-500 to-orange-500'
    return 'from-red-500 to-pink-500'
  }
  
  const getIcon = () => {
    if (confidence >= threshold) return <CheckCircle className="w-4 h-4" />
    if (confidence >= threshold - 0.2) return <TrendingUp className="w-4 h-4" />
    return <AlertCircle className="w-4 h-4" />
  }
  
  return (
    <div className="glass rounded-xl p-4">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          {getIcon()}
          <span className="text-sm font-medium">Confidence Score</span>
        </div>
        <span className={`text-sm font-bold ${
          isAboveThreshold ? 'text-green-400' : 'text-yellow-400'
        }`}>
          {percentage}%
        </span>
      </div>
      
      <div className="relative h-3 bg-gray-800 rounded-full overflow-hidden">
        {/* Threshold marker */}
        <div 
          className="absolute top-0 bottom-0 w-0.5 bg-white/50 z-10"
          style={{ left: `${threshold * 100}%` }}
        />
        
        {/* Confidence bar */}
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 0.3, ease: 'easeOut' }}
          className={`h-full bg-gradient-to-r ${getColorClass()} relative`}
        >
          {/* Glow effect */}
          <div className="absolute inset-0 bg-white/20 animate-pulse" />
        </motion.div>
      </div>
      
      <div className="flex items-center justify-between mt-2">
        <span className="text-xs text-gray-500">
          Threshold: {Math.round(threshold * 100)}%
        </span>
        <span className={`text-xs ${
          isAboveThreshold ? 'text-green-400' : 'text-yellow-400'
        }`}>
          {isAboveThreshold ? 'High Confidence' : 'Low Confidence'}
        </span>
      </div>
    </div>
  )
}