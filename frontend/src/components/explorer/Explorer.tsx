import React, { useState, useMemo } from 'react';
import { Search, Filter, MapPin, Star, Calendar, Users, Plane } from 'lucide-react';
import { getDestinations } from '../../services/api';

// Datos mockeados
const mockDestinations = [
  {
    id: 1,
    name: "Playa del Carmen",
    region: "Caribe Mexicano",
    type: "playa",
    price: 2500,
    rating: 4.8,
    image: "https://images.unsplash.com/photo-1512149177596-f817c7ef5d4c?w=800&h=600&fit=crop",
    description: "Paraíso caribeño con cenotes y ruinas mayas",
    duration: "4-7 días",
    highlights: ["Cenotes cristalinos", "Ruinas de Tulum", "Vida nocturna"]
  },
  {
    id: 2,
    name: "San Miguel de Allende",
    region: "Bajío",
    type: "cultura",
    price: 1800,
    rating: 4.9,
    image: "https://images.unsplash.com/photo-1518105779142-d975f22f1b0a?w=800&h=600&fit=crop",
    description: "Ciudad colonial llena de arte y tradición",
    duration: "3-5 días",
    highlights: ["Arquitectura colonial", "Gastronomía", "Artesanías"]
  },
  {
    id: 3,
    name: "Pico de Orizaba",
    region: "Veracruz",
    type: "montaña",
    price: 3200,
    rating: 4.6,
    image: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=600&fit=crop",
    description: "La montaña más alta de México para aventureros",
    duration: "5-8 días",
    highlights: ["Ascenso al pico", "Bosques de niebla", "Aventura extrema"]
  },
  {
    id: 4,
    name: "Oaxaca de Juárez",
    region: "Sur",
    type: "cultura",
    price: 2200,
    rating: 4.9,
    image: "https://images.unsplash.com/photo-1518638150340-f706e86654de?w=800&h=600&fit=crop",
    description: "Capital gastronómica y cultural de México",
    duration: "4-6 días",
    highlights: ["Mezcal auténtico", "Monte Albán", "Mercados tradicionales"]
  },
  {
    id: 5,
    name: "Holbox",
    region: "Caribe Mexicano",
    type: "playa",
    price: 3500,
    rating: 4.7,
    image: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&h=600&fit=crop",
    description: "Isla virgen con tiburones ballena",
    duration: "3-5 días",
    highlights: ["Tiburones ballena", "Playa virgen", "Tranquilidad total"]
  },
  {
    id: 6,
    name: "Pueblo Mágico de Bacalar",
    region: "Caribe Mexicano",
    type: "naturaleza",
    price: 2800,
    rating: 4.8,
    image: "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800&h=600&fit=crop",
    description: "La laguna de los siete colores",
    duration: "3-4 días",
    highlights: ["Laguna multicolor", "Kayak", "Cenotes cercanos"]
  }
];

const data = await getDestinations()

console.log(data);


const regions = ["Todas", "Caribe Mexicano", "Bajío", "Veracruz", "Sur"];
const types = ["Todos", "playa", "cultura", "montaña", "naturaleza"];
const priceRanges = [
  { label: "Todos", min: 0, max: Infinity },
  { label: "Económico (< $2000)", min: 0, max: 2000 },
  { label: "Moderado ($2000-3000)", min: 2000, max: 3000 },
  { label: "Premium (> $3000)", min: 3000, max: Infinity }
];

function Explorer() {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedRegion, setSelectedRegion] = useState("Todas");
  const [selectedType, setSelectedType] = useState("Todos");
  const [selectedPriceRange, setSelectedPriceRange] = useState(0);
  const [showFilters, setShowFilters] = useState(false);

  const filteredDestinations = useMemo(() => {
    return mockDestinations.filter(destination => {
      const matchesSearch = destination.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           destination.description.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesRegion = selectedRegion === "Todas" || destination.region === selectedRegion;
      const matchesType = selectedType === "Todos" || destination.type === selectedType;
      const priceRange = priceRanges[selectedPriceRange];
      const matchesPrice = destination.price >= priceRange.min && destination.price <= priceRange.max;
      
      return matchesSearch && matchesRegion && matchesType && matchesPrice;
    });
  }, [searchTerm, selectedRegion, selectedType, selectedPriceRange]);

  const getTypeColor = (type) => {
    const colors = {
      playa: "bg-blue-100 text-blue-800",
      cultura: "bg-purple-100 text-purple-800",
      montaña: "bg-green-100 text-green-800",
      naturaleza: "bg-emerald-100 text-emerald-800"
    };
    return colors[type] || "bg-gray-100 text-gray-800";
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-pink-50 to-purple-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md border-b border-orange-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Plane className="h-8 w-8 text-orange-600 transform rotate-45" />
              <h1 className="text-2xl font-bold bg-gradient-to-r from-orange-600 to-pink-600 bg-clip-text text-transparent">
                TripPy
              </h1>
            </div>
            <nav className="hidden md:flex space-x-8">
              <a href="#" className="text-gray-700 hover:text-orange-600 font-medium transition-colors">Destinos</a>
              <a href="#" className="text-gray-700 hover:text-orange-600 font-medium transition-colors">Experiencias</a>
              <a href="#" className="text-gray-700 hover:text-orange-600 font-medium transition-colors">Paquetes</a>
              <a href="#" className="text-gray-700 hover:text-orange-600 font-medium transition-colors">Contacto</a>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Descubre el
            <span className="bg-gradient-to-r from-orange-600 via-pink-600 to-purple-600 bg-clip-text text-transparent block">
              México Auténtico
            </span>
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Explora destinos únicos, vive experiencias locales y crea recuerdos inolvidables en el corazón de México
          </p>
        </div>
      </section>

      {/* Search and Filters */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-12">
        <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-6 shadow-xl border border-white/20">
          {/* Search Bar */}
          <div className="relative mb-6">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
            <input
              type="text"
              placeholder="Busca tu próximo destino..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-12 pr-4 py-4 rounded-xl border border-gray-200 focus:ring-2 focus:ring-orange-500 focus:border-transparent text-lg bg-white/80"
            />
          </div>

          {/* Filter Toggle */}
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="flex items-center space-x-2 text-orange-600 font-medium mb-4 hover:text-orange-700 transition-colors"
          >
            <Filter className="h-5 w-5" />
            <span>{showFilters ? 'Ocultar filtros' : 'Mostrar filtros'}</span>
          </button>

          {/* Filters */}
          {showFilters && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t border-gray-200">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Región</label>
                <select
                  value={selectedRegion}
                  onChange={(e) => setSelectedRegion(e.target.value)}
                  className="w-full p-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-orange-500 bg-white"
                >
                  {regions.map(region => (
                    <option key={region} value={region}>{region}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Tipo</label>
                <select
                  value={selectedType}
                  onChange={(e) => setSelectedType(e.target.value)}
                  className="w-full p-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-orange-500 bg-white"
                >
                  {types.map(type => (
                    <option key={type} value={type}>{type.charAt(0).toUpperCase() + type.slice(1)}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Precio</label>
                <select
                  value={selectedPriceRange}
                  onChange={(e) => setSelectedPriceRange(Number(e.target.value))}
                  className="w-full p-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-orange-500 bg-white"
                >
                  {priceRanges.map((range, index) => (
                    <option key={index} value={index}>{range.label}</option>
                  ))}
                </select>
              </div>
            </div>
          )}
        </div>
      </section>

      {/* Results Counter */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-8">
        <p className="text-gray-600 text-lg">
          {filteredDestinations.length} destino{filteredDestinations.length !== 1 ? 's' : ''} encontrado{filteredDestinations.length !== 1 ? 's' : ''}
        </p>
      </section>

      {/* Destinations Grid */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">
          {filteredDestinations.map((destination) => (
            <div
              key={destination.id}
              className="group bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-gray-100"
            >
              <div className="relative overflow-hidden">
                <img
                  src={destination.image}
                  alt={destination.name}
                  className="w-full h-64 object-cover group-hover:scale-110 transition-transform duration-500"
                />
                <div className="absolute top-4 left-4">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getTypeColor(destination.type)}`}>
                    {destination.type.charAt(0).toUpperCase() + destination.type.slice(1)}
                  </span>
                </div>
                <div className="absolute top-4 right-4 bg-white/90 backdrop-blur-sm rounded-full px-3 py-1">
                  <div className="flex items-center space-x-1">
                    <Star className="h-4 w-4 text-yellow-400 fill-current" />
                    <span className="text-sm font-medium">{destination.rating}</span>
                  </div>
                </div>
              </div>

              <div className="p-6">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="text-xl font-bold text-gray-900 mb-1 group-hover:text-orange-600 transition-colors">
                      {destination.name}
                    </h3>
                    <div className="flex items-center text-gray-500 text-sm">
                      <MapPin className="h-4 w-4 mr-1" />
                      {destination.region}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-orange-600">
                      ${destination.price.toLocaleString()}
                    </div>
                    <div className="text-sm text-gray-500">MXN por persona</div>
                  </div>
                </div>

                <p className="text-gray-600 mb-4 line-clamp-2">
                  {destination.description}
                </p>

                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center text-sm text-gray-500">
                    <Calendar className="h-4 w-4 mr-1" />
                    {destination.duration}
                  </div>
                  <div className="flex items-center text-sm text-gray-500">
                    <Users className="h-4 w-4 mr-1" />
                    Grupos pequeños
                  </div>
                </div>

                <div className="mb-4">
                  <div className="flex flex-wrap gap-2">
                    {destination.highlights.slice(0, 2).map((highlight, index) => (
                      <span
                        key={index}
                        className="px-2 py-1 bg-orange-50 text-orange-700 text-xs rounded-full"
                      >
                        {highlight}
                      </span>
                    ))}
                    {destination.highlights.length > 2 && (
                      <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
                        +{destination.highlights.length - 2} más
                      </span>
                    )}
                  </div>
                </div>

                <button className="w-full bg-gradient-to-r from-orange-500 to-pink-500 text-white py-3 rounded-xl font-medium hover:from-orange-600 hover:to-pink-600 transition-all duration-200 transform hover:scale-105 shadow-lg hover:shadow-xl">
                  Ver detalles
                </button>
              </div>
            </div>
          ))}
        </div>

        {filteredDestinations.length === 0 && (
          <div className="text-center py-20">
            <div className="text-6xl mb-4">🌵</div>
            <h3 className="text-2xl font-bold text-gray-900 mb-2">No encontramos destinos</h3>
            <p className="text-gray-600 mb-6">Intenta ajustar tus filtros para encontrar más opciones</p>
            <button
              onClick={() => {
                setSearchTerm("");
                setSelectedRegion("Todas");
                setSelectedType("Todos");
                setSelectedPriceRange(0);
              }}
              className="bg-orange-500 text-white px-6 py-3 rounded-xl font-medium hover:bg-orange-600 transition-colors"
            >
              Limpiar filtros
            </button>
          </div>
        )}
      </section>
    </div>
  );
}

export default Explorer