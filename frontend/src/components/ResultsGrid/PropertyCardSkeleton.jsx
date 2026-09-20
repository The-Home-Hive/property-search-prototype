/** Placeholder shaped like PropertyCard, shown while a search is in flight. */
export default function PropertyCardSkeleton() {
  return (
    <div className="card card--skeleton" aria-hidden="true">
      <div className="card__media skeleton" />
      <div className="card__body">
        <div className="skeleton skeleton--line skeleton--w60" />
        <div className="skeleton skeleton--line skeleton--w80" />
        <div className="skeleton skeleton--line skeleton--w40" />
        <div className="skeleton__tags">
          <span className="skeleton skeleton--pill" />
          <span className="skeleton skeleton--pill" />
          <span className="skeleton skeleton--pill" />
        </div>
      </div>
    </div>
  );
}
