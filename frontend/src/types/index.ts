// Re-export types from the static app and add new ones
export interface CommodityIndicator {
  value: number;
  min: number;
  max: number;
  label: string;
  color?: string;
}

export interface DailyRecommendation {
  id: number;
  text: string;
}

export interface MarketNews {
  id: number;
  date: string;
  author: string;
  title: string;
  content: string;
}

export interface WeatherUpdate {
  id: number;
  date: string;
  region: string;
  description: string;
  impact: string;
}

export interface HistoricalDataPoint {
  date: string;
  price: number;
  volume: number;
  rsi: number;
  stockUs: number;
  stockEu: number;
  atr: number;
  openInterest: number;
  macd: number;
  pivot: number;
}

export interface DashboardData {
  date: string;
  positionOfDay: "OPEN" | "CLOSED";
  ytdPerformance: number;
  indicators: {
    dayIndicator: CommodityIndicator;
    macroeco: CommodityIndicator;
    rsi: CommodityIndicator;
    macd: CommodityIndicator;
    percentK: CommodityIndicator;
    atr: CommodityIndicator;
    volOi: CommodityIndicator;
  };
  recommendations: DailyRecommendation[];
  chartData?: HistoricalDataPoint[];
  lastPress: MarketNews;
  weatherUpdates: WeatherUpdate[];
}

export interface Commodity {
  id: number;
  symbol: string;
  name: string;
  category: string;
  description?: string;
}

export interface HistoricalData {
  commodity_id: number;
  start_date: string;
  end_date: string;
  data: HistoricalDataPoint[];
}

export interface User {
  sub: string;
  email: string;
  name: string;
  permissions: string[];
}
