import { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';

import { fetchProperty } from '../../api/properties.js';
import { useApiResource } from '../../hooks/useApiResource.js';
import { formatBathrooms, formatBedrooms, formatPrice } from '../../lib/format.js';
import ImageCarousel from './ImageCarousel.jsx';
import { ArrowLeftIcon, HeartIcon, ShareIcon } from './icons.jsx';

/**
 * Detail view for one property, laid out per the wireframe: carousel, title,
 * description, with "Reserve / Buy" pinned to the bottom while the rest scrolls.
 *
 * The card's own data (title, primary image, price…) renders immediately; only
 * the description and the full image list wait on GET /properties/:id.
 */
export default function PropertyModal({ property, currencyCode, onClose }) {
  const dialogRef = useRef(null);
  const [saved, setSaved] = useState(false);
  const { data: detail, loading, error } = useApiResource(
    ({ signal }) => fetchProperty(property.id, { signal }),
    [property.id]
  );

  // Escape closes; the page behind stops scrolling; focus goes in and returns.
  useEffect(() => {
    const previouslyFocused = document.activeElement;
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    dialogRef.current?.focus();

    const onKeyDown = (event) => {
      if (event.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', onKeyDown);

    return () => {
      document.removeEventListener('keydown', onKeyDown);
      document.body.style.overflow = previousOverflow;
      previouslyFocused?.focus?.();
    };
  }, [onClose]);

  const share = async () => {
    const data = { title: property.title, text: property.title, url: window.location.href };
    try {
      if (navigator.share) await navigator.share(data);
      else await navigator.clipboard.writeText(`${data.title} — ${data.url}`);
    } catch {
      // Dismissed share sheet or blocked clipboard: nothing to recover.
    }
  };

  const images =
    detail?.images?.length > 0
      ? detail.images
      : property.primary_image
        ? [{ id: 'primary', url: property.primary_image }]
        : [];

  return createPortal(
    <div
      className="modal-backdrop"
      onMouseDown={(event) => {
        if (event.target === event.currentTarget) onClose();
      }}
    >
      <div
        className="modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="property-modal-title"
        tabIndex={-1}
        ref={dialogRef}
      >
        <div className="modal__scroll">
          <div className="modal__media">
            {images.length > 0 ? (
              <ImageCarousel images={images} alt={property.title} />
            ) : (
              <div className="modal__media-empty" aria-hidden="true" />
            )}

            <button
              type="button"
              className="icon-button modal__close"
              aria-label="Close"
              onClick={onClose}
            >
              <ArrowLeftIcon />
            </button>
            <div className="modal__actions">
              <button
                type="button"
                className="icon-button"
                aria-label="Share this property"
                onClick={share}
              >
                <ShareIcon />
              </button>
              <button
                type="button"
                className={`icon-button ${saved ? 'icon-button--active' : ''}`}
                aria-label={saved ? 'Remove from saved' : 'Save this property'}
                aria-pressed={saved}
                onClick={() => setSaved((value) => !value)}
              >
                <HeartIcon filled={saved} />
              </button>
            </div>
          </div>

          <div className="modal__content">
            <h2 className="modal__title" id="property-modal-title">
              {property.title}
            </h2>
            <p className="modal__price">
              {formatPrice(property.price, currencyCode)}
              {property.listing_type === 'rent' && <span className="card__per"> / month</span>}
            </p>
            <p className="modal__meta">
              {property.property_type} · {formatBedrooms(property.bedrooms)} ·{' '}
              {formatBathrooms(property.bathrooms)}
              {property.furnished && ' · Furnished'}
            </p>

            {loading ? (
              <div aria-hidden="true">
                <div className="skeleton skeleton--line skeleton--w100" />
                <div className="skeleton skeleton--line skeleton--w100" />
                <div className="skeleton skeleton--line skeleton--w60" />
              </div>
            ) : error ? (
              <p className="notice notice--error">Couldn’t load the full details. {error.message}</p>
            ) : (
              detail.description && <p className="modal__description">{detail.description}</p>
            )}
          </div>
        </div>

        <footer className="modal__footer">
          <div className="modal__footer-price">
            <span className="modal__footer-label">
              {property.listing_type === 'rent' ? 'Rent' : 'Price'}
            </span>
            <span className="modal__footer-amount">
              {formatPrice(property.price, currencyCode)}
              {property.listing_type === 'rent' && <span className="card__per"> / mo</span>}
            </span>
          </div>
          <button type="button" className="modal__cta">
            {property.listing_type === 'rent' ? 'Reserve' : 'Buy'}
          </button>
        </footer>
      </div>
    </div>,
    document.body
  );
}
