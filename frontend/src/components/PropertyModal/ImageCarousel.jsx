import { useEffect, useRef, useState } from 'react';

/**
 * Swipeable image strip. Swiping is native horizontal scroll-snap (works with
 * touch, trackpad and drag); the arrows and ←/→ keys scroll the same strip, and
 * the "1/3" indicator follows whichever slide is centred.
 */
export default function ImageCarousel({ images, alt }) {
  const trackRef = useRef(null);
  const [index, setIndex] = useState(0);
  const count = images.length;

  useEffect(() => {
    setIndex(0);
    if (trackRef.current) trackRef.current.scrollLeft = 0;
  }, [images]);

  const goTo = (next) => {
    const track = trackRef.current;
    if (!track || count === 0) return;
    const clamped = Math.max(0, Math.min(count - 1, next));
    track.scrollTo({ left: clamped * track.clientWidth, behavior: 'smooth' });
  };

  const handleScroll = () => {
    const track = trackRef.current;
    if (!track || !track.clientWidth) return;
    setIndex(Math.round(track.scrollLeft / track.clientWidth));
  };

  const handleKeyDown = (event) => {
    if (event.key === 'ArrowLeft') {
      event.preventDefault();
      goTo(index - 1);
    } else if (event.key === 'ArrowRight') {
      event.preventDefault();
      goTo(index + 1);
    }
  };

  return (
    <div
      className="carousel"
      role="group"
      aria-roledescription="carousel"
      aria-label={`${alt} photos`}
    >
      <div
        className="carousel__track"
        ref={trackRef}
        tabIndex={0}
        onScroll={handleScroll}
        onKeyDown={handleKeyDown}
      >
        {images.map((image, i) => (
          <img
            key={image.id ?? image.url}
            className="carousel__slide"
            src={image.url}
            alt={`${alt} — photo ${i + 1} of ${count}`}
            draggable={false}
          />
        ))}
      </div>

      {count > 1 && (
        <>
          <button
            type="button"
            className="carousel__nav carousel__nav--prev"
            aria-label="Previous photo"
            disabled={index === 0}
            onClick={() => goTo(index - 1)}
          >
            ‹
          </button>
          <button
            type="button"
            className="carousel__nav carousel__nav--next"
            aria-label="Next photo"
            disabled={index === count - 1}
            onClick={() => goTo(index + 1)}
          >
            ›
          </button>
        </>
      )}

      <span className="carousel__count" aria-live="polite">
        {Math.min(index + 1, count)}/{count}
      </span>
    </div>
  );
}
