'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

export default function Home() {
  const router = useRouter()

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('token')
    if (token) {
      router.push('/dashboard')
    }
  }, [router])

  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-8 bg-gray-100">
      <div className="text-center max-w-2xl">
        <h1 className="text-4xl font-bold mb-4 text-gray-900">Welcome to FluxPad 📊</h1>
        <p className="text-lg text-gray-600 mb-8">
          A lightweight, full-stack web application for intelligent data interaction through LLM-powered agents
        </p>
        
        <div className="space-x-4">
          <Link
            href="/login"
            className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg transition-colors"
          >
            Sign In
          </Link>
          <Link
            href="/register"
            className="inline-block bg-gray-600 hover:bg-gray-700 text-white font-medium py-2 px-6 rounded-lg transition-colors"
          >
            Get Started
          </Link>
        </div>

        <div className="mt-12 p-6 bg-white rounded-lg shadow-sm border">
          <h3 className="text-lg font-semibold mb-3 text-gray-900">Key Features</h3>
          <ul className="text-sm text-gray-600 space-y-2">
            <li>📤 Upload and manage CSV/Excel files</li>
            <li>🔍 Query your data with natural language</li>
            <li>🤖 AI-powered insights and analysis</li>
            <li>🎨 Modern, responsive interface</li>
          </ul>
        </div>
      </div>
    </main>
  )
}
