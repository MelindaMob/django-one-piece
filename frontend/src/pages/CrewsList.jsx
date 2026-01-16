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
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-op-yellow mx-auto mb-4"></div>
          <p className="text-op-yellow text-xl font-semibold">Chargement...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-900 border-4 border-op-red text-white p-6 rounded-lg shadow-2xl">
        <p className="text-xl font-bold">Erreur: {error}</p>
      </div>
    )
  }

  return (
    <div>
      <h1 className="font-pirata text-5xl text-op-yellow mb-8 drop-shadow-lg">Équipages</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {crews.map(crew => (
          <Link
            key={crew.id}
            to={`/crews/${crew.id}`}
            className="bg-gradient-to-br from-op-navy to-op-dark border-4 border-op-red rounded-xl p-6 hover:scale-105 hover:shadow-2xl hover:shadow-op-red transition-all duration-300 transform"
          >
            <h3 className="text-2xl font-bold text-op-yellow mb-3 font-pirata">{crew.name}</h3>
            {crew.ship_name && (
              <p className="text-gray-300 mb-2">
                <span className="text-op-blue font-semibold">🚢 Navire:</span> {crew.ship_name}
              </p>
            )}
            {crew.base_location && (
              <p className="text-gray-300">
                <span className="text-op-blue font-semibold">📍 Base:</span> {crew.base_location}
              </p>
            )}
          </Link>
        ))}
      </div>

      <div className="flex justify-center items-center gap-4 mt-8">
        <button
          onClick={() => setPage(p => Math.max(1, p - 1))}
          disabled={!previous}
          className="px-6 py-3 bg-op-red text-white font-bold rounded-lg hover:bg-opacity-80 disabled:opacity-50 disabled:cursor-not-allowed transition-all border-2 border-op-yellow"
        >
          Précédent
        </button>
        <span className="text-op-yellow font-bold text-lg">
          Page {page} sur {Math.ceil(count / 10)}
        </span>
        <button
          onClick={() => setPage(p => p + 1)}
          disabled={!next}
          className="px-6 py-3 bg-op-red text-white font-bold rounded-lg hover:bg-opacity-80 disabled:opacity-50 disabled:cursor-not-allowed transition-all border-2 border-op-yellow"
        >
          Suivant
        </button>
      </div>
    </div>
  )
}

export default CrewsList
