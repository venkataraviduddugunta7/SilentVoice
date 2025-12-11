'use client'

import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import Link from 'next/link'
import { 
  Book, 
  GraduationCap, 
  Search,
  Filter,
  ChevronRight,
  ChevronLeft,
  Star,
  Trophy,
  Target,
  Sparkles,
  Hand,
  Volume2,
  Eye,
  BookOpen,
  Users
} from 'lucide-react'
import dynamic from 'next/dynamic'

// Dynamic import for 3D components
const Avatar3D = dynamic(() => import('@/components/Avatar3D'), {
  ssr: false,
  loading: () => <div className="flex items-center justify-center h-full"><div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div></div>
})

// Sign dictionary data
const signDictionary = {
  categories: {
    greetings: {
      title: 'Greetings',
      icon: '👋',
      signs: [
        { word: 'Hello', description: 'Open hand, palm facing out, move in small wave', difficulty: 'beginner' },
        { word: 'Goodbye', description: 'Open hand, fingers together, wave side to side', difficulty: 'beginner' },
        { word: 'Thank You', description: 'Flat hand starts at chin, moves forward', difficulty: 'beginner' },
        { word: 'Please', description: 'Flat hand circles on chest', difficulty: 'beginner' },
        { word: 'Sorry', description: 'Closed fist circles on chest', difficulty: 'beginner' },
      ]
    },
    basics: {
      title: 'Basic Responses',
      icon: '💬',
      signs: [
        { word: 'Yes', description: 'Closed fist nods up and down', difficulty: 'beginner' },
        { word: 'No', description: 'Index and middle finger tap thumb', difficulty: 'beginner' },
        { word: 'Maybe', description: 'Flat hands alternate up and down', difficulty: 'intermediate' },
        { word: 'I Don\'t Know', description: 'Touch forehead, then move hand away palm up', difficulty: 'intermediate' },
      ]
    },
    questions: {
      title: 'Question Words',
      icon: '❓',
      signs: [
        { word: 'What', description: 'Both hands palm up, shake side to side', difficulty: 'intermediate' },
        { word: 'Where', description: 'Index finger up, shake side to side', difficulty: 'intermediate' },
        { word: 'When', description: 'Index finger circles around opposite index', difficulty: 'intermediate' },
        { word: 'Why', description: 'Middle fingers on forehead, move to Y shape', difficulty: 'intermediate' },
        { word: 'How', description: 'Bent fingers together, twist outward', difficulty: 'intermediate' },
        { word: 'Who', description: 'Index finger circles around lips', difficulty: 'intermediate' },
      ]
    },
    numbers: {
      title: 'Numbers',
      icon: '🔢',
      signs: [
        { word: 'One', description: 'Index finger up', difficulty: 'beginner' },
        { word: 'Two', description: 'Index and middle finger up', difficulty: 'beginner' },
        { word: 'Three', description: 'Index, middle, and ring finger up', difficulty: 'beginner' },
        { word: 'Four', description: 'All fingers except thumb up', difficulty: 'beginner' },
        { word: 'Five', description: 'All fingers up', difficulty: 'beginner' },
        { word: 'Ten', description: 'Thumbs up, shake', difficulty: 'beginner' },
      ]
    },
    actions: {
      title: 'Common Actions',
      icon: '🏃',
      signs: [
        { word: 'Help', description: 'Flat hand on opposite fist, both lift up', difficulty: 'beginner' },
        { word: 'Stop', description: 'Flat hand chops down on opposite palm', difficulty: 'beginner' },
        { word: 'Wait', description: 'Both hands wiggle fingers facing up', difficulty: 'beginner' },
        { word: 'Come', description: 'Index finger beckons toward self', difficulty: 'beginner' },
        { word: 'Go', description: 'Both hands point forward and move away', difficulty: 'beginner' },
      ]
    }
  },
  
  alphabet: [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 
    'U', 'V', 'W', 'X', 'Y', 'Z'
  ],
  
  learningPaths: [
    {
      title: 'Beginner Path',
      icon: '🌱',
      description: 'Start your sign language journey',
      lessons: [
        'Basic Greetings',
        'Yes and No',
        'Numbers 1-10',
        'Common Actions',
        'Alphabet A-M'
      ],
      duration: '2 weeks',
      difficulty: 'beginner'
    },
    {
      title: 'Intermediate Path',
      icon: '🚀',
      description: 'Build conversational skills',
      lessons: [
        'Question Words',
        'Common Phrases',
        'Full Alphabet',
        'Time and Dates',
        'Basic Sentences'
      ],
      duration: '4 weeks',
      difficulty: 'intermediate'
    },
    {
      title: 'Advanced Path',
      icon: '🏆',
      description: 'Master complex conversations',
      lessons: [
        'Complex Grammar',
        'Storytelling',
        'Regional Variations',
        'Technical Signs',
        'Poetry and Art'
      ],
      duration: '8 weeks',
      difficulty: 'advanced'
    }
  ]
}

export default function LearnPage() {
  const [selectedCategory, setSelectedCategory] = useState('greetings')
  const [selectedSign, setSelectedSign] = useState<any>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedDifficulty, setSelectedDifficulty] = useState<string | null>(null)
  const [showAlphabet, setShowAlphabet] = useState(false)
  const [selectedLetter, setSelectedLetter] = useState<string | null>(null)
  
  // Filter signs based on search and difficulty
  const getFilteredSigns = () => {
    const category = signDictionary.categories[selectedCategory as keyof typeof signDictionary.categories]
    if (!category) return []
    
    let filtered = category.signs
    
    if (searchQuery) {
      filtered = filtered.filter(sign => 
        sign.word.toLowerCase().includes(searchQuery.toLowerCase()) ||
        sign.description.toLowerCase().includes(searchQuery.toLowerCase())
      )
    }
    
    if (selectedDifficulty) {
      filtered = filtered.filter(sign => sign.difficulty === selectedDifficulty)
    }
    
    return filtered
  }
  
  const getDifficultyColor = (difficulty: string) => {
    switch(difficulty) {
      case 'beginner': return 'text-green-400 bg-green-500/20'
      case 'intermediate': return 'text-yellow-400 bg-yellow-500/20'
      case 'advanced': return 'text-red-400 bg-red-500/20'
      default: return 'text-gray-400 bg-gray-500/20'
    }
  }
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-black">
      {/* Header */}
      <header className="sticky top-0 z-50 glass border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 hover:opacity-80 transition">
            <ChevronLeft className="w-5 h-5" />
            <span className="font-semibold">Back</span>
          </Link>
          
          <div className="flex items-center gap-2">
            <GraduationCap className="w-5 h-5 text-purple-400" />
            <h1 className="text-xl font-bold gradient-text">Sign Language Academy</h1>
          </div>
          
          <div className="flex items-center gap-2">
            <Trophy className="w-5 h-5 text-yellow-400" />
            <span className="text-sm">Level 1</span>
          </div>
        </div>
      </header>
      
      {/* Hero Section */}
      <section className="relative py-12 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass mb-4"
          >
            <Sparkles className="w-4 h-4 text-yellow-400" />
            <span className="text-sm font-medium">Learn at your own pace</span>
          </motion.div>
          
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            Master <span className="gradient-text">Sign Language</span>
          </h1>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            Interactive lessons, real-time practice, and a comprehensive dictionary
          </p>
        </div>
      </section>
      
      {/* Learning Paths */}
      <section className="py-8 px-4">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
            <Target className="w-6 h-6 text-blue-400" />
            Learning Paths
          </h2>
          <div className="grid md:grid-cols-3 gap-4">
            {signDictionary.learningPaths.map((path, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.1 }}
                whileHover={{ y: -5 }}
                className="p-6 glass rounded-2xl hover:bg-white/10 transition-all cursor-pointer"
              >
                <div className="text-3xl mb-3">{path.icon}</div>
                <h3 className="text-xl font-semibold mb-2">{path.title}</h3>
                <p className="text-gray-400 text-sm mb-3">{path.description}</p>
                <div className="flex items-center justify-between text-sm">
                  <span className={`px-2 py-1 rounded-full ${getDifficultyColor(path.difficulty)}`}>
                    {path.difficulty}
                  </span>
                  <span className="text-gray-500">{path.duration}</span>
                </div>
                <div className="mt-4">
                  <div className="text-xs text-gray-500 mb-2">Includes:</div>
                  <div className="flex flex-wrap gap-1">
                    {path.lessons.slice(0, 3).map((lesson, i) => (
                      <span key={i} className="text-xs px-2 py-1 bg-white/5 rounded">
                        {lesson}
                      </span>
                    ))}
                    {path.lessons.length > 3 && (
                      <span className="text-xs px-2 py-1 text-gray-500">
                        +{path.lessons.length - 3} more
                      </span>
                    )}
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
      
      {/* Main Content */}
      <section className="py-8 px-4">
        <div className="max-w-7xl mx-auto">
          {/* Search and Filters */}
          <div className="mb-6 space-y-4">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
                <input
                  type="text"
                  placeholder="Search signs..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 glass rounded-xl bg-white/5 focus:bg-white/10 transition outline-none"
                />
              </div>
              
              <div className="flex gap-2">
                {['beginner', 'intermediate', 'advanced'].map((level) => (
                  <button
                    key={level}
                    onClick={() => setSelectedDifficulty(
                      selectedDifficulty === level ? null : level
                    )}
                    className={`px-4 py-2 rounded-lg capitalize transition ${
                      selectedDifficulty === level
                        ? getDifficultyColor(level)
                        : 'glass hover:bg-white/10'
                    }`}
                  >
                    {level}
                  </button>
                ))}
              </div>
              
              <button
                onClick={() => setShowAlphabet(!showAlphabet)}
                className={`px-4 py-2 rounded-lg flex items-center gap-2 transition ${
                  showAlphabet ? 'bg-blue-500/20 text-blue-400' : 'glass hover:bg-white/10'
                }`}
              >
                <BookOpen className="w-4 h-4" />
                Alphabet
              </button>
            </div>
          </div>
          
          {/* Alphabet Grid */}
          <AnimatePresence>
            {showAlphabet && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="mb-6"
              >
                <div className="p-6 glass rounded-2xl">
                  <h3 className="text-lg font-semibold mb-4">ASL Alphabet</h3>
                  <div className="grid grid-cols-6 md:grid-cols-13 gap-2">
                    {signDictionary.alphabet.map((letter) => (
                      <motion.button
                        key={letter}
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.9 }}
                        onClick={() => setSelectedLetter(letter)}
                        className={`aspect-square flex items-center justify-center text-xl font-bold rounded-lg transition ${
                          selectedLetter === letter
                            ? 'bg-blue-500/20 text-blue-400 border border-blue-500/50'
                            : 'glass hover:bg-white/10'
                        }`}
                      >
                        {letter}
                      </motion.button>
                    ))}
                  </div>
                  {selectedLetter && (
                    <div className="mt-4 p-4 bg-black/30 rounded-xl">
                      <p className="text-sm">
                        <span className="font-semibold">Letter {selectedLetter}:</span> 
                        <span className="ml-2 text-gray-400">
                          Practice finger spelling for the letter {selectedLetter}
                        </span>
                      </p>
                    </div>
                  )}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
          
          <div className="grid lg:grid-cols-3 gap-6">
            {/* Categories */}
            <div className="lg:col-span-1">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Book className="w-5 h-5 text-purple-400" />
                Categories
              </h3>
              <div className="space-y-2">
                {Object.entries(signDictionary.categories).map(([key, category]) => (
                  <motion.button
                    key={key}
                    whileHover={{ x: 5 }}
                    onClick={() => setSelectedCategory(key)}
                    className={`w-full text-left px-4 py-3 rounded-xl flex items-center gap-3 transition ${
                      selectedCategory === key
                        ? 'bg-gradient-to-r from-blue-600/20 to-purple-600/20 border border-blue-500/30'
                        : 'glass hover:bg-white/10'
                    }`}
                  >
                    <span className="text-2xl">{category.icon}</span>
                    <div className="flex-1">
                      <div className="font-medium">{category.title}</div>
                      <div className="text-xs text-gray-500">{category.signs.length} signs</div>
                    </div>
                    {selectedCategory === key && (
                      <ChevronRight className="w-4 h-4 text-blue-400" />
                    )}
                  </motion.button>
                ))}
              </div>
            </div>
            
            {/* Signs List */}
            <div className="lg:col-span-1">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Hand className="w-5 h-5 text-green-400" />
                Signs
              </h3>
              <div className="space-y-2 max-h-[600px] overflow-y-auto custom-scrollbar">
                {getFilteredSigns().map((sign, idx) => (
                  <motion.button
                    key={idx}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: idx * 0.05 }}
                    whileHover={{ x: 5 }}
                    onClick={() => setSelectedSign(sign)}
                    className={`w-full text-left px-4 py-3 rounded-xl transition ${
                      selectedSign?.word === sign.word
                        ? 'bg-gradient-to-r from-green-600/20 to-emerald-600/20 border border-green-500/30'
                        : 'glass hover:bg-white/10'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <div className="font-medium">{sign.word}</div>
                      <span className={`text-xs px-2 py-1 rounded-full ${
                        getDifficultyColor(sign.difficulty)
                      }`}>
                        {sign.difficulty}
                      </span>
                    </div>
                    <div className="text-xs text-gray-400 line-clamp-1">
                      {sign.description}
                    </div>
                  </motion.button>
                ))}
                
                {getFilteredSigns().length === 0 && (
                  <div className="text-center py-8 text-gray-500">
                    No signs found matching your criteria
                  </div>
                )}
              </div>
            </div>
            
            {/* Sign Detail / Practice */}
            <div className="lg:col-span-1">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Eye className="w-5 h-5 text-blue-400" />
                Practice
              </h3>
              
              {selectedSign ? (
                <motion.div
                  key={selectedSign.word}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="space-y-4"
                >
                  {/* 3D Avatar */}
                  <div className="aspect-video glass rounded-2xl overflow-hidden">
                    <Avatar3D 
                      signSequence={selectedSign.word}
                      isAnimating={true}
                    />
                  </div>
                  
                  {/* Sign Details */}
                  <div className="glass rounded-xl p-4">
                    <h4 className="text-xl font-bold mb-2">{selectedSign.word}</h4>
                    <p className="text-gray-300 mb-3">{selectedSign.description}</p>
                    
                    <div className="flex items-center gap-2 mb-3">
                      <span className={`px-3 py-1 rounded-full text-sm ${
                        getDifficultyColor(selectedSign.difficulty)
                      }`}>
                        {selectedSign.difficulty}
                      </span>
                      <button className="flex items-center gap-1 px-3 py-1 glass rounded-full text-sm hover:bg-white/10 transition">
                        <Volume2 className="w-3 h-3" />
                        Pronounce
                      </button>
                    </div>
                    
                    {/* Practice Tips */}
                    <div className="pt-3 border-t border-white/10">
                      <div className="text-sm text-gray-400 mb-2">Practice Tips:</div>
                      <ul className="text-sm space-y-1">
                        <li className="flex items-start gap-2">
                          <Star className="w-3 h-3 text-yellow-400 mt-0.5" />
                          <span className="text-gray-300">Start slowly and focus on hand shape</span>
                        </li>
                        <li className="flex items-start gap-2">
                          <Star className="w-3 h-3 text-yellow-400 mt-0.5" />
                          <span className="text-gray-300">Practice in front of a mirror</span>
                        </li>
                        <li className="flex items-start gap-2">
                          <Star className="w-3 h-3 text-yellow-400 mt-0.5" />
                          <span className="text-gray-300">Record yourself for comparison</span>
                        </li>
                      </ul>
                    </div>
                    
                    {/* Action Buttons */}
                    <div className="mt-4 flex gap-2">
                      <Link href="/translate" className="flex-1">
                        <button className="w-full px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg font-medium hover:shadow-lg hover:shadow-purple-500/25 transition">
                          Practice Now
                        </button>
                      </Link>
                      <button className="px-4 py-2 glass rounded-lg hover:bg-white/10 transition">
                        <Star className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </motion.div>
              ) : (
                <div className="aspect-video glass rounded-2xl flex flex-col items-center justify-center text-gray-500">
                  <Hand className="w-16 h-16 mb-4" />
                  <p>Select a sign to practice</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </section>
      
      {/* Community Section */}
      <section className="py-12 px-4 border-t border-white/10">
        <div className="max-w-7xl mx-auto text-center">
          <Users className="w-12 h-12 text-purple-400 mx-auto mb-4" />
          <h2 className="text-2xl font-bold mb-4">Join Our Community</h2>
          <p className="text-gray-400 mb-6 max-w-2xl mx-auto">
            Connect with learners worldwide, share experiences, and practice together
          </p>
          <button className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl font-semibold hover:shadow-2xl hover:shadow-purple-500/25 transition">
            Join Community
          </button>
        </div>
      </section>
    </div>
  )
}