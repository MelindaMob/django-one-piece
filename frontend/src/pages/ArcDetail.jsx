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

  if (!arc) return null

  return (
    <div>
      <Link
        to="/arcs"
        className="inline-flex items-center text-op-yellow hover:text-op-orange mb-6 transition-colors"
      >
        <span className="mr-2">←</span> Retour à la liste
      </Link>

      <div className="bg-gradient-to-br from-op-navy to-op-dark border-4 border-op-blue rounded-xl p-8 shadow-2xl">
        <h1 className="font-pirata text-5xl text-op-blue mb-6">{arc.name}</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {arc.saga && (
            <div className="bg-op-dark rounded-lg p-4 border-2 border-op-yellow">
              <p className="text-op-yellow font-bold mb-2">Saga</p>
              <p className="text-white text-xl">{arc.saga}</p>
            </div>
          )}
          <div className="bg-op-dark rounded-lg p-4 border-2 border-op-blue">
            <p className="text-op-blue font-bold mb-2">Épisodes</p>
            <p className="text-white text-xl">
              #{arc.start_episode_number} - #{arc.end_episode_number}
            </p>
          </div>
        </div>

        {arc.description && (
          <div className="mb-8 bg-op-dark rounded-lg p-6 border-2 border-op-blue">
            <h2 className="text-2xl font-bold text-op-yellow mb-4 font-pirata">Description</h2>
            <p className="text-gray-300 leading-relaxed">{arc.description}</p>
          </div>
        )}

        {arc.episodes && arc.episodes.length > 0 && (
          <div>
            <h2 className="text-3xl font-bold text-op-yellow mb-4 font-pirata">
              Épisodes ({arc.episodes.length})
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {arc.episodes.map(episode => (
                <div
                  key={episode.id}
                  className="bg-op-dark rounded-lg p-4 border-2 border-op-blue"
                >
                  <h3 className="text-xl font-bold text-op-blue mb-2">
                    Épisode #{episode.number}
                  </h3>
                  <p className="text-gray-300">{episode.title}</p>
                  {episode.air_date && (
                    <p className="text-gray-400 text-sm mt-2">
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
