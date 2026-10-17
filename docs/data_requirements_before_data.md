# Data Requirements & Source Discovery Plan

## 1. Data Strategy

The project will follow an **Egypt-first market intelligence strategy**.

Instead of first building a massive global perfume database, the initial dataset will identify fragrances currently offered by Egyptian inspired-fragrance brands and then enrich the corresponding original fragrances with global and Egyptian-market information.

The basic relationship is:

**Original fragrance ← inspired by ← Egyptian local fragrance**

For example:

`Dior Sauvage ← inspired by ← FIXD Comfort Zone`

`Dior Sauvage ← inspired by ← PAF Patchouli Rush`

`Dior Sauvage ← inspired by ← Sovran Tornado`

If many independent Egyptian brands produce a Sauvage-inspired fragrance, that becomes an observable measure of **competitive representation**.

It does not automatically prove sales or demand.

---

# 2. Core Data Model

The project should initially contain four main datasets.

| Dataset               | Unit of observation                                 |
| --------------------- | --------------------------------------------------- |
| `local_products`      | One Egyptian inspired perfume product               |
| `original_fragrances` | One original/reference fragrance                    |
| `inspired_by_mapping` | One local-product → original-fragrance relationship |
| `competitors`         | One Egyptian fragrance brand                        |

Customer/review data will become a fifth dataset later.

---

# 3. Egyptian Local Product Dataset

### File

`data/raw/egypt/local_products.csv`

### Unit of observation

**One product sold by one Egyptian fragrance brand.**

### Required variables

| Variable                 | Purpose                                   |
| ------------------------ | ----------------------------------------- |
| `local_product_id`       | Unique identifier                         |
| `local_brand`            | Competitor identification                 |
| `product_name`           | Local fragrance name                      |
| `inspired_by_raw`        | Exact inspiration text from website       |
| `original_brand_raw`     | Original fragrance brand if available     |
| `original_fragrance_raw` | Original fragrance name                   |
| `gender_category`        | Men / Women / Unisex                      |
| `concentration`          | EDP, Parfum, etc.                         |
| `size_ml`                | Bottle size                               |
| `price_egp`              | Current selling price                     |
| `regular_price_egp`      | Price before discount                     |
| `availability`           | In stock / sold out                       |
| `rating`                 | Customer rating when available            |
| `review_count`           | Number of reviews                         |
| `bestseller_flag`        | Whether retailer marks product bestseller |
| `fragrance_family`       | Woody, gourmand, fresh, etc.              |
| `top_notes`              | Product composition                       |
| `heart_notes`            | Product composition                       |
| `base_notes`             | Product composition                       |
| `season`                 | If explicitly provided                    |
| `longevity_claim`        | If explicitly provided                    |
| `projection_claim`       | If explicitly provided                    |
| `product_url`            | Reproducibility                           |
| `date_collected`         | Historical tracking                       |

Several of these fields will naturally contain missing values. That is acceptable.

We should not force every source into the same richness level.

---

# 4. Derived Local Variables

These should be created during processing rather than scraped.

| Derived variable | Definition                                   |
| ---------------- | -------------------------------------------- |
| `price_per_ml`   | `price_egp / size_ml`                        |
| `discount_pct`   | Difference between regular and current price |
| `has_reviews`    | Whether product has customer reviews         |
| `is_available`   | Normalized availability indicator            |
| `note_count`     | Number of listed notes                       |

Eventually we will also calculate information at the original-fragrance level such as:

`number_of_egyptian_alternatives`

`number_of_competing_brands`

`median_local_price`

`median_price_per_ml`

`alternative_availability_rate`

`total_local_review_count`

But these should **not yet be combined into one magical "market score."**

We first analyze their distributions and relationships.

---

# 5. Egyptian Competitor Sources

A first source-discovery pass has already identified several usable Egyptian brands.

| Source            | What it gives us                                                                                      | Initial assessment |
| ----------------- | ----------------------------------------------------------------------------------------------------- | ------------------ |
| Niche Essences    | Inspired fragrance, price, size, gender, rating/reviews, notes, family, season, longevity, projection | Excellent          |
| FIXD Fragrances   | Inspired fragrance, price, gender, reviews, bestseller information                                    | Excellent          |
| PAF               | Inspired fragrance, price, gender, product catalogue                                                  | Very good          |
| Matchy            | Inspired fragrance, prices, ratings, review counts                                                    | Very good          |
| Sina Fragrances   | Inspired fragrance, sizes, prices, notes                                                              | Very good          |
| Sovran            | Inspired fragrance, price, gender                                                                     | Good               |
| Mirage Fragrances | Inspired fragrance, price, availability                                                               | Good               |
| V Fragrances      | Inspired fragrance, price, gender, season/profile                                                     | Good               |
| RYZE              | Inspired fragrance, price, size, notes and bestseller labels                                          | Good               |

These are not hypothetical sources. Current catalog pages expose exactly the type of information needed.

For example, FIXD currently lists products inspired by Stronger With You Intensely, Y EDP, Sauvage, Aventus, Layton, Hacivat, Ultra Male and others, generally around LE600–750.

PAF exposes 20 men's-category products including alternatives inspired by Sauvage, Y, Stronger With You, Layton, Tobacco Vanille, Le Male Elixir and others, with observable prices.

Matchy provides an especially useful additional signal because some products expose both ratings and review counts.

Niche Essences provides particularly rich product metadata. Its Layton-inspired Sovereign product, for example, exposes size, price, review count, fragrance family, top/heart/base notes, season, projection, longevity and sillage.

This makes Niche Essences useful not only for price analysis but also for studying how Egyptian brands **position fragrances**.

---

# 6. Original Fragrance Dataset

### File

`data/raw/originals/original_fragrances.csv`

### Unit of observation

**One specific original fragrance/version.**

This distinction is important.

`Dior Sauvage EDT`

and

`Dior Sauvage EDP`

are not automatically the same product.

### Required fields

| Variable                   | Purpose                           |
| -------------------------- | --------------------------------- |
| `original_id`              | Unique key                        |
| `brand`                    | Designer/niche brand              |
| `fragrance_name`           | Normalized name                   |
| `concentration`            | EDT / EDP / Parfum etc.           |
| `release_year`             | Historical analysis               |
| `gender_category`          | Segmentation                      |
| `fragrance_family`         | Scent classification              |
| `accords`                  | Richer scent representation       |
| `top_notes`                | Composition                       |
| `heart_notes`              | Composition                       |
| `base_notes`               | Composition                       |
| `original_price_egp`       | Egyptian affordability comparison |
| `original_size_ml`         | Normalize price                   |
| `original_price_per_ml`    | Derived                           |
| `availability_egypt`       | Market accessibility              |
| `retailer_bestseller_flag` | Demand proxy                      |
| `google_trends_egypt`      | Egyptian search-interest proxy    |
| `source_url`               | Provenance                        |
| `date_collected`           | Reproducibility                   |

---

# 7. Original Price Source

For Egyptian retail prices, **FACES Egypt** is a strong candidate.

It sells authentic designer fragrances in EGP and exposes size, price, concentration, availability and in some cases bestseller labels.

For example, Dior Sauvage EDP is currently listed in several sizes, including 100 ml at EGP 9,480, while the corresponding inspired fragrances found in several Egyptian competitor catalogues are often below EGP 1,000.

That gives us enough information to calculate a meaningful quantity such as:

`original_price_per_ml`

versus

`inspired_price_per_ml`.

Notice what we are measuring:

**price difference**

not

**quality difference**.

Those are completely different questions.

---

# 8. Egyptian Demand Indicators

We do not have access to actual perfume sales across Egypt.

Therefore the project should not contain a variable called:

`sales`

unless we actually obtain sales data.

Instead, Egyptian demand will be treated as a **latent concept measured through multiple observable proxies**.

### Candidate evidence

| Observable variable                               | What it may tell us           |
| ------------------------------------------------- | ----------------------------- |
| Google Trends Egypt interest                      | Consumer search attention     |
| Number of Egyptian brands offering an alternative | Market/competitor recognition |
| Retailer bestseller label                         | Retail popularity signal      |
| Local review count                                | Customer engagement           |
| Local product availability                        | Market presence               |
| Number of retailers selling original              | Distribution presence         |

Google Trends officially supports Egypt-specific trend information, so search-interest analysis can be geographically restricted to Egypt.

We should preserve these variables independently first.

For example:

`egypt_search_interest`

`local_brand_count`

`local_review_volume`

`retailer_bestseller`

rather than immediately creating:

`demand_score = 0.4 × X + 0.3 × Y ...`

The weighting would currently be arbitrary.

---

# 9. Measuring "Weak Affordable Alternatives"

The business question:

> Which original perfumes have strong demand but weak affordable alternatives in Egypt?

actually contains two separate latent concepts.

### Demand

Possible evidence:

Egyptian search interest + retailer popularity + local competitive representation.

### Alternative strength

Possible evidence:

number of competing local brands + availability + review volume + ratings + price.

Therefore an interesting opportunity could eventually look like:

**high Egyptian interest**

combined with

**few local alternatives**

combined with

**large original-vs-inspired affordability gap**.

But we will let the data determine thresholds rather than inventing them now.

---

# 10. `inspired_by_mapping`

This may become one of the most important tables in the whole project.

### Structure

| local_product_id   | original_id  | match_method | match_confidence |
| ------------------ | ------------ | ------------ | ---------------- |
| FIXD_COMFORT_ZONE  | DIOR_SAUVAGE | explicit     | high             |
| PAF_PATCHOULI_RUSH | DIOR_SAUVAGE | explicit     | high             |
| SOVRAN_TORNADO     | DIOR_SAUVAGE | explicit     | high             |

Most Egyptian brands fortunately state their inspirations directly.

For example, FIXD explicitly identifies Comfort Zone as inspired by Sauvage, while Sovran explicitly identifies Tornado as inspired by Sauvage Dior.

That means we do **not** need machine learning to infer most mappings.

This is good data engineering:

use explicit evidence when explicit evidence exists.

---

# 11. Source Decisions: Fragrantica and Basenotes

Both are useful websites for human perfume research.

Neither should be our automated acquisition source.

Fragrantica's current terms explicitly define scraping/crawling as automated access and prohibit automated extraction without authorization. They also specifically restrict professional market research and systematic harvesting of fragrance fields.

Basenotes similarly states that robots, data mining and scraping tools may not be used for extraction without prior written consent.

Therefore:

| Source                         | Decision               |
| ------------------------------ | ---------------------- |
| Fragrantica automated scraping | Reject                 |
| Basenotes automated scraping   | Reject                 |
| Human reference/checking       | Potentially useful     |
| Licensed/authorized access     | Reconsider if obtained |

This is part of professional data science.

**"Can I scrape it?" is not the same question as "Should this dataset be built from it?"**

---

# 12. FragDB Decision

A current dataset called FragDB looks extremely attractive technically. Its schema contains 100k+ fragrances, accords, notes, ratings, reviews, longevity and other useful fields.

However, its records directly reference Fragrantica pages and its documentation describes periodic recrawls.

Because our project may eventually support a commercial fragrance business, we should **not use it as our primary dataset unless its provenance/licensing relationship with the upstream data is clearly established**.

Technically convenient does not equal clean provenance.

---

# 13. Open Data That We Can Use

`parfica-open-data` is considerably cleaner as a supplementary source.

Its repository explicitly documents column-level provenance and licensing. It provides a note taxonomy, fragrance-house information connected to Wikidata, and Open Beauty Facts mappings.

Its limitation is equally important:

it does **not** provide all the popularity, longevity, rating and review information we wanted.

Therefore it can support:

note normalization
brand normalization
note groups
reference metadata

but it will not be our main source of demand.

---

# 14. Customer Review Dataset

Customer reviews should be treated as a separate later acquisition phase.

### Unit of observation

**One customer review for one product.**

Potential schema:

| Field              | Meaning              |
| ------------------ | -------------------- |
| `review_id`        | Unique review        |
| `local_product_id` | Product              |
| `rating`           | Numeric satisfaction |
| `review_text`      | Customer language    |
| `review_date`      | Time                 |
| `source`           | Website/platform     |
| `date_collected`   | Provenance           |

Later NLP features may include:

`mentions_longevity`

`mentions_projection`

`mentions_similarity`

`mentions_price`

`mentions_packaging`

`mentions_value`

`sentiment`

This is how questions such as:

> Do customers care more about longevity or similarity?

eventually become analyzable.

---

# 15. Recommended Acquisition Order

The acquisition should **not** begin with global fragrance data.

It should follow:

**Egyptian competitors → inspiration mappings → original fragrances → Egyptian original prices → Egyptian demand indicators → reviews.**

That means our first real collection task is:

### Egyptian competitor catalogue acquisition

Initial target:

**8–10 local Egyptian brands**

and approximately:

**100–250 local products.**

That is large enough to reveal meaningful patterns while remaining realistic for a one-month project.

Once those products are collected, we will know exactly which original fragrances need enrichment.

That prevents us from collecting thousands of irrelevant original fragrances.

---

# 16. First Analysis Enabled by This Dataset

Once only the Egyptian catalogue and mappings exist, we can already answer meaningful questions.

We can calculate:

how many local brands imitate each original fragrance;

which original brands are imitated most frequently;

male/female/unisex product distribution;

local fragrance price distribution;

price-per-ml distribution;

most common bottle sizes;

market concentration around particular originals;

which Egyptian brands compete most directly;

which inspirations appear across many competitors;

which inspirations appear only once;

which categories are crowded versus relatively empty.

Then the original/demand dataset makes the analysis substantially stronger.

---

# 17. Project Principle

The project will distinguish carefully between:

**facts**

**proxies**

**claims**

**derived variables**

and

**business conclusions**.

For example:

> "Seven sampled Egyptian brands sell a fragrance inspired by Sauvage."

could be an observed fact.

> "Sauvage therefore has high Egyptian demand."

would be an inference.

> "Sauvage generated X Egyptian sales."

would be unsupported unless actual sales data exists.

Maintaining that distinction is one of the things that will make this project look professional rather than like a normal Kaggle notebook.


