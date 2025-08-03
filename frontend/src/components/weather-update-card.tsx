import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { WeatherUpdate } from "@/data/commodities-data";
import { CloudRainIcon, MapPinIcon } from "lucide-react";

interface WeatherUpdateCardProps {
  weatherUpdate: WeatherUpdate;
  className?: string;
}

export default function WeatherUpdateCard({
  weatherUpdate,
  className,
}: WeatherUpdateCardProps) {
  return (
    <Card className={className}>
      <CardHeader className="pb-2">
        <div className="flex items-center gap-2 mb-2">
          <CloudRainIcon className="h-5 w-5 text-primary" />

          <CardTitle className="text-lg font-medium">Weather Update</CardTitle>
        </div>
        <div className="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400">
          <MapPinIcon className="h-4 w-4" />

          <span>{weatherUpdate.region}</span>
          <span className="ml-auto">{weatherUpdate.date}</span>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          <div>
            <h4 className="text-sm font-medium mb-1">Conditions</h4>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {weatherUpdate.description}
            </p>
          </div>

          <div>
            <h4 className="text-sm font-medium mb-1">Market Impact</h4>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {weatherUpdate.impact}
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
