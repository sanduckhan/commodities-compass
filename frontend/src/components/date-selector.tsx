'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { CalendarIcon, ChevronLeftIcon, ChevronRightIcon } from 'lucide-react';

interface DateSelectorProps {
  currentDate: string;
  onDateChange: (date: string) => void;
  className?: string;
}

export default function DateSelector({
  currentDate,
  onDateChange,
  className,
}: DateSelectorProps) {
  // Handle navigation between dates - go one day back/forward
  const handlePrevious = () => {
    const date = new Date(currentDate);
    date.setDate(date.getDate() - 1);
    const newDate = date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long', 
      day: 'numeric'
    });
    onDateChange(newDate);
  };

  const handleNext = () => {
    const date = new Date(currentDate);
    date.setDate(date.getDate() + 1);
    const today = new Date();
    
    // Don't allow going beyond today
    if (date <= today) {
      const newDate = date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
      onDateChange(newDate);
    }
  };

  // Format date for display
  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  return (
    <Card className={className}>
      <CardContent className="p-4">
        <div className="flex items-center justify-between gap-2">
          <Button
            variant="outline"
            size="icon"
            onClick={handlePrevious}
          >
            <ChevronLeftIcon className="h-4 w-4" />
          </Button>

          <div className="flex items-center gap-2 min-w-[280px] justify-center">
            <CalendarIcon className="h-5 w-5 text-gray-500 hidden sm:block" />

            <div className="font-medium text-center">
              {formatDate(currentDate)}
            </div>
          </div>

          <Button
            variant="outline"
            size="icon"
            onClick={handleNext}
            disabled={new Date(currentDate).toDateString() === new Date().toDateString()}
          >
            <ChevronRightIcon className="h-4 w-4" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
