import { apiClient } from './client';
import type { PositionStatusResponse } from '@/types/dashboard';

export const dashboardApi = {
  getPositionStatus: async (targetDate?: string): Promise<PositionStatusResponse> => {
    const params = targetDate ? { target_date: targetDate } : {};
    const response = await apiClient.get('/dashboard/position-status', { params });
    return response.data;
  },
};