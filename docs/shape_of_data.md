# Dataset Preparation and Data Quality

Before starting the analysis and EDA, it is important to document the limitations of the available data and the preprocessing decisions made to make the dataset usable.

## 1. Initial Data Quality Assessment

The data collected for the Egyptian fragrance market contained several quality issues that made it unsuitable for direct analysis without additional cleaning.

The main issues identified were:

1. **Potentially unreliable reviews**  
   A significant portion of the available reviews appeared to be unreliable or potentially fabricated, which makes review-based analysis difficult to treat as ground truth.

2. **Unreliable ratings**  
   The same concern applies to product ratings. Since the reliability of the ratings could not be independently verified, they should be interpreted with caution.

3. **Incomplete fragrance information**  
   Fragrance metadata was inconsistent across products. Some products contained detailed information such as top, middle, and base notes, while others had only partial information or none at all.

Because of these limitations, the goal was not to create a perfectly complete representation of the Egyptian fragrance market. Instead, the goal was to extract the most reliable and useful information available from the collected data.

One of the main questions that motivated the analysis was:

> **What are the most frequently represented fragrances in the Egyptian market?**

---

## 2. Enriching the Dataset with Fragrantica Data

To improve the quality and depth of the fragrance information, the collected Egyptian-market data was combined with an original fragrance dataset sourced from **Fragrantica through Kaggle**.

The Fragrantica dataset provides additional information such as:

- Fragrance ratings and rating counts
- Fragrance year
- Top, middle, and base notes
- Perfumer information
- Main accords
- Brand and country information

However, the two datasets did not contain a reliable direct key that could be used to join them.

Therefore, a matching key was constructed to identify corresponding fragrances across the two datasets.

This matching process was not perfect. Some fragrances could not be reliably matched between the datasets, and a number of products had to be excluded from the enriched analysis.

---

## 3. Filtering the Reference Fragrance Data

As part of the cleaning process, fragrances from the original reference dataset were filtered using the following criteria:

- **Rating Value >= 3.79**
- **Rating Count >= 180**

These thresholds were selected based on the distribution of the reference dataset, particularly its statistical summaries, including the mean and lower quartile. The intention was to remove fragrances with relatively weak ratings or insufficient rating volume rather than arbitrarily selecting products based on personal preference.

It is important to note that these thresholds should **not be interpreted as statistically optimal cutoffs**. They were practical filtering criteria chosen to improve the reliability of the reference set for this specific analysis.

This filtering also resulted in the removal of some fragrances that may genuinely exist in the Egyptian market. The purpose was to prioritize products with stronger and more substantial reference data.

---

## 4. Handling Unmatched and Missing Data

Not every field available in the Egyptian-market dataset had an equivalent field in the Fragrantica dataset.

Several attempts were made to map these fields and recover equivalent information, but some mappings could not be established with sufficient confidence.

Rather than introducing potentially incorrect values, these fields will be excluded from specific parts of the analysis where a reliable equivalent is not available.

The original collected data is intentionally retained, however. This allows other users or future analyses to:

- Investigate the unmatched records
- Develop alternative matching strategies
- Apply different filtering criteria
- Recover additional information from external sources
- Test alternative approaches to data integration

In other words, the cleaning process is designed to support the current analysis without preventing future work on the raw data.

---

## 5. Dataset Structure Before Analysis

At the beginning of the analysis, the two main datasets contained the following fields.

### Fragrantica Reference Dataset

```python
[
    'url',
    'Perfume',
    'Brand',
    'Country',
    'Gender',
    'Rating Value',
    'Rating Count',
    'Year',
    'Top',
    'Middle',
    'Base',
    'Perfumer1',
    'Perfumer2',
    'mainaccord1',
    'mainaccord2',
    'mainaccord3',
    'mainaccord4',
    'mainaccord5'
]
```
### Egyptian Market Dataset

```python
[
    'product_name',
    'inspired_by',
    'size_unit',
    'variant_type',
    'price',
    'available',
    'identity',
    'product_url',
    'collected_date',
    'size',
    'price_per_unit',
    'review_count',
    'rate',
    'inspired_by_key',
    'Perfume',
    'Brand',
    'Top',
    'Middle',
    'Base',
    'Perfumer1',
    'mainaccord1',
    'mainaccord2',
    'mainaccord3',
    'mainaccord4',
    'mainaccord5',
    'matched_type',
    'local_brand'
]
```
## 6. Important Interpretation Notes

The resulting dataset should be considered a **curated analytical dataset**, rather than a complete or perfectly representative census of the Egyptian fragrance market.

Several limitations should be kept in mind:

- Ratings and reviews from the Egyptian-market source may contain unreliable or fabricated entries.
- Not all products could be matched to the Fragrantica reference dataset.
- Some fragrances were removed during the filtering process.
- Fragrance notes are incomplete for some products.
- The matching key was constructed because no reliable common identifier existed between the datasets.
- Some fields could not be mapped with sufficient confidence and will therefore be excluded from certain analyses.
- The filtering thresholds were selected based on the observed distribution of the reference data and are not presented as statistically validated market thresholds.

Despite these limitations, the resulting dataset provides a more structured foundation for exploring the Egyptian fragrance market and answering questions such as:

- Which fragrances are most represented in the Egyptian market?
- Which fragrance families and accords are most common?
- What are the dominant fragrance profiles?
- Which brands and fragrances have the strongest market presence?

The following sections will build on this cleaned dataset and proceed to **EDA and market-level analysis**.


