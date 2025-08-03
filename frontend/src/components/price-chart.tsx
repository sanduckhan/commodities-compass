'use client';

import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from '@/components/ui/chart';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Area, AreaChart, CartesianGrid, XAxis } from 'recharts';
import { DatePickerWithRange } from '@/components/date-range-picker';
import { Button } from '@/components/ui/button';
import { CalendarIcon, ZoomInIcon, ZoomOutIcon } from 'lucide-react';
import { useState, useMemo } from 'react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { METRIC_OPTIONS } from '@/data/commodities-data';

interface PriceChartProps {
  data: Array<{
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
  }>;
  title?: string;
  showDateRange?: boolean;
  selectedMetric?: string;
  onMetricChange?: (metric: string) => void;
}

export default function PriceChart({
  data,
  title = 'Price Chart',
  showDateRange = true,
  selectedMetric = 'price',
  onMetricChange,
}: PriceChartProps) {
  const [zoomLevel, setZoomLevel] = useState(1);

  // Find the selected metric configuration
  const metricConfig = useMemo(() => {
    return (
      METRIC_OPTIONS.find((option) => option.value === selectedMetric) ||
      METRIC_OPTIONS[0]
    );
  }, [selectedMetric]);

  // Format date for display
  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  // Adjust data points based on zoom level
  const visibleData = useMemo(() => {
    if (zoomLevel === 1) return data;

    const dataLength = data.length;
    const visiblePoints = Math.ceil(dataLength / zoomLevel);
    const startIndex = Math.max(0, dataLength - visiblePoints);

    return data.slice(startIndex);
  }, [data, zoomLevel]);

  // Handle metric change
  const handleMetricChange = (value: string) => {
    if (onMetricChange) {
      onMetricChange(value);
    }
  };

  return (
    <Card className="w-full">
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-lg font-medium">{title}</CardTitle>

        <div className="flex items-center gap-4">
          <Select
            value={selectedMetric}
            onValueChange={handleMetricChange}
            defaultValue="price"
          >
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Select metric" />
            </SelectTrigger>
            <SelectContent>
              {METRIC_OPTIONS.map((metric) => (
                <SelectItem key={metric.value} value={metric.value}>
                  {metric.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          <div className="flex items-center gap-2">
            {showDateRange && (
              <div className="hidden md:block">
                <DatePickerWithRange />
              </div>
            )}

            <div className="flex items-center gap-1">
              <Button
                variant="outline"
                size="icon"
                onClick={() => setZoomLevel((prev) => Math.max(1, prev - 1))}
                disabled={zoomLevel === 1}
              >
                <ZoomOutIcon className="h-4 w-4" />
              </Button>
              <Button
                variant="outline"
                size="icon"
                onClick={() => setZoomLevel((prev) => Math.min(4, prev + 1))}
                disabled={zoomLevel === 4}
              >
                <ZoomInIcon className="h-4 w-4" />
              </Button>
              {showDateRange && (
                <Button variant="outline" size="icon" className="md:hidden">
                  <CalendarIcon className="h-4 w-4" />
                </Button>
              )}
            </div>
          </div>
        </div>
      </CardHeader>

      <CardContent>
        <ChartContainer config={{}} className="aspect-[none] h-[300px]">
          <AreaChart data={visibleData}>
            <ChartTooltip content={<ChartTooltipContent />} />

            <defs>
              <linearGradient id="colorMetric" x1="0" y1="0" x2="0" y2="1">
                <stop
                  offset="5%"
                  stopColor={metricConfig.color}
                  stopOpacity={0.8}
                />

                <stop
                  offset="95%"
                  stopColor={metricConfig.color}
                  stopOpacity={0.1}
                />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />

            <XAxis
              dataKey="date"
              tickFormatter={formatDate}
              tickLine={false}
              axisLine={false}
              tick={{ fontSize: 12 }}
              minTickGap={30}
            />

            <Area
              type="monotone"
              dataKey={metricConfig.dataKey}
              stroke={metricConfig.color}
              fillOpacity={1}
              fill="url(#colorMetric)"
              strokeWidth={2}
              name={metricConfig.label}
            />
          </AreaChart>
        </ChartContainer>
      </CardContent>
    </Card>
  );
}
