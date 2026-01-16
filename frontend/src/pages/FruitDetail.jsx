import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'

function FruitDetail() {
  const { id } = useParams()
  const [fruit, setFruit] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchFruit()
  }, [id])

  const fetchFruit = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`/api/fruits/${id}/`)
      if (!response.ok) throw new Error('Fruit non trouvé')
      const data = await response.json()
      setFruit(data)
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

  if (!fruit) return null

  return (
    <div>
      <Link
        to="/fruits"
        className="inline-flex items-center text-op-yellow hover:text-op-orange mb-6 transition-colors"
      >
        <span className="mr-2">←</span> Retour à la liste
      </Link>

      <div className="bg-gradient-to-br from-op-navy to-op-dark border-4 border-op-orange rounded-xl p-8 shadow-2xl">
        <h1 className="font-pirata text-5xl text-op-orange mb-2">{fruit.name}</h1>
        {fruit.romanji && (
          <p className="text-2xl text-gray-400 italic mb-6">{fruit.romanji}</p>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="bg-op-dark rounded-lg p-4 border-2 border-op-blue">
            <p className="text-op-blue font-bold mb-2">Type</p>
            <p className="text-white text-xl">{fruit.fruit_type}</p>
          </div>
          <div className="bg-op-dark rounded-lg p-4 border-2 border-op-gold">
            <p className="text-op-gold font-bold mb-2">⭐ Rareté</p>
            <p className="text-white text-2xl font-bold">{fruit.rarity}/5</p>
          </div>
          <div className="bg-op-dark rounded-lg p-4 border-2 border-op-blue">
            <p className="text-op-blue font-bold mb-2">Statut</p>
            <p className="text-white">{fruit.status}</p>
          </div>
        </div>

        <div className="mb-8 bg-op-dark rounded-lg p-6 border-2 border-op-orange">
          <h2 className="text-2xl font-bold text-op-orange mb-4 font-pirata">Capacité</h2>
          <p className="text-gray-300 leading-relaxed text-lg">{fruit.ability}</p>
        </div>

        {fruit.weaknesses && (
          <div className="mb-8 bg-op-dark rounded-lg p-6 border-2 border-op-red">
            <h2 className="text-2xl font-bold text-op-red mb-4 font-pirata">Faiblesses</h2>
            <p className="text-gray-300 leading-relaxed">{fruit.weaknesses}</p>
          </div>
        )}

        {fruit.description && (
          <div className="mb-8 bg-op-dark rounded-lg p-6 border-2 border-op-blue">
            <h2 className="text-2xl font-bold text-op-yellow mb-4 font-pirata">Description</h2>
            <p className="text-gray-300 leading-relaxed">{fruit.description}</p>
          </div>
        )}

        {fruit.holders && fruit.holders.length > 0 && (
          <div>
            <h2 className="text-3xl font-bold text-op-yellow mb-4 font-pirata">Détenteurs</h2>
            <div className="space-y-4">
              {fruit.holders.map(holder => (
                <div
                  key={holder.id}
                  className="bg-op-dark rounded-lg p-6 border-2 border-op-blue"
                >
                  <Link
                    to={`/characters/${holder.character.id}`}
                    className="text-2xl font-bold text-op-yellow hover:text-op-orange transition-colors"
                  >
                    {holder.character.name}
                  </Link>
                  {holder.is_current && (
                    <span className="ml-4 inline-block px-3 py-1 bg-green-600 text-white rounded-full text-sm font-bold">
                      Actuel
                    </span>
                  )}
                  {holder.from_date && (
                    <p className="text-gray-400 mt-2">Du: {holder.from_date}</p>
                  )}
                  {holder.to_date && (
                    <p className="text-gray-400">Au: {holder.to_date}</p>
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

export default FruitDetail
