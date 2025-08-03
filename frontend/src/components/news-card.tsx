import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { MarketNews } from "@/data/commodities-data";
import { CalendarIcon, NewspaperIcon, UserIcon } from "lucide-react";

interface NewsCardProps {
  news: MarketNews;
  className?: string;
}

export default function NewsCard({ news, className }: NewsCardProps) {
  return (
    <Card className={className}>
      <CardHeader className="pb-2">
        <div className="flex items-center gap-2 mb-2">
          <NewspaperIcon className="h-5 w-5 text-primary" />

          <CardTitle className="text-lg font-medium">Last Press</CardTitle>
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
        <div className="flex items-center gap-1">
          <UserIcon className="h-3.5 w-3.5" />

          <span>{news.author}</span>
        </div>
      </CardFooter>
    </Card>
  );
}
