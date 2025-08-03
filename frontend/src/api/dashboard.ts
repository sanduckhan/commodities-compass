import { apiClient } from './client';

export interface CommodityIndicator {
  value: number;
  min: number;
  max: number;
  label: string;
}

export interface PositionStatusResponse {
  date: string;
  position: 'OPEN' | 'HEDGE' | 'MONITOR';
  day_indicator: CommodityIndicator | null;
}

export const dashboardApi = {
  getPositionStatus: async (targetDate?: string): Promise<PositionStatusResponse> => {
    const params = targetDate ? { target_date: targetDate } : {};
    const response = await apiClient.get('/dashboard/position-status', { params });
    return response.data;
  },
};