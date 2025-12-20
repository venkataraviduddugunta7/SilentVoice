'use client'

import React, { useState } from 'react'
import dynamic from 'next/dynamic'

// Dynamically import 3D avatar to avoid SSR issues
const HumanAvatar3D = dynamic(() => import('@/components/HumanAvatar3D'), {
  ssr: false,
  loading: () => (
    <div className="flex items-center justify-center h-full">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mb-4 mx-auto"></div>
        <p className="text-white">Loading avatar...</p>
      </div>
    </div>
  )
})

export default function AvatarAdjustPage() {
  const [testWord, setTestWord] = useState('hello')
  const testWords = ['hello', 'thank_you', 'yes', 'no', 'please', 'sorry', 'help', 'love', 'goodbye']
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-900 text-white">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6 text-center">Avatar Position Check</h1>
        
        {/* Main Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Avatar Display - Larger */}
          <div className="lg:col-span-2">
            <div className="bg-gray-800 rounded-lg p-4">
              <h2 className="text-xl font-semibold mb-4">Upper Body View</h2>
              <div className="aspect-video bg-black rounded-lg overflow-hidden">
                <HumanAvatar3D 
                  signSequence={testWord}
                  isAnimating={true}
                  useReadyPlayerMe={true}
                />
              </div>
            </div>
          </div>
          
          {/* Controls Panel */}
          <div className="space-y-4">
            {/* Position Info */}
            <div className="bg-gray-800 rounded-lg p-4">
              <h3 className="font-semibold mb-3">Current Settings:</h3>
              <div className="text-sm space-y-2 font-mono">
                <p className="text-green-400">Avatar Position: [0, -0.5, 0]</p>
                <p className="text-green-400">Avatar Scale: 1.5</p>
                <p className="text-blue-400">Camera: [0, 1.2, 1.8]</p>
                <p className="text-blue-400">FOV: 35°</p>
                <p className="text-yellow-400">Target: [0, 1, 0] (chest)</p>
              </div>
            </div>
            
            {/* Sign Selection */}
            <div className="bg-gray-800 rounded-lg p-4">
              <h3 className="font-semibold mb-3">Test Signs:</h3>
              <div className="grid grid-cols-2 gap-2">
                {testWords.map((word) => (
                  <button
                    key={word}
                    onClick={() => setTestWord(word)}
                    className={`px-3 py-2 rounded text-sm transition-colors ${
                      testWord === word 
                        ? 'bg-blue-600 text-white' 
                        : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                    }`}
                  >
                    {word.replace('_', ' ')}
                  </button>
                ))}
              </div>
            </div>
            
            {/* View Guide */}
            <div className="bg-gray-800 rounded-lg p-4">
              <h3 className="font-semibold mb-3">What You Should See:</h3>
              <ul className="text-sm space-y-1 text-gray-300">
                <li>✅ Head and face clearly visible</li>
                <li>✅ Both shoulders in frame</li>
                <li>✅ Chest area (reference point)</li>
                <li>✅ Both arms fully visible</li>
                <li>✅ Hands clearly shown</li>
                <li>❌ No legs/lower body</li>
                <li>❌ No wasted space above head</li>
              </ul>
            </div>
            
            {/* Instructions */}
            <div className="bg-gray-800 rounded-lg p-4">
              <h3 className="font-semibold mb-3">Controls:</h3>
              <ul className="text-sm space-y-1 text-gray-300">
                <li>🖱️ Drag to rotate view</li>
                <li>🔍 Scroll to zoom in/out</li>
                <li>👆 Click signs to test</li>
              </ul>
            </div>
          </div>
        </div>
        
        {/* Status Bar */}
        <div className="mt-6 bg-gray-800 rounded-lg p-4">
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-400">
              Current sign: <span className="text-blue-400 font-semibold">{testWord.replace('_', ' ')}</span>
            </span>
            <div className="flex gap-4">
              <a href="/translate" className="text-sm text-blue-400 hover:text-blue-300">
                → Translate Page
              </a>
              <a href="/test-avatar" className="text-sm text-blue-400 hover:text-blue-300">
                → Full Test Page
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}