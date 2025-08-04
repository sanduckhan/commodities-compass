import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { CloudRainIcon, Loader2, CalendarIcon } from "lucide-react";
import { useWeather } from "@/hooks/useDashboard";
import { cn } from "@/utils";

interface WeatherUpdateCardProps {
  targetDate?: string;
  className?: string;
}

export default function WeatherUpdateCard({
  targetDate,
  className,
}: WeatherUpdateCardProps) {
  const { data: weather, isLoading, error } = useWeather(targetDate);

  if (isLoading) {
    return (
      <Card className={cn("flex items-center justify-center h-[200px]", className)}>
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </Card>
    );
  }

  if (error || !weather) {
    return (
      <Card className={cn("flex items-center justify-center h-[200px]", className)}>
        <div className="text-center space-y-2">
          <p className="text-sm text-muted-foreground">Unable to load weather data</p>
          {error && (
            <p className="text-xs text-red-500">
              Error: {error.message || 'Unknown error'}
            </p>
          )}
        </div>
      </Card>
    );
  }

  return (
    <Card className={className}>
      <CardHeader className="pb-2">
        <div className="flex items-center gap-2 mb-2">
          <CloudRainIcon className="h-5 w-5 text-primary" />
          <CardTitle className="text-lg font-medium">Weather Update</CardTitle>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          <div>
            <h3 className="text-base font-semibold mb-1">Conditions</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {weather.description}
            </p>
          </div>

          <div>
            <h3 className="text-base font-semibold mb-1">Market Impact</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {weather.impact}
            </p>
          </div>
        </div>
      </CardContent>
      <CardFooter className="pt-0 flex flex-wrap gap-4 text-xs text-gray-500 dark:text-gray-400">
        <div className="flex items-center gap-1">
          <CalendarIcon className="h-3.5 w-3.5" />
          <span>{weather.date}</span>
        </div>
      </CardFooter>
    </Card>
  );
}
