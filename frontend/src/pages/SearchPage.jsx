import { useEffect } from 'react';

import FilterPanel from '../components/FilterPanel/FilterPanel.jsx';
import ResultsGrid from '../components/ResultsGrid/ResultsGrid.jsx';
import SearchBar from '../components/SearchBar/SearchBar.jsx';
import { useCountries, usePropertySearch } from '../hooks/useSearchData.js';
import { useSearchFilters } from '../hooks/useSearchFilters.js';

export default function SearchPage() {
  const {
    filters,
    activeFilterCount,
    setListingType,
    setCountryId,
    setCityId,
    setPriceBound,
    setField,
    toggleAmenity,
    clearFilters,
  } = useSearchFilters();

  const { data: countries, loading: countriesLoading, error: countriesError } = useCountries();

  // Country is one of the two conditions the search always carries, so the
  // first one is selected as soon as the list arrives rather than leaving the
  // page in a state that can't search.
  useEffect(() => {
    if (!filters.countryId && countries.length > 0) {
      setCountryId(String(countries[0].id));
    }
  }, [countries, filters.countryId, setCountryId]);

  const selectedCountry = countries.find(
    (country) => String(country.id) === String(filters.countryId)
  );

  const { data: properties, loading, error } = usePropertySearch(filters);

  return (
    <div className="page">
      <header className="page__header">
        <h1 className="page__title">Property Search</h1>
        <p className="page__subtitle">Kenya · Tanzania · Uganda</p>
      </header>

      <SearchBar
        filters={filters}
        countries={countries}
        countriesLoading={countriesLoading}
        countriesError={countriesError}
        onListingTypeChange={setListingType}
        onCountryChange={setCountryId}
        onCityChange={setCityId}
        onTownChange={(townId) => setField('townId', townId)}
      />

      {countriesError ? (
        <p className="notice notice--error">
          Couldn’t reach the API. Is the Django server running on{' '}
          <code>{import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}</code>?
        </p>
      ) : (
        <main className="layout">
          <FilterPanel
            filters={filters}
            activeFilterCount={activeFilterCount}
            onPriceChange={setPriceBound}
            onFieldChange={setField}
            onAmenityToggle={toggleAmenity}
            onClear={clearFilters}
          />

          <ResultsGrid
            properties={properties}
            loading={loading}
            error={error}
            currencyCode={selectedCountry?.currency_code}
            onClear={clearFilters}
          />
        </main>
      )}
    </div>
  );
}
