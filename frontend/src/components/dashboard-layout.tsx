'use client';

import { Button } from '@/components/ui/button';
import {
  MoonIcon,
  SunIcon,
  LayoutDashboardIcon,
  HistoryIcon,
  LogOutIcon,
} from 'lucide-react';
import { useState, useEffect } from 'react';
import { cn } from '@/utils';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Link } from 'react-router-dom';

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  // Check if mobile on mount and when window resizes
  useEffect(() => {
    const checkIfMobile = () => {
      if (window.innerWidth < 768) {
        setSidebarCollapsed(true);
      }
    };

    checkIfMobile();
    window.addEventListener('resize', checkIfMobile);

    return () => {
      window.removeEventListener('resize', checkIfMobile);
    };
  }, []);

  // Toggle theme
  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    document.documentElement.classList.toggle('dark', newTheme === 'dark');
  };

  return (
    <div className={cn('min-h-screen bg-gray-50 dark:bg-gray-900', theme)}>
      <div className="flex h-screen overflow-hidden">
        {/* Sidebar */}
        <aside
          className={cn(
            'flex flex-col h-full bg-background border-r transition-all duration-300 ease-in-out z-30',
            sidebarCollapsed ? 'w-16' : 'w-64'
          )}
        >
          {/* Logo and App Name */}
          <div className="flex items-center p-4 border-b">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary flex-shrink-0">
              <span className="text-lg font-bold text-primary-foreground">
                C
              </span>
            </div>
            {!sidebarCollapsed && (
              <div className="ml-3 flex flex-col">
                <span className="font-bold text-lg leading-tight">
                  Commodities
                </span>
                <span className="font-bold text-lg leading-tight">Compass</span>
              </div>
            )}
          </div>

          {/* Navigation */}
          <div className="flex-1 overflow-y-auto py-4">
            <nav className="px-2 space-y-1">
              <Button
                variant="ghost"
                className={cn(
                  'w-full justify-start',
                  sidebarCollapsed ? 'px-2' : 'px-3'
                )}
                asChild
              >
                <Link to="/dashboard">
                  <LayoutDashboardIcon
                    className={cn(
                      'h-5 w-5',
                      sidebarCollapsed ? 'mr-0' : 'mr-3'
                    )}
                  />

                  {!sidebarCollapsed && <span>Dashboard</span>}
                </Link>
              </Button>
              <Button
                variant="ghost"
                className={cn(
                  'w-full justify-start',
                  sidebarCollapsed ? 'px-2' : 'px-3'
                )}
                asChild
              >
                <Link to="/dashboard/historical">
                  <HistoryIcon
                    className={cn(
                      'h-5 w-5',
                      sidebarCollapsed ? 'mr-0' : 'mr-3'
                    )}
                  />

                  {!sidebarCollapsed && <span>Historical Data</span>}
                </Link>
              </Button>
            </nav>
          </div>

          {/* User profile at bottom */}
          <div className="border-t p-4">
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button
                  variant="ghost"
                  className={cn(
                    'w-full flex items-center',
                    sidebarCollapsed ? 'justify-center' : 'justify-start'
                  )}
                >
                  <Avatar className="h-8 w-8">
                    <AvatarImage
                      src="https://github.com/yusufhilmi.png"
                      alt="User"
                    />

                    <AvatarFallback>U</AvatarFallback>
                  </Avatar>
                  {!sidebarCollapsed && (
                    <span className="ml-3 truncate">User Profile</span>
                  )}
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" side="right">
                <DropdownMenuLabel>My Account</DropdownMenuLabel>
                <DropdownMenuSeparator />

                <DropdownMenuItem onClick={toggleTheme}>
                  {theme === 'light' ? (
                    <MoonIcon className="mr-2 h-4 w-4" />
                  ) : (
                    <SunIcon className="mr-2 h-4 w-4" />
                  )}
                  {theme === 'light' ? 'Dark Mode' : 'Light Mode'}
                </DropdownMenuItem>
                <DropdownMenuSeparator />

                <DropdownMenuItem>
                  <Link to="/login" className="flex w-full items-center">
                    <LogOutIcon className="mr-2 h-4 w-4" />
                    Log out
                  </Link>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </aside>

        {/* Main content */}
        <main className="flex-1 overflow-y-auto p-4 md:p-6">{children}</main>
      </div>
    </div>
  );
}
