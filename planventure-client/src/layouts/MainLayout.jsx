import { Box, Container } from '@mui/material';
import Navbar from '../components/navigation/Navbar';
import Footer from '../components/navigation/Footer';
import { useLocation } from 'react-router-dom';

const dashboardRoutes = ['/dashboard', '/trips', '/trips/new', '/trips/:tripId', '/trips/:tripId/edit'];

const MainLayout = ({ children }) => {
  const location = useLocation();
  
  // Check if current route is a dashboard route
  const isDashboardRoute = dashboardRoutes.some(route => {
    if (route.includes(':')) {
      const pattern = new RegExp('^' + route.replace(/:\w+/g, '[^/]+') + '$');
      return pattern.test(location.pathname);
    }
    return location.pathname === route;
  });

  // For dashboard routes, render children directly without MainLayout wrapping
  if (isDashboardRoute) {
    return children;
  }

  // For non-dashboard routes, use the standard layout
  return (
    <Box sx={{ 
      display: 'flex', 
      flexDirection: 'column', 
      minHeight: '100vh',
      width: '100%',
      position: 'relative'
    }}>
      <Navbar />
      <Container 
        component="main" 
        maxWidth="lg"
        sx={{ 
          flexGrow: 1,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          width: '100%',
          py: 3,
          px: { xs: 2, sm: 3, md: 4 },
          mt: 8,
          mb: 10
        }}
      >
        {children}
      </Container>
      <Footer />
    </Box>
  );
};

export default MainLayout;
