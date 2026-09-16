import { useCities, useTowns } from '../../hooks/useSearchData.js';

/**
 * The For Sale / To Rent tabs and the country → city → town cascade.
 *
 * Countries are fetched a level up, in SearchPage, because the selected
 * country's currency_code is what every price on the page is formatted with.
 * City and town are disabled until their parent is chosen — the backend has
 * nothing to populate them with until then.
 */
export default function SearchBar({
  filters,
  countries,
  countriesLoading,
  countriesError,
  onListingTypeChange,
  onCountryChange,
  onCityChange,
  onTownChange,
}) {
  const { data: cities, loading: citiesLoading } = useCities(filters.countryId);
  const { data: towns, loading: townsLoading } = useTowns(filters.cityId);

  return (
    <section className="search-bar" aria-label="Location and listing type">
      <div className="tabs" role="tablist" aria-label="Listing type">
        <button
          type="button"
          role="tab"
          aria-selected={filters.listingType === 'sale'}
          className={`tab ${filters.listingType === 'sale' ? 'tab--active' : ''}`}
          onClick={() => onListingTypeChange('sale')}
        >
          For Sale
        </button>
        <button
          type="button"
          role="tab"
          aria-selected={filters.listingType === 'rent'}
          className={`tab ${filters.listingType === 'rent' ? 'tab--active' : ''}`}
          onClick={() => onListingTypeChange('rent')}
        >
          To Rent
        </button>
      </div>

      <div className="location-row">
        <label className="field">
          <span className="field__label">Country</span>
          <select
            className="field__control"
            value={filters.countryId}
            disabled={countriesLoading || Boolean(countriesError)}
            onChange={(event) => onCountryChange(event.target.value)}
          >
            {countriesLoading && <option value="">Loading…</option>}
            {!countriesLoading &&
              countries.map((country) => (
                <option key={country.id} value={country.id}>
                  {country.name}
                </option>
              ))}
          </select>
        </label>

        <label className="field">
          <span className="field__label">City</span>
          <select
            className="field__control"
            value={filters.cityId}
            disabled={!filters.countryId || citiesLoading}
            onChange={(event) => onCityChange(event.target.value)}
          >
            <option value="">All cities</option>
            {cities.map((city) => (
              <option key={city.id} value={city.id}>
                {city.name}
              </option>
            ))}
          </select>
        </label>

        <label className="field">
          <span className="field__label">Town</span>
          <select
            className="field__control"
            value={filters.townId}
            disabled={!filters.cityId || townsLoading}
            onChange={(event) => onTownChange(event.target.value)}
          >
            <option value="">{filters.cityId ? 'All towns' : 'Select a city first'}</option>
            {towns.map((town) => (
              <option key={town.id} value={town.id}>
                {town.name}
              </option>
            ))}
          </select>
        </label>
      </div>
    </section>
  );
}
