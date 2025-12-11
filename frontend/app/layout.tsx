import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'SilentVoice | Breaking Communication Barriers',
  description: 'Real-time bidirectional sign language translator with 3D avatar rendering',
  keywords: 'sign language, translator, AI, real-time, accessibility',
  authors: [{ name: 'SilentVoice Team' }],
  openGraph: {
    title: 'SilentVoice',
    description: 'Breaking communication barriers with AI-powered sign language translation',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} bg-gradient-to-br from-gray-950 via-gray-900 to-black text-white min-h-screen`}>
        <div className="fixed inset-0 bg-[url('/grid.svg')] bg-center [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))]"></div>
        <div className="relative z-10">
          {children}
        </div>
      </body>
    </html>
  )
}