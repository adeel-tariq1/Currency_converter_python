
# Currency Converter

A command-line currency converter built with Python that retrieves exchange rates from the Frankfurter API and caches them locally using JSON.

## Features

- Convert amounts between supported currencies.
- Fetch exchange rates from the Frankfurter API.
- Cache multiple currency pairs in a local JSON file.
- Reuse cached rates for up to one hour.
- Automatically refresh missing or expired rates.
- Validate conversion amounts.
- Handle unsupported currencies and network errors.

## Technologies Used

- Python
- Requests
- Argparse
- JSON
- Datetime
- Frankfurter API

## Installation

1. Clone this repository:

   ```bash
   git clone YOUR_REPOSITORY_URL
   ```

2. Navigate to the project directory:

   ```bash
   cd Currency_converter
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application with an amount, source currency, and target currency:

```bash
python main.py 100 USD EUR
```

Another example:

```bash
python main.py 100 PKR USD
```

## Caching

The application stores exchange rates in `rate_cache.json`.

Each currency pair has its own cache entry containing the source currency, target currency, exchange rate, and UTC timestamp.

A cached rate is reused if it is less than one hour old. Missing or expired entries trigger a new API request.

The cache file is generated locally and excluded from Git.

## Learning Objectives

This project demonstrates working with REST APIs, command-line arguments, JSON file handling, timestamps, caching, input validation, and exception handling.

## Data Source

Exchange rates are provided by the [Frankfurter API](https://frankfurter.dev/).
