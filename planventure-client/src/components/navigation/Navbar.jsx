import { AppBar, Box, Toolbar, Typography, Button, Stack, IconButton, useMediaQuery, useTheme } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Menu as MenuIcon, Close as CloseIcon } from '@mui/icons-material';
import { useState } from 'react';

const Navbar = () => {
  const navigate = useNavigate();
  const { isAuthenticated, logout } = useAuth();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <AppBar position="fixed" sx={{ top: 0, zIndex: 1300 }}>
      <Toolbar sx={{ 
        px: { xs: 1, sm: 2, md: 3 },
        justifyContent: 'space-between',
        minHeight: { xs: 56, sm: 64 }
      }}>
        <Typography 
          variant="h6" 
          component="div" 
          sx={{ 
            flexGrow: 1, 
            cursor: 'pointer', 
            textAlign: 'left',
            fontWeight: 700,
            fontSize: { xs: '1.1rem', sm: '1.25rem' }
          }}
          onClick={() => navigate('/')}
        >
          Planventure
        </Typography>
        
        {!isMobile && (
          <Stack direction="row" spacing={1}>
            {isAuthenticated ? (
              <>
                <Button 
                  color="inherit" 
                  onClick={() => navigate('/trips')}
                  sx={{ fontSize: { sm: '0.875rem', md: '1rem' } }}
                >
                  My Trips
                </Button>
                <Button 
                  color="inherit" 
                  variant="outlined" 
                  onClick={handleLogout}
                  sx={{ borderColor: 'inherit', fontSize: { sm: '0.875rem', md: '1rem' } }}
                >
                  Logout
                </Button>
              </>
            ) : (
              <>
                <Button 
                  color="inherit" 
                  onClick={() => navigate('/login')}
                  sx={{ fontSize: { sm: '0.875rem', md: '1rem' } }}
                >
                  Login
                </Button>
                <Button 
                  color="inherit" 
                  variant="outlined" 
                  onClick={() => navigate('/signup')}
                  sx={{ borderColor: 'inherit', fontSize: { sm: '0.875rem', md: '1rem' } }}
                >
                  Sign Up
                </Button>
              </>
            )}
          </Stack>
        )}

        {isMobile && (
          <IconButton
            color="inherit"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            sx={{ ml: 1 }}
          >
            {mobileMenuOpen ? <CloseIcon /> : <MenuIcon />}
          </IconButton>
        )}
      </Toolbar>

      {isMobile && mobileMenuOpen && (
        <Box sx={{ 
          px: 2, 
          py: 2, 
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          display: 'flex',
          flexDirection: 'column',
          gap: 1
        }}>
          {isAuthenticated ? (
            <>
              <Button 
                color="inherit" 
                fullWidth
                onClick={() => {
                  navigate('/trips');
                  setMobileMenuOpen(false);
                }}
                sx={{ justifyContent: 'flex-start' }}
              >
                My Trips
              </Button>
              <Button 
                color="inherit" 
                fullWidth
                variant="outlined"
                onClick={() => {
                  handleLogout();
                  setMobileMenuOpen(false);
                }}
                sx={{ borderColor: 'inherit', justifyContent: 'flex-start' }}
              >
                Logout
              </Button>
            </>
          ) : (
            <>
              <Button 
                color="inherit" 
                fullWidth
                onClick={() => {
                  navigate('/login');
                  setMobileMenuOpen(false);
                }}
                sx={{ justifyContent: 'flex-start' }}
              >
                Login
              </Button>
              <Button 
                color="inherit" 
                fullWidth
                variant="outlined"
                onClick={() => {
                  navigate('/signup');
                  setMobileMenuOpen(false);
                }}
                sx={{ borderColor: 'inherit', justifyContent: 'flex-start' }}
              >
                Sign Up
              </Button>
            </>
          )}
        </Box>
      )}
    </AppBar>
  );
};

export default Navbar;