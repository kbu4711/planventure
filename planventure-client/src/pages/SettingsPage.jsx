import { Box, Typography, Paper, List, ListItem, ListItemIcon, ListItemText, Switch, Divider } from '@mui/material';
import { 
  Notifications as NotificationsIcon,
  Lock as LockIcon,
  Visibility as VisibilityIcon,
  Language as LanguageIcon,
  Help as HelpIcon
} from '@mui/icons-material';
import { useState } from 'react';

const SettingsPage = () => {
  const [settings, setSettings] = useState({
    notifications: true,
    emailUpdates: true,
    privateProfile: false,
    darkMode: false
  });

  const handleSettingChange = (setting) => {
    setSettings({
      ...settings,
      [setting]: !settings[setting]
    });
  };

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
          Settings
        </Typography>
        <Typography 
          variant="body2" 
          color="text.secondary"
          sx={{ fontSize: { xs: '0.875rem', sm: '1rem' } }}
        >
          Manage your preferences and account settings
        </Typography>
      </Box>

      <Box
        sx={{
          px: { xs: 1, sm: 1.5, md: 2, lg: 2.5 },
          py: 2
        }}
      >
        {/* Notifications Section */}
        <Paper elevation={0} sx={{ mb: 3, borderRadius: 2, border: '1px solid', borderColor: 'divider' }}>
          <Box sx={{ p: 3, backgroundColor: 'background.paper' }}>
            <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>
              Notifications
            </Typography>
            <List sx={{ p: 0 }}>
              <ListItem sx={{ pl: 0, pr: 0, justifyContent: 'space-between' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <ListItemIcon sx={{ minWidth: 40 }}>
                    <NotificationsIcon color="primary" />
                  </ListItemIcon>
                  <Box>
                    <ListItemText 
                      primary="Push Notifications"
                      secondary="Receive alerts about your trips"
                    />
                  </Box>
                </Box>
                <Switch
                  checked={settings.notifications}
                  onChange={() => handleSettingChange('notifications')}
                />
              </ListItem>
              <Divider sx={{ my: 1 }} />
              <ListItem sx={{ pl: 0, pr: 0, justifyContent: 'space-between' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <ListItemIcon sx={{ minWidth: 40 }}>
                    <NotificationsIcon color="primary" />
                  </ListItemIcon>
                  <Box>
                    <ListItemText 
                      primary="Email Updates"
                      secondary="Get updates about new features and events"
                    />
                  </Box>
                </Box>
                <Switch
                  checked={settings.emailUpdates}
                  onChange={() => handleSettingChange('emailUpdates')}
                />
              </ListItem>
            </List>
          </Box>
        </Paper>

        {/* Privacy Section */}
        <Paper elevation={0} sx={{ mb: 3, borderRadius: 2, border: '1px solid', borderColor: 'divider' }}>
          <Box sx={{ p: 3, backgroundColor: 'background.paper' }}>
            <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>
              Privacy & Security
            </Typography>
            <List sx={{ p: 0 }}>
              <ListItem sx={{ pl: 0, pr: 0, justifyContent: 'space-between' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <ListItemIcon sx={{ minWidth: 40 }}>
                    <VisibilityIcon color="primary" />
                  </ListItemIcon>
                  <Box>
                    <ListItemText 
                      primary="Private Profile"
                      secondary="Only you can see your trips"
                    />
                  </Box>
                </Box>
                <Switch
                  checked={settings.privateProfile}
                  onChange={() => handleSettingChange('privateProfile')}
                />
              </ListItem>
              <Divider sx={{ my: 1 }} />
              <ListItem sx={{ pl: 0, pr: 0, justifyContent: 'space-between' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <ListItemIcon sx={{ minWidth: 40 }}>
                    <LockIcon color="primary" />
                  </ListItemIcon>
                  <Box>
                    <ListItemText 
                      primary="Change Password"
                      secondary="Update your account password"
                    />
                  </Box>
                </Box>
                <Typography variant="body2" color="primary" sx={{ cursor: 'pointer', fontWeight: 600 }}>
                  Change
                </Typography>
              </ListItem>
            </List>
          </Box>
        </Paper>

        {/* Preferences Section */}
        <Paper elevation={0} sx={{ borderRadius: 2, border: '1px solid', borderColor: 'divider' }}>
          <Box sx={{ p: 3, backgroundColor: 'background.paper' }}>
            <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>
              Preferences
            </Typography>
            <List sx={{ p: 0 }}>
              <ListItem sx={{ pl: 0, pr: 0, justifyContent: 'space-between' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <ListItemIcon sx={{ minWidth: 40 }}>
                    <LanguageIcon color="primary" />
                  </ListItemIcon>
                  <Box>
                    <ListItemText 
                      primary="Language"
                      secondary="English (US)"
                    />
                  </Box>
                </Box>
              </ListItem>
              <Divider sx={{ my: 1 }} />
              <ListItem sx={{ pl: 0, pr: 0, justifyContent: 'space-between' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <ListItemIcon sx={{ minWidth: 40 }}>
                    <HelpIcon color="primary" />
                  </ListItemIcon>
                  <Box>
                    <ListItemText 
                      primary="Help & Support"
                      secondary="Get help or contact us"
                    />
                  </Box>
                </Box>
              </ListItem>
            </List>
          </Box>
        </Paper>
      </Box>
    </Box>
  );
};

export default SettingsPage;
