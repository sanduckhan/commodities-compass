import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import GaugeIndicator from "@/polymet/components/gauge-indicator";
import { CommodityIndicator } from "@/polymet/data/commodities-data";
import { TrendingUpIcon, ActivityIcon } from "lucide-react";

interface IndicatorsGridProps {
  indicators: {
    macroeco: CommodityIndicator;
    rsi: CommodityIndicator;
    macd: CommodityIndicator;
    percentK: CommodityIndicator;
    atr: CommodityIndicator;
    volOi: CommodityIndicator;
  };
  className?: string;
}

export default function IndicatorsGrid({
  indicators,
  className,
}: IndicatorsGridProps) {
  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="text-lg font-medium">Market Indicators</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* Tendances Category */}
          <div className="space-y-4">
            <div className="flex items-center gap-2 border-b pb-2">
              <TrendingUpIcon className="h-4 w-4 text-primary" />

              <h3 className="text-sm font-medium">Tendances</h3>
            </div>

            <div className="grid grid-cols-3 gap-4 justify-items-center">
              <GaugeIndicator
                value={indicators.macroeco.value}
                min={indicators.macroeco.min}
                max={indicators.macroeco.max}
                label={indicators.macroeco.label}
                size="sm"
              />

              <GaugeIndicator
                value={indicators.macd.value}
                min={indicators.macd.min}
                max={indicators.macd.max}
                label={indicators.macd.label}
                size="sm"
              />

              <GaugeIndicator
                value={indicators.volOi.value}
                min={indicators.volOi.min}
                max={indicators.volOi.max}
                label={indicators.volOi.label}
                size="sm"
              />
            </div>
          </div>

          {/* Volatilité Category */}
          <div className="space-y-4">
            <div className="flex items-center gap-2 border-b pb-2">
              <ActivityIcon className="h-4 w-4 text-primary" />

              <h3 className="text-sm font-medium">Volatilité</h3>
            </div>

            <div className="grid grid-cols-3 gap-4 justify-items-center">
              <GaugeIndicator
                value={indicators.rsi.value}
                min={indicators.rsi.min}
                max={indicators.rsi.max}
                label={indicators.rsi.label}
                size="sm"
              />

              <GaugeIndicator
                value={indicators.percentK.value}
                min={indicators.percentK.min}
                max={indicators.percentK.max}
                label={indicators.percentK.label}
                size="sm"
              />

              <GaugeIndicator
                value={indicators.atr.value}
                min={indicators.atr.min}
                max={indicators.atr.max}
                label={indicators.atr.label}
                size="sm"
              />
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
