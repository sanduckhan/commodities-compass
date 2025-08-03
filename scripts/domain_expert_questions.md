# Domain Expert Questions - Database Schema Clarification

Based on the Excel analysis and database model creation, here are questions that need clarification from the domain expert to ensure accurate implementation:

## 1. Technical Indicators & Calculations

### RSI & Stochastic Indicators
- **Question 1.1**: In the TECHNICALS table, we have both `rsi_14d` and another `rsi_14d` field. Are these different calculations or is one a duplicate?
- **Question 1.2**: What's the difference between `d` and `stochastic_d_14`? Are they different period calculations?
- **Question 1.3**: The `gain` and `perte` fields are stored as VARCHAR but seem like they should be numerical. Do these contain formulas or actual values?

### ATR (Average True Range)
- **Question 1.4**: We have both `atr` and `atr_14d` fields. Is `atr` a different period calculation, or are they the same?
- **Question 1.5**: Some ATR fields are stored as VARCHAR instead of DECIMAL. Do they contain formulas or should they be numerical?

### Bollinger Bands
- **Question 1.6**: What exactly is `limites_de_bolinger`? Is it the bandwidth (upper - lower) or something else?
- **Question 1.7**: What period and standard deviation multiplier are used for the Bollinger Bands calculations?

## 2. Market Data & Fundamentals

### COT Data & Market Correlations
- **Question 2.1**: What does `stock_us` represent? Is it an S&P 500 correlation factor?
- **Question 2.2**: Is `com_net_us` from the Commitments of Traders (COT) report? Which category (commercial long-short)?
- **Question 2.3**: Does this data apply to a specific commodity, or is it aggregated across multiple commodities?

### Volume & Open Interest
- **Question 2.4**: The `volume_oi` ratio - is this daily volume divided by total open interest?
- **Question 2.5**: Should we add a commodity symbol/identifier to link this data to specific trading instruments?

## 3. Scoring & Normalization

### Indicator Scoring System
- **Question 3.1**: In the INDICATOR table, what scale are the individual scores on (0-1, 0-100, -1 to 1)?
- **Question 3.2**: How are the normalized indicators calculated? What's the normalization method?
- **Question 3.3**: What's the weighting scheme for combining indicators into the final `indicator` score?

### Confidence & Decision Making
- **Question 3.4**: What scale is the `confiance` (confidence) field on? 0-1 or 0-100?
- **Question 3.5**: What are the possible values for `decision` and `direction` fields?
- **Question 3.6**: The `score` field contains TEXT - does this store formulas, descriptions, or structured data?

## 4. Macroeconomic Integration

### Economic Factors
- **Question 4.1**: What specific macroeconomic indicators are included in `macroeco_score`?
- **Question 4.2**: How is the `macroeco_bonus` calculated and applied to technical signals?
- **Question 4.3**: Is the `eco` field structured data or free-form text analysis?

## 5. Time Series & Data Relationships

### Data Synchronization
- **Question 5.1**: Should `technicals.timestamp` and `indicator.date` be linked? Are they the same time periods?
- **Question 5.2**: What's the frequency of this data? Daily, hourly, or other intervals?
- **Question 5.3**: Are the "dernier" (previous) values in INDICATOR table always from the immediately preceding period?

### Historical Context
- **Question 5.4**: The HISTORIQUE sheet failed to analyze - what type of data does it contain?
- **Question 5.5**: Is there a relationship between the 208 rows in TECHNICALS/INDICATOR and specific date ranges?

## 6. Research & External Data

### Bibliography & Research Impact
- **Question 6.1**: How is `impact_synthetiques` in BIBLIO_ALL quantified or categorized?
- **Question 6.2**: Are there standard categories for research impact (bullish/bearish/neutral)?
- **Question 6.3**: Should research entries be linked to specific commodities or market sectors?

### Weather & Agricultural Data
- **Question 6.4**: Which geographic regions does the METEO_ALL data cover?
- **Question 6.5**: Are there specific crop types or commodities that the weather data focuses on?
- **Question 6.6**: How is weather impact translated into trading signals?

## 7. Configuration & Performance

### Parameter Optimization
- **Question 7.1**: In the CONFIG table, what algorithm is used for parameter optimization?
- **Question 7.2**: How often are the `new_champion` values updated?
- **Question 7.3**: Are configuration changes applied in real-time or during specific update cycles?

### Performance Metrics
- **Question 7.4**: In BEST_PERF table, what does the `limite` field represent? Stop-loss levels?
- **Question 7.5**: What time period do the performance metrics cover?

## 8. Data Architecture & Missing Elements

### Primary Keys & Relationships
- **Question 8.1**: Should we add commodity symbols/identifiers to track multiple instruments?
- **Question 8.2**: Do we need user/account identifiers for multi-user scenarios?
- **Question 8.3**: Are there any foreign key relationships between tables that aren't obvious?

### Missing Data Types
- **Question 8.4**: The PERFORMANCE sheet has unnamed columns - what do these represent?
- **Question 8.5**: Should we add additional metadata like data source, calculation timestamp, or data quality flags?

## 9. Real-time vs Historical Data

### Data Updates
- **Question 9.1**: How frequently is this data updated in production?
- **Question 9.2**: Do we need to preserve historical versions of indicator calculations?
- **Question 9.3**: Are there different data pipelines for real-time vs end-of-day data?

## 10. Trading Implementation

### Signal Generation
- **Question 10.1**: How are the final trading signals generated from the indicator scores?
- **Question 10.2**: Are there risk management rules built into the decision logic?
- **Question 10.3**: Should we track actual trade executions and their outcomes?

---

## Recommended Next Steps

1. **Domain Expert Review**: Have the trading expert review these questions and provide clarifications
2. **Sample Data Review**: Examine a few rows of actual Excel data to understand value ranges and formats
3. **Business Logic Documentation**: Document the trading strategy and indicator calculation methods
4. **Data Dictionary**: Create a comprehensive data dictionary with exact specifications
5. **Validation Rules**: Define data validation rules and constraints for each field

## Priority Questions for Immediate Implementation

**High Priority** (needed before database creation):
- Questions 1.1, 1.3, 1.5 (data type clarifications)
- Questions 3.1, 3.4 (scoring scales)
- Questions 5.1, 5.2 (time series relationships)
- Question 8.1 (commodity identifiers)

**Medium Priority** (can be refined after initial implementation):
- Questions 2.1-2.3 (market data sources)
- Questions 4.1-4.3 (macroeconomic factors)
- Questions 6.1-6.6 (external data integration)

**Low Priority** (optimization and enhancement):
- Questions 7.1-7.5 (configuration and performance)
- Questions 9.1-9.3 (real-time data handling)
- Questions 10.1-10.3 (trading implementation)