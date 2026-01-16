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
      <div className="min-h-screen bg-op-gray">
        {/* Header rouge style One Piece officiel */}
        <header className="bg-op-red text-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-20">
              {/* Logo */}
              <Link to="/" className="flex items-center space-x-3 hover:opacity-90 transition-opacity">
                <div className="text-4xl">🏴‍☠️</div>
                <div className="flex flex-col">
                  <span className="text-2xl font-bold tracking-wide">ONE PIECE</span>
                  <span className="text-xs">ENCYCLOPEDIE</span>
                </div>
              </Link>

              {/* Navigation */}
              <nav className="hidden md:flex items-center space-x-6">
                <Link 
                  to="/characters" 
                  className="flex items-center space-x-2 px-4 py-2 hover:bg-op-red-dark rounded transition-colors"
                >
                  <span>👤</span>
                  <span className="font-medium">Personnages</span>
                </Link>
                <Link 
                  to="/crews" 
                  className="flex items-center space-x-2 px-4 py-2 hover:bg-op-red-dark rounded transition-colors"
                >
                  <span>🚢</span>
                  <span className="font-medium">Équipages</span>
                </Link>
                <Link 
                  to="/fruits" 
                  className="flex items-center space-x-2 px-4 py-2 hover:bg-op-red-dark rounded transition-colors"
                >
                  <span>🍎</span>
                  <span className="font-medium">Fruits du Démon</span>
                </Link>
                <Link 
                  to="/arcs" 
                  className="flex items-center space-x-2 px-4 py-2 hover:bg-op-red-dark rounded transition-colors"
                >
                  <span>📖</span>
                  <span className="font-medium">Arcs</span>
                </Link>
              </nav>
            </div>
          </div>
        </header>

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
        <footer className="bg-op-dark text-white mt-16 py-6">
          <div className="max-w-7xl mx-auto px-4 text-center">
            <p className="text-sm">© Encyclopédie de One Piece - Base de connaissances</p>
          </div>
        </footer>
      </div>
    </Router>
  )
}

export default App
