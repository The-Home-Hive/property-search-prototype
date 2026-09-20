import { describe, expect, it } from 'vitest';

import { buildPriceOptions, chooseStep } from '../src/lib/priceOptions.js';

// The bounds below are the ones actually seeded from data/source/, so these
// cases cover the real dropdowns rather than invented numbers.
const BANDS = {
  kenyaRent: [5_000, 700_000],
  kenyaSale: [500_000, 1_000_000_000],
  ugandaRent: [300_000, 30_000_000],
  tanzaniaSale: [5_000_000, 9_000_000_000],
};

describe('chooseStep', () => {
  it('picks a step that keeps the option count within the target', () => {
    const step = chooseStep(1_000_000_000 - 500_000, 40);
    expect((1_000_000_000 - 500_000) / step).toBeLessThanOrEqual(40);
  });

  it('only ever returns a round 1/2/2.5/5/10 × power-of-ten step', () => {
    for (const [min, max] of Object.values(BANDS)) {
      const step = chooseStep(max - min, 40);
      const magnitude = 10 ** Math.floor(Math.log10(step));
      expect([1, 2, 2.5, 5, 10]).toContain(step / magnitude);
    }
  });
});

describe('buildPriceOptions', () => {
  it('always offers the exact minimum and maximum of the band', () => {
    for (const [min, max] of Object.values(BANDS)) {
      const options = buildPriceOptions(min, max);
      expect(options[0]).toBe(min);
      expect(options[options.length - 1]).toBe(max);
    }
  });

  it('stays short enough to be a usable dropdown', () => {
    // The Kenyan sale list in data/source/ enumerates ~10,000 increments; the
    // derived ladder must not reproduce that.
    const options = buildPriceOptions(...BANDS.kenyaSale);
    expect(options.length).toBeLessThanOrEqual(45);
    expect(options.length).toBeGreaterThan(10);
  });

  it('returns strictly ascending values with no duplicates', () => {
    for (const [min, max] of Object.values(BANDS)) {
      const options = buildPriceOptions(min, max);
      for (let i = 1; i < options.length; i += 1) {
        expect(options[i]).toBeGreaterThan(options[i - 1]);
      }
    }
  });

  it('snaps the rungs between the ends to round multiples', () => {
    const options = buildPriceOptions(...BANDS.kenyaSale);
    const step = chooseStep(BANDS.kenyaSale[1] - BANDS.kenyaSale[0], 40);

    for (const value of options.slice(1, -1)) {
      expect(value % step).toBe(0);
    }
  });

  it('handles a degenerate band without looping forever', () => {
    expect(buildPriceOptions(1000, 1000)).toEqual([1000]);
    expect(buildPriceOptions(undefined, undefined)).toEqual([]);
  });
});
