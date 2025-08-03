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

export default function DashboardPage() {
  const [currentDate, setCurrentDate] = useState(HISTORICAL_DATA[0].date);
  const [selectedMetric, setSelectedMetric] = useState("price");

  // Get the data for the selected date
  const currentData =
    HISTORICAL_DATA.find((data) => data.date === currentDate) ||
    HISTORICAL_DATA[0];

  // Get all available dates
  const availableDates = HISTORICAL_DATA.map((data) => data.date);

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
          availableDates={availableDates}
          onDateChange={setCurrentDate}
          className="w-full md:w-auto"
        />
      </div>

      <PositionStatus
        position={currentData.positionOfDay}
        ytdPerformance={currentData.ytdPerformance}
        dayIndicator={currentData.indicators.dayIndicator}
      />

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        <div className="lg:col-span-2">
          <IndicatorsGrid
            indicators={{
              macroeco: currentData.indicators.macroeco,
              rsi: currentData.indicators.rsi,
              macd: currentData.indicators.macd,
              percentK: currentData.indicators.percentK,
              atr: currentData.indicators.atr,
              volOi: currentData.indicators.volOi,
            }}
          />
        </div>
        <div className="lg:col-span-3">
          <RecommendationsList recommendations={currentData.recommendations} />
        </div>
      </div>

      <div>
        <PriceChart
          data={currentData.chartData}
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
