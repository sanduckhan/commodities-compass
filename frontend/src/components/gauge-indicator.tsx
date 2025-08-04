import React from "react";
import { cn } from "@/utils";
import type { IndicatorRange } from "@/types/dashboard";

interface GaugeIndicatorProps {
  value: number;
  min: number;
  max: number;
  label: string;
  ranges?: IndicatorRange[];
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
  ranges,
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

  // Determine color based on ranges or fallback to percentage
  const getColor = () => {
    if (ranges && ranges.length > 0) {
      // Find which range the current value falls into
      for (const range of ranges) {
        if (value >= range.range_low && value <= range.range_high) {
          switch (range.area) {
            case 'RED': return "text-red-500";
            case 'ORANGE': return "text-yellow-500";
            case 'GREEN': return "text-green-500";
            default: return "text-gray-500";
          }
        }
      }
      // If no range matches, use default logic
      return "text-gray-500";
    }
    
    // Fallback to old percentage-based logic if no ranges provided
    if (percentage <= 33) return "text-red-500";
    if (percentage <= 66) return "text-yellow-500";
    return "text-green-500";
  };

  // Generate color sections based on ranges
  const generateColorSections = () => {
    if (!ranges || ranges.length === 0) {
      // Fallback to equal sections
      return [
        { startAngle: Math.PI, endAngle: Math.PI * 2/3, color: "text-red-500" },
        { startAngle: Math.PI * 2/3, endAngle: Math.PI * 1/3, color: "text-yellow-500" },
        { startAngle: Math.PI * 1/3, endAngle: 0, color: "text-green-500" }
      ];
    }

    // Convert ranges to angle sections
    return ranges.map(range => {
      const startPercent = ((range.range_low - min) / (max - min)) * 100;
      const endPercent = ((range.range_high - min) / (max - min)) * 100;
      
      // Convert percentages to angles (180° to 0° semicircle)
      const startAngle = Math.PI - (Math.max(0, Math.min(100, startPercent)) / 100) * Math.PI;
      const endAngle = Math.PI - (Math.max(0, Math.min(100, endPercent)) / 100) * Math.PI;
      
      const colorClass = range.area === 'RED' ? "text-red-500" : 
                        range.area === 'ORANGE' ? "text-yellow-500" : 
                        "text-green-500";
      
      return { startAngle, endAngle, color: colorClass };
    });
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

  // Get the color sections based on ranges
  const colorSections = generateColorSections();
  
  // Helper function to create SVG path for arc section
  const createArcPath = (startAngle: number, endAngle: number) => {
    const startX = centerX + radius * Math.cos(startAngle);
    const startY = centerY - radius * Math.abs(Math.sin(startAngle));
    const endX = centerX + radius * Math.cos(endAngle);
    const endY = centerY - radius * Math.abs(Math.sin(endAngle));
    
    const largeArcFlag = Math.abs(startAngle - endAngle) > Math.PI ? 1 : 0;
    
    return `M${startX},${startY} A${radius},${radius} 0 ${largeArcFlag},1 ${endX},${endY}`;
  };

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

          {/* Dynamic colored sections based on ranges */}
          {colorSections.map((section, index) => (
            <path
              key={index}
              d={createArcPath(section.startAngle, section.endAngle)}
              fill="none"
              stroke="currentColor"
              strokeWidth="8"
              className={section.color}
            />
          ))}

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
