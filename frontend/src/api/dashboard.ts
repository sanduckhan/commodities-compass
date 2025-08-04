import { apiClient } from './client';
import type { PositionStatusResponse, IndicatorsGridResponse } from '@/types/dashboard';

export const dashboardApi = {
  getPositionStatus: async (targetDate?: string): Promise<PositionStatusResponse> => {
    const params = targetDate ? { target_date: targetDate } : {};
    const response = await apiClient.get('/dashboard/position-status', { params });
    return response.data;
  },
  
  getIndicatorsGrid: async (targetDate?: string): Promise<IndicatorsGridResponse> => {
    const params = targetDate ? { target_date: targetDate } : {};
    const response = await apiClient.get('/dashboard/indicators-grid', { params });
    return response.data;
  },
};