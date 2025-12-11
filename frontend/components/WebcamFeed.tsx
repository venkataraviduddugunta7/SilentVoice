'use client'

import React, { forwardRef, useEffect, useRef, useImperativeHandle } from 'react'
import { Camera, CameraOff } from 'lucide-react'

interface WebcamFeedProps {
  isActive: boolean
  showLandmarks?: boolean
  className?: string
}

const WebcamFeed = forwardRef<HTMLVideoElement, WebcamFeedProps>(
  ({ isActive, showLandmarks = false, className = '' }, ref) => {
    const videoRef = useRef<HTMLVideoElement>(null)
    const streamRef = useRef<MediaStream | null>(null)
    
    useImperativeHandle(ref, () => videoRef.current!)
    
    useEffect(() => {
      const startCamera = async () => {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({
            video: {
              width: { ideal: 1280 },
              height: { ideal: 720 },
              facingMode: 'user'
            }
          })
          
          if (videoRef.current) {
            videoRef.current.srcObject = stream
            streamRef.current = stream
          }
        } catch (error) {
          console.error('Error accessing camera:', error)
        }
      }
      
      const stopCamera = () => {
        if (streamRef.current) {
          streamRef.current.getTracks().forEach(track => track.stop())
          streamRef.current = null
        }
        if (videoRef.current) {
          videoRef.current.srcObject = null
        }
      }
      
      if (isActive) {
        startCamera()
      } else {
        stopCamera()
      }
      
      return () => {
        stopCamera()
      }
    }, [isActive])
    
    return (
      <div className={`relative w-full h-full bg-gray-900 ${className}`}>
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className={`w-full h-full object-cover ${isActive ? '' : 'hidden'}`}
          style={{ transform: 'scaleX(-1)' }} // Mirror the video
        />
        
        {!isActive && (
          <div className="absolute inset-0 flex flex-col items-center justify-center text-gray-500">
            <CameraOff className="w-16 h-16 mb-4" />
            <p className="text-lg">Camera is off</p>
            <p className="text-sm mt-2">Click "Start Camera" to begin</p>
          </div>
        )}
        
        {showLandmarks && isActive && (
          <div className="absolute top-4 left-4 bg-black/50 backdrop-blur-sm px-3 py-1 rounded-full">
            <p className="text-xs text-green-400">Hand tracking active</p>
          </div>
        )}
      </div>
    )
  }
)

WebcamFeed.displayName = 'WebcamFeed'

export default WebcamFeed