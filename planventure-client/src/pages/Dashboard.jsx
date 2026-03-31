import { useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Typography, Button } from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import TripList from '../components/trips/TripList';
import travelingSvg from '../assets/undraw_traveling_yhxq.svg';

// ============================================================================
// CONSTANTS
// ============================================================================

const IMAGE_CONFIG = {
  maxWidth: '300px',
  width: '100%',
  height: 'auto',
  marginBottom: '1rem'
};

const SPACING = {
  header: { xs: 1, sm: 1.5, md: 2, lg: 2.5 },
  titleSize: { xs: '1.75rem', sm: '2rem', md: '2.125rem' }
};

const GRADIENT_TITLE_STYLE = {
  fontWeight: 800,
  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  WebkitBackgroundClip: 'text',
  WebkitTextFillColor: 'transparent',
  backgroundClip: 'text',
  mb: 1,
  fontSize: SPACING.titleSize
};

const STATE_MESSAGE_CONTAINER = {
  textAlign: 'center',
  py: 6,
  px: 2,
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  gap: 3
};

// ============================================================================
// REUSABLE STATE MESSAGE COMPONENT
// ============================================================================

const StateMessage = ({ 
  image, 
  imageAlt, 
  title, 
  description, 
  buttonText, 
  onButtonClick,
  imageOpacity = 1 
}) => (
  <Box sx={STATE_MESSAGE_CONTAINER}>
    <img
      src={image}
      alt={imageAlt}
      style={{
        ...IMAGE_CONFIG,
        opacity: imageOpacity
      }} 
    />
    <Typography variant="h4" component="h2" gutterBottom>
      {title}
    </Typography>
    <Typography 
      variant="body1" 
      color="text.secondary" 
      sx={{ maxWidth: '600px', mb: 3 }}
    >
      {description}
    </Typography>
    <Button
      variant="contained"
      size="large"
      startIcon={<AddIcon />}
      onClick={onButtonClick}
    >
      {buttonText}
    </Button>
  </Box>
);

// ============================================================================
// WELCOME MESSAGE COMPONENT
// ============================================================================

const WelcomeMessage = ({ onCreateTrip }) => (
  <StateMessage
    image={travelingSvg}
    imageAlt="Start your journey"
    title="Welcome to Planventure!"
    description="Ready to start planning your next adventure? Create your first trip and let us help you organize everything from destinations to activities."
    buttonText="Plan Your First Trip"
    onButtonClick={onCreateTrip}
  />
);

// ============================================================================
// ERROR STATE COMPONENT
// ============================================================================

const ErrorState = ({ onRetry }) => (
  <StateMessage
    image={travelingSvg}
    imageAlt="Error loading trips"
    title="Oops! Looks like our compass is spinning! 🧭"
    description="We're having trouble loading your adventures. Don't worry, even the best travelers sometimes lose their way! Try refreshing the page or come back later."
    buttonText="Try Again"
    onButtonClick={onRetry}
    imageOpacity={0.7}
  />
);

// ============================================================================
// MAIN DASHBOARD COMPONENT
// ============================================================================

const Dashboard = () => {
  const navigate = useNavigate();

  // Memoized callbacks to prevent unnecessary re-renders
  const handleCreateTrip = useCallback(() => {
    navigate('/trips/new');
  }, [navigate]);

  const handleRetry = useCallback(() => {
    window.location.reload();
  }, []);

  return (
    <Box sx={{ width: '100%', p: 0, m: 0 }}>
      {/* Header Section */}
      <Box sx={{ mb: 3, px: SPACING.header, pt: 2 }}>
        <Typography 
          variant="h4" 
          component="h1" 
          sx={GRADIENT_TITLE_STYLE}
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

      {/* Content Section */}
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          minHeight: 'calc(100vh - 200px)',
          backgroundColor: 'transparent',
          px: SPACING.header
        }}
      >
        <TripList
          WelcomeMessage={() => <WelcomeMessage onCreateTrip={handleCreateTrip} />}
          ErrorState={() => <ErrorState onRetry={handleRetry} />}
        />
      </Box>
    </Box>
  );
};

export default Dashboard;
