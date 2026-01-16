import React from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import CharactersList from './pages/CharactersList'
import CharacterDetail from './pages/CharacterDetail'
import CrewsList from './pages/CrewsList'
import CrewDetail from './pages/CrewDetail'
import FruitsList from './pages/FruitsList'
import FruitDetail from './pages/FruitDetail'
import ArcsList from './pages/ArcsList'
import ArcDetail from './pages/ArcDetail'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-op-dark via-op-navy to-blue-900">
        {/* Navbar avec thème One Piece */}
        <nav className="bg-op-dark border-b-4 border-op-red shadow-2xl">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-20">
              <Link to="/" className="flex items-center space-x-3 hover:opacity-80 transition-opacity">
                <span className="text-4xl">🏴‍☠️</span>
                <h1 className="font-pirata text-3xl md:text-4xl text-op-yellow font-bold tracking-wide">
                  Encyclopédie de One Piece
                </h1>
              </Link>
              <div className="hidden md:flex space-x-6">
                <Link 
                  to="/characters" 
                  className="text-white hover:text-op-yellow font-semibold transition-colors duration-200 px-4 py-2 rounded-lg hover:bg-opacity-20 hover:bg-op-yellow"
                >
                  Personnages
                </Link>
                <Link 
                  to="/crews" 
                  className="text-white hover:text-op-yellow font-semibold transition-colors duration-200 px-4 py-2 rounded-lg hover:bg-opacity-20 hover:bg-op-yellow"
                >
                  Équipages
                </Link>
                <Link 
                  to="/fruits" 
                  className="text-white hover:text-op-yellow font-semibold transition-colors duration-200 px-4 py-2 rounded-lg hover:bg-opacity-20 hover:bg-op-yellow"
                >
                  Fruits du Démon
                </Link>
                <Link 
                  to="/arcs" 
                  className="text-white hover:text-op-yellow font-semibold transition-colors duration-200 px-4 py-2 rounded-lg hover:bg-opacity-20 hover:bg-op-yellow"
                >
                  Arcs
                </Link>
              </div>
            </div>
          </div>
        </nav>

        {/* Contenu principal */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Routes>
            <Route path="/" element={<CharactersList />} />
            <Route path="/characters" element={<CharactersList />} />
            <Route path="/characters/:id" element={<CharacterDetail />} />
            <Route path="/crews" element={<CrewsList />} />
            <Route path="/crews/:id" element={<CrewDetail />} />
            <Route path="/fruits" element={<FruitsList />} />
            <Route path="/fruits/:id" element={<FruitDetail />} />
            <Route path="/arcs" element={<ArcsList />} />
            <Route path="/arcs/:id" element={<ArcDetail />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="bg-op-dark border-t-4 border-op-red mt-16 py-6">
          <div className="max-w-7xl mx-auto px-4 text-center text-gray-400">
            <p className="font-pirata text-lg">🏴‍☠️ Encyclopédie de One Piece - Base de connaissances</p>
          </div>
        </footer>
      </div>
    </Router>
  )
}

export default App
