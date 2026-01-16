import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

function FruitsList() {
  const [fruits, setFruits] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [search, setSearch] = useState('')
  const [page, setPage] = useState(1)
  const [count, setCount] = useState(0)
  const [next, setNext] = useState(null)
  const [previous, setPrevious] = useState(null)

  useEffect(() => {
    fetchFruits()
  }, [page, search])

  const fetchFruits = async () => {
    setLoading(true)
    setError(null)
    try {
      const url = new URL('/api/fruits/', window.location.origin)
      url.searchParams.append('page', page)
      if (search) {
        url.searchParams.append('search', search)
      }

      const response = await fetch(url)
      if (!response.ok) throw new Error('Erreur lors du chargement')

      const data = await response.json()
      setFruits(data.results || [])
      setCount(data.count || 0)
      setNext(data.next)
      setPrevious(data.previous)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (e) => {
    setSearch(e.target.value)
    setPage(1)
  }

  if (loading && fruits.length === 0) {
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
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-op-red mb-6">Fruits du Démon</h1>
        <input
          type="text"
          className="w-full px-6 py-3 bg-white border-2 border-gray-300 rounded-lg focus:outline-none focus:border-op-red text-lg"
          placeholder="🔍 Rechercher un fruit..."
          value={search}
          onChange={handleSearch}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {fruits.map(fruit => (
          <Link
            key={fruit.id}
            to={`/fruits/${fruit.id}`}
            className="bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow p-6 border-2 border-transparent hover:border-op-red"
          >
            <h3 className="text-2xl font-bold text-op-red mb-3">{fruit.name}</h3>
            {fruit.romanji && (
              <p className="text-gray-600 italic mb-2">{fruit.romanji}</p>
            )}
            <div className="space-y-2 text-gray-700">
              <p>
                <span className="font-semibold">Type:</span> {fruit.fruit_type}
              </p>
              <p className="text-op-red font-bold">
                ⭐ Rareté: {fruit.rarity}/5
              </p>
            </div>
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

export default FruitsList
