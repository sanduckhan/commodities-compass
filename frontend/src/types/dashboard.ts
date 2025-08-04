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