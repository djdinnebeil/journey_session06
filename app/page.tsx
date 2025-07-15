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
  KeyIcon,
  CpuChipIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline'

interface PostResult {
  summary: string
  post: string
  verify_result: string
  revision_count: number
  tech_check: string
  style_check: string
  // New supervisor pattern fields
  supervisor_insights?: {
    completed_steps?: string[]
    workflow_efficiency?: number
    completion_reason?: string
    revision_efficiency?: number
    verification_details?: any
    workflow_type?: string
  }
  workflow_pattern?: string
  quality_metrics?: {
    post_length?: number
    summary_length?: number
    character_efficiency?: number
    mention_compliance?: boolean
    technical_accuracy?: boolean
    style_compliance?: boolean
    overall_quality?: number
  }
}

// Simple markdown renderer for basic formatting
const renderMarkdown = (text: string): string => {
  return text
    // Bold text: **text** -> <strong>text</strong>
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    // Italic text: *text* -> <em>text</em>
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    // Links: [text](url) -> <a href="url">text</a>
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer" class="text-blue-600 underline">$1</a>')
    // Line breaks
    .replace(/\n/g, '<br />')
}

export default function Home() {
  const [paperTitle, setPaperTitle] = useState('')
  const [apiKey, setApiKey] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<PostResult | null>(null)
  const [useSupervisor, setUseSupervisor] = useState(true)

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
        openai_api_key: apiKey,
        use_supervisor: useSupervisor
      })
      
      setResult(response.data)
      toast.success('Post generated successfully!')
    } catch (error: any) {
      console.error('Error:', error)
      toast.error(error.response?.data?.detail || 'Failed to generate post')
      setResult(null) // Clear any previous results on error
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
            AI Social Media Post Generator v2.0
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Transform academic papers into engaging LinkedIn posts using advanced AI with Supervisor Pattern
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

              {/* Workflow Pattern Selection */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Workflow Pattern
                </label>
                <div className="flex space-x-4">
                  <label className="flex items-center">
                    <input
                      type="radio"
                      name="workflow"
                      checked={useSupervisor}
                      onChange={() => setUseSupervisor(true)}
                      className="mr-2"
                      disabled={loading}
                    />
                    <CpuChipIcon className="h-4 w-4 mr-1 text-indigo-600" />
                    <span className="text-sm">Supervisor Pattern (Recommended)</span>
                  </label>
                  <label className="flex items-center">
                    <input
                      type="radio"
                      name="workflow"
                      checked={!useSupervisor}
                      onChange={() => setUseSupervisor(false)}
                      className="mr-2"
                      disabled={loading}
                    />
                    <span className="text-sm">Linear Pattern</span>
                  </label>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  {useSupervisor 
                    ? "AI supervisor coordinates agents for optimal quality and intelligent routing"
                    : "Simple linear workflow with predictable execution order"
                  }
                </p>
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
                <div 
                  className="text-gray-700 leading-relaxed"
                  dangerouslySetInnerHTML={{ __html: renderMarkdown(result.summary) }}
                />
              </div>
            </div>

            {/* Social Media Post */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                <PaperAirplaneIcon className="h-6 w-6 mr-2 text-indigo-600" />
                LinkedIn Post
              </h2>
              <div className="bg-gray-50 rounded-lg p-4 mb-4">
                <div 
                  className="text-gray-700"
                  dangerouslySetInnerHTML={{ __html: renderMarkdown(result.post) }}
                />
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

            {/* Workflow Info - Moved to bottom */}
            {result.workflow_pattern && (
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                  <CpuChipIcon className="h-6 w-6 mr-2 text-indigo-600" />
                  Workflow: {result.workflow_pattern === 'supervised' ? 'Supervisor Pattern' : 'Linear Pattern'}
                </h2>
                
                {/* Workflow Insights */}
                {result.supervisor_insights && (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <div className="bg-blue-50 rounded-lg p-4">
                      <h3 className="font-medium text-blue-900 mb-2">Workflow Progress</h3>
                      <div className="space-y-1">
                        {result.supervisor_insights.completed_steps?.map((step, index) => (
                          <div key={index} className="flex items-center text-sm text-blue-700">
                            <CheckCircleIcon className="h-4 w-4 mr-2 text-green-500" />
                            {step}
                          </div>
                        ))}
                      </div>
                    </div>
                    
                    <div className="bg-green-50 rounded-lg p-4">
                      <h3 className="font-medium text-green-900 mb-2">
                        {result.workflow_pattern === 'supervised' ? 'Efficiency Metrics' : 'Linear Workflow Metrics'}
                      </h3>
                      <div className="space-y-1 text-sm text-green-700">
                        {result.supervisor_insights.workflow_efficiency && (
                          <div>
                            {result.workflow_pattern === 'supervised' ? 'Workflow' : 'Completion'}: {(result.supervisor_insights.workflow_efficiency * 100).toFixed(0)}%
                          </div>
                        )}
                        {result.supervisor_insights.completion_reason && (
                          <div>Reason: {result.supervisor_insights.completion_reason.replace(/_/g, ' ')}</div>
                        )}
                        {result.supervisor_insights.workflow_type && (
                          <div>Type: {result.supervisor_insights.workflow_type.replace(/_/g, ' ')}</div>
                        )}
                        {result.supervisor_insights.revision_efficiency && (
                          <div>
                            {result.workflow_pattern === 'supervised' ? 'Revision Efficiency' : 'Revision Rate'}: {(result.supervisor_insights.revision_efficiency * 100).toFixed(0)}%
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                )}

                {/* Quality Metrics */}
                {result.quality_metrics && (
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h3 className="font-medium text-gray-900 mb-2 flex items-center">
                      <ChartBarIcon className="h-4 w-4 mr-2" />
                      Quality Metrics
                    </h3>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      {result.quality_metrics.overall_quality !== undefined && (
                        <div className="text-center">
                          <div className="font-semibold text-lg text-indigo-600">
                            {(result.quality_metrics.overall_quality * 100).toFixed(0)}%
                          </div>
                          <div className="text-gray-600">Overall Quality</div>
                        </div>
                      )}
                      {result.quality_metrics.character_efficiency !== undefined && (
                        <div className="text-center">
                          <div className="font-semibold text-lg text-blue-600">
                            {(result.quality_metrics.character_efficiency * 100).toFixed(0)}%
                          </div>
                          <div className="text-gray-600">Char Efficiency</div>
                        </div>
                      )}
                      {result.quality_metrics.mention_compliance !== undefined && (
                        <div className="text-center">
                          <div className={`font-semibold text-lg ${result.quality_metrics.mention_compliance ? 'text-green-600' : 'text-red-600'}`}>
                            {result.quality_metrics.mention_compliance ? '✓' : '✗'}
                          </div>
                          <div className="text-gray-600">@AIMakerspace</div>
                        </div>
                      )}
                      {result.quality_metrics.post_length && (
                        <div className="text-center">
                          <div className="font-semibold text-lg text-purple-600">
                            {result.quality_metrics.post_length}
                          </div>
                          <div className="text-gray-600">Characters</div>
                        </div>
                      )}
                    </div>
                    
                    {/* Additional metrics row for detailed breakdown */}
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm mt-4 pt-4 border-t border-gray-200">
                      {result.quality_metrics.technical_accuracy !== undefined && (
                        <div className="text-center">
                          <div className={`font-semibold text-lg ${result.quality_metrics.technical_accuracy ? 'text-green-600' : 'text-red-600'}`}>
                            {result.quality_metrics.technical_accuracy ? '✓' : '✗'}
                          </div>
                          <div className="text-gray-600">Technical Accuracy</div>
                        </div>
                      )}
                      {result.quality_metrics.style_compliance !== undefined && (
                        <div className="text-center">
                          <div className={`font-semibold text-lg ${result.quality_metrics.style_compliance ? 'text-green-600' : 'text-red-600'}`}>
                            {result.quality_metrics.style_compliance ? '✓' : '✗'}
                          </div>
                          <div className="text-gray-600">Style Compliance</div>
                        </div>
                      )}
                      {result.quality_metrics.summary_length && (
                        <div className="text-center">
                          <div className="font-semibold text-lg text-gray-600">
                            {result.quality_metrics.summary_length}
                          </div>
                          <div className="text-gray-600">Summary Length</div>
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
} 