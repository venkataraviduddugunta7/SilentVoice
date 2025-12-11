'use client'

import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import Link from 'next/link'
import { 
  Camera, 
  Mic, 
  Users, 
  Brain, 
  Shield, 
  Zap,
  ChevronRight,
  Globe,
  Heart,
  Sparkles
} from 'lucide-react'

export default function HomePage() {
  const [mounted, setMounted] = useState(false)
  
  useEffect(() => {
    setMounted(true)
  }, [])
  
  if (!mounted) return null
  
  return (
    <div className="min-h-screen overflow-hidden">
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center px-4">
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float"></div>
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float animation-delay-2000"></div>
        </div>
        
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="relative z-10 text-center max-w-6xl mx-auto"
        >
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.5 }}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass mb-6"
          >
            <Sparkles className="w-4 h-4 text-yellow-400" />
            <span className="text-sm font-medium">AI-Powered • Real-Time • Privacy-First</span>
          </motion.div>
          
          <h1 className="text-6xl md:text-8xl font-bold mb-6">
            <span className="gradient-text">SilentVoice</span>
          </h1>
          
          <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto">
            Breaking communication barriers with real-time bidirectional 
            sign language translation powered by cutting-edge AI
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Link href="/translate">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl font-semibold text-lg flex items-center gap-2 hover:shadow-2xl hover:shadow-purple-500/25 transition-all"
              >
                Start Translating
                <ChevronRight className="w-5 h-5" />
              </motion.button>
            </Link>
            
            <Link href="/learn">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="px-8 py-4 glass border border-white/20 rounded-xl font-semibold text-lg hover:bg-white/10 transition-all"
              >
                Learn Sign Language
              </motion.button>
            </Link>
          </div>
        </motion.div>
      </section>
      
      {/* Features Section */}
      <section className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <motion.h2 
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            className="text-4xl md:text-5xl font-bold text-center mb-16"
          >
            <span className="gradient-text">Hackathon MVP Features</span>
          </motion.h2>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.1 }}
                whileHover={{ y: -5 }}
                className="p-6 glass rounded-2xl hover:bg-white/10 transition-all"
              >
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${feature.gradient} flex items-center justify-center mb-4`}>
                  <feature.icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-gray-400">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
      
      {/* Stats Section */}
      <section className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-4 gap-6">
            {stats.map((stat, idx) => (
              <motion.div
                key={idx}
                initial={{ scale: 0 }}
                whileInView={{ scale: 1 }}
                transition={{ delay: idx * 0.1 }}
                className="text-center"
              >
                <div className="text-4xl md:text-5xl font-bold gradient-text mb-2">
                  {stat.value}
                </div>
                <div className="text-gray-400">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
      
      {/* CTA Section */}
      <section className="py-20 px-4">
        <motion.div 
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          className="max-w-4xl mx-auto text-center p-12 glass rounded-3xl"
        >
          <Heart className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Join the Movement
          </h2>
          <p className="text-xl text-gray-300 mb-8">
            Help us make the world more inclusive, one sign at a time
          </p>
          <Link href="/translate">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="px-8 py-4 bg-gradient-to-r from-pink-600 to-purple-600 rounded-xl font-semibold text-lg hover:shadow-2xl hover:shadow-purple-500/25 transition-all"
            >
              Get Started Now
            </motion.button>
          </Link>
        </motion.div>
      </section>
    </div>
  )
}

const features = [
  {
    icon: Camera,
    title: "Sign → Speech Translation",
    description: "Real-time hand tracking with MediaPipe and LSTM model for accurate gesture recognition",
    gradient: "from-blue-500 to-cyan-500"
  },
  {
    icon: Mic,
    title: "Speech → 3D Sign Rendering",
    description: "Convert spoken words into animated 3D sign language with our custom avatar",
    gradient: "from-purple-500 to-pink-500"
  },
  {
    icon: Shield,
    title: "Privacy-Preserving",
    description: "All processing happens locally on your device. Your data never leaves your browser",
    gradient: "from-green-500 to-emerald-500"
  },
  {
    icon: Brain,
    title: "AI Confidence System",
    description: "Smart confidence thresholds prevent incorrect guesses and ensure accuracy",
    gradient: "from-orange-500 to-red-500"
  },
  {
    icon: Zap,
    title: "Real-Time Debug Mode",
    description: "Developer-friendly debug mode shows hand landmarks and confidence scores",
    gradient: "from-yellow-500 to-orange-500"
  },
  {
    icon: Globe,
    title: "Finger-Spelling Fallback",
    description: "Automatic fallback to finger-spelling for unknown words or phrases",
    gradient: "from-indigo-500 to-purple-500"
  }
]

const stats = [
  { value: "95%", label: "Accuracy Rate" },
  { value: "<50ms", label: "Latency" },
  { value: "100%", label: "Privacy" },
  { value: "24/7", label: "Availability" }
]