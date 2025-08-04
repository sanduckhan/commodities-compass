export interface IndicatorRange {
  range_low: number;
  range_high: number;
  area: 'RED' | 'ORANGE' | 'GREEN';
}

export interface CommodityIndicator {
  value: number;
  min: number;
  max: number;
  label: string;
  ranges?: IndicatorRange[];
}

export interface PositionStatusResponse {
  date: string;
  position: 'OPEN' | 'HEDGE' | 'MONITOR';
  ytd_performance: number;
}

export interface IndicatorsGridResponse {
  date: string;
  indicators: {
    [key: string]: CommodityIndicator;
  };
}

export interface RecommendationsResponse {
  date: string;
  recommendations: string[];
  raw_score: string | null;
}

export interface ChartDataPoint {
  date: string;
  close?: number | null;
  volume?: number | null;
  open_interest?: number | null;
  rsi_14d?: number | null;
  macd?: number | null;
  stock_us?: number | null;
  com_net_us?: number | null;
}

export interface ChartDataResponse {
  data: ChartDataPoint[];
}

export interface NewsResponse {
  date: string;
  title: string;
  content: string;
  author: string | null;
}

export interface WeatherResponse {
  date: string;
  description: string;
  impact: string;
}