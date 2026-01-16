import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'

function ArcDetail() {
  const { id } = useParams()
  const [arc, setArc] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchArc()
  }, [id])

  const fetchArc = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`/api/arcs/${id}/`)
      if (!response.ok) throw new Error('Arc non trouvé')
      const data = await response.json()
      setArc(data)
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

  if (!arc) return null

  return (
    <div>
      <Link
        to="/arcs"
        className="inline-flex items-center text-op-red hover:underline mb-6"
      >
        <span className="mr-2">←</span> Retour à la liste
      </Link>

      <div className="bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-4xl font-bold text-op-red mb-6">{arc.name}</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {arc.saga && (
            <div className="bg-op-gray rounded-lg p-4">
              <p className="text-gray-600 font-semibold mb-2">Saga</p>
              <p className="text-xl">{arc.saga}</p>
            </div>
          )}
          <div className="bg-op-gray rounded-lg p-4">
            <p className="text-gray-600 font-semibold mb-2">Épisodes</p>
            <p className="text-xl">
              #{arc.start_episode_number} - #{arc.end_episode_number}
            </p>
          </div>
        </div>

        {arc.description && (
          <div className="mb-8 bg-op-gray rounded-lg p-6">
            <h2 className="text-2xl font-bold text-op-red mb-4">Description</h2>
            <p className="text-gray-700 leading-relaxed">{arc.description}</p>
          </div>
        )}

        {arc.episodes && arc.episodes.length > 0 && (
          <div>
            <h2 className="text-2xl font-bold text-op-red mb-4">
              Épisodes ({arc.episodes.length})
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {arc.episodes.map(episode => (
                <div
                  key={episode.id}
                  className="bg-op-gray rounded-lg p-4"
                >
                  <h3 className="text-xl font-bold text-op-red mb-2">
                    Épisode #{episode.number}
                  </h3>
                  <p className="text-gray-700">{episode.title}</p>
                  {episode.air_date && (
                    <p className="text-gray-600 text-sm mt-2">
                      Diffusé le: {episode.air_date}
                    </p>
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

export default ArcDetail
