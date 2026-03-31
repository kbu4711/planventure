import { useNavigate } from 'react-router-dom';
import { Box, Typography, Button } from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import TripList from '../components/trips/TripList';
import travelingSvg from '../assets/undraw_traveling_yhxq.svg';

const Dashboard = () => {
  const navigate = useNavigate();

  const WelcomeMessage = () => (
    <Box
      sx={{
        textAlign: 'center',
        py: 6,
        px: 2,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 3
      }}
    >
      <img
        src={travelingSvg}
        alt="Start your journey"
        style={{
          maxWidth: '300px',
          width: '100%',
          height: 'auto',
          marginBottom: '1rem'
        }} 
      />
      <Typography variant="h4" component="h2" gutterBottom>
        Welcome to Planventure! 
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ maxWidth: '600px', mb: 3 }}>
        Ready to start planning your next adventure? Create your first trip and let us help you organize everything from destinations to activities.
      </Typography>
      <Button
        variant="contained"
        size="large"
        startIcon={<AddIcon />}
        onClick={() => navigate('/trips/new')}
      >
        Plan Your First Trip
      </Button>
    </Box>
  );

  const ErrorState = () => (
    <Box
      sx={{
        textAlign: 'center',
        py: 6,
        px: 2,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 3
      }}
    >
      <img
        src={travelingSvg}
        alt="Error loading trips"
        style={{
          maxWidth: '300px',
          width: '100%',
          height: 'auto',
          marginBottom: '1rem',
          opacity: 0.7
        }}
      />
      <Typography variant="h5" component="h2" gutterBottom>
        Oops! Looks like our compass is spinning! 🧭
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ maxWidth: '600px', mb: 3 }}>
        We're having trouble loading your adventures. Don't worry, even the best travelers sometimes lose their way! Try refreshing the page or come back later.
      </Typography>
      <Button
        variant="contained"
        onClick={() => window.location.reload()}
      >
        Try Again
      </Button>
    </Box>
  );

  return (
    <Box sx={{ width: '100%', p: 0, m: 0 }}>
      <Box sx={{ mb: 3, px: { xs: 1, sm: 1.5, md: 2, lg: 2.5 }, pt: 2 }}>
        <Typography 
          variant="h4" 
          component="h1" 
          sx={{
            fontWeight: 800,
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            mb: 1,
            fontSize: { xs: '1.75rem', sm: '2rem', md: '2.125rem' }
          }}
        >
          My Trips
        </Typography>
        <Typography 
          variant="body2" 
          color="text.secondary"
          sx={{ fontSize: { xs: '0.875rem', sm: '1rem' } }}
        >
          Organize and plan your journeys
        </Typography>
      </Box>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          minHeight: 'calc(100vh - 200px)',
          backgroundColor: 'transparent',
          borderRadius: 0,
          border: 'none',
          px: { xs: 1, sm: 1.5, md: 2, lg: 2.5 }
        }}
      >
        <TripList
          WelcomeMessage={WelcomeMessage}
          ErrorState={ErrorState}
        />
      </Box>
    </Box>
  );
};

export default Dashboard;
