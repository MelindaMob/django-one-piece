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

  if (!crew) return null

  return (
    <div>
      <Link
        to="/crews"
        className="inline-flex items-center text-op-red hover:underline mb-6"
      >
        <span className="mr-2">←</span> Retour à la liste
      </Link>

      <div className="bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-4xl font-bold text-op-red mb-6">{crew.name}</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {crew.ship_name && (
            <div className="bg-op-gray rounded-lg p-4">
              <p className="text-gray-600 font-semibold mb-2">🚢 Navire</p>
              <p className="text-xl">{crew.ship_name}</p>
            </div>
          )}
          {crew.base_location && (
            <div className="bg-op-gray rounded-lg p-4">
              <p className="text-gray-600 font-semibold mb-2">📍 Base</p>
              <p className="text-xl">{crew.base_location}</p>
            </div>
          )}
          {crew.captain && (
            <div className="bg-op-gray rounded-lg p-4">
              <p className="text-gray-600 font-semibold mb-2">👑 Capitaine</p>
              <Link
                to={`/characters/${crew.captain.id}`}
                className="text-xl text-op-red hover:underline"
              >
                {crew.captain.name}
              </Link>
            </div>
          )}
        </div>

        {crew.description && (
          <div className="mb-8 bg-op-gray rounded-lg p-6">
            <h2 className="text-2xl font-bold text-op-red mb-4">Description</h2>
            <p className="text-gray-700 leading-relaxed">{crew.description}</p>
          </div>
        )}

        {crew.members && crew.members.length > 0 && (
          <div>
            <h2 className="text-2xl font-bold text-op-red mb-4">
              Membres ({crew.members.length})
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {crew.members.map(member => (
                <Link
                  key={member.id}
                  to={`/characters/${member.id}`}
                  className="bg-op-gray rounded-lg p-4 hover:bg-gray-200 transition-colors"
                >
                  <h3 className="text-xl font-bold text-op-red mb-2">{member.name}</h3>
                  {member.bounty > 0 && (
                    <p className="text-op-red font-semibold">
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
