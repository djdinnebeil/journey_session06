'use client'

import { useState } from 'react'
import axios from 'axios'
import toast from 'react-hot-toast'
import { 
  PaperAirplaneIcon, 
  SparklesIcon, 
  DocumentTextIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  KeyIcon
} from '@heroicons/react/24/outline'

interface PostResult {
  summary: string
  post: string
  verify_result: string
  revision_count: number
  tech_check: string
  style_check: string
}

export default function Home() {
  const [paperTitle, setPaperTitle] = useState('')
  const [apiKey, setApiKey] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<PostResult | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!paperTitle.trim()) {
      toast.error('Please enter a paper title')
      return
    }

    if (!apiKey.trim()) {
      toast.error('Please enter your OpenAI API key')
      return
    }

    setLoading(true)
    try {
      const response = await axios.post('/api/generate-post', {
        paper_title: paperTitle,
        openai_api_key: apiKey
      })
      
      setResult(response.data)
      toast.success('Post generated successfully!')
    } catch (error: any) {
      console.error('Error:', error)
      toast.error(error.response?.data?.detail || 'Failed to generate post')
    } finally {
      setLoading(false)
    }
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
    toast.success('Copied to clipboard!')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex justify-center mb-4">
            <SparklesIcon className="h-12 w-12 text-indigo-600" />
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            AI Social Media Post Generator
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Transform academic papers into engaging LinkedIn posts using advanced AI
          </p>
          <p className="text-sm text-gray-500 max-w-xl mx-auto mt-4">
            Simply enter your OpenAI API key and a paper title to get started. Your API key is only used for this request and never stored.
          </p>
        </div>

        {/* Input Form */}
        <div className="max-w-2xl mx-auto mb-8">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="apiKey" className="block text-sm font-medium text-gray-700 mb-2">
                  OpenAI API Key
                </label>
                <div className="relative">
                  <KeyIcon className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                  <input
                    type="password"
                    id="apiKey"
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                    placeholder="Enter your OpenAI API key..."
                    className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                    disabled={loading}
                  />
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  Your API key is only used for this request and is not stored anywhere.
                </p>
              </div>
              
              <div>
                <label htmlFor="paperTitle" className="block text-sm font-medium text-gray-700 mb-2">
                  Academic Paper Title
                </label>
                <div className="relative">
                  <DocumentTextIcon className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
                  <input
                    type="text"
                    id="paperTitle"
                    value={paperTitle}
                    onChange={(e) => setPaperTitle(e.target.value)}
                    placeholder="Enter the title of an academic paper..."
                    className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                    disabled={loading}
                  />
                </div>
              </div>
              
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white font-medium py-3 px-6 rounded-lg transition duration-200 flex items-center justify-center space-x-2"
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    <span>Generating...</span>
                  </>
                ) : (
                  <>
                    <PaperAirplaneIcon className="h-5 w-5" />
                    <span>Generate Post</span>
                  </>
                )}
              </button>
            </form>
          </div>
        </div>

        {/* Results */}
        {result && (
          <div className="max-w-4xl mx-auto space-y-6">
            {/* Summary */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                <DocumentTextIcon className="h-6 w-6 mr-2 text-indigo-600" />
                Generated Summary
              </h2>
              <div className="bg-gray-50 rounded-lg p-4">
                <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">{result.summary}</p>
              </div>
            </div>

            {/* Social Media Post */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                <PaperAirplaneIcon className="h-6 w-6 mr-2 text-indigo-600" />
                LinkedIn Post
              </h2>
              <div className="bg-gray-50 rounded-lg p-4 mb-4">
                <p className="text-gray-700 whitespace-pre-wrap">{result.post}</p>
              </div>
              <button
                onClick={() => copyToClipboard(result.post)}
                className="bg-indigo-100 hover:bg-indigo-200 text-indigo-700 px-4 py-2 rounded-lg transition duration-200"
              >
                Copy to Clipboard
              </button>
            </div>

            {/* Verification Status */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Quality Checks
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="flex items-center space-x-2">
                  {result.tech_check === 'pass' ? (
                    <CheckCircleIcon className="h-5 w-5 text-green-500" />
                  ) : (
                    <ExclamationTriangleIcon className="h-5 w-5 text-yellow-500" />
                  )}
                  <span className="text-sm">
                    Technical: <span className="font-medium">{result.tech_check}</span>
                  </span>
                </div>
                <div className="flex items-center space-x-2">
                  {result.style_check === 'pass' ? (
                    <CheckCircleIcon className="h-5 w-5 text-green-500" />
                  ) : (
                    <ExclamationTriangleIcon className="h-5 w-5 text-yellow-500" />
                  )}
                  <span className="text-sm">
                    Style: <span className="font-medium">{result.style_check}</span>
                  </span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="text-sm">
                    Revisions: <span className="font-medium">{result.revision_count}</span>
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
} 