import { get } from './client.js';

/** GET /countries -> [{ id, name, currency_code }] */
export function fetchCountries(options) {
  return get('countries', {}, options);
}

/** GET /cities?country_id= -> [{ id, name }] */
export function fetchCities(countryId, options) {
  return get('cities', { country_id: countryId }, options);
}

/** GET /towns?city_id= -> [{ id, name }] */
export function fetchTowns(cityId, options) {
  return get('towns', { city_id: cityId }, options);
}
