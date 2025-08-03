import { apiClient } from './client';
import { DashboardData, Commodity, HistoricalData } from '../types';

export const api = {
  // Auth endpoints
  auth: {
    me: () => apiClient.get('/auth/me'),
    verify: () => apiClient.get('/auth/verify'),
  },

  // Dashboard endpoints
  dashboard: {
    getData: (date?: string) =>
      apiClient.get<DashboardData>('/dashboard', { params: { target_date: date } }),
    getSummary: () =>
      apiClient.get('/dashboard/summary'),
  },

  // Commodities endpoints
  commodities: {
    getAll: () =>
      apiClient.get<Commodity[]>('/commodities'),
    getById: (id: number) =>
      apiClient.get<Commodity>(`/commodities/${id}`),
  },

  // Historical data endpoints
  historical: {
    getData: (commodityId: number, startDate?: string, endDate?: string) =>
      apiClient.get<HistoricalData>(`/historical/${commodityId}`, {
        params: { start_date: startDate, end_date: endDate },
      }),
    getIndicator: (commodityId: number, indicator: string, period: number = 30) =>
      apiClient.get(`/historical/${commodityId}/indicators`, {
        params: { indicator, period },
      }),
  },
};
