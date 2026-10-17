# Business Questions & Data Requirements

## 1. Business Objective

### Primary Question

> **How can data science help an Egyptian affordable/inspired fragrance brand understand its market and make better product decisions?**

The objective of this project is to develop a data-driven framework for an Egyptian fragrance brand operating in the affordable and inspired-fragrance segment.

The analysis will combine global fragrance intelligence, Egyptian market data, competitor information, and customer feedback to identify market opportunities and support decisions related to:

* Product selection
* Pricing
* Customer segmentation
* Competitive positioning
* Product characteristics
* Market opportunities
* Customer preferences
* Recommendation systems

The project follows an end-to-end data science workflow:

```text
Business Requirements
        ↓
Data Requirements
        ↓
Source Discovery & Evaluation
        ↓
Data Acquisition
        ↓
Data Validation
        ↓
Data Integration
        ↓
Exploratory & Statistical Analysis
        ↓
Feature Engineering
        ↓
Machine Learning / Data Products
        ↓
Business Insights & Decisions
```

---

# 2. Business Context

The target market is **Egypt**, with a particular focus on the affordable fragrance segment and local brands offering fragrances inspired by internationally recognized perfumes.

The business opportunity is centered around understanding the relationship between:

* Affordability
* Fragrance similarity
* Fragrance performance
* Brand recognition
* Product variety
* Availability
* Packaging
* Customer preferences
* Competitive positioning

A central market hypothesis is that affordable inspired fragrances may provide consumers with a greater perceived value-for-money by allowing them to access multiple fragrances within a limited budget.

This hypothesis will be evaluated using available market and customer evidence rather than treated as an established fact.

---

# 3. Core Business Decisions

The data platform should support the following business decisions.

## Decision 1 — Product Selection

**Which fragrances should be launched first?**

## Decision 2 — Pricing

**What price should be charged for each product?**

## Decision 3 — Customer Targeting

**Which customer segment should the brand target?**

## Decision 4 — Market Opportunity

**Which original fragrances have strong demand but weak or limited affordable alternatives in Egypt?**

## Decision 5 — Product Characteristics

**Which fragrance characteristics are associated with higher ratings, stronger demand, or better customer satisfaction?**

## Decision 6 — Competitive Positioning

**Which competitors are positioned similarly to the intended brand?**

## Decision 7 — Demand / Rating Prediction

**Can the expected popularity or customer rating of a fragrance be predicted from its characteristics?**

## Decision 8 — Recommendation

**Can a recommendation system identify suitable Egyptian/local fragrances based on fragrance characteristics and customer preferences?**

---

# 4. Customer Behavior Questions

Understanding customer decision-making is critical for determining product positioning and the value proposition.

### Key questions

1. What factors most influence the decision to purchase an affordable or inspired fragrance?
2. How important are:

   * Price
   * Original fragrance price
   * Original brand recognition
   * Scent
   * Similarity to the original
   * Longevity
   * Projection/sillage
   * Packaging
   * Availability
   * Variety
3. Why would a customer choose an inspired fragrance instead of the original?
4. How important is similarity to the original fragrance?
5. How important are longevity and projection?
6. Do customers perceive affordable inspired fragrances as providing better value-for-money?
7. Do lower prices encourage customers to purchase multiple fragrances instead of one expensive fragrance?

The relative importance of these factors should be determined from customer evidence rather than predefined assumptions.

---

# 5. Business Hypotheses

The following hypotheses represent initial assumptions to be evaluated using data.

### H1 — Value for Money

**Consumers perceive affordable inspired fragrances as providing higher value-for-money than original fragrances.**

### H2 — Variety

**Lower prices increase the ability or willingness of consumers to purchase multiple fragrances rather than one expensive fragrance.**

### H3 — Similarity

**Similarity to the original fragrance is an important factor in the purchase decision.**

### H4 — Performance

**Longevity and projection significantly influence customer satisfaction.**

### H5 — Brand Trade-off

**Some consumers trade original-brand prestige for affordability and variety.**

### H6 — Competition as a Demand Signal

**Original fragrances with a larger number of Egyptian inspired alternatives may have stronger market demand or awareness.**

H6 should be tested against independent demand indicators because the number of competitors alone does not establish popularity.

---

# 6. Data Domains

The project will investigate three primary data domains.

```text
                 🇪🇬 EGYPTIAN FRAGRANCE MARKET

                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
       GLOBAL           EGYPTIAN          CUSTOMER
      FRAGRANCE          MARKET            VOICE
        DATA              DATA              DATA
          │                 │                 │
          │                 │                 │
     Fragrance DBs      Local brands       Reviews
     Official sites    Prices             Comments
     Retailers         Competitors        Surveys
     Public datasets   Sizes              Social data
          │                 │                 │
          └─────────────────┼─────────────────┘
                            ▼
                     DATA INTEGRATION
                            │
                            ▼
                     MARKET ANALYSIS
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
          Pricing        Product        Customer
                         Selection      Preferences
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                  DATA PRODUCTS / ML
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
        Opportunity     Prediction    Recommendation
          Scoring
```

---

# 7. Global / Original Fragrance Data

Global fragrance data will provide information about internationally recognized and original fragrances.

Potential variables include:

* Original brand
* Fragrance name
* Release year
* Gender/category
* Fragrance family
* Accords
* Top notes
* Heart/middle notes
* Base notes
* Rating
* Review count
* Popularity indicators
* Longevity
* Projection/sillage
* Season classification
* Day/night classification
* Customer reviews

### Potential Sources

Potential sources include:

* Fragrance databases
* Official perfume-house websites
* Retailers
* Public datasets
* Research datasets
* APIs where available

**Fragrantica** is considered a potential source for global fragrance information due to its extensive perfume catalog, fragrance notes, ratings, reviews, and community-generated information.

Source selection will depend on an evaluation of:

* Provenance
* Accessibility
* Completeness
* Accuracy
* Freshness
* Reproducibility
* Terms of use
* Technical acquisition constraints
* Suitability for public portfolio use

No source will be considered authoritative solely because it is large or popular.

---

# 8. Egyptian Market Data

Egyptian market data is required to understand local competition and market positioning.

Potential variables include:

* Local brand
* Local product name
* Original / inspired-by fragrance
* Original brand
* Price in EGP
* Bottle size
* Price per ml
* Concentration
* Availability
* Product category
* Local rating
* Review count
* Product description
* Competitor
* Date observed

This data will support analysis of:

* Egyptian price segments
* Competitive positioning
* Inspired-by relationships
* Local alternatives
* Product availability
* Bottle-size positioning
* Price-per-ml economics
* Market gaps
* Competitive density

---

# 9. Customer & Review Data

Customer and review data will provide information that cannot be reliably captured through structured product attributes alone.

Potential sources include:

* Product reviews
* Customer comments
* Surveys
* Public social discussions
* Retail reviews
* Customer questions

Potential information to extract includes:

* Overall sentiment
* Scent satisfaction
* Longevity perception
* Projection/sillage perception
* Similarity to the original
* Price/value perception
* Packaging perception
* Availability
* Purchase motivations
* Positive attributes
* Complaints

Natural Language Processing may be used to transform unstructured customer feedback into structured variables.

---

# 10. Research Questions by Data Requirement

## A — Structured Fragrance / Product Data

Questions that can potentially be investigated using structured datasets:

1. What perfume characteristics are associated with higher prices?
2. What fragrance profiles are most popular?
3. What are the most frequently used fragrance notes?
4. How are perfumes distributed by gender/category?
5. How are prices distributed by:

   * Brand
   * Bottle size
   * Concentration
   * Fragrance family
   * Other product characteristics?
6. Which fragrance families or accords are associated with higher ratings?
7. Which fragrance characteristics are associated with stronger popularity?

---

## B — Customer / Review Data

Questions requiring customer opinions or behavioral evidence:

1. Which customer segments should be targeted?
2. What matters most to customers: longevity, projection, scent, price, similarity, packaging, or brand?
3. Why do customers choose inspired fragrances instead of originals?
4. How important is similarity to the original?
5. Do customers perceive inspired fragrances as better value-for-money?
6. How strongly do longevity and projection influence customer satisfaction?
7. What characteristics do customers associate with a high-quality fragrance?

---

## C — Egyptian Market Data

Questions specifically dependent on the Egyptian market:

1. Which market segment should the first product target?
2. What price segment should the brand enter?
3. What price should be charged?
4. Which original fragrances have the largest number of Egyptian alternatives?
5. What bottle sizes are most commonly offered?
6. Which bottle sizes appear most attractive to customers?
7. What price-per-ml patterns exist across competitors?
8. Which local brands are positioned similarly to the intended brand?
9. Which original fragrances have strong representation in the Egyptian market?
10. Which fragrance characteristics are associated with stronger local performance?

---

## D — Multi-Dataset Questions

These questions require integration of multiple data sources.

### D1 — Market Opportunity

**Which original perfumes have strong demand but weak affordable alternatives in Egypt?**

Potential evidence:

```text
Global popularity
        +
Global reviews / ratings
        +
Egyptian alternatives
        +
Egyptian prices
        +
Egyptian availability
        ↓
Market Opportunity
```

---

### D2 — Competition as a Popularity Signal

**Does the number of Egyptian inspired alternatives for an original fragrance correlate with its popularity or demand?**

This should be evaluated using independent demand proxies.

---

### D3 — Global vs Egyptian Market

**Do fragrances that are popular globally also demonstrate strong demand or competitive activity in Egypt?**

---

### D4 — Egyptian Market Gaps

**Which globally popular fragrances have weak or limited Egyptian alternatives?**

---

### D5 — Seasonal and Occasion Suitability

**Can day/night and summer/winter suitability be inferred from fragrance characteristics, customer perception, or both?**

Potential evidence:

```text
Fragrance characteristics
        +
Expert / database classification
        +
Customer reviews
        ↓
Season / Occasion Classification
```

The analysis should compare structured classifications with customer-perceived suitability where sufficient data is available.

---

### D6 — New Product Opportunities

**Which globally attractive fragrances have limited representation in the Egyptian market and may represent opportunities for a new brand?**

Potential signals:

* Global popularity
* Global customer interest
* Egyptian availability
* Number of Egyptian alternatives
* Competitive density
* Price segment
* Fragrance characteristics
* Customer sentiment

---

# 11. Data Availability Limitations

## Actual Egyptian Sales Data

Actual sales data from Egyptian perfume brands may not be publicly available.

Sales should therefore **not** be inferred directly from review counts, search interest, or competitor counts.

Where actual sales data is unavailable, alternative demand proxies may be evaluated, such as:

* Review count
* Search interest
* Product availability
* Number of competing products
* Social engagement
* Public popularity indicators

Any proxy must be explicitly documented and its limitations evaluated.

Example:

> **Actual Egyptian sales data was unavailable; publicly observable demand indicators were therefore evaluated as potential proxies for market demand.**

---

# 12. Business Constraints

Data-driven recommendations must operate within practical business constraints.

## 12.1 Manufacturing

Required information may include:

* Minimum production quantity
* Cost per bottle
* Fragrance oil cost
* Packaging cost
* Bottle cost
* Available bottle sizes
* Production capacity
* Production lead time

## 12.2 Business Economics

Required information may include:

* Target profit margin
* Marketing budget
* Distribution cost
* Shipping cost
* Expected customer acquisition cost
* Target revenue
* Inventory constraints

## 12.3 Regulatory

The project should investigate requirements applicable to perfumes/cosmetics in Egypt, including where relevant:

* Product registration/notification
* Manufacturing requirements
* Labeling requirements
* Safety requirements
* Applicable regulatory authorities

Regulatory information should be obtained from authoritative sources.

## 12.4 Brand Positioning

The intended brand positioning should eventually be defined as one or more of:

* Mass market
* Affordable
* Premium affordable
* Luxury-inspired
* Niche

Brand positioning will influence:

* Target customer
* Product selection
* Price range
* Packaging
* Marketing strategy
* Competitive set

---

# 13. Data Requirements Principles

The project follows the principle:

> **Data should be collected because it provides evidence for a business question or enables a business decision.**

The analytical process should therefore follow:

```text
Business Question
        ↓
Required Evidence
        ↓
Required Variables
        ↓
Potential Data Sources
        ↓
Source Evaluation
        ↓
Data Acquisition
        ↓
Data Validation
        ↓
Analysis
        ↓
Business Insight
        ↓
Decision
```

---

# 14. Source Evaluation Criteria

Every potential data source will be evaluated according to:

### Provenance

Where did the data originate?

### Reliability

How trustworthy is the source?

### Completeness

Does it contain the variables required for the intended analysis?

### Accuracy

How likely is the information to be correct?

### Freshness

How recent is the information?

### Consistency

Are fields represented consistently across records?

### Reproducibility

Can the acquisition process be repeated?

### Accessibility

Can the data be accessed reliably using a sustainable acquisition method?

### Usage Constraints

Can the data be legally and appropriately used for the intended project and portfolio?

---

# 15. Initial Data Architecture

The initial architecture is expected to contain three major data domains.

```text
                    GLOBAL / ORIGINAL
                         FRAGRANCE
                           DATA
                             │
                             │
                             ▼
                    Fragrance Knowledge
                             │
                             │
                             ├── Notes
                             ├── Accords
                             ├── Families
                             ├── Ratings
                             ├── Reviews
                             └── Popularity
                             │
                             ▼
                      DATA INTEGRATION
                             ▲
                             │
                             ├── Egyptian Brands
                             ├── Inspired-by Relationships
                             ├── Prices
                             ├── Sizes
                             ├── Availability
                             └── Competition
                             │
                     EGYPTIAN MARKET
                           DATA
                             │
                             +
                             │
                       CUSTOMER VOICE
                             │
                             ├── Reviews
                             ├── Comments
                             ├── Surveys
                             └── Preferences
```

The final number of datasets and their schemas will be determined during source discovery and data evaluation.

---

# 16. Project Scope for the Data Discovery Phase

The initial data discovery phase will:

1. Translate business questions into explicit data requirements.
2. Identify variables required to answer each question.
3. Define the unit of observation for each dataset.
4. Identify potential data sources.
5. Evaluate sources based on provenance, quality, completeness, freshness, accessibility, reproducibility, and usage constraints.
6. Select appropriate sources.
7. Design reproducible acquisition pipelines.
8. Store original acquired data in `data/raw/`.
9. Document source metadata and acquisition procedures.
10. Validate the acquired raw data before downstream processing.

The project will avoid committing to a specific dataset before the source evaluation process is complete.
