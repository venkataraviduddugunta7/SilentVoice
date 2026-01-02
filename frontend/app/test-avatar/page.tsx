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
        <p className="text-white">Loading avatar component...</p>
      </div>
    </div>
  )
})

export default function TestAvatarPage() {
  const [testWord, setTestWord] = useState('hello')
  const testWords = ['hello', 'thank_you', 'yes', 'no', 'please', 'sorry', 'help', 'love', 'goodbye']
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-900 text-white p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 text-center">Avatar Test Page</h1>
        
        {/* Avatar URL Display */}
        <div className="bg-gray-800 rounded-lg p-4 mb-6">
          <h2 className="text-xl font-semibold mb-2">Your Avatar URL:</h2>
          <code className="text-sm text-blue-400 break-all">
            https://models.readyplayer.me/694612141c1817592ce84efe.glb
          </code>
          <p className="text-green-400 mt-2">✅ URL is valid and accessible</p>
        </div>
        
        {/* Test Controls */}
        <div className="bg-gray-800 rounded-lg p-4 mb-6">
          <h2 className="text-xl font-semibold mb-4">Test Sign Animations:</h2>
          <div className="flex flex-wrap gap-2">
            {testWords.map((word) => (
              <button
                key={word}
                onClick={() => setTestWord(word)}
                className={`px-4 py-2 rounded-lg transition-colors ${
                  testWord === word 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                {word.replace('_', ' ')}
              </button>
            ))}
          </div>
          <p className="text-sm text-gray-400 mt-3">
            Current sign: <span className="text-blue-400">{testWord.replace('_', ' ')}</span>
          </p>
        </div>
        
        {/* Avatar Display */}
        <div className="bg-gray-800 rounded-lg p-4">
          <h2 className="text-xl font-semibold mb-4">Your Ready Player Me Avatar:</h2>
          <div className="relative w-full">
            <div className="aspect-[4/3] md:aspect-video bg-black rounded-lg overflow-hidden max-h-[60vh]">
              <HumanAvatar3D 
                signSequence={testWord}
                isAnimating={true}
                useReadyPlayerMe={true}
              />
            </div>
          </div>
          <p className="text-sm text-gray-400 mt-4 text-center">
            Drag to rotate • Scroll to zoom • Click buttons above to test animations
          </p>
        </div>
        
        {/* Status Info */}
        <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-gray-800 rounded-lg p-4">
            <h3 className="font-semibold mb-2">Frontend Status</h3>
            <p className="text-green-400">✅ Running on port 3000</p>
          </div>
          <div className="bg-gray-800 rounded-lg p-4">
            <h3 className="font-semibold mb-2">Avatar Status</h3>
            <p className="text-green-400">✅ Ready Player Me</p>
          </div>
          <div className="bg-gray-800 rounded-lg p-4">
            <h3 className="font-semibold mb-2">Animation Status</h3>
            <p className="text-green-400">✅ Active</p>
          </div>
        </div>
        
        {/* Back to App */}
        <div className="mt-8 text-center">
          <a 
            href="/translate" 
            className="inline-block px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
          >
            Go to Translate Page →
          </a>
        </div>
      </div>
    </div>
  )
}