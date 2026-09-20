import { formatPrice } from '../../lib/format.js';
import { buildPriceOptions } from '../../lib/priceOptions.js';
import { useAmenities, usePriceRange, usePropertyTypes } from '../../hooks/useSearchData.js';

// The backend filters bedrooms and bathrooms as minimums (>=), so the options
// read as "1+" rather than exact counts.
const ROOM_COUNTS = [1, 2, 3, 4, 5, 6];

export default function FilterPanel({
  filters,
  activeFilterCount,
  onPriceChange,
  onFieldChange,
  onAmenityToggle,
  onClear,
}) {
  const { data: priceRange } = usePriceRange(filters.countryId, filters.listingType);
  const { data: propertyTypes } = usePropertyTypes();
  const { data: amenities } = useAmenities();

  const currency = priceRange?.currency_code;
  const priceOptions = priceRange?.min_price
    ? buildPriceOptions(Number(priceRange.min_price), Number(priceRange.max_price))
    : [];

  return (
    <aside className="filter-panel" aria-label="Filters">
      <div className="filter-panel__header">
        <h2 className="filter-panel__title">Filters</h2>
        <button
          type="button"
          className="link-button"
          onClick={onClear}
          disabled={activeFilterCount === 0}
        >
          Clear all{activeFilterCount > 0 ? ` (${activeFilterCount})` : ''}
        </button>
      </div>

      <fieldset className="filter-group">
        <legend className="filter-group__legend">
          Price {currency ? <span className="filter-group__hint">({currency})</span> : null}
        </legend>
        <div className="filter-group__pair">
          <label className="field">
            <span className="field__label">Minimum</span>
            <select
              className="field__control"
              value={filters.minPrice}
              disabled={priceOptions.length === 0}
              onChange={(event) => onPriceChange('minPrice', event.target.value)}
            >
              <option value="">Any</option>
              {priceOptions.map((value) => (
                <option key={value} value={value}>
                  {formatPrice(value, currency)}
                </option>
              ))}
            </select>
          </label>

          <label className="field">
            <span className="field__label">Maximum</span>
            <select
              className="field__control"
              value={filters.maxPrice}
              disabled={priceOptions.length === 0}
              onChange={(event) => onPriceChange('maxPrice', event.target.value)}
            >
              <option value="">Any</option>
              {priceOptions.map((value) => (
                <option key={value} value={value}>
                  {formatPrice(value, currency)}
                </option>
              ))}
            </select>
          </label>
        </div>
        {priceOptions.length === 0 && filters.countryId && (
          <p className="filter-group__hint">
            No price band is seeded for this country and listing type.
          </p>
        )}
      </fieldset>

      <fieldset className="filter-group">
        <legend className="filter-group__legend">Property type</legend>
        <select
          className="field__control"
          value={filters.propertyType}
          onChange={(event) => onFieldChange('propertyType', event.target.value)}
        >
          <option value="">Any type</option>
          {propertyTypes.map((type) => (
            <option key={type} value={type}>
              {type}
            </option>
          ))}
        </select>
      </fieldset>

      <fieldset className="filter-group">
        <legend className="filter-group__legend">Rooms</legend>
        <div className="filter-group__pair">
          <label className="field">
            <span className="field__label">Bedrooms</span>
            <select
              className="field__control"
              value={filters.bedrooms}
              onChange={(event) => onFieldChange('bedrooms', event.target.value)}
            >
              <option value="">Any</option>
              {ROOM_COUNTS.map((count) => (
                <option key={count} value={count}>
                  {count}+
                </option>
              ))}
            </select>
          </label>

          <label className="field">
            <span className="field__label">Bathrooms</span>
            <select
              className="field__control"
              value={filters.bathrooms}
              onChange={(event) => onFieldChange('bathrooms', event.target.value)}
            >
              <option value="">Any</option>
              {ROOM_COUNTS.map((count) => (
                <option key={count} value={count}>
                  {count}+
                </option>
              ))}
            </select>
          </label>
        </div>
      </fieldset>

      <fieldset className="filter-group">
        <legend className="filter-group__legend">Amenities</legend>
        <p className="filter-group__hint">A property must have every amenity you tick.</p>
        <div className="checkbox-list">
          {amenities.map((amenity) => (
            <label key={amenity.id} className="checkbox">
              <input
                type="checkbox"
                checked={filters.amenityIds.includes(amenity.id)}
                onChange={() => onAmenityToggle(amenity.id)}
              />
              <span>{amenity.name}</span>
            </label>
          ))}
        </div>
      </fieldset>
    </aside>
  );
}
