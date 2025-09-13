import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

// API Base URL (configurable via Vite env: VITE_API_BASE)
const API_BASE_URL = (import.meta as any).env?.VITE_API_BASE || 'http://127.0.0.1:8000'

// Configure axios instance
axios.defaults.baseURL = API_BASE_URL
axios.defaults.timeout = 20000

// Types
interface AnalysisResult {
  keyword: string
  search_intent: string
  related_keywords: string[]
  content_opportunities: string[]
  user_questions: string[]
  wikipedia_sources: Array<{
    title: string
    url: string
    relevance_score: number
  }>
}

interface ContentBrief {
  title: string
  meta_description: string
  content_type: string
  word_count_target: number
  outline: string[]
  call_to_action: string
  created_at: string
}

/*
interface Task {
  task_id: string
  status: string
  progress: number
  message: string
  result?: any
  error?: string
}
*/

function App() {
  const [activeTab, setActiveTab] = useState('analysis')
  const [keyword, setKeyword] = useState('')
  const [goal, setGoal] = useState('')
  const [loading, setLoading] = useState(false)
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null)
  const [brief, setBrief] = useState<ContentBrief | null>(null)
  // const [task, setTask] = useState<Task | null>(null)
  const [error, setError] = useState('')

  // Auth state
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'))
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const isAuthed = Boolean(token)

  // Attach token to axios default headers when it changes
  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    } else {
      delete axios.defaults.headers.common['Authorization']
    }
  }, [token])

  // Keywords for bulk processing
  // const [bulkKeywords, setBulkKeywords] = useState('')
  // const [bulkResults, setBulkResults] = useState<any>(null)

  // Calendar keywords
  // const [calendarKeywords, setCalendarKeywords] = useState('')
  // const [calendarWeeks, setCalendarWeeks] = useState(4)
  // const [calendar, setCalendar] = useState<any>(null)

  const handleAnalysis = async () => {
    if (!keyword.trim()) return
    
    setLoading(true)
    setError('')
    try {
      const response = await axios.post(`${API_BASE_URL}/seo/analyze`, {
        keyword: keyword.trim(),
        goal: goal.trim()
      })
      setAnalysis(response.data)
    } catch (err: any) {
      // 401 means not authenticated
      if (err.response?.status === 401) {
        setError('Not authenticated. Please log in first.')
      } else {
        setError(err.response?.data?.detail || 'Analysis failed')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleBrief = async () => {
    if (!keyword.trim()) return
    
    setLoading(true)
    setError('')
    try {
      const response = await axios.post(`${API_BASE_URL}/seo/brief`, {
        keyword: keyword.trim(),
        goal: goal.trim()
      })
      setBrief(response.data)
    } catch (err: any) {
      if (err.response?.status === 401) {
        setError('Not authenticated. Please log in first.')
      } else {
        setError(err.response?.data?.detail || 'Brief generation failed')
      }
    } finally {
      setLoading(false)
    }
  }

  /*
  const handleArticle = async () => {
    if (!keyword.trim()) return
    
    setLoading(true)
    setError('')
    try {
      const response = await axios.post(`${API_BASE_URL}/seo/article`, {
        keyword: keyword.trim(),
        goal: goal.trim()
      })
      setTask({
        task_id: response.data.task_id,
        status: 'processing',
        progress: 0,
        message: response.data.message
      })
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Article generation failed')
    } finally {
      setLoading(false)
    }
  }

  const checkTaskStatus = async () => {
    if (!task?.task_id) return
    
    try {
      const response = await axios.get(`${API_BASE_URL}/tasks/${task.task_id}`)
      setTask(response.data)
    } catch (err: any) {
      setError('Failed to check task status')
    }
  }

  const handleBulkProcess = async () => {
    const keywords = bulkKeywords.split('\n').filter(k => k.trim())
    if (keywords.length === 0) return
    
    setLoading(true)
    setError('')
    try {
      const response = await axios.post(`${API_BASE_URL}/seo/bulk`, {
        keywords: keywords.map(k => k.trim()),
        goal: goal.trim()
      })
      setBulkResults(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Bulk processing failed')
    } finally {
      setLoading(false)
    }
  }

  const handleCalendar = async () => {
    const keywords = calendarKeywords.split('\n').filter(k => k.trim())
    if (keywords.length === 0) return
    
    setLoading(true)
    setError('')
    try {
      const response = await axios.post(`${API_BASE_URL}/seo/calendar`, {
        keywords: keywords.map(k => k.trim()),
        goal: goal.trim(),
        timeframe_weeks: calendarWeeks
      })
      setCalendar(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Calendar creation failed')
    } finally {
      setLoading(false)
    }
  }
  */

  const handleLogin = async () => {
    setError('')
    if (!email.trim() || !password.trim()) {
      setError('Email and password are required')
      return
    }
    try {
      const res = await axios.post(`/auth/login`, { email, password })
      setToken(res.data.access_token)
      localStorage.setItem('token', res.data.access_token)
    } catch (err: any) {
      const msg = err?.response?.data?.detail || err?.message || 'Login failed'
      setError(String(msg))
    }
  }

  const handleRegister = async () => {
    setError('')
    if (!email.trim() || !password.trim()) {
      setError('Email and password are required')
      return
    }
    if (password.length < 8) {
      setError('Password must be at least 8 characters')
      return
    }
    try {
      await axios.post(`/auth/register`, { email, password, full_name: email.split('@')[0] || 'User' })
      await handleLogin()
    } catch (err: any) {
      const msg = err?.response?.data?.detail || err?.message || 'Registration failed'
      setError(String(msg))
    }
  }

  const handleLogout = () => {
    setToken(null)
    localStorage.removeItem('token')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b w-full">
        <div className="w-full px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">🚀 Smart SEO Assistant</h1>
          <p className="text-gray-600 mt-2">AI-powered SEO content planning and generation</p>
        </div>
      </header>

      {/* Main Content */}
  <main className="w-full mx-auto px-4 py-8">
        {/* Auth Bar */}
        <div className="bg-white rounded-lg p-4 mb-6 shadow-sm flex flex-col md:flex-row md:items-end gap-3">
          <div className="text-sm text-gray-600 flex-1">{isAuthed ? 'Authenticated' : 'Not authenticated'}</div>
          {!isAuthed ? (
            <div className="flex flex-col md:flex-row gap-3 w-full md:w-auto">
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Email"
                className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
                className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <div className="flex gap-2">
                <button onClick={handleLogin} className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">Log in</button>
                <button onClick={handleRegister} className="bg-gray-700 text-white px-4 py-2 rounded-lg hover:bg-gray-800">Register</button>
              </div>
            </div>
          ) : (
            <div className="flex gap-2">
              <button onClick={handleLogout} className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600">Log out</button>
            </div>
          )}
        </div>
        {/* Tab Navigation */}
        <div className="mb-8">
          <nav className="flex space-x-8">
            {[
              { id: 'analysis', label: '🔍 Analysis' },
              { id: 'brief', label: '📝 Content Brief' },
              { id: 'article', label: '📄 Full Article' },
              { id: 'bulk', label: '📊 Bulk Process' },
              { id: 'calendar', label: '📅 Content Calendar' }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  activeTab === tab.id
                    ? 'bg-blue-500 text-white'
                    : 'bg-white text-gray-700 hover:bg-gray-50'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Common Input Fields */}
        <div className="bg-white rounded-lg p-6 mb-6 shadow-sm">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Keyword
              </label>
              <input
                type="text"
                value={keyword}
                onChange={(e) => setKeyword(e.target.value)}
                placeholder="Enter your target keyword..."
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Goal (Optional)
              </label>
              <input
                type="text"
                value={goal}
                onChange={(e) => setGoal(e.target.value)}
                placeholder="Describe your content goal..."
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <p className="text-red-800">{error}</p>
          </div>
        )}

        {/* Tab Content */}
        {activeTab === 'analysis' && (
          <div className="bg-white rounded-lg p-6 shadow-sm">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold">Keyword Analysis</h2>
              <button
                onClick={handleAnalysis}
                disabled={loading || !keyword.trim()}
                className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 disabled:opacity-50"
              >
                {loading ? 'Analyzing...' : 'Analyze Keyword'}
              </button>
            </div>

            {analysis && (
              <div className="space-y-6">
                <div>
                  <h3 className="font-medium text-gray-900 mb-2">Search Intent</h3>
                  <p className="text-gray-700 bg-gray-50 p-3 rounded">{analysis.search_intent}</p>
                </div>

                <div>
                  <h3 className="font-medium text-gray-900 mb-2">Related Keywords</h3>
                  <div className="flex flex-wrap gap-2">
                    {analysis.related_keywords.map((kw, idx) => (
                      <span key={idx} className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                        {kw}
                      </span>
                    ))}
                  </div>
                </div>

                <div>
                  <h3 className="font-medium text-gray-900 mb-2">Content Opportunities</h3>
                  <ul className="list-disc list-inside space-y-1">
                    {analysis.content_opportunities.map((opp, idx) => (
                      <li key={idx} className="text-gray-700">{opp}</li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h3 className="font-medium text-gray-900 mb-2">User Questions</h3>
                  <ul className="list-disc list-inside space-y-1">
                    {analysis.user_questions.map((q, idx) => (
                      <li key={idx} className="text-gray-700">{q}</li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h3 className="font-medium text-gray-900 mb-2">Wikipedia Sources</h3>
                  <div className="space-y-2">
                    {analysis.wikipedia_sources.map((source, idx) => (
                      <div key={idx} className="border border-gray-200 rounded p-3">
                        <a href={source.url} target="_blank" rel="noopener noreferrer" 
                           className="text-blue-600 hover:text-blue-800 font-medium">
                          {source.title}
                        </a>
                        <p className="text-sm text-gray-500">Relevance: {(source.relevance_score * 100).toFixed(1)}%</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Additional tabs content would go here... */}
        {activeTab === 'brief' && (
          <div className="bg-white rounded-lg p-6 shadow-sm">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold">Content Brief</h2>
              <button
                onClick={handleBrief}
                disabled={loading || !keyword.trim()}
                className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 disabled:opacity-50"
              >
                {loading ? 'Generating...' : 'Generate Brief'}
              </button>
            </div>

            {brief && (
              <div className="space-y-4">
                <div>
                  <h3 className="font-medium text-gray-900">Title</h3>
                  <p className="text-lg text-gray-800 mt-1">{brief.title}</p>
                </div>

                <div>
                  <h3 className="font-medium text-gray-900">Meta Description</h3>
                  <p className="text-gray-700 bg-gray-50 p-3 rounded">{brief.meta_description}</p>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <h3 className="font-medium text-gray-900">Content Type</h3>
                    <p className="text-gray-700">{brief.content_type}</p>
                  </div>
                  <div>
                    <h3 className="font-medium text-gray-900">Target Word Count</h3>
                    <p className="text-gray-700">{brief.word_count_target} words</p>
                  </div>
                </div>

                <div>
                  <h3 className="font-medium text-gray-900">Content Outline</h3>
                  <ol className="list-decimal list-inside space-y-2 mt-2">
                    {brief.outline.map((item, idx) => (
                      <li key={idx} className="text-gray-700">{item}</li>
                    ))}
                  </ol>
                </div>

                <div>
                  <h3 className="font-medium text-gray-900">Call to Action</h3>
                  <p className="text-gray-700 bg-yellow-50 p-3 rounded">{brief.call_to_action}</p>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Placeholder for other tabs */}
        {activeTab === 'article' && (
          <div className="bg-white rounded-lg p-6 shadow-sm">
            <h2 className="text-xl font-semibold mb-4">Full Article Generation</h2>
            <p className="text-gray-600">Article generation functionality coming soon...</p>
          </div>
        )}

        {activeTab === 'bulk' && (
          <div className="bg-white rounded-lg p-6 shadow-sm">
            <h2 className="text-xl font-semibold mb-4">Bulk Processing</h2>
            <p className="text-gray-600">Bulk processing functionality coming soon...</p>
          </div>
        )}

        {activeTab === 'calendar' && (
          <div className="bg-white rounded-lg p-6 shadow-sm">
            <h2 className="text-xl font-semibold mb-4">Content Calendar</h2>
            <p className="text-gray-600">Content calendar functionality coming soon...</p>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
