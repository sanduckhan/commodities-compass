import React from "react";
import { cn } from "@/lib/utils";

interface GaugeIndicatorProps {
  value: number;
  min: number;
  max: number;
  label: string;
  size?: "sm" | "md" | "lg";
  showValue?: boolean;
  showLabel?: boolean;
  className?: string;
}

export default function GaugeIndicator({
  value,
  min,
  max,
  label,
  size = "md",
  showValue = true,
  showLabel = true,
  className,
}: GaugeIndicatorProps) {
  // Calculate the percentage for the gauge position
  const percentage = Math.max(
    0,
    Math.min(100, ((value - min) / (max - min)) * 100)
  );

  console.log(percentage);

  // Determine color based on value position
  const getColor = () => {
    if (percentage <= 33) return "text-red-500";
    if (percentage <= 66) return "text-yellow-500";
    return "text-green-500";
  };

  // Size classes
  const sizeClasses = {
    sm: "w-20 h-12",
    md: "w-28 h-18",
    lg: "w-36 h-22",
  };

  // Font size classes based on gauge size
  const fontSizeClasses = {
    sm: "text-xl",
    md: "text-2xl",
    lg: "text-3xl",
  };

  // Calculate marker position on the perimeter
  const markerRotation = percentage * 1.8 - 90; // 180 degrees range, -90 to center at 0
  const markerRadius = 50; // Radius of the gauge arc
  const markerX =
    60 + markerRadius * Math.cos((markerRotation * Math.PI) / 180);
  const markerY =
    60 + markerRadius * Math.sin((markerRotation * Math.PI) / 180);

  return (
    <div className={cn("flex flex-col items-center", className)}>
      <div className={cn("relative", sizeClasses[size])}>
        {/* Gauge background */}
        <svg
          className="w-full h-full"
          viewBox="0 0 120 80"
          xmlns="http://www.w3.org/2000/svg"
        >
          {/* Gauge background arc */}
          <path
            d="M10,60 A50,50 0 0,1 110,60"
            fill="none"
            stroke="currentColor"
            strokeWidth="8"
            className="text-gray-200 dark:text-gray-700"
          />

          {/* Colored sections */}
          <path
            d="M10,60 A50,50 0 0,1 43.3,18.6"
            fill="none"
            stroke="currentColor"
            strokeWidth="8"
            className="text-red-500"
          />

          <path
            d="M43.3,18.6 A50,50 0 0,1 76.7,18.6"
            fill="none"
            stroke="currentColor"
            strokeWidth="8"
            className="text-yellow-500"
          />

          <path
            d="M76.7,18.6 A50,50 0 0,1 110,60"
            fill="none"
            stroke="currentColor"
            strokeWidth="8"
            className="text-green-500"
          />

          {/* Marker on the perimeter */}
          <circle
            cx={markerX}
            cy={markerY}
            r="4"
            fill="currentColor"
            className="text-gray-800 dark:text-gray-200"
          />

          {/* Value display in the center */}
          {showValue && (
            <text
              x="60"
              y="65"
              textAnchor="middle"
              dominantBaseline="middle"
              className={cn(
                "font-mono font-bold",
                fontSizeClasses[size],
                getColor()
              )}
              fill="currentColor"
            >
              {value.toFixed(2)}
            </text>
          )}
        </svg>
      </div>

      {/* Label - only show if showLabel is true */}
      {showLabel && (
        <div className="mt-2 text-center">
          <span className="text-xs font-medium text-gray-600 dark:text-gray-400">
            {label}
          </span>
        </div>
      )}
    </div>
  );
}
