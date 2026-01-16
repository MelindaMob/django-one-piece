import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

function CrewsList() {
  const [crews, setCrews] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [page, setPage] = useState(1)
  const [count, setCount] = useState(0)
  const [next, setNext] = useState(null)
  const [previous, setPrevious] = useState(null)

  useEffect(() => {
    fetchCrews()
  }, [page])

  const fetchCrews = async () => {
    setLoading(true)
    setError(null)
    try {
      const url = new URL('/api/crews/', window.location.origin)
      url.searchParams.append('page', page)
      
      const response = await fetch(url)
      if (!response.ok) throw new Error('Erreur lors du chargement')
      
      const data = await response.json()
      setCrews(data.results || [])
      setCount(data.count || 0)
      setNext(data.next)
      setPrevious(data.previous)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  if (loading && crews.length === 0) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <p className="text-op-red text-xl font-semibold">Chargement...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-100 border-2 border-red-500 text-red-800 p-6 rounded-lg">
        <p className="text-xl font-bold">Erreur: {error}</p>
      </div>
    )
  }

  return (
    <div>
      <h1 className="text-4xl font-bold text-op-red mb-8">Équipages</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {crews.map(crew => (
          <Link
            key={crew.id}
            to={`/crews/${crew.id}`}
            className="bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow p-6 border-2 border-transparent hover:border-op-red"
          >
            <h3 className="text-2xl font-bold text-op-red mb-3">{crew.name}</h3>
            {crew.ship_name && (
              <p className="text-gray-700 mb-2">
                <span className="font-semibold">🚢 Navire:</span> {crew.ship_name}
              </p>
            )}
            {crew.base_location && (
              <p className="text-gray-700">
                <span className="font-semibold">📍 Base:</span> {crew.base_location}
              </p>
            )}
          </Link>
        ))}
      </div>

      <div className="flex justify-center items-center gap-4 mt-8">
        <button
          onClick={() => setPage(p => Math.max(1, p - 1))}
          disabled={!previous}
          className="px-6 py-2 bg-op-red text-white font-semibold rounded hover:bg-op-red-dark disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Précédent
        </button>
        <span className="text-gray-700 font-semibold">
          Page {page} sur {Math.ceil(count / 10)}
        </span>
        <button
          onClick={() => setPage(p => p + 1)}
          disabled={!next}
          className="px-6 py-2 bg-op-red text-white font-semibold rounded hover:bg-op-red-dark disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Suivant
        </button>
      </div>
    </div>
  )
}

export default CrewsList
