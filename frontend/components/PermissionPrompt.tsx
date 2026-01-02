'use client'

import React from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Camera, Mic, Shield, AlertCircle, X } from 'lucide-react'

interface PermissionPromptProps {
  show: boolean
  onRequestPermissions: () => void
  onClose: () => void
  cameraRequired?: boolean
  microphoneRequired?: boolean
  error?: string | null
}

export default function PermissionPrompt({
  show,
  onRequestPermissions,
  onClose,
  cameraRequired = false,
  microphoneRequired = false,
  error
}: PermissionPromptProps) {
  if (!show) return null

  const getPermissionText = () => {
    if (cameraRequired && microphoneRequired) {
      return 'camera and microphone'
    } else if (cameraRequired) {
      return 'camera'
    } else if (microphoneRequired) {
      return 'microphone'
    }
    return 'media devices'
  }

  const getPermissionIcon = () => {
    if (cameraRequired && microphoneRequired) {
      return (
        <div className="flex gap-2">
          <Camera className="w-8 h-8" />
          <Mic className="w-8 h-8" />
        </div>
      )
    } else if (cameraRequired) {
      return <Camera className="w-12 h-12" />
    } else if (microphoneRequired) {
      return <Mic className="w-12 h-12" />
    }
    return <Shield className="w-12 h-12" />
  }

  return (
    <AnimatePresence>
      {show && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-[100]"
          />
          
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            className="fixed inset-0 flex items-center justify-center z-[101] p-4"
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
          >
            <div className="w-full max-w-md mx-auto">
            <div className="bg-gray-900 rounded-2xl shadow-2xl border border-white/10 overflow-hidden max-h-[90vh] overflow-y-auto">
              <div className="relative p-6">
                <button
                  onClick={onClose}
                  className="absolute top-4 right-4 p-1 rounded-lg hover:bg-white/10 transition"
                >
                  <X className="w-5 h-5 text-gray-400" />
                </button>
                
                <div className="flex flex-col items-center text-center">
                  <div className="mb-4 p-4 rounded-full bg-gradient-to-br from-blue-500/20 to-purple-500/20">
                    {getPermissionIcon()}
                  </div>
                  
                  <h2 className="text-2xl font-bold mb-2">Permission Required</h2>
                  
                  <p className="text-gray-400 mb-6">
                    SilentVoice needs access to your {getPermissionText()} to enable sign language translation.
                  </p>
                  
                  {error && (
                    <div className="w-full mb-4 p-3 rounded-lg bg-red-500/10 border border-red-500/20">
                      <div className="flex items-start gap-2">
                        <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                        <p className="text-sm text-red-400">{error}</p>
                      </div>
                    </div>
                  )}
                  
                  <div className="w-full space-y-3">
                    {cameraRequired && (
                      <div className="flex items-center gap-3 p-3 rounded-lg bg-white/5">
                        <Camera className="w-5 h-5 text-blue-400" />
                        <div className="text-left flex-1">
                          <p className="text-sm font-medium">Camera Access</p>
                          <p className="text-xs text-gray-400">For detecting sign language gestures</p>
                        </div>
                      </div>
                    )}
                    
                    {microphoneRequired && (
                      <div className="flex items-center gap-3 p-3 rounded-lg bg-white/5">
                        <Mic className="w-5 h-5 text-green-400" />
                        <div className="text-left flex-1">
                          <p className="text-sm font-medium">Microphone Access</p>
                          <p className="text-xs text-gray-400">For speech recognition</p>
                        </div>
                      </div>
                    )}
                  </div>
                  
                  <div className="flex gap-3 w-full mt-6">
                    <button
                      onClick={onClose}
                      className="flex-1 px-4 py-3 rounded-lg bg-white/10 hover:bg-white/20 transition font-medium"
                    >
                      Cancel
                    </button>
                    <button
                      onClick={onRequestPermissions}
                      className="flex-1 px-4 py-3 rounded-lg bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 transition font-medium"
                    >
                      Grant Access
                    </button>
                  </div>
                  
                  <p className="text-xs text-gray-500 mt-4">
                    Your privacy is important. We only access your {getPermissionText()} when you're actively using the translator.
                  </p>
                </div>
              </div>
            </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
