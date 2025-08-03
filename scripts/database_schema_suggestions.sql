-- PostgreSQL Database Schema Suggestions for Commodities Compass
-- Generated from Excel analysis

-- Table: technicals (from sheet: TECHNICALS)
-- Estimated rows: 208
CREATE TABLE technicals (
    timestamp TIMESTAMP NOT NULL,
    close INTEGER NOT NULL,
    high INTEGER NOT NULL,
    low INTEGER NOT NULL,
    volume INTEGER NOT NULL,
    open_interest INTEGER NOT NULL,
    implied_volatility DECIMAL(15,6),
    stock_us DECIMAL(15,6),
    com_net_us DECIMAL(15,6),
    r3 DECIMAL(15,6) NOT NULL,
    r2 DECIMAL(15,6) NOT NULL,
    r1 DECIMAL(15,6) NOT NULL,
    pivot DECIMAL(15,6) NOT NULL,
    s1 DECIMAL(15,6) NOT NULL,
    s2 DECIMAL(15,6) NOT NULL,
    s3 DECIMAL(15,6) NOT NULL,
    ema12 DECIMAL(15,6) NOT NULL,
    ema26 DECIMAL(15,6) NOT NULL,
    macd DECIMAL(15,6) NOT NULL,
    signal DECIMAL(15,6),
    rsi_14d DECIMAL(15,6),
    d DECIMAL(15,6),
    atr_14d VARCHAR(100),
    limites_de_bolinger DECIMAL(15,6) NOT NULL,
    gain VARCHAR(100) NOT NULL,
    perte VARCHAR(100) NOT NULL,
    gain_14d DECIMAL(15,6),
    perte_14d DECIMAL(15,6),
    rs DECIMAL(15,6),
    rsi_14d DECIMAL(15,6),
    stochastic_k_14 DECIMAL(15,6),
    stochastic_d_14 DECIMAL(15,6),
    close_pivot VARCHAR(100) NOT NULL,
    volatility DECIMAL(15,6),
    volume_oi DECIMAL(15,6) NOT NULL,
    atr VARCHAR(100) NOT NULL,
    bollinger DECIMAL(15,6) NOT NULL,
    bande_sup DECIMAL(15,6) NOT NULL,
    bande_inf DECIMAL(15,6) NOT NULL,
    moyenne_decaler VARCHAR(100),
    decision VARCHAR(100),
    confiance DECIMAL(15,6),
    direction VARCHAR(100),
    score TEXT,
    conclusion DECIMAL(15,6),
    row INTEGER NOT NULL
);

-- Table: indicator (from sheet: INDICATOR)
-- Estimated rows: 208
CREATE TABLE indicator (
    date TIMESTAMP NOT NULL,
    rsi_score DECIMAL(15,6),
    macd_score DECIMAL(15,6),
    stochastic_score DECIMAL(15,6),
    atr_score DECIMAL(15,6),
    close_pivot DECIMAL(15,6) NOT NULL,
    volume_oi DECIMAL(15,6),
    rsi_norm DECIMAL(15,6),
    macd_norm DECIMAL(15,6),
    stoch_k_norm DECIMAL(15,6),
    atr_norm DECIMAL(15,6),
    close_pivot_norm DECIMAL(15,6) NOT NULL,
    vol_oi_norm DECIMAL(15,6),
    indicator DECIMAL(15,6),
    momentum DECIMAL(15,6),
    macroeco_bonus DECIMAL(15,6) NOT NULL,
    final_indicator DECIMAL(15,6),
    conclusion VARCHAR(100),
    macroeco_score DECIMAL(15,6),
    eco TEXT NOT NULL,
    final_indicator_dernier DECIMAL(15,6),
    dernier_macroeco DECIMAL(15,6),
    dernier_rsi DECIMAL(15,6),
    dernier_macd DECIMAL(15,6),
    dernier_k DECIMAL(15,6),
    dernier_atr DECIMAL(15,6),
    dernier_close_pivot DECIMAL(15,6),
    dernier_vol_oi DECIMAL(15,6),
    derniere_conclusion VARCHAR(100)
);

-- Table: biblio_all (from sheet: BIBLIO_ALL)
-- Estimated rows: 93
CREATE TABLE biblio_all (
    date TIMESTAMP NOT NULL,
    auteur VARCHAR(100) NOT NULL,
    resume TEXT NOT NULL,
    mots_cle TEXT,
    impact_synthetiques TEXT NOT NULL,
    date_text VARCHAR(100) NOT NULL
);

-- Table: meteo_all (from sheet: METEO_ALL)
-- Estimated rows: 90
CREATE TABLE meteo_all (
    date TIMESTAMP NOT NULL,
    texte TEXT NOT NULL,
    resume TEXT NOT NULL,
    mots_cle VARCHAR(286) NOT NULL,
    impact_synthetiques TEXT NOT NULL
);

-- Table: podcast (from sheet: PODCAST)
-- Estimated rows: 1
CREATE TABLE podcast (
    date TIMESTAMP NOT NULL,
    conclusion TEXT NOT NULL,
    meteo_date TIMESTAMP NOT NULL,
    meteo_conclusion TEXT NOT NULL,
    press_date TIMESTAMP NOT NULL,
    press_auteur VARCHAR(100) NOT NULL,
    press_text TEXT NOT NULL,
    position VARCHAR(100) NOT NULL,
    dialogue TEXT NOT NULL
);

-- Table: performance (from sheet: PERFORMANCE)
-- Estimated rows: 18
CREATE TABLE performance (
    unnamed_0 DECIMAL(15,6),
    unnamed_1 TEXT,
    unnamed_2 DECIMAL(15,6),
    unnamed_3 DECIMAL(15,6),
    unnamed_4 DECIMAL(15,6),
    unnamed_5 DECIMAL(15,6),
    unnamed_6 DECIMAL(15,6),
    unnamed_7 DECIMAL(15,6),
    unnamed_8 VARCHAR(100)
);

-- Table: config (from sheet: CONFIG)
-- Estimated rows: 21
CREATE TABLE config (
    parametre VARCHAR(100),
    indicator VARCHAR(100),
    val_min DECIMAL(15,6),
    val_max DECIMAL(15,6),
    pas DECIMAL(15,6),
    actuel DECIMAL(15,6),
    new_champion DECIMAL(15,6),
    test DECIMAL(15,6)
);

-- Table: best_perf (from sheet: BEST PERF)
-- Estimated rows: 3
CREATE TABLE best_perf (
    performance VARCHAR(100) NOT NULL,
    actuelle DECIMAL(15,6) NOT NULL,
    new DECIMAL(15,6) NOT NULL,
    limite VARCHAR(100) NOT NULL
);

-- Suggested Indexes
