import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth0 } from '@auth0/auth0-react';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { ShieldCheckIcon } from 'lucide-react';
import fullLogo from '@/assets/logo_big.png';

export default function LoginPage() {
  const navigate = useNavigate();
  const { loginWithRedirect, isAuthenticated, isLoading, error } = useAuth0();

  useEffect(() => {
    // Only redirect if authenticated AND we have a valid token
    if (isAuthenticated && !error) {
      const token = localStorage.getItem('auth0_token');
      if (token) {
        navigate('/dashboard');
      }
    }
  }, [isAuthenticated, error, navigate]);

  const handleLogin = () => {
    loginWithRedirect({
      appState: { returnTo: '/dashboard' },
    });
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50 dark:bg-gray-900">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <div className="w-full max-w-md px-6">
        {/* Logo and Title Section */}
        <div className="text-center mb-8">
          <img
            src={fullLogo}
            alt="Commodities Compass"
            className="h-64 w-auto object-contain mx-auto mb-6"
          />
          <p className="text-lg text-gray-600 dark:text-gray-400">
            Professional market insights for commodity traders
          </p>
        </div>

        {/* Login Card */}
        <Card className="shadow-xl border-0">
          <CardHeader className="space-y-1 pb-6">
            <CardTitle className="text-2xl text-center">Sign in to your account</CardTitle>
            <CardDescription className="text-center">
              Use your organization credentials to access your dashboard
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <Button
              onClick={handleLogin}
              className="w-full h-12 text-base font-medium"
              size="lg"
              disabled={isLoading}
            >
              <ShieldCheckIcon className="mr-2 h-5 w-5" />
              {isLoading ? 'Connecting...' : 'Sign in with Auth0'}
            </Button>

            <div className="relative my-6">
              <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t border-gray-300 dark:border-gray-600" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-card px-4 text-muted-foreground">
                  Secure authentication
                </span>
              </div>
            </div>

            <div className="bg-gray-50 dark:bg-gray-800/50 rounded-lg p-4">
              <p className="text-sm text-center text-gray-600 dark:text-gray-400">
                <span className="inline-flex items-center gap-1">
                  <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                  Your credentials are protected with enterprise-grade encryption
                </span>
              </p>
            </div>
          </CardContent>
          <CardFooter className="pt-4">
            <p className="text-xs text-center text-muted-foreground w-full">
              By signing in, you agree to our Terms of Service and Privacy Policy
            </p>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}
