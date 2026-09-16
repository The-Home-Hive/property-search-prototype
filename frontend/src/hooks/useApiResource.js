import { useEffect, useState } from 'react';

/**
 * Runs a loader from src/api on mount and whenever `deps` change, cancelling
 * the in-flight request first so fast filter changes can't land out of order.
 *
 * `enabled: false` is for dropdowns that have nothing to ask for yet — no city
 * list until a country is picked — and clears back to `initialData`.
 */
export function useApiResource(loader, deps, { enabled = true, initialData = null } = {}) {
  const [data, setData] = useState(initialData);
  const [loading, setLoading] = useState(enabled);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!enabled) {
      setData(initialData);
      setLoading(false);
      setError(null);
      return undefined;
    }

    const controller = new AbortController();
    setLoading(true);
    setError(null);

    loader({ signal: controller.signal })
      .then((result) => {
        setData(result);
        setLoading(false);
      })
      .catch((err) => {
        if (err.name === 'AbortError') return;
        setError(err);
        setLoading(false);
      });

    return () => controller.abort();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [enabled, ...deps]);

  return { data, loading, error };
}
