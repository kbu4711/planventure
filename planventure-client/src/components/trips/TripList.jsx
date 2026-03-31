import { useState, useEffect } from 'react';
import { 
  Grid, 
  Typography, 
  Box, 
  Alert,
  Button,
  useMediaQuery,
  useTheme
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import TripCard from './TripCard';
import { useNavigate } from 'react-router-dom';
import { tripService } from '../../services/tripService';

const TripList = ({ WelcomeMessage, ErrorState }) => {
  const [trips, setTrips] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  useEffect(() => {
    const fetchTrips = async () => {
      try {
        setLoading(true);
        const data = await tripService.getAllTrips();
        console.log('TripList received data:', data); // Debug log
        
        if (!data || !data.trips) {
          console.error('Invalid data format:', data);
          setError('Unexpected data format received');
          return;
        }
        
        setTrips(data.trips);
      } catch (err) {
        console.error('TripList error:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchTrips();
  }, []);

  // Loading state with skeleton cards
  if (loading) {
    return (
      <Grid container spacing={{ xs: 1, sm: 1.5, md: 2, lg: 2.5 }}>
        {[1, 2, 3, 4, 5, 6].map((skeleton) => (
          <Grid item xs={12} sm={6} md={6} lg={4} key={skeleton}>
            <TripCard loading={true} />
          </Grid>
        ))}
      </Grid>
    );
  }

  // Error state
  if (error) {
    return <ErrorState />;
  }

  // Empty state
  if (trips.length === 0) {
    return <WelcomeMessage />;
  }

  // Sort trips - upcoming first, then by reverse date
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

  // Loaded state with trips
  return (
    <Box sx={{ animation: 'fadeIn 0.4s ease-in', width: '100%' }}>
      <Grid 
        container 
        spacing={{ xs: 1, sm: 1.5, md: 2, lg: 2.5 }}
        sx={{
          '@keyframes fadeIn': {
            '0%': { opacity: 0 },
            '100%': { opacity: 1 }
          }
        }}
      >
        {sortedTrips.map((trip, index) => (
          <Grid 
            item 
            xs={12} 
            sm={6}
            md={6}
            lg={4}
            key={trip.id}
            sx={{
              animation: `slideIn 0.5s ease-out ${index * 0.1}s both`,
              '@keyframes slideIn': {
                '0%': { opacity: 0, transform: 'translateY(20px)' },
                '100%': { opacity: 1, transform: 'translateY(0)' }
              }
            }}
          >
            <TripCard trip={trip} />
          </Grid>
        ))}
        <Grid 
          item 
          xs={12}
          sm={6}
          md={6}
          lg={4}
          sx={{
            animation: `slideIn 0.5s ease-out ${sortedTrips.length * 0.1}s both`,
            '@keyframes slideIn': {
              '0%': { opacity: 0, transform: 'translateY(20px)' },
              '100%': { opacity: 1, transform: 'translateY(0)' }
            }
          }}
        >
          <Box sx={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Button
              variant="outlined"
              sx={{ 
                height: '100%',
                width: '100%',
                minHeight: 380,
                minWidth: 220,
                maxWidth: 380,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                borderColor: 'divider',
                color: 'text.secondary',
                fontWeight: 600,
                transition: 'all 0.3s ease',
                '&:hover': {
                  borderColor: 'primary.main',
                  color: 'primary.main',
                  backgroundColor: 'primary.lighter',
                  transform: 'translateY(-4px)'
                }
              }}
              onClick={() => navigate('/trips/new')}
            >
              <AddIcon sx={{ mb: 1, fontSize: 32 }} />
              <Typography variant="button">Create New Trip</Typography>
            </Button>
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
};

export default TripList;
