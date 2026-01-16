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

  if (!character) return null

  return (
    <div>
      <Link 
        to="/characters" 
        className="inline-flex items-center text-op-yellow hover:text-op-orange mb-6 transition-colors"
      >
        <span className="mr-2">←</span> Retour à la liste
      </Link>
      
      <div className="bg-gradient-to-br from-op-navy to-op-dark border-4 border-op-yellow rounded-xl p-8 shadow-2xl">
        <h1 className="font-pirata text-5xl text-op-yellow mb-2">{character.name}</h1>
        {character.epithet && (
          <p className="text-2xl text-op-orange italic mb-6">"{character.epithet}"</p>
        )}
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="bg-op-dark rounded-lg p-4 border-2 border-op-blue">
            <p className="text-op-blue font-bold mb-2">Rôle</p>
            <p className="text-white">{character.role}</p>
          </div>
          <div className="bg-op-dark rounded-lg p-4 border-2 border-op-gold">
            <p className="text-op-gold font-bold mb-2">Prime</p>
            <p className="text-white text-2xl font-bold">
              {character.bounty > 0 ? `${character.bounty.toLocaleString()} Berries` : 'Aucune'}
            </p>
          </div>
          <div className="bg-op-dark rounded-lg p-4 border-2 border-op-blue">
            <p className="text-op-blue font-bold mb-2">Origine</p>
            <p className="text-white">{character.origin || 'N/A'}</p>
          </div>
          <div className="bg-op-dark rounded-lg p-4 border-2 border-op-blue">
            <p className="text-op-blue font-bold mb-2">Statut</p>
            <p className="text-white">{character.status}</p>
          </div>
        </div>

        {character.description && (
          <div className="mb-8 bg-op-dark rounded-lg p-6 border-2 border-op-blue">
            <h2 className="text-2xl font-bold text-op-yellow mb-4 font-pirata">Description</h2>
            <p className="text-gray-300 leading-relaxed">{character.description}</p>
          </div>
        )}

        {character.crews && character.crews.length > 0 && (
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-op-yellow mb-4 font-pirata">Équipages</h2>
            <div className="flex flex-wrap gap-3">
              {character.crews.map(crew => (
                <Link
                  key={crew.id}
                  to={`/crews/${crew.id}`}
                  className="px-4 py-2 bg-op-red text-white rounded-lg hover:bg-opacity-80 transition-all border-2 border-op-yellow"
                >
                  {crew.name}
                </Link>
              ))}
            </div>
          </div>
        )}

        {character.fruits_history && character.fruits_history.length > 0 && (
          <div>
            <h2 className="text-3xl font-bold text-op-yellow mb-4 font-pirata">Fruits du Démon</h2>
            <div className="space-y-4">
              {character.fruits_history.map(holder => (
                <div
                  key={holder.id}
                  className="bg-op-dark rounded-lg p-6 border-2 border-op-orange"
                >
                  <Link
                    to={`/fruits/${holder.devil_fruit.id}`}
                    className="text-2xl font-bold text-op-orange hover:text-op-yellow transition-colors"
                  >
                    {holder.devil_fruit.name}
                  </Link>
                  <p className="text-gray-400 mt-2">{holder.devil_fruit.fruit_type}</p>
                  {holder.is_current && (
                    <span className="inline-block mt-2 px-3 py-1 bg-green-600 text-white rounded-full text-sm font-bold">
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
