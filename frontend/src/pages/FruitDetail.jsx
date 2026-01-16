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

  if (!fruit) return null

  return (
    <div>
      <Link
        to="/fruits"
        className="inline-flex items-center text-op-red hover:underline mb-6"
      >
        <span className="mr-2">←</span> Retour à la liste
      </Link>

      <div className="bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-4xl font-bold text-op-red mb-2">{fruit.name}</h1>
        {fruit.romanji && (
          <p className="text-2xl text-gray-600 italic mb-6">{fruit.romanji}</p>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="bg-op-gray rounded-lg p-4">
            <p className="text-gray-600 font-semibold mb-2">Type</p>
            <p className="text-xl">{fruit.fruit_type}</p>
          </div>
          <div className="bg-op-gray rounded-lg p-4">
            <p className="text-gray-600 font-semibold mb-2">⭐ Rareté</p>
            <p className="text-xl font-bold text-op-red">{fruit.rarity}/5</p>
          </div>
          <div className="bg-op-gray rounded-lg p-4">
            <p className="text-gray-600 font-semibold mb-2">Statut</p>
            <p className="text-xl">{fruit.status}</p>
          </div>
        </div>

        <div className="mb-8 bg-op-gray rounded-lg p-6">
          <h2 className="text-2xl font-bold text-op-red mb-4">Capacité</h2>
          <p className="text-gray-700 leading-relaxed text-lg">{fruit.ability}</p>
        </div>

        {fruit.weaknesses && (
          <div className="mb-8 bg-op-gray rounded-lg p-6">
            <h2 className="text-2xl font-bold text-op-red mb-4">Faiblesses</h2>
            <p className="text-gray-700 leading-relaxed">{fruit.weaknesses}</p>
          </div>
        )}

        {fruit.description && (
          <div className="mb-8 bg-op-gray rounded-lg p-6">
            <h2 className="text-2xl font-bold text-op-red mb-4">Description</h2>
            <p className="text-gray-700 leading-relaxed">{fruit.description}</p>
          </div>
        )}

        {fruit.holders && fruit.holders.length > 0 && (
          <div>
            <h2 className="text-2xl font-bold text-op-red mb-4">Détenteurs</h2>
            <div className="space-y-4">
              {fruit.holders.map(holder => (
                <div
                  key={holder.id}
                  className="bg-op-gray rounded-lg p-6"
                >
                  <Link
                    to={`/characters/${holder.character.id}`}
                    className="text-xl font-bold text-op-red hover:underline"
                  >
                    {holder.character.name}
                  </Link>
                  {holder.is_current && (
                    <span className="ml-4 inline-block px-3 py-1 bg-green-500 text-white rounded text-sm font-bold">
                      Actuel
                    </span>
                  )}
                  {holder.from_date && (
                    <p className="text-gray-600 mt-2">Du: {holder.from_date}</p>
                  )}
                  {holder.to_date && (
                    <p className="text-gray-600">Au: {holder.to_date}</p>
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
