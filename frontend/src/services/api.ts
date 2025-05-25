// API configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export interface Destination {
  name: string;
  country: string;
  description: string;
  slug: string;
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
  return fetchFromApi<Destination[]>('/explorer');
};

// Obtener destino por slug
export const getDestinationBySlug = (slug: string): Promise<Destination> => {
  return fetchFromApi<Destination>(`/details/${slug}`);
};
