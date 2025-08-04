import { useQuery } from '@tanstack/react-query';
import { dashboardApi, PositionStatusResponse } from '@/api/dashboard';
import type { IndicatorsGridResponse } from '@/types/dashboard';

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