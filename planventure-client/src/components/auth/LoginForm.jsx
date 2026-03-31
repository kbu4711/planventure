import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { 
  Box, 
  TextField, 
  Button, 
  Typography, 
  Alert,
  InputAdornment,
  IconButton,
  Link,
  CircularProgress
} from '@mui/material';
import { Visibility, VisibilityOff, Email, Lock } from '@mui/icons-material';
import { useAuth } from '../../context/AuthContext';
import { api } from '../../services/api';

const LoginForm = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, setIsAuthenticated } = useAuth();
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [formErrors, setFormErrors] = useState({
    email: '',
    password: ''
  });

  // Add state for success message
  const [successMessage, setSuccessMessage] = useState(
    location.state?.message || ''
  );

  // Pre-fill email if coming from signup
  useEffect(() => {
    if (location.state?.email) {
      setFormData(prev => ({
        ...prev,
        email: location.state.email
      }));
    }
  }, [location.state]);

  const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email.trim()) return 'Email address is required';
    if (!re.test(email)) return 'Please enter a valid email address';
    return '';
  };

  const validatePassword = (password) => {
    if (!password) return 'Password is required';
    if (password.length < 6) return 'Password must be at least 6 characters long';
    return '';
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear errors when user types
    setFormErrors(prev => ({
      ...prev,
      [name]: ''
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate form
    const emailError = validateEmail(formData.email);
    const passwordError = validatePassword(formData.password);
    
    if (emailError || passwordError) {
      setFormErrors({
        email: emailError,
        password: passwordError
      });
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const response = await api.auth.login(formData);
      console.log('Login response:', response);
      console.log('Response token:', response?.token);

      if (response && response.token) {
        login(response); // Pass the entire response
        console.log('Login successful, redirecting to dashboard...');
        navigate('/dashboard', { replace: true });
      } else {
        console.error('Invalid login response - no token present:', response);
        setError('Invalid email or password');
      }
    } catch (err) {
      console.error('Login error:', err);
      setError(err.message || 'An error occurred during login');
    } finally {
      setIsLoading(false);
    }
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{
        width: '100%',
        display: 'flex',
        flexDirection: 'column',
        gap: 2.5
      }}
    >
      {/* Header */}
      <Box sx={{ textAlign: 'center', mb: 1 }}>
        <Typography 
          variant="h4" 
          component="h1" 
          sx={{ 
            fontWeight: 700,
            background: 'linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            mb: 0.5
          }}
        >
          Welcome Back
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Sign in to your account to continue
        </Typography>
      </Box>

      {/* Success Alert */}
      {successMessage && (
        <Alert 
          severity="success" 
          sx={{ 
            mb: 1,
            borderRadius: 2,
            animation: 'slideDown 0.3s ease-in-out'
          }}
        >
          {successMessage}
        </Alert>
      )}

      {/* Error Alert */}
      {error && (
        <Alert 
          severity="error" 
          sx={{ 
            mb: 1,
            borderRadius: 2,
            animation: 'slideDown 0.3s ease-in-out'
          }}
        >
          {error}
        </Alert>
      )}

      {/* Email Field */}
      <TextField
        fullWidth
        label="Email Address"
        name="email"
        type="email"
        placeholder="you@example.com"
        value={formData.email}
        onChange={handleChange}
        error={!!formErrors.email}
        helperText={formErrors.email}
        disabled={isLoading}
        required
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <Email sx={{ color: formErrors.email ? 'error.main' : 'action.active', mr: 1 }} />
            </InputAdornment>
          ),
        }}
        sx={{
          '& .MuiOutlinedInput-root': {
            transition: 'all 0.2s ease',
            '&:hover': {
              boxShadow: '0 4px 12px rgba(79, 70, 229, 0.08)'
            },
            '&.Mui-focused': {
              boxShadow: '0 4px 20px rgba(79, 70, 229, 0.15)'
            }
          }
        }}
      />

      {/* Password Field */}
      <TextField
        fullWidth
        label="Password"
        name="password"
        type={showPassword ? 'text' : 'password'}
        placeholder="••••••"
        value={formData.password}
        onChange={handleChange}
        error={!!formErrors.password}
        helperText={formErrors.password}
        disabled={isLoading}
        required
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <Lock sx={{ color: formErrors.password ? 'error.main' : 'action.active', mr: 1 }} />
            </InputAdornment>
          ),
          endAdornment: (
            <InputAdornment position="end">
              <IconButton
                aria-label="toggle password visibility"
                onClick={togglePasswordVisibility}
                edge="end"
                disabled={isLoading}
              >
                {showPassword ? <VisibilityOff /> : <Visibility />}
              </IconButton>
            </InputAdornment>
          ),
        }}
        sx={{
          '& .MuiOutlinedInput-root': {
            transition: 'all 0.2s ease',
            '&:hover': {
              boxShadow: '0 4px 12px rgba(79, 70, 229, 0.08)'
            },
            '&.Mui-focused': {
              boxShadow: '0 4px 20px rgba(79, 70, 229, 0.15)'
            }
          }
        }}
      />

      {/* Submit Button */}
      <Button
        type="submit"
        variant="contained"
        color="primary"
        size="large"
        disabled={isLoading}
        sx={{ 
          mt: 1,
          py: 1.5,
          fontWeight: 600,
          fontSize: '1rem',
          textTransform: 'none',
          borderRadius: 2,
          background: 'linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%)',
          transition: 'all 0.3s ease',
          position: 'relative',
          overflow: 'hidden',
          '&:hover:not(:disabled)': {
            background: 'linear-gradient(135deg, #3730A3 0%, #6D28D9 100%)',
            transform: 'translateY(-2px)',
            boxShadow: '0 12px 24px rgba(79, 70, 229, 0.4)'
          },
          '&:disabled': {
            opacity: 0.7
          }
        }}
      >
        {isLoading ? (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <CircularProgress size={20} color="inherit" />
            <span>Signing in...</span>
          </Box>
        ) : (
          'Sign In'
        )}
      </Button>

      {/* Sign Up Link */}
      <Typography 
        variant="body2" 
        sx={{ 
          textAlign: 'center', 
          mt: 1,
          color: 'text.secondary'
        }}
      >
        Don't have an account?{' '}
        <Link
          component="button"
          type="button"
          variant="body2"
          onClick={(e) => {
            e.preventDefault();
            navigate('/signup');
          }}
          sx={{ 
            fontWeight: 600,
            textDecoration: 'none',
            color: 'primary.main',
            cursor: 'pointer',
            transition: 'color 0.2s ease',
            '&:hover': {
              color: 'primary.dark',
              textDecoration: 'underline'
            }
          }}
        >
          Create one now
        </Link>
      </Typography>
    </Box>
  );
};

export default LoginForm;