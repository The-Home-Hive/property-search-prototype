# pricing

Owns `PriceRange` — the min/max price bounds offered in the price dropdown, per `country_id` + `listing_type` (`sale` / `rent`), in that country's currency. This is what lets the frontend switch price bands instantly when the user changes country or listing type.

Populated by `apps/seeding` management commands from `data/source/<country>/<country>_{rent,sale}_price_list.docx`, not by hand.
