import { 
  Card, 
  CardContent, 
  Typography, 
  CardActions, 
  Button,
  Chip,
  Box,
  Skeleton,
  Stack
} from '@mui/material';
import { 
  LocationOn, 
  DateRange,
  ArrowForward,
  TrendingUp,
  TrendingDown
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const TripCard = ({ trip, loading }) => {
  const navigate = useNavigate();

  const calculateDuration = (startDate, endDate) => {
    const start = new Date(startDate);
    const end = new Date(endDate);
    const days = Math.ceil((end - start) / (1000 * 60 * 60 * 24)) + 1;
    return days;
  };

  const isUpcoming = (startDate) => {
    return new Date(startDate) > new Date();
  };

  if (loading) {
    return (
      <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
        <Skeleton variant="rectangular" height={140} />
        <CardContent>
          <Skeleton variant="text" height={32} width="80%" />
          <Skeleton variant="text" height={24} width="60%" />
          <Skeleton variant="text" height={24} width="40%" />
        </CardContent>
        <CardActions>
          <Skeleton variant="rectangular" width={100} height={36} />
        </CardActions>
      </Card>
    );
  }

  const duration = calculateDuration(trip.start_date, trip.end_date);
  const upcoming = isUpcoming(trip.start_date);
  const startDate = new Date(trip.start_date);
  const endDate = new Date(trip.end_date);

  return (
    <Card 
      sx={{ 
        height: '100%',
        width: '100%',
        minWidth: 220,
        maxWidth: 380,
        display: 'flex', 
        flexDirection: 'column',
        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        cursor: 'pointer',
        '&:hover': {
          elevation: 8,
          transform: 'translateY(-8px)',
          boxShadow: '0 12px 32px rgba(79, 70, 229, 0.15)'
        }
      }}
      onClick={() => navigate(`/trips/${trip.id}`)}
    >
      <Box 
        sx={{ 
          background: upcoming 
            ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
            : 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
          height: 140,
          display: 'flex',
          alignItems: 'flex-end',
          justifyContent: 'space-between',
          p: 2,
          color: 'white'
        }}
      >
        <Box>
          <Typography variant="body2" sx={{ opacity: 0.9, fontWeight: 500 }}>
            {duration} days
          </Typography>
        </Box>
        <Chip
          icon={upcoming ? <TrendingUp /> : <TrendingDown />}
          label={upcoming ? 'Upcoming' : 'Past'}
          size="small"
          sx={{
            backgroundColor: 'rgba(255, 255, 255, 0.25)',
            color: 'white',
            fontWeight: 600
          }}
        />
      </Box>

      <CardContent sx={{ flexGrow: 1, minHeight: 180 }}>
        <Typography 
          gutterBottom 
          variant="h6" 
          component="h2"
          sx={{ 
            fontWeight: 700,
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            display: '-webkit-box',
            WebkitLineClamp: 2,
            WebkitBoxOrient: 'vertical',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            mb: 2
          }}
        >
          {trip.title}
        </Typography>

        <Stack spacing={1} sx={{ mt: 1 }}>
          <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1 }}>
            <LocationOn 
              fontSize="small" 
              sx={{ color: 'primary.main', flexShrink: 0, mt: 0.3 }} 
            />
            <Typography 
              variant="body2" 
              color="text.secondary" 
              sx={{ 
                fontWeight: 500,
                display: '-webkit-box',
                WebkitLineClamp: 2,
                WebkitBoxOrient: 'vertical',
                overflow: 'hidden',
                textOverflow: 'ellipsis'
              }}
            >
              {trip.destination}
            </Typography>
          </Box>

          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <DateRange 
              fontSize="small" 
              sx={{ color: 'primary.main', flexShrink: 0 }} 
            />
            <Typography 
              variant="caption" 
              color="text.secondary"
              sx={{ fontWeight: 500, whiteSpace: 'nowrap' }}
            >
              {startDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })} - {endDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: '2-digit' })}
            </Typography>
          </Box>
        </Stack>
      </CardContent>

      <CardActions sx={{ pt: 0 }}>
        <Button 
          size="small" 
          endIcon={<ArrowForward />}
          onClick={(e) => {
            e.stopPropagation();
            navigate(`/trips/${trip.id}`);
          }}
          sx={{ fontWeight: 600, fontSize: { xs: '0.75rem', sm: '0.875rem' } }}
        >
          View Details
        </Button>
      </CardActions>
    </Card>
  );
};

export default TripCard;
