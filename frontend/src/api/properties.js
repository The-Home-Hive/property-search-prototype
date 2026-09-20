import { get } from './client.js';

/** GET /amenities -> [{ id, name }]. /properties matches on these ids. */
export function fetchAmenities(options) {
  return get('amenities', {}, options);
}

/** GET /property-types -> ["Apartment", "Bungalow", ...] (plain strings). */
export function fetchPropertyTypes(options) {
  return get('property-types', {}, options);
}

/**
 * GET /properties?[filters] -> [{ id, title, primary_image, town, city, country, listing_type,
 * property_type, price, bedrooms, bathrooms, furnished, status, amenities[] }]
 *
 * All filtering is the backend's job: each parameter present becomes another
 * AND condition, and a property is returned only if it satisfies every one.
 * No match is a 200 with an empty array, never an error.
 *
 * Note the shapes the backend expects: country/city/town are ids, bedrooms and
 * bathrooms are minimums (>=), and amenities is a comma-separated id list that
 * must ALL be present on a property.
 */
export function searchProperties(filters, options) {
  const { amenityIds = [], ...rest } = filters;

  return get(
    'properties',
    { ...rest, amenities: amenityIds.length ? amenityIds.join(',') : '' },
    options
  );
}

/**
 * GET /properties/:id -> the search-result shape plus { description,
 * images: [{ id, url, sort_order, is_primary }] } with images already ordered
 * for the carousel. 404s for inactive or unknown ids.
 */
export function fetchProperty(id, options) {
  return get(`properties/${id}`, {}, options);
}
