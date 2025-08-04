import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { CalendarIcon, NewspaperIcon, UserIcon, Loader2 } from "lucide-react";
import { useNews } from "@/hooks/useDashboard";
import { cn } from "@/utils";

interface NewsCardProps {
  targetDate?: string;
  className?: string;
}

export default function NewsCard({ targetDate, className }: NewsCardProps) {
  const { data: news, isLoading, error } = useNews(targetDate);

  if (isLoading) {
    return (
      <Card className={cn("flex items-center justify-center h-[200px]", className)}>
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </Card>
    );
  }

  if (error || !news) {
    return (
      <Card className={cn("flex items-center justify-center h-[200px]", className)}>
        <div className="text-center space-y-2">
          <p className="text-sm text-muted-foreground">Unable to load news</p>
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
          <NewspaperIcon className="h-5 w-5 text-primary" />
          <CardTitle className="text-lg font-medium">Market Research</CardTitle>
        </div>
        <h3 className="text-base font-semibold">{news.title}</h3>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-gray-600 dark:text-gray-400">
          {news.content}
        </p>
      </CardContent>
      <CardFooter className="pt-0 flex flex-wrap gap-4 text-xs text-gray-500 dark:text-gray-400">
        <div className="flex items-center gap-1">
          <CalendarIcon className="h-3.5 w-3.5" />
          <span>{news.date}</span>
        </div>
        {news.author && (
          <div className="flex items-center gap-1">
            <UserIcon className="h-3.5 w-3.5" />
            <span>{news.author}</span>
          </div>
        )}
      </CardFooter>
    </Card>
  );
}
