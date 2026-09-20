/**
 * Prices are stored as whole units of each country's own currency (KES, UGX,
 * TZS) and are never converted between them, so every amount is formatted with
 * the currency code the API reported alongside it.
 */
export function formatPrice(value, currencyCode) {
  if (value === null || value === undefined) return '—';
  if (!currencyCode) return new Intl.NumberFormat('en-US').format(value);

  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currencyCode,
    currencyDisplay: 'code',
    maximumFractionDigits: 0,
  }).format(value);
}

/** "3 bedrooms" / "1 bedroom" / "Studio" — bedrooms can legitimately be 0. */
export function formatBedrooms(count) {
  if (count === 0) return 'Studio';
  return `${count} bedroom${count === 1 ? '' : 's'}`;
}

export function formatBathrooms(count) {
  return `${count} bathroom${count === 1 ? '' : 's'}`;
}
