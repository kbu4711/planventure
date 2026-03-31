import { Box, Container } from '@mui/material';
import Navbar from '../components/navigation/Navbar';
import Footer from '../components/navigation/Footer';

const AuthLayout = ({ children }) => {
  return (
    <Box sx={{ 
      display: 'flex', 
      flexDirection: 'column', 
      minHeight: '100vh',
      width: '100%',
      position: 'relative',
      background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
      '&::before': {
        content: '""',
        position: 'absolute',
        top: '-50%',
        right: '-10%',
        width: '600px',
        height: '600px',
        borderRadius: '50%',
        background: 'rgba(79, 70, 229, 0.05)',
        pointerEvents: 'none',
        zIndex: 0
      },
      '&::after': {
        content: '""',
        position: 'absolute',
        bottom: '-30%',
        left: '-10%',
        width: '500px',
        height: '500px',
        borderRadius: '50%',
        background: 'rgba(79, 70, 229, 0.03)',
        pointerEvents: 'none',
        zIndex: 0
      }
    }}>
      <Navbar />
      <Container 
        component="main" 
        maxWidth="xs"
        sx={{ 
          flexGrow: 1,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          py: { xs: 2, sm: 4, md: 6 },
          px: { xs: 1, sm: 2 },
          mt: { xs: 7, sm: 8, md: 6 },
          mb: { xs: 8, sm: 10, md: 6 },
          position: 'relative',
          zIndex: 1
        }}
      >
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            bgcolor: 'background.paper',
            p: { xs: 2.5, sm: 3, md: 4 },
            borderRadius: 2,
            boxShadow: { xs: '0 10px 30px rgba(79, 70, 229, 0.1)', md: '0 20px 60px rgba(79, 70, 229, 0.12)' },
            width: '100%',
            maxWidth: { xs: '100%', sm: '420px' },
            backdropFilter: 'blur(10px)',
            border: '1px solid rgba(255, 255, 255, 0.8)',
            transition: 'all 0.3s ease-in-out',
            '&:hover': {
              boxShadow: { xs: '0 15px 40px rgba(79, 70, 229, 0.14)', md: '0 25px 70px rgba(79, 70, 229, 0.16)' },
              transform: 'translateY(-2px)'
            }
          }}
        >
          {children}
        </Box>
      </Container>
      <Footer />
    </Box>
  );
};

export default AuthLayout;