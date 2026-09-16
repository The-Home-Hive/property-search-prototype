import { useCallback, useState } from 'react';

/**
 * Holds every filter the user can set, and the rules for what a change to one
 * does to the others.
 *
 * Country and listing type are the two conditions the search always carries —
 * the technical design has them unbracketed in the query, and the price bands
 * and currency are defined per country + listing type — so they are never
 * cleared, only changed. Everything else is optional and empty means "unset",
 * which src/api/client.js drops from the query string entirely.
 */

const OPTIONAL_DEFAULTS = {
  cityId: '',
  townId: '',
  minPrice: '',
  maxPrice: '',
  propertyType: '',
  bedrooms: '',
  bathrooms: '',
  amenityIds: [],
};

export const INITIAL_FILTERS = {
  listingType: 'sale',
  countryId: '',
  ...OPTIONAL_DEFAULTS,
};

export function useSearchFilters() {
  const [filters, setFilters] = useState(INITIAL_FILTERS);

  // Switching tabs keeps the location but drops the price: a "to rent" figure
  // is meaningless against the sale band, and vice versa.
  const setListingType = useCallback((listingType) => {
    setFilters((current) => ({ ...current, listingType, minPrice: '', maxPrice: '' }));
  }, []);

  // A new country invalidates its dependents: city and town belong to the old
  // country, and the price band is in the old country's currency.
  const setCountryId = useCallback((countryId) => {
    setFilters((current) => ({
      ...current,
      countryId,
      cityId: '',
      townId: '',
      minPrice: '',
      maxPrice: '',
    }));
  }, []);

  const setCityId = useCallback((cityId) => {
    setFilters((current) => ({ ...current, cityId, townId: '' }));
  }, []);

  /** Keeps the two price ends from crossing: the one just set always wins. */
  const setPriceBound = useCallback((bound, value) => {
    setFilters((current) => {
      const next = { ...current, [bound]: value };
      const min = Number(next.minPrice);
      const max = Number(next.maxPrice);

      if (next.minPrice && next.maxPrice && min > max) {
        return bound === 'minPrice' ? { ...next, maxPrice: '' } : { ...next, minPrice: '' };
      }
      return next;
    });
  }, []);

  const setField = useCallback((field, value) => {
    setFilters((current) => ({ ...current, [field]: value }));
  }, []);

  const toggleAmenity = useCallback((amenityId) => {
    setFilters((current) => ({
      ...current,
      amenityIds: current.amenityIds.includes(amenityId)
        ? current.amenityIds.filter((id) => id !== amenityId)
        : [...current.amenityIds, amenityId],
    }));
  }, []);

  /** Resets the optional filters only — the search still needs a country and a tab. */
  const clearFilters = useCallback(() => {
    setFilters((current) => ({ ...current, ...OPTIONAL_DEFAULTS }));
  }, []);

  const activeFilterCount = countActiveFilters(filters);

  return {
    filters,
    activeFilterCount,
    setListingType,
    setCountryId,
    setCityId,
    setPriceBound,
    setField,
    toggleAmenity,
    clearFilters,
  };
}

function countActiveFilters(filters) {
  return Object.entries(OPTIONAL_DEFAULTS).reduce((count, [field]) => {
    const value = filters[field];
    if (Array.isArray(value)) return count + value.length;
    return value === '' ? count : count + 1;
  }, 0);
}
