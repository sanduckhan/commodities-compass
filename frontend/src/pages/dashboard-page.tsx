"use client";

import DateSelector from "@/components/date-selector";
import IndicatorsGrid from "@/components/indicators-grid";
import NewsCard from "@/components/news-card";
import PositionStatus from "@/components/position-status";
import PriceChart from "@/components/price-chart";
import RecommendationsList from "@/components/recommendations-list";
import WeatherUpdateCard from "@/components/weather-update-card";
import {
  HISTORICAL_DATA,
  METRIC_OPTIONS,
} from "@/data/commodities-data";
import { useState } from "react";

// Convert date string to ISO format for API
const convertToISODate = (dateStr: string): string | undefined => {
  try {
    const date = new Date(dateStr);
    return date.toISOString().split('T')[0]; // YYYY-MM-DD format
  } catch {
    return undefined;
  }
};

export default function DashboardPage() {
  const today = new Date().toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });
  const [currentDate, setCurrentDate] = useState(today);
  const [selectedMetric, setSelectedMetric] = useState("close");

  // Get the data for the selected date
  const currentData =
    HISTORICAL_DATA.find((data) => data.date === currentDate) ||
    HISTORICAL_DATA[0];


  // Find the selected metric configuration
  const metricConfig =
    METRIC_OPTIONS.find((option) => option.value === selectedMetric) ||
    METRIC_OPTIONS[0];

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row gap-4 items-start md:items-center justify-between">
        <h1 className="text-2xl font-bold">Commodities Dashboard</h1>
        <DateSelector
          currentDate={currentDate}
          onDateChange={setCurrentDate}
          className="w-full md:w-auto"
        />
      </div>

      <PositionStatus
        targetDate={convertToISODate(currentDate)}
      />

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        <div className="lg:col-span-2">
          <IndicatorsGrid
            targetDate={convertToISODate(currentDate)}
          />
        </div>
        <div className="lg:col-span-3">
          <RecommendationsList targetDate={convertToISODate(currentDate)} />
        </div>
      </div>

      <div>
        <PriceChart
          title={`${metricConfig.label} Trend`}
          selectedMetric={selectedMetric}
          onMetricChange={setSelectedMetric}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <NewsCard news={currentData.lastPress} />

        <WeatherUpdateCard weatherUpdate={currentData.weatherUpdates[0]} />
      </div>
    </div>
  );
}
