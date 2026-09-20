import PropertyCard from './PropertyCard.jsx';
import PropertyCardSkeleton from './PropertyCardSkeleton.jsx';

const SKELETON_COUNT = 6;

/**
 * The results list and its three non-result states.
 *
 * A combination that matches nothing is a normal 200 with an empty array, not
 * an error, so it gets a plain spoken-English empty state rather than a blank
 * screen or a failure message.
 */
export default function ResultsGrid({ properties, loading, error, currencyCode, onClear }) {
  if (error) {
    return (
      <p className="notice notice--error">
        Something went wrong loading properties. {error.message}
      </p>
    );
  }

  return (
    <section className="results" aria-label="Search results" aria-busy={loading}>
      <header className="results__header">
        <h2 className="results__count">
          {loading ? 'Searching…' : `${properties.length} ${properties.length === 1 ? 'property' : 'properties'} found`}
        </h2>
      </header>

      {loading ? (
        <div className="results__grid">
          {Array.from({ length: SKELETON_COUNT }, (_, i) => (
            <PropertyCardSkeleton key={i} />
          ))}
        </div>
      ) : properties.length === 0 ? (
        <div className="empty-state">
          <p className="empty-state__title">No properties found</p>
          <p className="empty-state__body">
            No property matches every filter you’ve set. Try widening the price range or
            removing a filter.
          </p>
          <button type="button" className="button" onClick={onClear}>
            Clear filters
          </button>
        </div>
      ) : (
        <div className="results__grid">
          {properties.map((property) => (
            <PropertyCard
              key={property.id}
              property={property}
              currencyCode={currencyCode}
              onOpen={() => {}}
            />
          ))}
        </div>
      )}
    </section>
  );
}
