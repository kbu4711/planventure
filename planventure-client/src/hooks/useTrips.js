import { useState, useEffect } from 'react';
import { tripService } from '../services/tripService';

/**
 * Custom hook for fetching and managing trips data
 * @returns {Object} { trips, loading, error, refetch }
 */
export const useTrips = () => {
  const [trips, setTrips] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchTrips = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await tripService.getAllTrips();
      console.log('useTrips received data:', data);

      if (!data || !data.trips) {
        console.error('Invalid data format:', data);
        setError('Unexpected data format received');
        return;
      }

      setTrips(data.trips);
    } catch (err) {
      console.error('useTrips error:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTrips();
  }, []);

  // Sort trips - upcoming first, then by date
  const sortedTrips = [...trips].sort((a, b) => {
    const aStart = new Date(a.start_date);
    const bStart = new Date(b.start_date);
    const now = new Date();
    const aIsUpcoming = aStart > now;
    const bIsUpcoming = bStart > now;

    if (aIsUpcoming !== bIsUpcoming) {
      return aIsUpcoming ? -1 : 1;
    }
    return aStart - bStart;
  });

  return {
    trips: sortedTrips,
    loading,
    error,
    refetch: fetchTrips  // Allow manual refetch if needed
  };
};
