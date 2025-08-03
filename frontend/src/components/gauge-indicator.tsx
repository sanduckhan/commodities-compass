import React from "react";
import { cn } from "@/utils";

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
  // Arc goes from (10,60) to (110,60) - this is a semicircle with center at (60,60)
  // For the top semicircle, angles go from π (180°) to 0 (0°)
  const arcStartAngle = Math.PI; // 180° - leftmost point (10,60)
  const currentAngle = arcStartAngle - (percentage / 100) * Math.PI; // Interpolate along the arc
  
  const centerX = 60;
  const centerY = 60; 
  const radius = 50;
  
  // For the TOP semicircle, y coordinates should be LESS than centerY
  const markerX = centerX + radius * Math.cos(currentAngle);
  const markerY = centerY - radius * Math.abs(Math.sin(currentAngle)); // Use negative to go upward

  // Calculate equal sections for colored arcs (each section is 60 degrees = π/3 radians)
  const section1Angle = Math.PI * 2/3; // 120° - end of red section
  const section2Angle = Math.PI * 1/3; // 60° - end of yellow section
  
  // Calculate coordinates for section boundaries
  const section1X = centerX + radius * Math.cos(section1Angle);
  const section1Y = centerY - radius * Math.abs(Math.sin(section1Angle));
  const section2X = centerX + radius * Math.cos(section2Angle);
  const section2Y = centerY - radius * Math.abs(Math.sin(section2Angle));

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

          {/* Colored sections - equally divided */}
          {/* Red section: 0-33% (180° to 120°) */}
          <path
            d={`M10,60 A50,50 0 0,1 ${section1X},${section1Y}`}
            fill="none"
            stroke="currentColor"
            strokeWidth="8"
            className="text-red-500"
          />

          {/* Yellow section: 33-66% (120° to 60°) */}
          <path
            d={`M${section1X},${section1Y} A50,50 0 0,1 ${section2X},${section2Y}`}
            fill="none"
            stroke="currentColor"
            strokeWidth="8"
            className="text-yellow-500"
          />

          {/* Green section: 66-100% (60° to 0°) */}
          <path
            d={`M${section2X},${section2Y} A50,50 0 0,1 110,60`}
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
