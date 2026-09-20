import { formatBathrooms, formatBedrooms, formatPrice } from '../../lib/format.js';

export default function PropertyCard({ property, currencyCode }) {
  return (
    <article className="card">
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
    </article>
  );
}
