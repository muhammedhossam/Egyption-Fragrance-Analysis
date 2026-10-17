Yes — and this is actually the **most important shift** in how you're approaching this project.

Previously, your workflow was basically:

```text
Find dataset
   ↓
Load dataset
   ↓
Clean it
   ↓
EDA
   ↓
Find something interesting
   ↓
Build model
```

That can produce a technically good notebook, but it doesn't necessarily solve a business problem.

For this project, we're going to deliberately reverse it:

```text
Business
   ↓
Business Decision
   ↓
Business Question
   ↓
Evidence Required
   ↓
Data Required
   ↓
Data Source
   ↓
Data Acquisition
   ↓
Data Validation
   ↓
EDA
   ↓
Statistical Analysis
   ↓
ML
   ↓
Business Decision
```

And yes — **I'll keep teaching you through the decisions rather than just giving you the finished code.**

---

# Phase 0.2 — Data Requirements

Let's start with the hardest and most valuable question:

> **Which original perfumes have strong demand but weak affordable alternatives in Egypt?**

Before searching for a single dataset, we need to dissect the question.

---

## Step 1 — Define the question precisely

The sentence sounds simple:

> "Which original perfumes have strong demand but weak affordable alternatives?"

But look at it carefully.

It contains **three concepts that aren't directly measurable**:

### 1. "Strong demand"

What exactly is demand?

We could potentially observe:

* Number of reviews
* Rating
* Search interest
* Number of retailers carrying the product
* Number of competing products
* Social engagement
* Sales — if available

But these aren't equivalent.

For example:

```text
Perfume A
10,000 reviews

Perfume B
500 reviews
```

Can we conclude A sold 20× more?

**No.**

Reviews are a proxy, not sales.

This distinction is extremely important in professional data science.

---

### 2. "Affordable alternatives"

Affordable relative to **what?**

Suppose:

```text
Original = 12,000 EGP
Inspired = 800 EGP
```

That's obviously a large price difference.

But:

```text
Original = 2,500 EGP
Inspired = 1,800 EGP
```

Is that still an affordable alternative?

We need to define the concept mathematically.

Potentially:

```text
Price Ratio =
Inspired Price / Original Price
```

or:

```text
Discount =
1 - (Inspired Price / Original Price)
```

For example:

```text
Original       Inspired       Ratio

10,000 EGP       1,000 EGP      0.10
 5,000 EGP       1,000 EGP      0.20
 2,000 EGP       1,000 EGP      0.50
```

Now we're beginning to turn a business concept into a measurable variable.

---

### 3. "Weak alternatives"

This is even more interesting.

What makes alternatives "weak"?

Maybe:

```text
Few competitors
+
Low availability
+
Poor ratings
+
Few reviews
+
Large price gap
```

But again, we shouldn't assume the definition.

We need to investigate what data exists.

---

# Step 2 — Decompose the question

Let's write the question as:

```text
                    MARKET OPPORTUNITY
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
       ORIGINAL DEMAND            EGYPTIAN ALTERNATIVES
             │                           │
             ▼                           ▼
       How popular?                How strong?
             │                           │
       ┌─────┼─────┐              ┌─────┼─────┐
       ▼     ▼     ▼              ▼     ▼     ▼
    Reviews Search  ...         Count Rating Price
             │                           │
             └─────────────┬─────────────┘
                           ▼
                     MARKET GAP
```

This tells us immediately that **one dataset probably won't be enough.**

That's an important discovery.

---

# Step 3 — Define the unit of observation

This is another thing I want you to get comfortable with.

Ask:

> **What does one row represent?**

For our global fragrance dataset, one row might represent:

```text
one original perfume
```

Example:

| perfume_id | brand | perfume | rating | review_count | notes |
| ---------- | ----- | ------- | -----: | -----------: | ----- |
| 001        | Dior  | Sauvage |    4.2 |       12,500 | ...   |

For the Egyptian market dataset, one row might represent:

```text
one local product
```

| product_id | local_brand | product   | inspired_by  | price_egp | size_ml |
| ---------- | ----------- | --------- | ------------ | --------: | ------: |
| E001       | Brand X     | Product Y | Dior Sauvage |       650 |     100 |

Notice something?

We have two different entities:

```text
ORIGINAL PERFUME
        ↓
Egyptian alternative
```

So eventually we need a **relationship between them**.

That relationship is extremely important.

---

# Step 4 — Identify the required entities

I would initially expect something like:

```text
Brand
  │
  └── Perfume
          │
          ├── Notes
          ├── Accords
          ├── Family
          ├── Ratings
          └── Reviews


Egyptian Brand
  │
  └── Local Product
          │
          ├── Inspired By
          ├── Price
          ├── Size
          ├── Rating
          └── Availability
```

And eventually:

```text
Original Perfume
       │
       │ inspired_by
       ▼
Egyptian Product
```

That relationship may become one of the most important pieces of the entire project.

---

# Step 5 — Define the evidence we need

Now let's create our **first Data Requirements Matrix**.

| Concept              | What we need to measure  | Possible variables                           |
| -------------------- | ------------------------ | -------------------------------------------- |
| Global demand        | Popularity of original   | rating, review_count, popularity indicators  |
| Egyptian demand      | Local interest           | local reviews, availability, search interest |
| Alternatives         | Competition              | number of inspired products                  |
| Affordability        | Price difference         | original price, local price, price ratio     |
| Alternative strength | Competitive quality      | local rating, reviews, availability          |
| Similarity           | Relationship to original | inspired_by                                  |
| Market gap           | Opportunity              | demand vs alternative strength               |

This is already much more useful than:

> "Let's find a perfume dataset."

---

# Step 6 — Now we face a real data science problem

Suppose we find this:

```text
Original:
Creed Aventus

Global:
Rating = 4.3
Reviews = 25,000

Egypt:
Alternative 1 = 900 EGP
Alternative 2 = 750 EGP
Alternative 3 = 1,100 EGP
```

Can we say:

> "Aventus is a good opportunity"?

Not yet.

Maybe Egypt already has:

```text
20 other alternatives
```

that we haven't discovered.

Or perhaps those three products are unavailable.

Or perhaps customers hate the alternatives.

So we need something like:

```text
Opportunity =
High Original Demand
        ×
Low Alternative Strength
```

But **we should not choose the mathematical formula yet.**

First we need to discover what data is actually available.

This is an important professional principle:

> **Don't design the metric before understanding the data-generating process.**

---

# Step 7 — Source discovery comes BEFORE acquisition

Now we're finally ready to start looking for data.

But notice how different our search will be.

We're not searching:

> "perfume dataset Kaggle"

We're searching for **specific evidence**.

For example:

### Global fragrance information

We need:

```text
perfume
brand
notes
accords
family
rating
review count
popularity
```

### Egyptian market

We need:

```text
local brand
product
inspired-by
price
size
availability
reviews
```

### Customer voice

We need:

```text
review text
rating
longevity
projection
scent
price/value
similarity
```

And now we can evaluate sources against requirements.

---

# Step 8 — Our first source evaluation table

We'll eventually maintain something like:

| Source   | Domain  | Variables         | Coverage | Provenance | Freshness | Reproducibility | Usage constraints | Decision |
| -------- | ------- | ----------------- | -------- | ---------- | --------- | --------------- | ----------------- | -------- |
| Source A | Global  | Notes, ratings... | High     | ...        | ...       | ...             | ...               | Evaluate |
| Source B | Egypt   | Prices...         | ...      | ...        | ...       | ...             | ...               | Evaluate |
| Source C | Reviews | Review text...    | ...      | ...        | ...       | ...             | ...               | Evaluate |

**Do not fill this with guesses.**

We'll investigate each source.

---

# And here's where I want you to make the next move

Rather than me immediately giving you 10 websites, let's do this properly.

### Our first source-discovery target is:

## **Global / Original Fragrance Data**

We need to find the best available sources for:

```text
perfume
brand
release year
gender/category
family
accords
top notes
heart notes
base notes
rating
review count
popularity
longevity
projection
reviews
```

**Fragrantica is one candidate, not automatically the winner.**

Our job is to evaluate it against alternatives.

### Your task

Before we touch code, I want you to think like the person responsible for the dataset and answer:

> **For the "strong demand" part of our market-opportunity question, which observable variables would you consider useful, and why?**

Don't worry about being correct.

Give me your reasoning—even if you say:

> "I think review count represents demand because..."

Then I'll challenge the reasoning and we'll turn it into a proper **data requirement specification** together.

That's the habit I want you to build: **question the measurement before touching the dataset.**
