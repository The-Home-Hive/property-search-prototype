"""Deterministic, template-based listing descriptions.

Pure functions of a property's own fields (plus its id, used only to pick among
wording variants), so re-running the seed produces identical text.
"""

OPENERS = {
    "House": [
        "A spacious family house",
        "A well-kept detached house",
        "A comfortable family home",
    ],
    "Villa": [
        "An elegant villa",
        "A refined villa with generous living space",
        "A bright, open-plan villa",
    ],
    "Townhouse": [
        "A modern townhouse",
        "A neat multi-level townhouse",
        "A low-maintenance townhouse",
    ],
    "Bungalow": [
        "A single-storey bungalow",
        "An easy-living bungalow",
        "A charming bungalow",
    ],
    "Apartment": [
        "A bright apartment",
        "A well-planned apartment",
        "A modern apartment",
    ],
    "Studio Apartment": [
        "A smart, compact studio apartment",
        "An efficient open-plan studio",
        "A cosy studio apartment",
    ],
    "Office": [
        "A functional office space",
        "A professional office suite",
        "A flexible commercial office",
    ],
    "Land": [
        "A level plot of land",
        "A well-positioned plot",
        "A promising parcel of land",
    ],
}

CLOSERS = {
    "House": "Ideal for a growing household looking for room to settle.",
    "Villa": "A relaxed setting for entertaining and everyday living.",
    "Townhouse": "A practical choice for those who want space without a big garden to look after.",
    "Bungalow": "Everything on one level, well suited to families and retirees alike.",
    "Apartment": "Convenient for professionals and small households alike.",
    "Studio Apartment": "A sensible base for a single occupant or a couple.",
    "Office": "Ready to host a small team or client-facing business.",
    "Land": "A blank canvas for residential or commercial development, subject to local zoning approvals.",
}


def _plural(n: int, word: str) -> str:
    return f"{n} {word}" if n == 1 else f"{n} {word}s"


def _join(items: list[str]) -> str:
    if len(items) <= 2:
        return " and ".join(items)
    return ", ".join(items[:-1]) + f" and {items[-1]}"


def build_description(prop, amenity_names: list[str]) -> str:
    ptype = prop.property_type
    variants = OPENERS.get(ptype, [f"A {ptype.lower()}"])
    opener = variants[prop.id % len(variants)]
    town, city, country = prop.town.name, prop.town.city.name, prop.town.city.country.name
    action = "for rent" if prop.listing_type == "rent" else "for sale"

    sentences = [f"{opener} {action} in {town}, {city}, {country}."]

    if ptype not in {"Land", "Office"}:
        layout = []
        if ptype != "Studio Apartment" and prop.bedrooms:
            layout.append(_plural(prop.bedrooms, "bedroom"))
        if prop.bathrooms:
            layout.append(_plural(prop.bathrooms, "bathroom"))
        if layout:
            verb = "Offering" if ptype != "Studio Apartment" else "With"
            sentences.append(f"{verb} {_join(layout)}, it is laid out for everyday comfort.")
        sentences.append(
            "It comes furnished, so you can move straight in."
            if prop.furnished
            else "It is offered unfurnished, leaving you free to make it your own."
        )
    elif ptype == "Office" and prop.furnished:
        sentences.append("The space is fitted out and furnished, ready for day-one use.")

    if amenity_names:
        sentences.append(f"On-site features include {_join([a.lower() for a in amenity_names])}.")

    sentences.append(CLOSERS.get(ptype, "Contact us to arrange a viewing."))
    return " ".join(sentences)
