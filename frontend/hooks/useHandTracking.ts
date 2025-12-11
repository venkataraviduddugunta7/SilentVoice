import { useState, useEffect, useCallback, RefObject } from 'react'
import { Hands, Results } from '@mediapipe/hands'
import { Camera } from '@mediapipe/camera_utils'

interface HandTrackingHook {
  landmarks: Results | null
  isTracking: boolean
  startTracking: () => void
  stopTracking: () => void
  error: string | null
}

export function useHandTracking(
  videoRef: RefObject<HTMLVideoElement>,
  canvasRef: RefObject<HTMLCanvasElement>
): HandTrackingHook {
  const [landmarks, setLandmarks] = useState<Results | null>(null)
  const [isTracking, setIsTracking] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [hands, setHands] = useState<Hands | null>(null)
  const [camera, setCamera] = useState<Camera | null>(null)
  
  // Initialize MediaPipe Hands
  useEffect(() => {
    const initializeHands = async () => {
      try {
        // Dynamic import to avoid SSR issues
        const { Hands } = await import('@mediapipe/hands')
        
        const handsInstance = new Hands({
          locateFile: (file) => {
            return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`
          }
        })
        
        handsInstance.setOptions({
          maxNumHands: 2,
          modelComplexity: 1,
          minDetectionConfidence: 0.5,
          minTrackingConfidence: 0.5
        })
        
        handsInstance.onResults((results: Results) => {
          setLandmarks(results)
          
          // Draw on canvas if available
          if (canvasRef.current && results.multiHandLandmarks) {
            const canvas = canvasRef.current
            const ctx = canvas.getContext('2d')
            if (ctx) {
              // Clear canvas
              ctx.clearRect(0, 0, canvas.width, canvas.height)
              
              // Draw landmarks and connections
              results.multiHandLandmarks.forEach((landmarks) => {
                drawConnectors(ctx, landmarks, HAND_CONNECTIONS)
                drawLandmarks(ctx, landmarks)
              })
            }
          }
        })
        
        setHands(handsInstance)
      } catch (err) {
        console.error('Failed to initialize MediaPipe Hands:', err)
        setError('Failed to initialize hand tracking')
      }
    }
    
    initializeHands()
    
    return () => {
      if (hands) {
        hands.close()
      }
    }
  }, [canvasRef])
  
  // Start tracking
  const startTracking = useCallback(async () => {
    if (!hands || !videoRef.current) {
      setError('Hand tracking not initialized or video not available')
      return
    }
    
    try {
      // Dynamic import Camera utils
      const { Camera } = await import('@mediapipe/camera_utils')
      
      const cameraInstance = new Camera(videoRef.current, {
        onFrame: async () => {
          if (hands && videoRef.current) {
            await hands.send({ image: videoRef.current })
          }
        },
        width: 1280,
        height: 720
      })
      
      await cameraInstance.start()
      setCamera(cameraInstance)
      setIsTracking(true)
      setError(null)
    } catch (err) {
      console.error('Failed to start tracking:', err)
      setError('Failed to start camera')
    }
  }, [hands, videoRef])
  
  // Stop tracking
  const stopTracking = useCallback(() => {
    if (camera) {
      camera.stop()
      setCamera(null)
    }
    setIsTracking(false)
    setLandmarks(null)
  }, [camera])
  
  return {
    landmarks,
    isTracking,
    startTracking,
    stopTracking,
    error
  }
}

// Hand connections for drawing
const HAND_CONNECTIONS = [
  [0, 1], [1, 2], [2, 3], [3, 4], // Thumb
  [0, 5], [5, 6], [6, 7], [7, 8], // Index finger
  [0, 9], [9, 10], [10, 11], [11, 12], // Middle finger
  [0, 13], [13, 14], [14, 15], [15, 16], // Ring finger
  [0, 17], [17, 18], [18, 19], [19, 20], // Pinky
  [5, 9], [9, 13], [13, 17] // Palm
]

// Helper function to draw connectors
function drawConnectors(
  ctx: CanvasRenderingContext2D,
  landmarks: any[],
  connections: number[][]
) {
  ctx.strokeStyle = '#00FF00'
  ctx.lineWidth = 2
  
  connections.forEach(([start, end]) => {
    const startPoint = landmarks[start]
    const endPoint = landmarks[end]
    
    ctx.beginPath()
    ctx.moveTo(startPoint.x * ctx.canvas.width, startPoint.y * ctx.canvas.height)
    ctx.lineTo(endPoint.x * ctx.canvas.width, endPoint.y * ctx.canvas.height)
    ctx.stroke()
  })
}

// Helper function to draw landmarks
function drawLandmarks(ctx: CanvasRenderingContext2D, landmarks: any[]) {
  ctx.fillStyle = '#FF0000'
  
  landmarks.forEach((landmark) => {
    ctx.beginPath()
    ctx.arc(
      landmark.x * ctx.canvas.width,
      landmark.y * ctx.canvas.height,
      5,
      0,
      2 * Math.PI
    )
    ctx.fill()
  })
}