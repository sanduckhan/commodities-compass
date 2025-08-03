import { useAuth0 } from '@auth0/auth0-react';
import { useEffect } from 'react';

export const useAuth = () => {
  const { user, logout, getAccessTokenSilently, isLoading, isAuthenticated, error } = useAuth0();

  // Store token in localStorage for API calls
  useEffect(() => {
    const storeToken = async () => {
      if (isAuthenticated) {
        try {
          const token = await getAccessTokenSilently();
          localStorage.setItem('auth0_token', token);
        } catch (error) {
          console.error('Error getting access token:', error);
        }
      }
    };

    storeToken();
  }, [isAuthenticated, getAccessTokenSilently]);

  // Handle logout
  const handleLogout = () => {
    // Clear stored tokens
    localStorage.removeItem('auth0_token');
    
    // Logout from Auth0 and redirect to homepage
    logout({
      logoutParams: {
        returnTo: window.location.origin
      }
    });
  };

  return {
    user,
    logout: handleLogout,
    isLoading,
    isAuthenticated,
    error,
  };
};