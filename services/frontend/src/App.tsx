import { useEffect, useState } from 'react'
import type { FormEvent } from 'react'
import './App.css'

type Note = { id: number; title: string; body: string; created_at: string }

// Relative URL on purpose: no host, no port, no CORS. The dev proxy (Vite) or nginx
// (container) routes /api to the API service.
const API = '/api'

export default function App() {
  const [notes, setNotes] = useState<Note[]>([])
  const [title, setTitle] = useState('')
  const [body, setBody] = useState('')
  const [error, setError] = useState('')
  const [reload, setReload] = useState(0)

  // Re-fetch whenever `reload` changes. State is set inside the promise callbacks,
  // never synchronously in the effect body, which is what React expects.
  useEffect(() => {
    let cancelled = false
    fetch(`${API}/notes`)
      .then((res) => {
        if (!res.ok) throw new Error(`GET /api/notes returned ${res.status}`)
        return res.json() as Promise<Note[]>
      })
      .then((data) => {
        if (cancelled) return
        setNotes(data)
        setError('')
      })
      .catch((e) => {
        if (!cancelled) setError(String(e))
      })
    return () => {
      cancelled = true
    }
  }, [reload])

  async function add(e: FormEvent) {
    e.preventDefault()
    try {
      const res = await fetch(`${API}/notes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, body }),
      })
      if (!res.ok) throw new Error(`POST /api/notes returned ${res.status}`)
      setTitle('')
      setBody('')
      setReload((n) => n + 1)
    } catch (e) {
      setError(String(e))
    }
  }

  return (
    <main className="notes">
      <h1>Notes</h1>
      {error && <p className="error">{error}</p>}
      <form onSubmit={add}>
        <input placeholder="Title" value={title} onChange={(e) => setTitle(e.target.value)} required />
        <input placeholder="Body" value={body} onChange={(e) => setBody(e.target.value)} required />
        <button type="submit">Add</button>
      </form>
      <ul>
        {notes.map((n) => (
          <li key={n.id}>
            <b>{n.title}</b>: {n.body}
          </li>
        ))}
      </ul>
    </main>
  )
}
