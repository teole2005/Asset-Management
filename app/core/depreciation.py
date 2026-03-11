"""
Depreciation calculator using the Double-Declining Balance method.

For IT assets with a 5-year lifespan:
- Annual depreciation rate = 2 / lifespan = 40%
- Each year, 40% of the REMAINING value is depreciated
- After the lifespan expires, value drops to 0

Example for a $1000 device:
  Year 0: $1,000 (100%)
  Year 1: $600   (60%)
  Year 2: $360   (36%)
  Year 3: $216   (21.6%)
  Year 4: $130   (13%)
  Year 5: $78    (7.8%)  → forced to $0 at expiry
"""

from datetime import datetime, timezone


def calculate_depreciation(
    purchase_price: float,
    purchase_date_str: str,
    lifespan_years: int = 5,
) -> dict:
    """
    Calculate current depreciation status using double-declining balance.

    Returns a dict with:
      - original_price: the purchase price
      - current_value: depreciated value today
      - depreciation_amount: total amount depreciated
      - depreciation_pct: percentage of value lost (0-100)
      - remaining_pct: percentage of value remaining (0-100)
      - age_years: fractional years since purchase
      - lifespan_years: the configured lifespan
      - is_expired: True if age >= lifespan
      - estimated_resale: conservative resale estimate (80% of current_value)
    """
    if not purchase_price or not purchase_date_str:
        return None

    try:
        purchase_price = float(str(purchase_price).replace(",", "").replace("$", "").strip())
    except (ValueError, TypeError):
        return None

    if purchase_price <= 0:
        return None

    # Parse purchase date
    try:
        date_str = str(purchase_date_str).split(" ")[0]  # handle "2026-02-06 00:00:00"
        purchase_date = datetime.strptime(date_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        try:
            purchase_date = datetime.strptime(str(purchase_date_str), "%d/%m/%Y")
        except (ValueError, TypeError):
            return None

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    age_days = (now - purchase_date).days
    age_years = max(0, age_days / 365.25)

    # Double-declining balance rate
    rate = 2.0 / lifespan_years  # 0.40 for 5-year lifespan

    if age_years >= lifespan_years:
        current_value = 0.0
        is_expired = True
    else:
        # Apply DDB: value = price * (1 - rate) ^ age_years
        current_value = purchase_price * ((1 - rate) ** age_years)
        current_value = round(current_value, 2)
        is_expired = False

    depreciation_amount = round(purchase_price - current_value, 2)
    depreciation_pct = round((depreciation_amount / purchase_price) * 100, 1)
    remaining_pct = round(100 - depreciation_pct, 1)
    estimated_resale = round(current_value * 0.8, 2)  # 80% of current value

    return {
        "original_price": purchase_price,
        "current_value": current_value,
        "depreciation_amount": depreciation_amount,
        "depreciation_pct": depreciation_pct,
        "remaining_pct": remaining_pct,
        "age_years": round(age_years, 2),
        "lifespan_years": lifespan_years,
        "is_expired": is_expired,
        "estimated_resale": estimated_resale,
    }
