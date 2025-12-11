'use client'

import React, { useEffect, useRef } from 'react'

interface GestureVisualizerProps {
  landmarks: any
  className?: string
}

export default function GestureVisualizer({ landmarks, className = '' }: GestureVisualizerProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  
  useEffect(() => {
    if (!landmarks || !canvasRef.current) return
    
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    if (!ctx) return
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    
    // Set canvas size
    canvas.width = canvas.offsetWidth
    canvas.height = canvas.offsetHeight
    
    // Draw hand landmarks
    if (landmarks.multiHandLandmarks) {
      landmarks.multiHandLandmarks.forEach((handLandmarks: any) => {
        // Draw connections
        const connections = [
          [0, 1], [1, 2], [2, 3], [3, 4], // Thumb
          [0, 5], [5, 6], [6, 7], [7, 8], // Index finger
          [0, 9], [9, 10], [10, 11], [11, 12], // Middle finger
          [0, 13], [13, 14], [14, 15], [15, 16], // Ring finger
          [0, 17], [17, 18], [18, 19], [19, 20], // Pinky
          [5, 9], [9, 13], [13, 17] // Palm
        ]
        
        ctx.strokeStyle = '#3B82F6'
        ctx.lineWidth = 2
        
        connections.forEach(([start, end]) => {
          const startPoint = handLandmarks[start]
          const endPoint = handLandmarks[end]
          
          ctx.beginPath()
          ctx.moveTo(startPoint.x * canvas.width, startPoint.y * canvas.height)
          ctx.lineTo(endPoint.x * canvas.width, endPoint.y * canvas.height)
          ctx.stroke()
        })
        
        // Draw landmarks
        handLandmarks.forEach((landmark: any, index: number) => {
          const x = landmark.x * canvas.width
          const y = landmark.y * canvas.height
          
          ctx.fillStyle = index === 0 ? '#EF4444' : '#10B981' // Red for wrist, green for others
          ctx.beginPath()
          ctx.arc(x, y, 5, 0, 2 * Math.PI)
          ctx.fill()
          
          // Draw landmark index (in debug mode)
          ctx.fillStyle = '#FFFFFF'
          ctx.font = '10px Arial'
          ctx.fillText(index.toString(), x + 7, y - 7)
        })
      })
    }
  }, [landmarks])
  
  return (
    <canvas
      ref={canvasRef}
      className={`pointer-events-none ${className}`}
      style={{ width: '100%', height: '100%' }}
    />
  )
}