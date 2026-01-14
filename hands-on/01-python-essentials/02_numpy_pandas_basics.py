"""
============================================================
MODULE 1.2: NUMPY & PANDAS FOR AI/ML
============================================================
Time: 45-60 minutes
Goal: Master data manipulation for AI applications

SETUP (run once):
    pip install numpy pandas

HOW TO RUN:
    source ../venv/bin/activate
    python3 02_numpy_pandas_basics.py
============================================================
"""

import numpy as np
import pandas as pd

# ============================================================
# PART 1: NUMPY - THE FOUNDATION OF AI/ML
# ============================================================
print("\n" + "="*60)
print("PART 1: NUMPY ESSENTIALS")
print("="*60)

# Why NumPy? All AI/ML libraries use NumPy arrays internally
# - 50x faster than Python lists
# - Used for: embeddings, vectors, matrices, tensors

# Creating arrays
print("\n--- Creating Arrays ---")
arr1 = np.array([1, 2, 3, 4, 5])
arr2 = np.zeros(5)                    # [0, 0, 0, 0, 0]
arr3 = np.ones((3, 3))                # 3x3 matrix of 1s
arr4 = np.arange(0, 10, 2)            # [0, 2, 4, 6, 8]
arr5 = np.linspace(0, 1, 5)           # 5 evenly spaced from 0 to 1

print(f"Basic array: {arr1}")
print(f"Zeros: {arr2}")
print(f"Ones matrix:\n{arr3}")
print(f"Range: {arr4}")
print(f"Linspace: {arr5}")

# Array operations (vectorized - super fast!)
print("\n--- Vectorized Operations ---")
a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])

print(f"a + b = {a + b}")           # Element-wise addition
print(f"a * b = {a * b}")           # Element-wise multiplication
print(f"a * 2 = {a * 2}")           # Scalar multiplication
print(f"a ** 2 = {a ** 2}")         # Square each element
print(f"np.sqrt(a) = {np.sqrt(a)}") # Square root

# CRITICAL FOR AI: Dot product and matrix operations
print("\n--- Matrix Operations (Critical for AI!) ---")
matrix1 = np.array([[1, 2], [3, 4]])
matrix2 = np.array([[5, 6], [7, 8]])

print(f"Matrix 1:\n{matrix1}")
print(f"Matrix 2:\n{matrix2}")
print(f"Dot product:\n{np.dot(matrix1, matrix2)}")
print(f"Transpose:\n{matrix1.T}")

# VECTORS & EMBEDDINGS PREVIEW
print("\n--- Vectors (Preview of Embeddings) ---")
# In AI, text is converted to vectors (embeddings)
# These are high-dimensional arrays representing meaning

# Simulating word embeddings (real ones have 1536 dimensions!)
word_king = np.array([0.8, 0.2, 0.9, 0.1])
word_queen = np.array([0.7, 0.3, 0.85, 0.9])
word_man = np.array([0.9, 0.1, 0.3, 0.1])
word_woman = np.array([0.85, 0.15, 0.25, 0.9])

# The famous: king - man + woman ≈ queen
result = word_king - word_man + word_woman
print(f"king - man + woman = {result}")
print(f"Actual queen vector = {word_queen}")
print(f"Similarity: {np.dot(result, word_queen) / (np.linalg.norm(result) * np.linalg.norm(word_queen)):.3f}")

# Cosine similarity (used everywhere in RAG!)
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print(f"\nCosine similarity (king, queen): {cosine_similarity(word_king, word_queen):.3f}")
print(f"Cosine similarity (king, man): {cosine_similarity(word_king, word_man):.3f}")

# Array indexing and slicing
print("\n--- Indexing & Slicing ---")
arr = np.array([[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]])

print(f"Full array:\n{arr}")
print(f"First row: {arr[0]}")
print(f"First column: {arr[:, 0]}")
print(f"Submatrix (top-left 2x2): \n{arr[:2, :2]}")
print(f"Every other element: {arr[0, ::2]}")

# Boolean indexing (filtering)
print("\n--- Boolean Indexing ---")
data = np.array([10, 25, 30, 45, 50, 15])
print(f"Original: {data}")
print(f"Greater than 25: {data[data > 25]}")
print(f"Between 20 and 40: {data[(data > 20) & (data < 40)]}")

# Statistical operations
print("\n--- Statistics ---")
scores = np.array([85, 90, 78, 92, 88, 76, 95, 89])
print(f"Scores: {scores}")
print(f"Mean: {np.mean(scores):.2f}")
print(f"Std Dev: {np.std(scores):.2f}")
print(f"Min/Max: {np.min(scores)}, {np.max(scores)}")
print(f"Percentile 75: {np.percentile(scores, 75):.2f}")


# ============================================================
# PART 2: PANDAS - DATA MANIPULATION POWERHOUSE
# ============================================================
print("\n" + "="*60)
print("PART 2: PANDAS ESSENTIALS")
print("="*60)

# Why Pandas? It's how you work with structured data in AI
# - Loading data (CSV, JSON, databases)
# - Cleaning and transforming data
# - Preparing data for ML models

# Creating DataFrames (like Salesforce report data)
print("\n--- Creating DataFrames ---")

# From dictionary (most common)
sf_data = {
    "AccountId": ["001", "002", "003", "004", "005"],
    "Name": ["Acme Corp", "Tech Inc", "Global Ltd", "StartUp Co", "Enterprise"],
    "Industry": ["Technology", "Technology", "Finance", "Technology", "Healthcare"],
    "Revenue": [1000000, 500000, 2500000, 150000, 3000000],
    "Employees": [500, 200, 1000, 25, 1500],
    "IsActive": [True, True, False, True, True]
}

df = pd.DataFrame(sf_data)
print(df)

# Basic info
print("\n--- DataFrame Info ---")
print(f"Shape: {df.shape}")  # (rows, columns)
print(f"Columns: {list(df.columns)}")
print(f"Data types:\n{df.dtypes}")

# Accessing data
print("\n--- Accessing Data ---")
print(f"First 2 rows:\n{df.head(2)}")
print(f"Single column (Name):\n{df['Name']}")
print(f"Multiple columns:\n{df[['Name', 'Revenue']]}")
print(f"Single row (index 0):\n{df.iloc[0]}")
print(f"Specific cell (row 1, column 'Name'): {df.loc[1, 'Name']}")

# Filtering (like SOQL WHERE)
print("\n--- Filtering (like SOQL WHERE) ---")
tech_companies = df[df['Industry'] == 'Technology']
print(f"Technology companies:\n{tech_companies}")

high_revenue = df[df['Revenue'] > 500000]
print(f"\nHigh revenue (>500k):\n{high_revenue}")

# Complex filters
complex_filter = df[(df['Industry'] == 'Technology') & (df['Revenue'] > 200000)]
print(f"\nTech companies with revenue > 200k:\n{complex_filter}")

# Sorting
print("\n--- Sorting ---")
sorted_by_revenue = df.sort_values('Revenue', ascending=False)
print(f"Sorted by Revenue (desc):\n{sorted_by_revenue}")

# Aggregations (like SOQL GROUP BY)
print("\n--- Aggregations (like GROUP BY) ---")
by_industry = df.groupby('Industry').agg({
    'Revenue': 'sum',
    'Employees': 'mean',
    'AccountId': 'count'
}).rename(columns={'AccountId': 'Count'})
print(by_industry)

# Adding/modifying columns
print("\n--- Adding/Modifying Columns ---")
df['RevenuePerEmployee'] = df['Revenue'] / df['Employees']
df['Size'] = df['Employees'].apply(lambda x: 'Large' if x > 500 else 'Small')
print(df[['Name', 'Employees', 'RevenuePerEmployee', 'Size']])

# Handling missing data (CRITICAL for AI!)
print("\n--- Handling Missing Data ---")
df_with_nulls = df.copy()
df_with_nulls.loc[1, 'Revenue'] = None
df_with_nulls.loc[3, 'Industry'] = None

print(f"Data with nulls:\n{df_with_nulls}")
print(f"\nNull counts:\n{df_with_nulls.isnull().sum()}")

# Fill nulls
df_filled = df_with_nulls.fillna({
    'Revenue': df_with_nulls['Revenue'].mean(),
    'Industry': 'Unknown'
})
print(f"\nAfter filling nulls:\n{df_filled}")


# ============================================================
# PART 3: REAL AI/ML DATA PREPARATION EXAMPLE
# ============================================================
print("\n" + "="*60)
print("PART 3: AI/ML DATA PREPARATION")
print("="*60)

# Simulating Lead data for ML scoring
leads_data = {
    "LeadId": [f"00Q{i:03d}" for i in range(1, 11)],
    "Company": ["Acme", "Tech", "Global", "Start", "Big", "Small", "Med", "New", "Old", "Fast"],
    "Industry": ["Tech", "Tech", "Finance", "Tech", "Healthcare", "Tech", "Finance", "Tech", "Healthcare", "Tech"],
    "Employees": [500, 200, 1000, 25, 1500, 50, 300, 10, 800, 150],
    "HasEmail": [True, True, False, True, True, False, True, True, False, True],
    "HasPhone": [True, False, True, True, True, True, False, True, True, False],
    "LeadSource": ["Web", "Event", "Web", "Referral", "Web", "Event", "Web", "Referral", "Event", "Web"],
    "Converted": [True, False, True, False, True, False, True, False, True, False]  # Target variable!
}

leads_df = pd.DataFrame(leads_data)
print("Lead Data for ML:")
print(leads_df)

# Feature Engineering for ML
print("\n--- Feature Engineering ---")

# One-hot encoding categorical variables
industry_dummies = pd.get_dummies(leads_df['Industry'], prefix='Industry')
source_dummies = pd.get_dummies(leads_df['LeadSource'], prefix='Source')

# Create features DataFrame
features = pd.concat([
    leads_df[['Employees', 'HasEmail', 'HasPhone']].astype(int),
    industry_dummies,
    source_dummies
], axis=1)

print("Engineered Features:")
print(features)

# Normalize numerical features (required for many ML models)
from sklearn.preprocessing import StandardScaler

# Only normalize 'Employees' column
features['Employees_Scaled'] = StandardScaler().fit_transform(features[['Employees']])
print(f"\nScaled Employees column:\n{features[['Employees', 'Employees_Scaled']]}")

# Prepare for ML
X = features.drop('Employees', axis=1)  # Features
y = leads_df['Converted'].astype(int)   # Target

print(f"\nFeatures shape: {X.shape}")
print(f"Target shape: {y.shape}")
print(f"Target distribution:\n{y.value_counts()}")


# ============================================================
# PART 4: WORKING WITH TEXT DATA (FOR RAG/NLP)
# ============================================================
print("\n" + "="*60)
print("PART 4: TEXT DATA FOR AI")
print("="*60)

# Text data processing - essential for RAG systems
documents = pd.DataFrame({
    "doc_id": [1, 2, 3, 4, 5],
    "title": [
        "Account Management Best Practices",
        "Lead Qualification Process",
        "Opportunity Pipeline Guide",
        "Customer Success Metrics",
        "Sales Forecasting Methods"
    ],
    "content": [
        "This guide covers how to manage customer accounts effectively in Salesforce.",
        "Learn the BANT methodology for qualifying leads and scoring opportunities.",
        "Understanding your sales pipeline stages helps improve conversion rates.",
        "Track NPS, CSAT, and churn metrics to measure customer satisfaction.",
        "Use historical data and AI to predict future sales more accurately."
    ],
    "category": ["Account", "Lead", "Opportunity", "Service", "Analytics"]
})

print("Documents DataFrame:")
print(documents)

# Text processing
print("\n--- Text Processing ---")

# Lowercase
documents['content_lower'] = documents['content'].str.lower()

# Word count
documents['word_count'] = documents['content'].str.split().str.len()

# Contains keyword
documents['mentions_salesforce'] = documents['content'].str.contains('Salesforce', case=False)

print(documents[['title', 'word_count', 'mentions_salesforce']])

# Combining text for embeddings (common in RAG)
documents['combined_text'] = documents['title'] + ": " + documents['content']
print("\n--- Combined Text (for Embeddings) ---")
for idx, row in documents.iterrows():
    print(f"Doc {row['doc_id']}: {row['combined_text'][:60]}...")


# ============================================================
# 🎯 PRACTICE EXERCISES
# ============================================================
print("\n" + "="*60)
print("🎯 PRACTICE EXERCISES")
print("="*60)

print("""
EXERCISE 1: NumPy - Similarity Search
-------------------------------------
Given these "embeddings" (simplified), find which document 
is most similar to the query using cosine similarity:

query = np.array([0.5, 0.8, 0.3, 0.9])
doc1 = np.array([0.4, 0.7, 0.2, 0.85])
doc2 = np.array([0.1, 0.2, 0.9, 0.1])
doc3 = np.array([0.6, 0.9, 0.4, 0.95])

Which document is most similar to the query?
(Hint: Use the cosine_similarity function from above)


EXERCISE 2: Pandas - Lead Scoring
---------------------------------
Create a lead scoring function using the leads_df DataFrame:
- 30 points if HasEmail is True
- 20 points if HasPhone is True
- 30 points if Employees > 100
- 20 points if Industry is 'Tech'

Add a 'Score' column and classify as:
- 'Hot' if score >= 80
- 'Warm' if score >= 50
- 'Cold' otherwise


EXERCISE 3: Data Pipeline
-------------------------
Create a function that:
1. Takes a DataFrame of Salesforce records
2. Cleans null values
3. Adds derived columns
4. Returns prepared data for ML

def prepare_for_ml(df: pd.DataFrame) -> tuple:
    '''
    Returns: (X_features, y_target, feature_names)
    '''
    pass


EXERCISE 4: Text Chunking for RAG
---------------------------------
Given a long document, split it into chunks of roughly 100 words
with 20 words overlap. This is essential for RAG systems!

def chunk_text(text: str, chunk_size: int = 100, overlap: int = 20) -> list:
    '''
    Returns: List of text chunks
    '''
    pass

Test with:
long_text = '''
Salesforce is a cloud-based software company headquartered in San Francisco, 
California. It provides customer relationship management software and applications 
focused on sales, customer service, marketing automation, analytics, and application 
development. Founded in 1999 by former Oracle executive Marc Benioff, Salesforce has 
grown to become one of the largest software companies in the world. The company's 
main service is its CRM platform, which helps businesses manage their customer 
interactions and data throughout the customer lifecycle.
'''
""")


# ============================================================
# 🏆 SUMMARY
# ============================================================
print("\n" + "="*60)
print("🏆 NUMPY & PANDAS COMPLETE!")
print("="*60)
print("""
You now know:

NumPy:
✅ Creating and manipulating arrays
✅ Vectorized operations (10-100x faster than loops)
✅ Matrix operations (critical for AI)
✅ Cosine similarity (used in RAG!)

Pandas:
✅ DataFrames - like Salesforce reports
✅ Filtering - like SOQL WHERE
✅ Grouping - like GROUP BY
✅ Feature engineering for ML
✅ Text data preparation

NEXT STEPS:
1. Complete the exercises above
2. Move to: 03_first_ml_model.py (Build your first ML model!)
3. Then: Week 2 - GenAI Deep Dive
""")
