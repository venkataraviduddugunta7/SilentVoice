'use client'

import React, { Suspense, useRef, useEffect, useState } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, Html } from '@react-three/drei'
import { useGLTF } from '@react-three/drei'
import * as THREE from 'three'

// Your Ready Player Me Avatar URL
const AVATAR_URL = 'https://models.readyplayer.me/694612141c1817592ce84efe.glb'

// Sign language animations mapping - optimized for visibility
const SIGN_ANIMATIONS = {
  hello: {
    rightArm: { rotation: [-0.3, 0, -Math.PI/3], position: [0.5, 1.5, 0.5] },
    rightHand: { rotation: [0, 0, Math.PI/8], waveAnimation: true },
  },
  thank_you: {
    rightArm: { rotation: [-Math.PI/6, 0, -0.2], position: [0.3, 1.2, 0.5] },
    rightHand: { rotation: [Math.PI/4, 0, 0], moveForward: true },
  },
  yes: {
    rightArm: { rotation: [-Math.PI/3, 0, -0.2], position: [0.3, 1.3, 0.4] },
    rightHand: { rotation: [Math.PI/3, 0, 0], nodAnimation: true },
  },
  no: {
    rightArm: { rotation: [-0.2, 0, -Math.PI/4], position: [0.4, 1.4, 0.3] },
    rightHand: { rotation: [0, Math.PI/4, 0], shakeAnimation: true },
  },
  please: {
    rightArm: { rotation: [-Math.PI/6, 0, -0.1], position: [0, 1.2, 0.4] },
    rightHand: { rotation: [0, 0, 0], circularMotion: true },
  },
  sorry: {
    rightArm: { rotation: [-Math.PI/6, 0, -0.1], position: [0, 1.2, 0.4] },
    rightHand: { rotation: [Math.PI/2, 0, 0], circularMotion: true },
  },
  help: {
    rightArm: { rotation: [-0.2, 0, -Math.PI/4], position: [0.3, 1.3, 0.3] },
    leftArm: { rotation: [-Math.PI/3, 0, Math.PI/4], position: [-0.3, 1.2, 0.5] },
  },
  love: {
    rightArm: { rotation: [-Math.PI/3, Math.PI/6, 0], position: [0.2, 1.2, 0.4] },
    leftArm: { rotation: [-Math.PI/3, -Math.PI/6, 0], position: [-0.2, 1.2, 0.4] },
  },
  goodbye: {
    rightArm: { rotation: [-0.2, 0, -Math.PI/2.5], position: [0.5, 1.5, 0.4] },
    rightHand: { rotation: [0, 0, Math.PI/6], waveAnimation: true },
  }
}

// Ready Player Me Avatar Component
function ReadyPlayerMeAvatar({ signSequence = '', isAnimating = false }) {
  const group = useRef()
  const { scene } = useGLTF(AVATAR_URL)
  
  // Clone the scene to avoid mutation issues
  const clonedScene = React.useMemo(() => scene.clone(), [scene])
  
  // Animation bones
  const bones = useRef({
    rightArm: null,
    leftArm: null,
    rightHand: null,
    leftHand: null,
    spine: null
  })
  
  // Animation state
  const animationTime = useRef(0)
  const [currentSign, setCurrentSign] = useState(null)
  
  useEffect(() => {
    if (clonedScene) {
      // Find animation bones in the model
      clonedScene.traverse((child) => {
        if (child.isBone) {
          const name = child.name.toLowerCase()
          if (name.includes('rightarm') || name.includes('right_arm') || name.includes('r_upperarm')) {
            bones.current.rightArm = child
          } else if (name.includes('leftarm') || name.includes('left_arm') || name.includes('l_upperarm')) {
            bones.current.leftArm = child
          } else if (name.includes('righthand') || name.includes('right_hand') || name.includes('r_hand')) {
            bones.current.rightHand = child
          } else if (name.includes('lefthand') || name.includes('left_hand') || name.includes('l_hand')) {
            bones.current.leftHand = child
          } else if (name.includes('spine') || name.includes('chest')) {
            bones.current.spine = child
          }
        }
      })
    }
  }, [clonedScene])
  
  useEffect(() => {
    // Update current sign based on sequence
    if (signSequence) {
      const words = signSequence.toLowerCase().split(' ')
      for (const word of words) {
        if (SIGN_ANIMATIONS[word]) {
          setCurrentSign(word)
          break
        }
      }
    } else {
      setCurrentSign(null)
    }
  }, [signSequence])
  
  useFrame((state, delta) => {
    if (!isAnimating || !currentSign || !SIGN_ANIMATIONS[currentSign]) return
    
    animationTime.current += delta
    const animation = SIGN_ANIMATIONS[currentSign]
    
    // Animate right arm
    if (bones.current.rightArm && animation.rightArm) {
      const targetRotation = animation.rightArm.rotation
      bones.current.rightArm.rotation.x = THREE.MathUtils.lerp(
        bones.current.rightArm.rotation.x,
        targetRotation[0],
        0.15
      )
      bones.current.rightArm.rotation.y = THREE.MathUtils.lerp(
        bones.current.rightArm.rotation.y,
        targetRotation[1],
        0.15
      )
      bones.current.rightArm.rotation.z = THREE.MathUtils.lerp(
        bones.current.rightArm.rotation.z,
        targetRotation[2],
        0.15
      )
    }
    
    // Animate left arm
    if (bones.current.leftArm && animation.leftArm) {
      const targetRotation = animation.leftArm.rotation
      bones.current.leftArm.rotation.x = THREE.MathUtils.lerp(
        bones.current.leftArm.rotation.x,
        targetRotation[0],
        0.15
      )
      bones.current.leftArm.rotation.y = THREE.MathUtils.lerp(
        bones.current.leftArm.rotation.y,
        targetRotation[1],
        0.15
      )
      bones.current.leftArm.rotation.z = THREE.MathUtils.lerp(
        bones.current.leftArm.rotation.z,
        targetRotation[2],
        0.15
      )
    }
    
    // Animate hands with special animations - more visible
    if (bones.current.rightHand && animation.rightHand) {
      if (animation.rightHand.waveAnimation) {
        bones.current.rightHand.rotation.z = Math.sin(animationTime.current * 5) * 0.5
      } else if (animation.rightHand.nodAnimation) {
        bones.current.rightHand.rotation.x = Math.sin(animationTime.current * 4) * 0.5
      } else if (animation.rightHand.shakeAnimation) {
        bones.current.rightHand.rotation.y = Math.sin(animationTime.current * 6) * 0.4
      } else if (animation.rightHand.circularMotion) {
        bones.current.rightHand.position.x = Math.sin(animationTime.current * 2) * 0.15
        bones.current.rightHand.position.z = Math.cos(animationTime.current * 2) * 0.15
      }
    }
  })
  
  return (
    <group ref={group} position={[0, -0.5, 0]} scale={1.5}>
      <primitive object={clonedScene} />
    </group>
  )
}

// Fallback Simple Avatar (only used if RPM avatar fails)
function SimpleAvatar({ signSequence = '', isAnimating = false }) {
  const groupRef = useRef()
  
  return (
    <group ref={groupRef} position={[0, -0.5, 0]} scale={1.2}>
      {/* Upper Body */}
      <mesh position={[0, 0, 0]}>
        <boxGeometry args={[0.8, 1, 0.4]} />
        <meshStandardMaterial color="#4A5568" />
      </mesh>
      
      {/* Head */}
      <mesh position={[0, 0.9, 0]}>
        <sphereGeometry args={[0.3]} />
        <meshStandardMaterial color="#FDB5A6" />
      </mesh>
      
      {/* Eyes */}
      <mesh position={[-0.08, 0.95, 0.25]}>
        <sphereGeometry args={[0.04]} />
        <meshStandardMaterial color="#2D3748" />
      </mesh>
      <mesh position={[0.08, 0.95, 0.25]}>
        <sphereGeometry args={[0.04]} />
        <meshStandardMaterial color="#2D3748" />
      </mesh>
      
      {/* Arms - visible for signs */}
      <mesh position={[-0.5, 0.3, 0]}>
        <capsuleGeometry args={[0.08, 0.6, 4, 8]} />
        <meshStandardMaterial color="#FDB5A6" />
      </mesh>
      <mesh position={[0.5, 0.3, 0]}>
        <capsuleGeometry args={[0.08, 0.6, 4, 8]} />
        <meshStandardMaterial color="#FDB5A6" />
      </mesh>
      
      {/* Hands */}
      <mesh position={[-0.5, -0.1, 0]}>
        <sphereGeometry args={[0.08]} />
        <meshStandardMaterial color="#FDB5A6" />
      </mesh>
      <mesh position={[0.5, -0.1, 0]}>
        <sphereGeometry args={[0.08]} />
        <meshStandardMaterial color="#FDB5A6" />
      </mesh>
    </group>
  )
}

// Avatar Scene Component
function AvatarScene({ signSequence, isAnimating, useReadyPlayerMe }) {
  const [avatarError, setAvatarError] = useState(false)
  
  return (
    <>
      {/* Lighting optimized for sign language */}
      <ambientLight intensity={0.7} />
      <directionalLight position={[5, 5, 5]} intensity={1} castShadow />
      <directionalLight position={[-5, 5, 5]} intensity={0.8} />
      <spotLight position={[0, 3, 3]} intensity={0.5} angle={0.6} penumbra={0.5} />
      <pointLight position={[0, 0, 2]} intensity={0.3} />
      
      {/* Avatar Selection */}
      {useReadyPlayerMe && !avatarError ? (
        <Suspense fallback={
          <Html center>
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mb-4"></div>
              <p className="text-sm text-gray-400">Loading avatar...</p>
            </div>
          </Html>
        }>
          <ReadyPlayerMeAvatar 
            signSequence={signSequence} 
            isAnimating={isAnimating}
          />
        </Suspense>
      ) : (
        <SimpleAvatar 
          signSequence={signSequence} 
          isAnimating={isAnimating}
        />
      )}
      
      {/* Camera Controls */}
      <OrbitControls 
        target={[0, 1, 0]}
        enablePan={false}
        enableZoom={true}
        maxPolarAngle={Math.PI / 2.2}
        minPolarAngle={Math.PI / 3.5}
        maxDistance={2.2}
        minDistance={1}
        autoRotate={false}
        enableRotate={true}
        rotateSpeed={0.5}
      />
    </>
  )
}

// Main Component
export default function HumanAvatar3D({ 
  signSequence = '', 
  isAnimating = false, 
  useReadyPlayerMe = true 
}) {
  const [mounted, setMounted] = useState(false)
  
  useEffect(() => {
    setMounted(true)
  }, [])
  
  // Don't render on server
  if (!mounted) {
    return (
      <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-gray-900 to-black">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-sm text-gray-400">Initializing avatar...</p>
        </div>
      </div>
    )
  }
  
  return (
    <div className="relative w-full h-full bg-gradient-to-br from-gray-900 via-black to-gray-900 overflow-hidden">
      <Canvas
        shadows
        camera={{ position: [0, 1.2, 1.8], fov: 35 }}
        gl={{ antialias: true, alpha: true }}
      >
        <AvatarScene 
          signSequence={signSequence}
          isAnimating={isAnimating}
          useReadyPlayerMe={useReadyPlayerMe}
        />
      </Canvas>
      
      {/* Minimal Status */}
      <div className="absolute top-2 right-2">
        <div className="bg-black/40 backdrop-blur-sm rounded px-2 py-1">
          <p className="text-[10px] text-gray-400">
            {useReadyPlayerMe ? '🎭' : '📦'}
          </p>
        </div>
      </div>
      
      {/* Current Sign */}
      {signSequence && (
        <div className="absolute bottom-2 left-2 right-2">
          <div className="bg-black/40 backdrop-blur-sm rounded px-2 py-1">
            <p className="text-[10px] text-gray-300 text-center">
              {signSequence}
            </p>
          </div>
        </div>
      )}
    </div>
  )
}