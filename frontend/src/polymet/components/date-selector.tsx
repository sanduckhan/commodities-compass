"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { CalendarIcon, ChevronLeftIcon, ChevronRightIcon } from "lucide-react";
import { useState } from "react";

interface DateSelectorProps {
  currentDate: string;
  availableDates: string[];
  onDateChange: (date: string) => void;
  className?: string;
}

export default function DateSelector({
  currentDate,
  availableDates,
  onDateChange,
  className,
}: DateSelectorProps) {
  // Find the index of the current date in the available dates array
  const currentIndex = availableDates.findIndex((date) => date === currentDate);

  // Handle navigation between dates
  const handlePrevious = () => {
    if (currentIndex < availableDates.length - 1) {
      onDateChange(availableDates[currentIndex + 1]);
    }
  };

  const handleNext = () => {
    if (currentIndex > 0) {
      onDateChange(availableDates[currentIndex - 1]);
    }
  };

  // Format date for display
  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString("en-US", {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
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
            disabled={currentIndex >= availableDates.length - 1}
          >
            <ChevronLeftIcon className="h-4 w-4" />
          </Button>

          <div className="flex-1 flex items-center gap-2">
            <CalendarIcon className="h-5 w-5 text-gray-500 hidden sm:block" />

            <div className="hidden md:block font-medium">
              {formatDate(currentDate)}
            </div>
            <div className="md:hidden w-full">
              <Select value={currentDate} onDateChange={onDateChange}>
                <SelectTrigger>
                  <SelectValue placeholder="Select date" />
                </SelectTrigger>
                <SelectContent>
                  {availableDates.map((date) => (
                    <SelectItem key={date} value={date}>
                      {formatDate(date)}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>

          <Button
            variant="outline"
            size="icon"
            onClick={handleNext}
            disabled={currentIndex <= 0}
          >
            <ChevronRightIcon className="h-4 w-4" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
