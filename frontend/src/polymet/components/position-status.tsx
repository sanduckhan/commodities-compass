import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { PlayIcon, PauseIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { useState, useRef, useEffect } from "react";
import GaugeIndicator from "@/polymet/components/gauge-indicator";
import { CommodityIndicator } from "@/polymet/data/commodities-data";

interface PositionStatusProps {
  position: "OPEN" | "CLOSED";
  ytdPerformance: number;
  dayIndicator?: CommodityIndicator;
  className?: string;
  bulletinAudioUrl?: string;
  bulletinTitle?: string;
}

export default function PositionStatus({
  position,
  ytdPerformance,
  dayIndicator,
  className,
  bulletinAudioUrl = "/bulletin-of-the-day.mp3", // Default audio URL
  bulletinTitle = "Bulletin of the Day",
}: PositionStatusProps) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);

  const audioRef = useRef<HTMLAudioElement | null>(null);

  const togglePlayPause = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const handleTimeUpdate = () => {
    if (audioRef.current) {
      setCurrentTime(audioRef.current.currentTime);
    }
  };

  const handleLoadedMetadata = () => {
    if (audioRef.current) {
      setDuration(audioRef.current.duration);
    }
  };

  const handleProgressChange = (value: number[]) => {
    if (audioRef.current) {
      audioRef.current.currentTime = value[0];
      setCurrentTime(value[0]);
    }
  };

  const formatTime = (time: number) => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
  };

  return (
    <Card className={cn("flex flex-col md:flex-row h-[180px]", className)}>
      <div className="flex-1 border-b md:border-b-0 md:border-r border-border flex flex-col justify-between">
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-gray-500 dark:text-gray-400">
            Position of the Day
          </CardTitle>
        </CardHeader>
        <CardContent className="flex items-center justify-center py-6 flex-grow">
          <Badge
            className={cn(
              "text-xl font-bold px-8 py-3",
              position === "OPEN"
                ? "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300"
                : "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300"
            )}
          >
            {position}
          </Badge>
        </CardContent>
      </div>

      {/* Day Indicator Section */}
      <div className="flex-1 border-b md:border-b-0 md:border-r border-border flex flex-col justify-between">
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-gray-500 dark:text-gray-400">
            Day Indicator
          </CardTitle>
        </CardHeader>
        <CardContent className="flex justify-center items-center py-4 flex-grow">
          {dayIndicator && (
            <GaugeIndicator
              value={dayIndicator.value}
              min={dayIndicator.min}
              max={dayIndicator.max}
              label={dayIndicator.label}
              size="md"
              showLabel={false}
            />
          )}
        </CardContent>
      </div>

      {/* Audio Player Section */}
      <div className="flex-1 border-b md:border-b-0 md:border-r border-border flex flex-col justify-between">
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-gray-500 dark:text-gray-400">
            {bulletinTitle}
          </CardTitle>
        </CardHeader>
        <CardContent className="flex items-center py-4 flex-grow">
          <div className="w-full space-y-4">
            <audio
              ref={audioRef}
              src={bulletinAudioUrl}
              onTimeUpdate={handleTimeUpdate}
              onLoadedMetadata={handleLoadedMetadata}
              onEnded={() => setIsPlaying(false)}
            />

            <div className="flex items-center gap-3">
              <Button
                variant="outline"
                size="icon"
                className="h-10 w-10 flex-shrink-0"
                onClick={togglePlayPause}
              >
                {isPlaying ? (
                  <PauseIcon className="h-5 w-5" />
                ) : (
                  <PlayIcon className="h-5 w-5" />
                )}
              </Button>

              <div className="flex-1">
                <Slider
                  value={[currentTime]}
                  max={duration || 100}
                  step={0.1}
                  onValueChange={handleProgressChange}
                  className="w-full"
                />
              </div>

              <span className="text-sm text-gray-500 dark:text-gray-400 min-w-[80px] text-right flex-shrink-0">
                {formatTime(currentTime)} / {formatTime(duration)}
              </span>
            </div>
          </div>
        </CardContent>
      </div>

      <div className="flex-1 flex flex-col justify-between">
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-gray-500 dark:text-gray-400">
            YTD Performance
          </CardTitle>
        </CardHeader>
        <CardContent className="flex items-center justify-center py-6 flex-grow">
          <div className="text-3xl font-bold">{ytdPerformance.toFixed(2)}%</div>
        </CardContent>
      </div>
    </Card>
  );
}
