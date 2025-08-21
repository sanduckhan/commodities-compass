'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { CalendarIcon, ChevronLeftIcon, ChevronRightIcon } from 'lucide-react';
import { DatePicker } from 'antd';
import type { Dayjs } from 'dayjs';
import dayjs from 'dayjs';
import { useState } from 'react';
import 'dayjs/locale/en';

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
  const [isOpen, setIsOpen] = useState(false);

  // Convert string date to dayjs object
  const currentDayjs = dayjs(currentDate);

  // Helper function to check if a date is a weekend
  const isWeekend = (date: Dayjs) => {
    const day = date.day();
    return day === 0 || day === 6; // Sunday = 0, Saturday = 6
  };

  // Helper function to get the next business day
  const getNextBusinessDay = (date: Date, direction: 'forward' | 'backward') => {
    const newDate = new Date(date);
    const increment = direction === 'forward' ? 1 : -1;
    
    do {
      newDate.setDate(newDate.getDate() + increment);
    } while (isWeekend(dayjs(newDate)));
    
    return newDate;
  };

  // Handle navigation to previous business day
  const handlePrevious = () => {
    const date = new Date(currentDate);
    const previousBusinessDay = getNextBusinessDay(date, 'backward');
    
    const newDate = previousBusinessDay.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
    onDateChange(newDate);
  };

  // Handle navigation to next business day
  const handleNext = () => {
    const date = new Date(currentDate);
    const nextBusinessDay = getNextBusinessDay(date, 'forward');
    const today = new Date();
    
    // Don't allow going beyond today
    if (nextBusinessDay <= today) {
      const newDate = nextBusinessDay.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
      onDateChange(newDate);
    }
  };

  // Handle date selection from calendar
  const handleCalendarChange = (date: Dayjs | null) => {
    if (date) {
      const newDate = date.toDate().toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
      onDateChange(newDate);
      setIsOpen(false);
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


  // Check if next button should be disabled
  const isNextDisabled = () => {
    const nextBusinessDay = getNextBusinessDay(new Date(currentDate), 'forward');
    return nextBusinessDay > new Date();
  };

  // Disable weekends and future dates
  const disabledDate = (current: Dayjs) => {
    const today = dayjs().endOf('day');
    return isWeekend(current) || current.isAfter(today);
  };

  return (
    <Card className={className}>
      <CardContent className="p-4">
        <div className="flex items-center justify-between gap-2 date-selector-container relative">
          <Button
            variant="outline"
            size="icon"
            onClick={handlePrevious}
            title="Previous business day"
          >
            <ChevronLeftIcon className="h-4 w-4" />
          </Button>

          <div className="relative flex-1 flex justify-center">
            <div className="relative">
              <Button
                variant="ghost"
                className="min-w-[280px] justify-center font-medium hover:bg-accent h-10 px-4 flex items-center gap-2"
                onClick={() => setIsOpen(!isOpen)}
              >
                <CalendarIcon className="h-5 w-5 text-gray-500" />
                <span>{formatDate(currentDate)}</span>
              </Button>
              
              <DatePicker
                value={currentDayjs}
                onChange={handleCalendarChange}
                disabledDate={disabledDate}
                open={isOpen}
                onOpenChange={setIsOpen}
                allowClear={false}
                placement="bottom"
                style={{ 
                  position: 'absolute',
                  left: 0,
                  top: 0,
                  width: '100%',
                  height: '100%',
                  opacity: 0,
                  pointerEvents: 'none'
                }}
                popupAlign={{
                  points: ['tc', 'bc'],
                  offset: [0, 4]
                }}
                getPopupContainer={(trigger) => trigger?.closest('.date-selector-container') || document.body}
              />
            </div>
          </div>

          <Button
            variant="outline"
            size="icon"
            onClick={handleNext}
            disabled={isNextDisabled()}
            title="Next business day"
          >
            <ChevronRightIcon className="h-4 w-4" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}