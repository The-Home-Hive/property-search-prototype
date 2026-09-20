import { fetchCities, fetchCountries, fetchTowns } from '../api/locations.js';
import { fetchPriceRange } from '../api/pricing.js';
import { fetchAmenities, fetchPropertyTypes, searchProperties } from '../api/properties.js';
import { useApiResource } from './useApiResource.js';

export function useCountries() {
  return useApiResource((options) => fetchCountries(options), [], { initialData: [] });
}

export function useCities(countryId) {
  return useApiResource((options) => fetchCities(countryId, options), [countryId], {
    enabled: Boolean(countryId),
    initialData: [],
  });
}

export function useTowns(cityId) {
  return useApiResource((options) => fetchTowns(cityId, options), [cityId], {
    enabled: Boolean(cityId),
    initialData: [],
  });
}

/** `{}` comes back when a country has no band seeded for that listing type. */
export function usePriceRange(countryId, listingType) {
  return useApiResource(
    (options) => fetchPriceRange(countryId, listingType, options),
    [countryId, listingType],
    { enabled: Boolean(countryId && listingType), initialData: null }
  );
}

export function useAmenities() {
  return useApiResource((options) => fetchAmenities(options), [], { initialData: [] });
}

export function usePropertyTypes() {
  return useApiResource((options) => fetchPropertyTypes(options), [], { initialData: [] });
}

/**
 * The search itself. Every filter is a dependency, so adding, changing or
 * clearing any one of them re-runs the query — which is the behaviour the
 * requirements describe.
 */
export function usePropertySearch(filters) {
  const {
    countryId,
    listingType,
    cityId,
    townId,
    minPrice,
    maxPrice,
    propertyType,
    bedrooms,
    bathrooms,
    amenityIds,
  } = filters;

  const amenityKey = amenityIds.join(',');

  return useApiResource(
    (options) =>
      searchProperties(
        {
          country: countryId,
          listing_type: listingType,
          city: cityId,
          town: townId,
          min_price: minPrice,
          max_price: maxPrice,
          property_type: propertyType,
          bedrooms,
          bathrooms,
          amenityIds,
        },
        options
      ),
    [
      countryId,
      listingType,
      cityId,
      townId,
      minPrice,
      maxPrice,
      propertyType,
      bedrooms,
      bathrooms,
      amenityKey,
    ],
    { enabled: Boolean(countryId), initialData: [] }
  );
}
