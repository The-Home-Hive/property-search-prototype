/**
 * The single place that knows how to reach the backend.
 *
 * Every endpoint is unpaginated and returns either a plain array or a plain
 * object, so there is no envelope to unwrap. Routes have no trailing slash —
 * Django's urls.py registers them as `countries`, not `countries/`.
 */

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

/** Drops params that are null, undefined or '' so absent filters stay absent. */
function toQueryString(params = {}) {
  const search = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value === null || value === undefined || value === '') continue;
    search.append(key, value);
  }
  const query = search.toString();
  return query ? `?${query}` : '';
}

export async function get(path, params, { signal } = {}) {
  const response = await fetch(`${BASE_URL}/${path}${toQueryString(params)}`, { signal });

  if (!response.ok) {
    throw new Error(`GET /${path} failed with ${response.status}`);
  }

  return response.json();
}
