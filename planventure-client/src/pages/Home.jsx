import { Box, Button, Container, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import planventureLogo from '../assets/planventure-logo.svg';

const Home = () => {
  const navigate = useNavigate();

  return (
    <Container maxWidth="sm">
      <Box 
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          py: { xs: 3, sm: 6, md: 8 },
          px: { xs: 1, sm: 2 },
        }}
      >
        <img 
          src={planventureLogo} 
          alt="Planventure Logo"
          style={{
            height: 'clamp(120px, 25vw, 280px)',
            width: 'auto',
            marginBottom: 'clamp(1rem, 5vw, 2rem)'
          }}
        />
        <Typography 
          variant="h3" 
          component="h1"
          sx={{ 
            mb: 2, 
            textAlign: 'center',
            color: 'secondary.main',
            fontSize: { xs: '1.75rem', sm: '2.125rem', md: '2.5rem' },
            fontWeight: 700
          }}
        >
          Welcome to Planventure
        </Typography>
        <Typography 
          variant="body1"
          sx={{ 
            mb: { xs: 2, sm: 3 }, 
            textAlign: 'center',
            color: 'secondary.light',
            fontSize: { xs: '0.9375rem', sm: '1rem' },
            lineHeight: 1.6
          }}
        >
          Your next adventure begins here. Start planning unforgettable trips with our intuitive planning tools and make every journey memorable.
        </Typography>
        <Button 
          variant="contained" 
          size="large"
          onClick={() => navigate('/login')}
          sx={{ 
            mt: { xs: 2, sm: 3 },
            px: { xs: 3, sm: 4 },
            py: { xs: 1, sm: 1.5 }
          }}
        >
          Get Started
        </Button>
      </Box>
    </Container>
  );
};

export default Home;