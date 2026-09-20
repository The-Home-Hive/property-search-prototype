import { get } from './client.js';

/**
 * GET /price-range?country_id=&listing_type=
 *   -> { currency_code, min_price, max_price }, or {} when no band is seeded.
 *
 * Only the bounds come back — the per-increment values in the client's source
 * documents are not stored — so the dropdown ladder is derived in
 * lib/priceOptions.js.
 */
export function fetchPriceRange(countryId, listingType, options) {
  return get('price-range', { country_id: countryId, listing_type: listingType }, options);
}
