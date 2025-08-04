import { useQuery } from '@tanstack/react-query';
import { dashboardApi, PositionStatusResponse } from '@/api/dashboard';
import type { IndicatorsGridResponse, RecommendationsResponse, ChartDataResponse } from '@/types/dashboard';

export const usePositionStatus = (targetDate?: string) => {
  return useQuery<PositionStatusResponse>({
    queryKey: ['position-status', targetDate],
    queryFn: () => dashboardApi.getPositionStatus(targetDate),
    staleTime: 24 * 60 * 60 * 1000, // Consider data fresh for 24 hours
    refetchInterval: false, // No automatic refetching
    refetchOnWindowFocus: false, // Don't refetch when window regains focus
    refetchOnMount: false, // Don't refetch when component mounts if data exists
  });
};

export const useIndicatorsGrid = (targetDate?: string) => {
  return useQuery<IndicatorsGridResponse>({
    queryKey: ['indicators-grid', targetDate],
    queryFn: () => dashboardApi.getIndicatorsGrid(targetDate),
    staleTime: 24 * 60 * 60 * 1000, // Consider data fresh for 24 hours
    refetchInterval: false, // No automatic refetching
    refetchOnWindowFocus: false, // Don't refetch when window regains focus
    refetchOnMount: false, // Don't refetch when component mounts if data exists
  });
};

export const useRecommendations = (targetDate?: string) => {
  return useQuery<RecommendationsResponse>({
    queryKey: ['recommendations', targetDate],
    queryFn: () => dashboardApi.getRecommendations(targetDate),
    staleTime: 24 * 60 * 60 * 1000, // Consider data fresh for 24 hours
    refetchInterval: false, // No automatic refetching
    refetchOnWindowFocus: false, // Don't refetch when window regains focus
    refetchOnMount: false, // Don't refetch when component mounts if data exists
  });
};

export const useChartData = (days: number = 30) => {
  return useQuery<ChartDataResponse>({
    queryKey: ['chart-data', days],
    queryFn: () => dashboardApi.getChartData(days),
    staleTime: 24 * 60 * 60 * 1000, // Consider data fresh for 24 hours
    refetchInterval: false, // No automatic refetching
    refetchOnWindowFocus: false, // Don't refetch when window regains focus
    refetchOnMount: false, // Don't refetch when component mounts if data exists
  });
};