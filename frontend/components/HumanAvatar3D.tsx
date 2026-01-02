'use client'

import React, { Suspense, useRef, useEffect, useState } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, Html } from '@react-three/drei'
import { useGLTF } from '@react-three/drei'
import * as THREE from 'three'
import { motion, AnimatePresence } from 'framer-motion'

// Your Ready Player Me Avatar URL
const AVATAR_URL = 'https://models.readyplayer.me/694612141c1817592ce84efe.glb'

// Sign language animations mapping - optimized for visibility
const SIGN_ANIMATIONS = {
  hello: {
    rightArm: { rotation: [-0.3, 0, -Math.PI / 3], position: [0.5, 1.5, 0.5] },
    rightHand: { rotation: [0, 0, Math.PI / 8], waveAnimation: true },
  },
  thank_you: {
    rightArm: { rotation: [-Math.PI / 6, 0, -0.2], position: [0.3, 1.2, 0.5] },
    rightHand: { rotation: [Math.PI / 4, 0, 0], moveForward: true },
  },
  yes: {
    rightArm: { rotation: [-Math.PI / 3, 0, -0.2], position: [0.3, 1.3, 0.4] },
    rightHand: { rotation: [Math.PI / 3, 0, 0], nodAnimation: true },
  },
  no: {
    rightArm: { rotation: [-0.2, 0, -Math.PI / 4], position: [0.4, 1.4, 0.3] },
    rightHand: { rotation: [0, Math.PI / 4, 0], shakeAnimation: true },
  },
  please: {
    rightArm: { rotation: [-Math.PI / 6, 0, -0.1], position: [0, 1.2, 0.4] },
    rightHand: { rotation: [0, 0, 0], circularMotion: true },
  },
  sorry: {
    rightArm: { rotation: [-Math.PI / 6, 0, -0.1], position: [0, 1.2, 0.4] },
    rightHand: { rotation: [Math.PI / 2, 0, 0], circularMotion: true },
  },
  help: {
    rightArm: { rotation: [-0.2, 0, -Math.PI / 4], position: [0.3, 1.3, 0.3] },
    leftArm: { rotation: [-Math.PI / 3, 0, Math.PI / 4], position: [-0.3, 1.2, 0.5] },
  },
  love: {
    rightArm: { rotation: [-Math.PI / 3, Math.PI / 6, 0], position: [0.2, 1.2, 0.4] },
    leftArm: { rotation: [-Math.PI / 3, -Math.PI / 6, 0], position: [-0.2, 1.2, 0.4] },
  },
  goodbye: {
    rightArm: { rotation: [-0.2, 0, -Math.PI / 2.5], position: [0.5, 1.5, 0.4] },
    rightHand: { rotation: [0, 0, Math.PI / 6], waveAnimation: true },
  }
}

// Ready Player Me Avatar Component
function ReadyPlayerMeAvatar({ signSequence = '', isAnimating = false, isMobile = false }) {
  const group = useRef<THREE.Group>(null)
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

  // New States for enhanced interaction
  const [isWalking, setIsWalking] = useState(true)
  const walkTime = useRef(0)

  // Initial Entrance Animation - useLayoutEffect to prevent visual flash at wrong position
  React.useLayoutEffect(() => {
    // Start slightly back for a natural entry, but not too far (-1.5m)
    if (group.current) {
      group.current.position.z = -1.5
      setIsWalking(true)
    }
  }, [])

  // Setup Smile and find bones
  useEffect(() => {
    if (clonedScene) {
      // Find animation bones in the model (type-safe version)
      clonedScene.traverse((child: THREE.Object3D) => {
        if (child instanceof THREE.Mesh) {
          // Facial Expressions (Morph Targets)
          if (child.morphTargetDictionary && child.morphTargetInfluences) {
            const smileIndex = child.morphTargetDictionary['mouthSmile'] || child.morphTargetDictionary['smile']
            if (smileIndex !== undefined && child.morphTargetInfluences) {
              child.morphTargetInfluences[smileIndex] = 0.7 // Gentle smile
            }
          }
          // Ensure visibility from all angles
          child.frustumCulled = false;
          if (child.material) {
            child.material.side = THREE.DoubleSide; // Handle one-sided materials
          }
        }

        if ('isBone' in child && child.isBone) {
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
    // 1. Entrance Walking Animation
    if (isWalking && group.current) {
      walkTime.current += delta

      // Move forward
      group.current.position.z = THREE.MathUtils.lerp(group.current.position.z, 0, delta * 2)

      // Bobbing motion
      group.current.position.y = -0.5 + Math.sin(walkTime.current * 10) * 0.05

      // Slight rotation sway
      group.current.rotation.y = Math.sin(walkTime.current * 5) * 0.05

      // Arm swing while walking
      if (bones.current.rightArm && bones.current.leftArm) {
        bones.current.rightArm.rotation.x = Math.sin(walkTime.current * 10) * 0.3
        bones.current.leftArm.rotation.x = -Math.sin(walkTime.current * 10) * 0.3
        bones.current.rightArm.rotation.z = -0.2
        bones.current.leftArm.rotation.z = 0.2
      }

      // Stop walking when close
      if (Math.abs(group.current.position.z) < 0.1) {
        setIsWalking(false)
        group.current.position.z = 0
        group.current.position.y = -0.5
        group.current.rotation.y = 0
      }
      return
    }

    // 2. Idle Animation (Hands clasped, breathing)
    if (!isAnimating && !currentSign) {
      animationTime.current += delta

      // Breathing (Spine/Chest)
      if (bones.current.spine) {
        bones.current.spine.rotation.x = Math.sin(animationTime.current * 2) * 0.02
      }

      // Hands Clasped Pose
      // Right Arm
      if (bones.current.rightArm) {
        bones.current.rightArm.rotation.x = THREE.MathUtils.lerp(bones.current.rightArm.rotation.x, -0.5, 0.1)
        bones.current.rightArm.rotation.y = THREE.MathUtils.lerp(bones.current.rightArm.rotation.y, -0.5, 0.1) // Bring inward
        bones.current.rightArm.rotation.z = THREE.MathUtils.lerp(bones.current.rightArm.rotation.z, -0.2, 0.1)
      }
      // Left Arm
      if (bones.current.leftArm) {
        bones.current.leftArm.rotation.x = THREE.MathUtils.lerp(bones.current.leftArm.rotation.x, -0.5, 0.1)
        bones.current.leftArm.rotation.y = THREE.MathUtils.lerp(bones.current.leftArm.rotation.y, 0.5, 0.1) // Bring inward
        bones.current.leftArm.rotation.z = THREE.MathUtils.lerp(bones.current.leftArm.rotation.z, 0.2, 0.1)
      }
      // Hands
      if (bones.current.rightHand) {
        bones.current.rightHand.rotation.x = THREE.MathUtils.lerp(bones.current.rightHand.rotation.x, 0, 0.1)
        const handX = Math.sin(animationTime.current) * 0.005
        bones.current.rightHand.position.set(handX, 0, 0) // Micro movement
      }
      return
    }

    // 3. Sign Language Animation (Existing logic)
    if (!currentSign || !SIGN_ANIMATIONS[currentSign]) return

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
    <group ref={group} position={[0, -0.5, 0]} scale={isMobile ? 1.2 : 1.5}>
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
function AvatarScene({ signSequence, isAnimating, useReadyPlayerMe, isMobile }) {
  const [avatarError, setAvatarError] = useState(false)

  return (
    <>
      {/* Studio lighting for 360 observability */}
      <ambientLight intensity={0.6} />
      {/* Front lights */}
      <directionalLight position={[5, 5, 5]} intensity={1.2} castShadow />
      <directionalLight position={[-5, 5, 5]} intensity={0.8} />
      {/* Back/Rim light for side and back visibility */}
      <directionalLight position={[0, 5, -5]} intensity={1.0} />
      <directionalLight position={[0, 0, -5]} intensity={0.5} />

      <spotLight position={[0, 5, 5]} intensity={0.8} angle={0.6} penumbra={0.5} />
      <pointLight position={[0, 2, 2]} intensity={0.4} />

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
            isMobile={isMobile}
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
        target={[0, 1.45, 0]}
        enablePan={false}
        enableZoom={true}
        maxPolarAngle={Math.PI / 2.2}
        minPolarAngle={Math.PI / 3.5}
        maxDistance={4.0}
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
  const [isMobile, setIsMobile] = useState(false)
  // State for delayed subtitle clearing
  const [displaySign, setDisplaySign] = useState('')

  useEffect(() => {
    setMounted(true)
    setIsMobile(window.innerWidth < 768)
    
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768)
    }
    
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  useEffect(() => {
    if (signSequence) {
      setDisplaySign(signSequence)
      // Clear subtitle after 3 seconds of no updates
      const timer = setTimeout(() => {
        setDisplaySign('')
      }, 3000)
      return () => clearTimeout(timer)
    }
  }, [signSequence])

  // Don't render on server
  if (!mounted) {
    return (
      <div className="w-full h-full flex items-center justify-center bg-[radial-gradient(circle_at_center,_#ffffff_0%,_#f3f4f6_100%)]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-slate-800 mx-auto mb-4"></div>
          <p className="text-sm text-slate-600">Initializing avatar...</p>
        </div>
      </div>
    )
  }

  // isMobile is now managed by state

  return (
    <div className="relative w-full h-full min-h-[300px] max-h-[80vh] bg-gray-50 overflow-hidden">
      {/* Premium Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-[-20%] right-[-10%] w-[500px] h-[500px] bg-amber-200/40 rounded-full mix-blend-multiply filter blur-[80px] animate-float opacity-70"></div>
        <div className="absolute bottom-[-20%] left-[-10%] w-[500px] h-[500px] bg-blue-200/40 rounded-full mix-blend-multiply filter blur-[80px] animate-float animation-delay-2000 opacity-70"></div>
        <div className="absolute top-[40%] left-[30%] w-[300px] h-[300px] bg-purple-100/40 rounded-full mix-blend-multiply filter blur-[60px] animate-pulse opacity-50"></div>

        {/* Apple-style Grain/Noise Overlay for Texture */}
        <div className="absolute inset-0 opacity-[0.03] pointer-events-none bg-[url('https://grainy-gradients.vercel.app/noise.svg')]"></div>
      </div>

      <Canvas
        shadows
        camera={{
          position: [0, 1.45, isMobile ? 3.5 : 2.1],
          fov: isMobile ? 50 : 40
        }}
        gl={{ antialias: true, alpha: true }}
        className="relative z-10 w-full h-full"
        style={{ touchAction: 'none' }}
      >
        <AvatarScene
          signSequence={signSequence}
          isAnimating={isAnimating}
          useReadyPlayerMe={useReadyPlayerMe}
          isMobile={isMobile}
        />
      </Canvas>

      {/* Cinematic Subtitles - Apple TV Style */}
      <AnimatePresence>
        {displaySign && (
          <div className="absolute md:bottom-12 bottom-6 left-0 right-0 flex justify-center z-20 px-2 pointer-events-none">
            <motion.div
              initial={{ opacity: 0, y: 10, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, scale: 1, transition: { duration: 0.4 } }}
              className="bg-black/40 backdrop-blur-md md:px-4 px-2 md:py-2 py-2 rounded-xl border border-white/5 shadow-2xl max-w-2xl"
            >
              <p className="md:text-lg text-base font-light text-white tracking-wide text-center drop-shadow-sm leading-relaxed">
                {displaySign}
              </p>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  )
}