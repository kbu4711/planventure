import { Box, Typography, Container, Paper, Alert } from '@mui/material';
import { Info as InfoIcon } from '@mui/icons-material';

const TripPlannerPage = () => {
  return (
    <Box sx={{ width: '100%', p: 0, m: 0 }}>
      <Box sx={{ mb: 4, px: { xs: 1, sm: 1.5, md: 2, lg: 2.5 }, pt: 2 }}>
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
          Trip Planner
        </Typography>
        <Typography 
          variant="body2" 
          color="text.secondary"
          sx={{ fontSize: { xs: '0.875rem', sm: '1rem' } }}
        >
          Plan your itineraries and organize your activities
        </Typography>
      </Box>

      <Box
        sx={{
          px: { xs: 1, sm: 1.5, md: 2, lg: 2.5 },
          py: 4
        }}
      >
        <Paper
          elevation={0}
          sx={{
            p: 4,
            backgroundColor: 'background.paper',
            borderRadius: 2,
            border: '1px solid',
            borderColor: 'divider',
            textAlign: 'center'
          }}
        >
          <Alert severity="info" sx={{ mb: 3 }}>
            <InfoIcon sx={{ mr: 1, display: 'inline' }} />
            Trip planner feature coming soon! Select a trip from "My Trips" to start planning.
          </Alert>
          
          <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
            Create and manage your trip itineraries
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ maxWidth: 600, mx: 'auto' }}>
            Once you've created a trip, you'll be able to plan your day-by-day activities, add accommodations, 
            transportation details, and much more to make your journey unforgettable.
          </Typography>
        </Paper>
      </Box>
    </Box>
  );
};

export default TripPlannerPage;
