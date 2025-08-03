import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { DailyRecommendation } from "@/data/commodities-data";
import { CheckCircleIcon, TrendingUpIcon } from "lucide-react";

interface RecommendationsListProps {
  recommendations: DailyRecommendation[];
  className?: string;
}

export default function RecommendationsList({
  recommendations,
  className,
}: RecommendationsListProps) {
  return (
    <Card className={className}>
      <CardHeader className="pb-2">
        <CardTitle className="text-lg font-medium flex items-center gap-2">
          <TrendingUpIcon className="h-5 w-5 text-primary" />
          Recommendations of the Day
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[300px] pr-4">
          <ul className="space-y-3">
            {recommendations.map((recommendation) => (
              <li key={recommendation.id} className="flex items-start gap-2">
                <CheckCircleIcon className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />

                <span className="text-sm">{recommendation.text}</span>
              </li>
            ))}
          </ul>
        </ScrollArea>
      </CardContent>
    </Card>
  );
}
