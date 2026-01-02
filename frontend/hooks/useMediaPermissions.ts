import { useState, useEffect, useCallback } from 'react'

type PermissionState = 'granted' | 'denied' | 'prompt' | 'checking' | 'not-supported'

interface MediaPermissions {
  camera: PermissionState
  microphone: PermissionState
}

export function useMediaPermissions() {
  const [permissions, setPermissions] = useState<MediaPermissions>({
    camera: 'checking',
    microphone: 'checking'
  })
  const [error, setError] = useState<string | null>(null)

  // Check if permissions API is supported
  const isPermissionsAPISupported = typeof navigator !== 'undefined' && 'permissions' in navigator

  // Check permission status using Permissions API
  const checkPermissionStatus = useCallback(async (name: 'camera' | 'microphone'): Promise<PermissionState> => {
    try {
      // For iOS Safari and some browsers, permissions API might not be available
      if (!isPermissionsAPISupported) {
        // Try to check if media devices are available
        if (typeof navigator !== 'undefined' && navigator.mediaDevices) {
          try {
            const devices = await navigator.mediaDevices.enumerateDevices()
            const hasDevice = devices.some(device => 
              name === 'camera' ? device.kind === 'videoinput' : device.kind === 'audioinput'
            )
            
            // If we can enumerate devices, likely permission was granted before
            if (devices.length > 0 && devices[0].label) {
              return 'granted'
            }
            
            return hasDevice ? 'prompt' : 'not-supported'
          } catch {
            return 'prompt'
          }
        }
        return 'prompt'
      }

      // Use Permissions API for browsers that support it
      const permissionName = name === 'camera' ? 'camera' as PermissionName : 'microphone' as PermissionName
      const result = await navigator.permissions.query({ name: permissionName })
      return result.state as PermissionState
    } catch (err) {
      console.warn(`Could not check ${name} permission:`, err)
      return 'prompt'
    }
  }, [isPermissionsAPISupported])

  // Request camera permission
  const requestCameraPermission = useCallback(async (): Promise<boolean> => {
    try {
      setError(null)
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: {
          width: { ideal: 1280 },
          height: { ideal: 720 },
          facingMode: 'user'
        }
      })
      
      // Stop the stream immediately after getting permission
      stream.getTracks().forEach(track => track.stop())
      
      setPermissions(prev => ({ ...prev, camera: 'granted' }))
      return true
    } catch (err: any) {
      console.error('Camera permission error:', err)
      
      if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
        setPermissions(prev => ({ ...prev, camera: 'denied' }))
        setError('Camera access was denied. Please enable it in your browser settings.')
      } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
        setPermissions(prev => ({ ...prev, camera: 'not-supported' }))
        setError('No camera found on this device.')
      } else if (err.name === 'NotReadableError' || err.name === 'TrackStartError') {
        setError('Camera is already in use by another application.')
      } else {
        setError(`Camera error: ${err.message || 'Unknown error'}`)
      }
      
      return false
    }
  }, [])

  // Request microphone permission
  const requestMicrophonePermission = useCallback(async (): Promise<boolean> => {
    try {
      setError(null)
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true
        }
      })
      
      // Stop the stream immediately after getting permission
      stream.getTracks().forEach(track => track.stop())
      
      setPermissions(prev => ({ ...prev, microphone: 'granted' }))
      return true
    } catch (err: any) {
      console.error('Microphone permission error:', err)
      
      if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
        setPermissions(prev => ({ ...prev, microphone: 'denied' }))
        setError('Microphone access was denied. Please enable it in your browser settings.')
      } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
        setPermissions(prev => ({ ...prev, microphone: 'not-supported' }))
        setError('No microphone found on this device.')
      } else if (err.name === 'NotReadableError' || err.name === 'TrackStartError') {
        setError('Microphone is already in use by another application.')
      } else {
        setError(`Microphone error: ${err.message || 'Unknown error'}`)
      }
      
      return false
    }
  }, [])

  // Request both permissions
  const requestAllPermissions = useCallback(async (): Promise<boolean> => {
    try {
      setError(null)
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: {
          width: { ideal: 1280 },
          height: { ideal: 720 },
          facingMode: 'user'
        },
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true
        }
      })
      
      // Stop the stream immediately after getting permission
      stream.getTracks().forEach(track => track.stop())
      
      setPermissions({
        camera: 'granted',
        microphone: 'granted'
      })
      return true
    } catch (err: any) {
      console.error('Permission error:', err)
      
      // Try to determine which permission failed
      const cameraSuccess = await requestCameraPermission()
      const micSuccess = await requestMicrophonePermission()
      
      return cameraSuccess || micSuccess
    }
  }, [requestCameraPermission, requestMicrophonePermission])

  // Check permissions on mount
  useEffect(() => {
    const checkPermissions = async () => {
      if (typeof navigator === 'undefined' || !navigator.mediaDevices) {
        setPermissions({
          camera: 'not-supported',
          microphone: 'not-supported'
        })
        setError('Media devices are not supported in this browser.')
        return
      }

      const [cameraState, microphoneState] = await Promise.all([
        checkPermissionStatus('camera'),
        checkPermissionStatus('microphone')
      ])

      setPermissions({
        camera: cameraState,
        microphone: microphoneState
      })
    }

    checkPermissions()
  }, [checkPermissionStatus])

  return {
    permissions,
    error,
    requestCameraPermission,
    requestMicrophonePermission,
    requestAllPermissions,
    isSupported: typeof navigator !== 'undefined' && !!navigator.mediaDevices
  }
}
