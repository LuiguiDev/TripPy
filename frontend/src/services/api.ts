// API configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export interface Destination {
  id: string;
  nombre: string;
  codigo_iata: string;
  slug: string;
  estado: string;
  descripcion: string;
  imagenes: string[];
  precio_ida: number;
  precio_vuelta: number;
  precio_por_día: number,
  enlace: string;
}


const fetchFromApi = async <T>(endpoint: string): Promise<T> => {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
};

// Obtener todas las destinaciones
export const getDestinations = (): Promise<Destination[]> => {
  return fetchFromApi<Destination[]>('/destinos');
};

