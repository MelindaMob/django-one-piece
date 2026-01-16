import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'

function CrewDetail() {
  const { id } = useParams()
  const [crew, setCrew] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchCrew()
  }, [id])

  const fetchCrew = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`/api/crews/${id}/`)
      if (!response.ok) throw new Error('Équipage non trouvé')
      const data = await response.json()
      setCrew(data)
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

  if (!crew) return null

  return (
    <div>
      <Link
        to="/crews"
        className="inline-flex items-center text-op-yellow hover:text-op-orange mb-6 transition-colors"
      >
        <span className="mr-2">←</span> Retour à la liste
      </Link>

      <div className="bg-gradient-to-br from-op-navy to-op-dark border-4 border-op-red rounded-xl p-8 shadow-2xl">
        <h1 className="font-pirata text-5xl text-op-yellow mb-6">{crew.name}</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {crew.ship_name && (
            <div className="bg-op-dark rounded-lg p-4 border-2 border-op-blue">
              <p className="text-op-blue font-bold mb-2">🚢 Navire</p>
              <p className="text-white text-xl">{crew.ship_name}</p>
            </div>
          )}
          {crew.base_location && (
            <div className="bg-op-dark rounded-lg p-4 border-2 border-op-blue">
              <p className="text-op-blue font-bold mb-2">📍 Base</p>
              <p className="text-white text-xl">{crew.base_location}</p>
            </div>
          )}
          {crew.captain && (
            <div className="bg-op-dark rounded-lg p-4 border-2 border-op-gold">
              <p className="text-op-gold font-bold mb-2">👑 Capitaine</p>
              <Link
                to={`/characters/${crew.captain.id}`}
                className="text-white text-xl hover:text-op-yellow transition-colors"
              >
                {crew.captain.name}
              </Link>
            </div>
          )}
        </div>

        {crew.description && (
          <div className="mb-8 bg-op-dark rounded-lg p-6 border-2 border-op-blue">
            <h2 className="text-2xl font-bold text-op-yellow mb-4 font-pirata">Description</h2>
            <p className="text-gray-300 leading-relaxed">{crew.description}</p>
          </div>
        )}

        {crew.members && crew.members.length > 0 && (
          <div>
            <h2 className="text-3xl font-bold text-op-yellow mb-4 font-pirata">
              Membres ({crew.members.length})
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {crew.members.map(member => (
                <Link
                  key={member.id}
                  to={`/characters/${member.id}`}
                  className="bg-op-dark rounded-lg p-4 border-2 border-op-blue hover:border-op-yellow transition-all hover:scale-105"
                >
                  <h3 className="text-xl font-bold text-op-yellow mb-2">{member.name}</h3>
                  {member.bounty > 0 && (
                    <p className="text-op-gold font-semibold">
                      💰 {member.bounty.toLocaleString()} Berries
                    </p>
                  )}
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default CrewDetail
