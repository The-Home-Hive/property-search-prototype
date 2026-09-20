import { formatBathrooms, formatBedrooms, formatPrice } from '../../lib/format.js';

export default function PropertyCard({ property, currencyCode, onOpen }) {
  const open = () => onOpen(property);

  return (
    <article
      className="card"
      role="button"
      tabIndex={0}
      aria-label={`View details: ${property.title}`}
      onClick={open}
      onKeyDown={(event) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          open();
        }
      }}
    >
      <div className="card__media">
        {property.primary_image ? (
          <img
            className="card__image"
            src={property.primary_image}
            alt=""
            loading="lazy"
            decoding="async"
          />
        ) : (
          <div className="card__image card__image--empty" aria-hidden="true" />
        )}
      </div>

      <div className="card__body">
        <header className="card__header">
          <h3 className="card__title">{property.property_type}</h3>
          <p className="card__price">
            {formatPrice(property.price, currencyCode)}
            {property.listing_type === 'rent' && <span className="card__per"> / month</span>}
          </p>
        </header>

        <p className="card__location">
          {property.town}, {property.city}, {property.country}
        </p>

        <ul className="card__specs">
          <li>{formatBedrooms(property.bedrooms)}</li>
          <li>{formatBathrooms(property.bathrooms)}</li>
          {property.furnished && <li>Furnished</li>}
        </ul>

        {property.amenities.length > 0 && (
          <ul className="tag-list">
            {property.amenities.map((amenity) => (
              <li key={amenity} className="tag">
                {amenity}
              </li>
            ))}
          </ul>
        )}
      </div>
    </article>
  );
}
