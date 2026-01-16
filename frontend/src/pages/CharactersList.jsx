import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

function CharactersList() {
  const [characters, setCharacters] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [search, setSearch] = useState('')
  const [page, setPage] = useState(1)
  const [count, setCount] = useState(0)
  const [next, setNext] = useState(null)
  const [previous, setPrevious] = useState(null)

  useEffect(() => {
    fetchCharacters()
  }, [page, search])

  const fetchCharacters = async () => {
    setLoading(true)
    setError(null)
    try {
      const url = new URL('/api/characters/', window.location.origin)
      url.searchParams.append('page', page)
      if (search) {
        url.searchParams.append('search', search)
      }
      
      const response = await fetch(url)
      if (!response.ok) throw new Error('Erreur lors du chargement')
      
      const data = await response.json()
      setCharacters(data.results || [])
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

  if (loading && characters.length === 0) {
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
      <div className="mb-8">
        <h1 className="font-pirata text-5xl text-op-yellow mb-4 drop-shadow-lg">Personnages</h1>
        <input
          type="text"
          className="w-full px-6 py-4 bg-op-navy border-4 border-op-yellow rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-4 focus:ring-op-yellow focus:ring-opacity-50 text-lg"
          placeholder="🔍 Rechercher un personnage..."
          value={search}
          onChange={handleSearch}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {characters.map(character => (
          <Link 
            key={character.id} 
            to={`/characters/${character.id}`}
            className="bg-gradient-to-br from-op-navy to-op-dark border-4 border-op-yellow rounded-xl p-6 hover:scale-105 hover:shadow-2xl hover:shadow-op-yellow transition-all duration-300 transform"
          >
            <h3 className="text-2xl font-bold text-op-yellow mb-3 font-pirata">{character.name}</h3>
            {character.epithet && (
              <p className="text-op-orange italic mb-2">"{character.epithet}"</p>
            )}
            <div className="space-y-2 text-gray-300">
              <p><span className="font-semibold text-op-blue">Rôle:</span> {character.role}</p>
              {character.bounty > 0 && (
                <p className="text-op-gold font-bold">
                  💰 {character.bounty.toLocaleString()} Berries
                </p>
              )}
              {character.crews && character.crews.length > 0 && (
                <p className="text-sm">
                  <span className="font-semibold text-op-blue">Équipages:</span>{' '}
                  {character.crews.map(c => c.name).join(', ')}
                </p>
              )}
              {character.current_fruits && character.current_fruits.length > 0 && (
                <p className="text-sm">
                  <span className="font-semibold text-op-blue">Fruits:</span>{' '}
                  {character.current_fruits.map(f => f.name).join(', ')}
                </p>
              )}
            </div>
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

export default CharactersList
