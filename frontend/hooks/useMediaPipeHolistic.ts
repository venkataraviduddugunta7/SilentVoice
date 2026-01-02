import { useState, useEffect, useCallback, RefObject } from 'react'
import { Holistic, Results as HolisticResults } from '@mediapipe/holistic'
import { Camera } from '@mediapipe/camera_utils'
import { drawConnectors, drawLandmarks } from '@mediapipe/drawing_utils'
import { HAND_CONNECTIONS, POSE_CONNECTIONS, FACEMESH_TESSELATION } from '@mediapipe/holistic'

export interface HolisticTrackingData {
  leftHandLandmarks: any[] | null
  rightHandLandmarks: any[] | null
  poseLandmarks: any[] | null
  faceLandmarks: any[] | null
  timestamp: number
}

interface HolisticTrackingHook {
  trackingData: HolisticTrackingData | null
  isTracking: boolean
  startTracking: () => void
  stopTracking: () => void
  error: string | null
}

export function useMediaPipeHolistic(
  videoRef: RefObject<HTMLVideoElement>,
  canvasRef: RefObject<HTMLCanvasElement>
): HolisticTrackingHook {
  const [trackingData, setTrackingData] = useState<HolisticTrackingData | null>(null)
  const [isTracking, setIsTracking] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [holistic, setHolistic] = useState<Holistic | null>(null)
  const [camera, setCamera] = useState<Camera | null>(null)

  // Initialize MediaPipe Holistic
  useEffect(() => {
    const initializeHolistic = async () => {
      try {
        // Dynamic import to avoid SSR issues
        const { Holistic } = await import('@mediapipe/holistic')

        const holisticInstance = new Holistic({
          locateFile: (file) => {
            return `https://cdn.jsdelivr.net/npm/@mediapipe/holistic/${file}`
          }
        })

        holisticInstance.setOptions({
          modelComplexity: 1,
          smoothLandmarks: true,
          enableSegmentation: false,
          smoothSegmentation: false,
          refineFaceLandmarks: true,
          minDetectionConfidence: 0.5,
          minTrackingConfidence: 0.5
        })

        holisticInstance.onResults((results: HolisticResults) => {
          // Process and store tracking data
          const data: HolisticTrackingData = {
            leftHandLandmarks: results.leftHandLandmarks ? 
              results.leftHandLandmarks.map(l => ({
                x: l.x,
                y: l.y,
                z: l.z,
                visibility: l.visibility || 1
              })) : null,
            rightHandLandmarks: results.rightHandLandmarks ?
              results.rightHandLandmarks.map(l => ({
                x: l.x,
                y: l.y,
                z: l.z,
                visibility: l.visibility || 1
              })) : null,
            poseLandmarks: results.poseLandmarks ?
              results.poseLandmarks.map(l => ({
                x: l.x,
                y: l.y,
                z: l.z,
                visibility: l.visibility || 0
              })) : null,
            faceLandmarks: results.faceLandmarks ?
              results.faceLandmarks.slice(0, 100).map(l => ({ // Limit face landmarks for performance
                x: l.x,
                y: l.y,
                z: l.z
              })) : null,
            timestamp: Date.now()
          }

          setTrackingData(data)

          // Draw on canvas if available
          if (canvasRef.current && results.image) {
            const canvas = canvasRef.current
            const ctx = canvas.getContext('2d')
            if (ctx) {
              // Set canvas size to match video
              canvas.width = results.image.width
              canvas.height = results.image.height

              // Clear canvas
              ctx.save()
              ctx.clearRect(0, 0, canvas.width, canvas.height)

              // Draw the image
              ctx.drawImage(results.image, 0, 0, canvas.width, canvas.height)

              // Draw pose landmarks
              if (results.poseLandmarks) {
                drawConnectors(ctx, results.poseLandmarks, POSE_CONNECTIONS, {
                  color: '#00FF00',
                  lineWidth: 4
                })
                drawLandmarks(ctx, results.poseLandmarks, {
                  color: '#FF0000',
                  lineWidth: 2,
                  radius: 6
                })
              }

              // Draw face mesh (simplified)
              if (results.faceLandmarks) {
                drawConnectors(ctx, results.faceLandmarks, FACEMESH_TESSELATION, {
                  color: '#C0C0C070',
                  lineWidth: 1
                })
              }

              // Draw left hand
              if (results.leftHandLandmarks) {
                drawConnectors(ctx, results.leftHandLandmarks, HAND_CONNECTIONS, {
                  color: '#CC0000',
                  lineWidth: 5
                })
                drawLandmarks(ctx, results.leftHandLandmarks, {
                  color: '#00FF00',
                  lineWidth: 2,
                  radius: 5
                })
              }

              // Draw right hand
              if (results.rightHandLandmarks) {
                drawConnectors(ctx, results.rightHandLandmarks, HAND_CONNECTIONS, {
                  color: '#00CC00',
                  lineWidth: 5
                })
                drawLandmarks(ctx, results.rightHandLandmarks, {
                  color: '#FF0000',
                  lineWidth: 2,
                  radius: 5
                })
              }

              ctx.restore()
            }
          }
        })

        setHolistic(holisticInstance)
      } catch (err) {
        console.error('Failed to initialize MediaPipe Holistic:', err)
        setError('Failed to initialize holistic tracking')
      }
    }

    initializeHolistic()

    return () => {
      if (holistic) {
        holistic.close()
      }
    }
  }, [canvasRef])

  // Start tracking
  const startTracking = useCallback(async () => {
    if (!holistic || !videoRef.current) {
      setError('Holistic tracking not initialized or video not available')
      return
    }

    try {
      // Request camera permission
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: 1280,
          height: 720,
          facingMode: 'user'
        }
      })

      if (videoRef.current) {
        videoRef.current.srcObject = stream
      }

      // Dynamic import Camera utils
      const { Camera } = await import('@mediapipe/camera_utils')

      const cameraInstance = new Camera(videoRef.current, {
        onFrame: async () => {
          if (holistic && videoRef.current) {
            await holistic.send({ image: videoRef.current })
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
      setError('Failed to start camera. Please check permissions.')
    }
  }, [holistic, videoRef])

  // Stop tracking
  const stopTracking = useCallback(() => {
    if (camera) {
      camera.stop()
      setCamera(null)
    }
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream
      stream.getTracks().forEach(track => track.stop())
      videoRef.current.srcObject = null
    }
    setIsTracking(false)
    setTrackingData(null)
  }, [camera, videoRef])

  return {
    trackingData,
    isTracking,
    startTracking,
    stopTracking,
    error
  }
}
