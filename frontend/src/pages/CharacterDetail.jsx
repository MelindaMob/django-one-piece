import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'

function CharacterDetail() {
  const { id } = useParams()
  const [character, setCharacter] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchCharacter()
  }, [id])

  const fetchCharacter = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`/api/characters/${id}/`)
      if (!response.ok) throw new Error('Personnage non trouvé')
      const data = await response.json()
      setCharacter(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
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

  if (!character) return null

  return (
    <div>
      <Link 
        to="/characters" 
        className="inline-flex items-center text-op-red hover:underline mb-6"
      >
        <span className="mr-2">←</span> Retour à la liste
      </Link>
      
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-4xl font-bold text-op-red mb-2">{character.name}</h1>
        {character.epithet && (
          <p className="text-2xl text-gray-600 italic mb-6">"{character.epithet}"</p>
        )}
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="bg-op-gray rounded-lg p-4">
            <p className="text-gray-600 font-semibold mb-2">Rôle</p>
            <p className="text-xl">{character.role}</p>
          </div>
          <div className="bg-op-gray rounded-lg p-4">
            <p className="text-gray-600 font-semibold mb-2">Prime</p>
            <p className="text-xl font-bold text-op-red">
              {character.bounty > 0 ? `${character.bounty.toLocaleString()} Berries` : 'Aucune'}
            </p>
          </div>
          <div className="bg-op-gray rounded-lg p-4">
            <p className="text-gray-600 font-semibold mb-2">Origine</p>
            <p className="text-xl">{character.origin || 'N/A'}</p>
          </div>
          <div className="bg-op-gray rounded-lg p-4">
            <p className="text-gray-600 font-semibold mb-2">Statut</p>
            <p className="text-xl">{character.status}</p>
          </div>
        </div>

        {character.description && (
          <div className="mb-8 bg-op-gray rounded-lg p-6">
            <h2 className="text-2xl font-bold text-op-red mb-4">Description</h2>
            <p className="text-gray-700 leading-relaxed">{character.description}</p>
          </div>
        )}

        {character.crews && character.crews.length > 0 && (
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-op-red mb-4">Équipages</h2>
            <div className="flex flex-wrap gap-3">
              {character.crews.map(crew => (
                <Link
                  key={crew.id}
                  to={`/crews/${crew.id}`}
                  className="px-4 py-2 bg-op-red text-white rounded hover:bg-op-red-dark transition-colors"
                >
                  {crew.name}
                </Link>
              ))}
            </div>
          </div>
        )}

        {character.fruits_history && character.fruits_history.length > 0 && (
          <div>
            <h2 className="text-2xl font-bold text-op-red mb-4">Fruits du Démon</h2>
            <div className="space-y-4">
              {character.fruits_history.map(holder => (
                <div
                  key={holder.id}
                  className="bg-op-gray rounded-lg p-6"
                >
                  <Link
                    to={`/fruits/${holder.devil_fruit.id}`}
                    className="text-xl font-bold text-op-red hover:underline"
                  >
                    {holder.devil_fruit.name}
                  </Link>
                  <p className="text-gray-600 mt-2">{holder.devil_fruit.fruit_type}</p>
                  {holder.is_current && (
                    <span className="inline-block mt-2 px-3 py-1 bg-green-500 text-white rounded text-sm font-bold">
                      Actuel
                    </span>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default CharacterDetail
