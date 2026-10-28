
import argparse
import requests

from datetime import datetime, timedelta, timezone
from caching import load_json, save_to_json


API_URL = "https://api.frankfurter.dev/v2/rate"
CACHE_DURATION = timedelta(hours=1)


parser = argparse.ArgumentParser(
    description="Convert one currency to another"
)

parser.add_argument("amount", type=float, help="Amount to convert")
parser.add_argument("source", help="Source currency, e.g. USD")
parser.add_argument("target", help="Target currency, e.g. EUR")

args = parser.parse_args()


def get_rate(source, target):
    """Return a fresh cached rate or fetch one from the API."""
    source = source.upper()
    target = target.upper()
    cache_key = f"{source}_{target}"

    cache_data = load_json()
    cached_entry = cache_data.get(cache_key)

    if cached_entry:
        try:
            saved_time = datetime.fromisoformat(
                cached_entry["timestamp"]
            )
            current_time = datetime.now(timezone.utc)
            age = current_time - saved_time
            cached_rate = float(cached_entry["rate"])

            if (
                timedelta(0) <= age < CACHE_DURATION
                and cached_rate > 0
            ):
                print("Using cached exchange rate.")
                return {
                    "base": source,
                    "quote": target,
                    "rate": cached_rate
                }

        except (KeyError, TypeError, ValueError):
            pass

    # Cache is missing or expired. Fetch a fresh rate.
    try:
        response = requests.get(
            f"{API_URL}/{source}/{target}",
            timeout=10
        )
        response.raise_for_status()
        rate_data = response.json()

        if not isinstance(rate_data, dict):
            raise RuntimeError("The API returned an unexpected response.")

        rate = float(rate_data["rate"])
        base = rate_data["base"].upper()
        quote = rate_data["quote"].upper()

        if rate <= 0 or base != source or quote != target:
            raise RuntimeError("The API returned invalid exchange-rate data.")

    except requests.exceptions.HTTPError as e:
        raise ValueError(
            f"Could not get the exchange rate for {source} to {target}. "
            "Check that both currency codes are supported."
        ) from e

    except requests.exceptions.RequestException as e:
        raise RuntimeError(
            "Network error: unable to fetch the exchange rate. "
            "Check your internet connection and try again."
        ) from e

    except (ValueError, KeyError, TypeError) as e:
        raise RuntimeError(
            "The API returned invalid exchange-rate data."
        ) from e

    # Update the cache with the new rate and current UTC timestamp.
    cache_data[cache_key] = {
        "source": source,
        "target": target,
        "rate": rate,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    try:
        save_to_json(cache_data)
    except RuntimeError:
        print("Warning: Exchange rate could not be saved to cache.")

    print("Fetched a fresh exchange rate.")
    rate_data = {
                "base": base,
                "quote": quote,
                "rate": rate
                        }
    return rate_data


def conversion(amount, source, target):
    """Validate input and calculate the converted amount."""
    if amount <= 0:
        raise ValueError("Please enter an amount greater than zero.")

    source = source.upper()
    target = target.upper()

    rate_data = get_rate(source, target)
    converted_amount = amount * rate_data["rate"]

    return {
        "source": rate_data["base"],
        "target": rate_data["quote"],
        "amount": amount,
        "exchange_rate": rate_data["rate"],
        "converted_amount": round(converted_amount, 2)
    }


if __name__ == "__main__":
    try:
        result = conversion(
            args.amount,
            args.source,
            args.target
        )

        print(
            f"{result['amount']:.2f} {result['source']} = "
            f"{result['converted_amount']:.2f} {result['target']}"
        )
        print(f"Exchange rate: {result['exchange_rate']}")

    except (ValueError, RuntimeError) as e:
        print(f"Error: {e}")
