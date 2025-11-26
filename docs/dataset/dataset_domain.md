classDiagram
    %% ========================
    %% AGGREGATES
    %% ========================

    class Asset {
        <<AggregateRoot>>
        +UUID id
        +string name
        +string country_code  // ex.: "US", "BR"
        --
        +Listing[] listings
        +PriceFact[] prices
        +AssetIndicatorFact[] indicators
    }

    class Country {
        <<AggregateRoot>>
        +UUID id
        +string code         // ISO 3166-1, ex.: "US","BR"
        +string name         // ex.: "UNITED STATES","BRAZIL"
        --
        +CountryIndicatorFact[] indicators
    }

    %% ========================
    %% VALUE OBJECTS
    %% ========================

    class Listing {
        <<ValueObject>>
        +string symbol       // "AAPL","MSFT34","PETR4.SA"
        +string exchange     // "NASDAQ","NYSE","B3"
        +string currency     // "USD","BRL"
    }

    class PriceFact {
        <<ValueObject>>
        +string interval     // "1min","5min","1h","1d"
        +datetime ts         // UTC, period end
        +Decimal open
        +Decimal high
        +Decimal low
        +Decimal close
        +int volume
        --
        +Listing listing     // referência à listagem
    }

    class AssetIndicatorFact {
        <<ValueObject>>
        +string symbol       // "AAPL","PETR4.SA"
        +datetime ts         // UTC, min precision
        +string name         // "P_E","VOLATILITY","BETA"
        +Decimal value
    }

    class CountryIndicatorFact {
        <<ValueObject>>
        +string country_code // "US","BR"
        +datetime ts         // UTC, min precision
        +string name         // "SELIC","GDP","CPI"
        +Decimal value
    }

    %% ========================
    %% REPOSITORIES (PORTS)
    %% ========================

    class PriceReadRepository {
        <<interface>>
        +get_prices(symbol, interval, start, end) Iterable~PriceFact~
    }

    class AssetIndicatorReadRepository {
        <<interface>>
        +get_asset_indicators(symbol, name, start, end) Iterable~AssetIndicatorFact~
    }

    class CountryIndicatorReadRepository {
        <<interface>>
        +get_country_indicators(country_code, name, start, end) Iterable~CountryIndicatorFact~
    }

    %% ========================
    %% RELATIONSHIPS
    %% ========================

    Asset "1" o-- "*" Listing : has
    Asset "1" o-- "*" PriceFact : has prices
    Asset "1" o-- "*" AssetIndicatorFact : has indicators

    Country "1" o-- "*" CountryIndicatorFact : has indicators

    PriceFact "*" --> "1" Listing : listing

    %% referência lógica por código (não objeto)
    Asset "0..*" ..> Country : country_code\n(ligação por código)

    PriceReadRepository ..> PriceFact : returns
    AssetIndicatorReadRepository ..> AssetIndicatorFact : returns
    CountryIndicatorReadRepository ..> CountryIndicatorFact : returns
