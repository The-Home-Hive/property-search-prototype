/**
 * Builds the values offered in the price dropdowns.
 *
 * The client's source documents enumerate every increment (the Kenyan sale list
 * alone runs to roughly ten thousand entries), but the documented price_range
 * schema stores only a min and a max per country + listing type, and
 * GET /price-range returns just those bounds. So the ladder between them is
 * derived here: a round step is chosen so the dropdown stays usable, and both
 * the true minimum and the true maximum always appear.
 */

const NICE_MULTIPLIERS = [1, 2, 2.5, 5, 10];

/** Smallest "round" step (1, 2, 2.5 or 5 × a power of ten) that keeps the
 *  option count at or under `targetCount`. */
export function chooseStep(span, targetCount) {
  const magnitude = 10 ** Math.floor(Math.log10(span / targetCount));

  for (const multiplier of NICE_MULTIPLIERS) {
    const step = multiplier * magnitude;
    if (span / step <= targetCount) return step;
  }

  return 10 * magnitude;
}

export function buildPriceOptions(minPrice, maxPrice, targetCount = 40) {
  if (!Number.isFinite(minPrice) || !Number.isFinite(maxPrice)) return [];
  if (maxPrice <= minPrice) return [minPrice];

  const step = chooseStep(maxPrice - minPrice, targetCount);
  const values = [minPrice];

  // Snap the rungs after the first to exact multiples of the step, so the list
  // reads 500,000 / 25,000,000 / 50,000,000 rather than 500,000 / 25,500,000.
  for (let value = Math.ceil(minPrice / step) * step; value < maxPrice; value += step) {
    if (value > minPrice) values.push(Math.round(value));
  }

  values.push(maxPrice);
  return values;
}
