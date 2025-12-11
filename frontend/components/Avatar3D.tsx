'use client'

import React, { useRef, useEffect, useState } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, Html } from '@react-three/drei'
import * as THREE from 'three'

// Sign pose data (simplified for demo - in production, load from database)
const signPoses: Record<string, any> = {
  hello: {
    rightHand: { rotation: [0, 0, Math.PI / 4], position: [0.5, 1.2, 0] },
    leftHand: { rotation: [0, 0, 0], position: [-0.5, 0.8, 0] },
  },
  thank_you: {
    rightHand: { rotation: [Math.PI / 6, 0, 0], position: [0.3, 1.0, 0.2] },
    leftHand: { rotation: [0, 0, 0], position: [-0.5, 0.8, 0] },
  },
  please: {
    rightHand: { rotation: [0, Math.PI / 4, 0], position: [0, 1.1, 0.3] },
    leftHand: { rotation: [0, 0, 0], position: [-0.5, 0.8, 0] },
  },
  yes: {
    rightHand: { rotation: [Math.PI / 3, 0, 0], position: [0.4, 1.3, 0] },
    leftHand: { rotation: [0, 0, 0], position: [-0.5, 0.8, 0] },
  },
  no: {
    rightHand: { rotation: [0, 0, Math.PI / 6], position: [0.4, 1.1, 0] },
    leftHand: { rotation: [0, 0, 0], position: [-0.5, 0.8, 0] },
  },
  help: {
    rightHand: { rotation: [Math.PI / 4, 0, 0], position: [0.3, 1.2, 0.1] },
    leftHand: { rotation: [-Math.PI / 4, 0, 0], position: [-0.3, 0.9, 0.2] },
  },
}

// Animated Arm Component
function AnimatedArm({ pose, side }: { pose: any; side: 'right' | 'left' }) {
  const groupRef = useRef<THREE.Group>(null)
  const currentRotation = useRef(new THREE.Euler(...pose.rotation))
  const currentPosition = useRef(new THREE.Vector3(...pose.position))
  
  useEffect(() => {
    currentRotation.current = new THREE.Euler(...pose.rotation)
    currentPosition.current = new THREE.Vector3(...pose.position)
  }, [pose])
  
  useFrame(() => {
    if (groupRef.current) {
      // Smoothly interpolate rotation
      groupRef.current.rotation.x += (currentRotation.current.x - groupRef.current.rotation.x) * 0.1
      groupRef.current.rotation.y += (currentRotation.current.y - groupRef.current.rotation.y) * 0.1
      groupRef.current.rotation.z += (currentRotation.current.z - groupRef.current.rotation.z) * 0.1
      
      // Smoothly interpolate position
      groupRef.current.position.lerp(currentPosition.current, 0.1)
    }
  })
  
  return (
    <group ref={groupRef}>
      <mesh>
        <boxGeometry args={[0.1, 0.6, 0.1]} />
        <meshStandardMaterial color="#FDB2A9" />
      </mesh>
      {/* Hand */}
      <mesh position={[0, -0.35, 0]}>
        <sphereGeometry args={[0.08, 16, 16]} />
        <meshStandardMaterial color="#FDB2A9" />
      </mesh>
      {/* Fingers (simplified) */}
      {[0, 1, 2, 3, 4].map((i) => (
        <mesh key={`${side}f${i}`} position={[0, -0.4 - i * 0.05, 0]}>
          <boxGeometry args={[0.02, 0.08, 0.02]} />
          <meshStandardMaterial color="#FDB2A9" />
        </mesh>
      ))}
    </group>
  )
}

// Simplified 3D Avatar Model
function AvatarModel({ signSequence, isAnimating }: { signSequence: string; isAnimating: boolean }) {
  const groupRef = useRef<THREE.Group>(null)
  const [currentPose, setCurrentPose] = useState(signPoses.hello)
  
  // Update pose when sign changes
  useEffect(() => {
    const pose = signPoses[signSequence?.toLowerCase().replace(/\s+/g, '_')] || signPoses.hello
    setCurrentPose(pose)
  }, [signSequence])
  
  // Animate the model
  useFrame((state) => {
    if (groupRef.current && isAnimating) {
      groupRef.current.rotation.y = Math.sin(state.clock.elapsedTime) * 0.1
    }
  })
  
  return (
    <group ref={groupRef}>
      {/* Body */}
      <mesh position={[0, 0, 0]}>
        <cylinderGeometry args={[0.3, 0.4, 2, 32]} />
        <meshStandardMaterial color="#4A5568" />
      </mesh>
      
      {/* Head */}
      <mesh position={[0, 1.5, 0]}>
        <sphereGeometry args={[0.3, 32, 32]} />
        <meshStandardMaterial color="#FDB2A9" />
      </mesh>
      
      {/* Eyes */}
      <mesh position={[-0.1, 1.55, 0.25]}>
        <sphereGeometry args={[0.03, 16, 16]} />
        <meshStandardMaterial color="#000000" />
      </mesh>
      <mesh position={[0.1, 1.55, 0.25]}>
        <sphereGeometry args={[0.03, 16, 16]} />
        <meshStandardMaterial color="#000000" />
      </mesh>
      
      {/* Right Arm */}
      <AnimatedArm pose={currentPose.rightHand} side="right" />
      
      {/* Left Arm */}
      <AnimatedArm pose={currentPose.leftHand} side="left" />
      
      {/* Sign Label */}
      {signSequence && (
        <Html position={[0, 2.5, 0]} center>
          <div className="px-3 py-1 bg-blue-500/20 backdrop-blur-sm rounded-full border border-blue-500/50">
            <span className="text-blue-400 text-sm font-medium">{signSequence}</span>
          </div>
        </Html>
      )}
    </group>
  )
}

export default function Avatar3D({ 
  signSequence = '', 
  isAnimating = false 
}: { 
  signSequence?: string
  isAnimating?: boolean 
}) {
  return (
    <div className="w-full h-full bg-gradient-to-b from-gray-900 to-black">
      <Canvas
        camera={{ position: [0, 1, 5], fov: 50 }}
        gl={{ antialias: true, alpha: true }}
      >
        {/* Lighting */}
        <ambientLight intensity={0.5} />
        <directionalLight position={[10, 10, 5]} intensity={1} />
        <directionalLight position={[-10, -10, -5]} intensity={0.5} />
        <spotLight position={[0, 5, 0]} intensity={0.8} angle={0.3} />
        
        {/* Avatar Model */}
        <AvatarModel signSequence={signSequence} isAnimating={isAnimating} />
        
        {/* Controls */}
        <OrbitControls 
          enablePan={false}
          enableZoom={true}
          maxPolarAngle={Math.PI / 1.5}
          minPolarAngle={Math.PI / 3}
          maxDistance={8}
          minDistance={3}
        />
        
        {/* Grid Helper */}
        <gridHelper args={[10, 10, '#4A5568', '#2D3748']} />
      </Canvas>
      
      {/* Instructions */}
      <div className="absolute bottom-4 left-4 right-4 text-center">
        <p className="text-xs text-gray-500">
          Drag to rotate • Scroll to zoom • Avatar shows ASL signs
        </p>
      </div>
    </div>
  )
}