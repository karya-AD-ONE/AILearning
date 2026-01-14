"""
============================================================
MODULE 1.3: BUILD YOUR FIRST ML MODEL
============================================================
Time: 45-60 minutes
Goal: Understand ML fundamentals by building a Lead Scorer

This is what you need for interviews!
- Understand ML pipeline
- Train a real model
- Evaluate and improve it

SETUP:
    pip install scikit-learn

HOW TO RUN:
    source ../venv/bin/activate
    python3 03_first_ml_model.py
============================================================
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("🤖 BUILDING YOUR FIRST ML MODEL")
print("="*60)

# ============================================================
# PART 1: THE ML PIPELINE (INTERVIEW ESSENTIAL!)
# ============================================================
print("""
┌─────────────────────────────────────────────────────────────┐
│                    THE ML PIPELINE                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. DATA COLLECTION     →  Gather your raw data             │
│         ↓                                                   │
│  2. DATA PREPARATION    →  Clean, transform, engineer       │
│         ↓                                                   │
│  3. SPLIT DATA          →  Train set (80%) / Test set (20%) │
│         ↓                                                   │
│  4. TRAIN MODEL         →  Model learns patterns            │
│         ↓                                                   │
│  5. EVALUATE            →  Test on unseen data              │
│         ↓                                                   │
│  6. IMPROVE             →  Tune, iterate, optimize          │
│         ↓                                                   │
│  7. DEPLOY              →  Put in production                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
""")


# ============================================================
# PART 2: PROBLEM - SALESFORCE LEAD SCORING
# ============================================================
print("\n" + "="*60)
print("PROBLEM: Predict which leads will convert")
print("="*60)

# Create realistic lead data (simulating what you'd export from Salesforce)
np.random.seed(42)  # For reproducibility
n_samples = 500

# Generate synthetic lead data
data = {
    'LeadId': [f'00Q{i:05d}' for i in range(n_samples)],
    'Company': [f'Company_{i}' for i in range(n_samples)],
    'Industry': np.random.choice(['Technology', 'Finance', 'Healthcare', 'Manufacturing', 'Retail'], n_samples),
    'Employees': np.random.randint(10, 5000, n_samples),
    'AnnualRevenue': np.random.randint(100000, 50000000, n_samples),
    'LeadSource': np.random.choice(['Web', 'Referral', 'Event', 'Partner', 'Cold Call'], n_samples),
    'HasEmail': np.random.choice([True, False], n_samples, p=[0.85, 0.15]),
    'HasPhone': np.random.choice([True, False], n_samples, p=[0.7, 0.3]),
    'ResponseTime': np.random.randint(0, 72, n_samples),  # Hours to respond
    'WebsiteVisits': np.random.randint(0, 50, n_samples),
    'EmailsOpened': np.random.randint(0, 20, n_samples),
    'MeetingsScheduled': np.random.randint(0, 5, n_samples),
}

df = pd.DataFrame(data)

# Create target variable with realistic logic
# Leads are more likely to convert if:
# - Large company (more employees)
# - Quick response time
# - More engagement (website visits, emails, meetings)
# - Technology or Finance industry
# - Referral source

conversion_score = (
    (df['Employees'] > 500).astype(int) * 15 +
    (df['ResponseTime'] < 24).astype(int) * 20 +
    (df['WebsiteVisits'] > 10).astype(int) * 15 +
    (df['EmailsOpened'] > 5).astype(int) * 15 +
    (df['MeetingsScheduled'] > 0).astype(int) * 25 +
    (df['Industry'].isin(['Technology', 'Finance'])).astype(int) * 10 +
    (df['LeadSource'] == 'Referral').astype(int) * 15 +
    np.random.randint(-15, 15, n_samples)  # Add some noise
)

df['Converted'] = (conversion_score > 50).astype(int)

print(f"Dataset shape: {df.shape}")
print(f"\nSample data:")
print(df.head(10))
print(f"\nConversion rate: {df['Converted'].mean()*100:.1f}%")


# ============================================================
# PART 3: DATA PREPARATION (Feature Engineering)
# ============================================================
print("\n" + "="*60)
print("STEP 2: DATA PREPARATION")
print("="*60)

# Select features (what we'll use to predict)
print("\n--- Selecting Features ---")

# Numerical features
numerical_features = ['Employees', 'AnnualRevenue', 'ResponseTime', 
                      'WebsiteVisits', 'EmailsOpened', 'MeetingsScheduled']

# Categorical features (need encoding)
categorical_features = ['Industry', 'LeadSource']

# Boolean features
boolean_features = ['HasEmail', 'HasPhone']

print(f"Numerical features: {numerical_features}")
print(f"Categorical features: {categorical_features}")
print(f"Boolean features: {boolean_features}")

# Encode categorical variables
print("\n--- Encoding Categorical Variables ---")
df_encoded = df.copy()

# One-hot encoding for Industry and LeadSource
industry_dummies = pd.get_dummies(df['Industry'], prefix='Industry')
source_dummies = pd.get_dummies(df['LeadSource'], prefix='Source')

print(f"Industry columns: {list(industry_dummies.columns)}")
print(f"Source columns: {list(source_dummies.columns)}")

# Build feature matrix
X = pd.concat([
    df[numerical_features],
    df[boolean_features].astype(int),
    industry_dummies,
    source_dummies
], axis=1)

y = df['Converted']

print(f"\nFeature matrix shape: {X.shape}")
print(f"Features: {list(X.columns)}")


# ============================================================
# PART 4: TRAIN/TEST SPLIT
# ============================================================
print("\n" + "="*60)
print("STEP 3: TRAIN/TEST SPLIT")
print("="*60)

# Split data: 80% train, 20% test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set: {X_train.shape[0]} samples")
print(f"Test set: {X_test.shape[0]} samples")
print(f"\nTraining conversion rate: {y_train.mean()*100:.1f}%")
print(f"Test conversion rate: {y_test.mean()*100:.1f}%")

# Scale numerical features (important for many ML algorithms!)
print("\n--- Scaling Features ---")
scaler = StandardScaler()
X_train_scaled = X_train.copy()
X_test_scaled = X_test.copy()

X_train_scaled[numerical_features] = scaler.fit_transform(X_train[numerical_features])
X_test_scaled[numerical_features] = scaler.transform(X_test[numerical_features])  # Use same scaler!

print("Scaled numerical features (mean≈0, std≈1)")


# ============================================================
# PART 5: TRAIN MODEL
# ============================================================
print("\n" + "="*60)
print("STEP 4: TRAIN MODEL")
print("="*60)

# Model 1: Logistic Regression (simple, interpretable)
print("\n--- Model 1: Logistic Regression ---")
lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_train_scaled, y_train)
print("✓ Logistic Regression trained!")

# Model 2: Random Forest (powerful, handles non-linear relationships)
print("\n--- Model 2: Random Forest ---")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train_scaled, y_train)
print("✓ Random Forest trained!")


# ============================================================
# PART 6: EVALUATE MODELS
# ============================================================
print("\n" + "="*60)
print("STEP 5: EVALUATE MODELS")
print("="*60)

def evaluate_model(model, X_test, y_test, model_name):
    """Evaluate and print model performance"""
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n{'='*40}")
    print(f"📊 {model_name} Results")
    print(f"{'='*40}")
    print(f"Accuracy: {accuracy*100:.1f}%")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Not Converted', 'Converted']))
    
    print(f"Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"                Predicted")
    print(f"              No    Yes")
    print(f"Actual No   [{cm[0,0]:4d}  {cm[0,1]:4d}]")
    print(f"       Yes  [{cm[1,0]:4d}  {cm[1,1]:4d}]")
    
    return accuracy

lr_accuracy = evaluate_model(lr_model, X_test_scaled, y_test, "Logistic Regression")
rf_accuracy = evaluate_model(rf_model, X_test_scaled, y_test, "Random Forest")


# ============================================================
# PART 7: UNDERSTAND THE MODEL (Interpretability)
# ============================================================
print("\n" + "="*60)
print("STEP 6: INTERPRET THE MODEL")
print("="*60)

# Feature Importance (Random Forest)
print("\n--- Feature Importance (Random Forest) ---")
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False)

print("Top 10 Most Important Features:")
for i, row in feature_importance.head(10).iterrows():
    bar = '█' * int(row['importance'] * 50)
    print(f"  {row['feature']:25} {bar} {row['importance']:.3f}")

# Logistic Regression Coefficients (interpretable!)
print("\n--- Logistic Regression Coefficients ---")
coefficients = pd.DataFrame({
    'feature': X.columns,
    'coefficient': lr_model.coef_[0]
}).sort_values('coefficient', ascending=False)

print("Features that INCREASE conversion probability:")
for i, row in coefficients.head(5).iterrows():
    print(f"  ↑ {row['feature']:25} (+{row['coefficient']:.3f})")

print("\nFeatures that DECREASE conversion probability:")
for i, row in coefficients.tail(5).iterrows():
    print(f"  ↓ {row['feature']:25} ({row['coefficient']:.3f})")


# ============================================================
# PART 8: MAKE PREDICTIONS (Use the Model!)
# ============================================================
print("\n" + "="*60)
print("STEP 7: MAKE PREDICTIONS")
print("="*60)

# Create a new lead to score
new_lead = pd.DataFrame([{
    'Employees': 1000,
    'AnnualRevenue': 5000000,
    'ResponseTime': 4,  # Quick response!
    'WebsiteVisits': 20,
    'EmailsOpened': 8,
    'MeetingsScheduled': 2,
    'HasEmail': 1,
    'HasPhone': 1,
    'Industry_Finance': 0,
    'Industry_Healthcare': 0,
    'Industry_Manufacturing': 0,
    'Industry_Retail': 0,
    'Industry_Technology': 1,  # Tech company
    'Source_Cold Call': 0,
    'Source_Event': 0,
    'Source_Partner': 0,
    'Source_Referral': 1,  # Referral lead
    'Source_Web': 0,
}])

# Scale the numerical features
new_lead_scaled = new_lead.copy()
new_lead_scaled[numerical_features] = scaler.transform(new_lead[numerical_features])

# Make predictions
lr_prediction = lr_model.predict(new_lead_scaled)[0]
lr_probability = lr_model.predict_proba(new_lead_scaled)[0][1]

rf_prediction = rf_model.predict(new_lead_scaled)[0]
rf_probability = rf_model.predict_proba(new_lead_scaled)[0][1]

print("New Lead Profile:")
print("  • 1000 employees, $5M revenue")
print("  • Technology industry, Referral source")
print("  • 4-hour response time")
print("  • 20 website visits, 8 emails opened, 2 meetings")

print(f"\n🎯 Predictions:")
print(f"  Logistic Regression: {'WILL CONVERT ✓' if lr_prediction else 'WILL NOT CONVERT ✗'}")
print(f"    Probability: {lr_probability*100:.1f}%")
print(f"  Random Forest: {'WILL CONVERT ✓' if rf_prediction else 'WILL NOT CONVERT ✗'}")
print(f"    Probability: {rf_probability*100:.1f}%")


# ============================================================
# PART 9: SAVE THE MODEL (For Production)
# ============================================================
print("\n" + "="*60)
print("STEP 8: SAVE MODEL FOR PRODUCTION")
print("="*60)

import joblib

# Save the model and scaler
joblib.dump(rf_model, 'lead_scorer_model.pkl')
joblib.dump(scaler, 'lead_scorer_scaler.pkl')
print("✓ Model saved: lead_scorer_model.pkl")
print("✓ Scaler saved: lead_scorer_scaler.pkl")

# How to load and use later:
print("""
# To use the model later:
import joblib

model = joblib.load('lead_scorer_model.pkl')
scaler = joblib.load('lead_scorer_scaler.pkl')

# Prepare new lead data...
prediction = model.predict(new_lead_scaled)
probability = model.predict_proba(new_lead_scaled)[0][1]
""")


# ============================================================
# 🎯 PRACTICE EXERCISES
# ============================================================
print("\n" + "="*60)
print("🎯 PRACTICE EXERCISES")
print("="*60)

print("""
EXERCISE 1: Add More Features
-----------------------------
Add these features to improve the model:
- 'DaysSinceCreated': Random 1-90 days
- 'CompanyWebsiteExists': Boolean
- 'LinkedInConnected': Boolean

Train a new model and compare accuracy.


EXERCISE 2: Try Different Models
--------------------------------
Try these other models and compare:
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB

Which one performs best?


EXERCISE 3: Hyperparameter Tuning
---------------------------------
Use GridSearchCV to find best parameters:

from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 20, None],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(RandomForestClassifier(), param_grid, cv=5)
grid_search.fit(X_train_scaled, y_train)
print(f"Best params: {grid_search.best_params_}")


EXERCISE 4: Cross-Validation
----------------------------
Use cross-validation for more robust evaluation:

from sklearn.model_selection import cross_val_score

scores = cross_val_score(rf_model, X, y, cv=5)
print(f"CV Scores: {scores}")
print(f"Mean: {scores.mean():.3f} (+/- {scores.std()*2:.3f})")


EXERCISE 5: Build an Opportunity Probability Model
--------------------------------------------------
Create a model to predict opportunity win probability:
- Features: Amount, Stage, DaysInStage, CompetitorCount, ProductCount
- Target: IsWon (0 or 1)

This is a real Salesforce use case!
""")


# ============================================================
# 🏆 INTERVIEW QUESTIONS
# ============================================================
print("\n" + "="*60)
print("🏆 INTERVIEW QUESTIONS YOU CAN NOW ANSWER")
print("="*60)

print("""
1. What is the difference between supervised and unsupervised learning?
   → Supervised: Has labeled target (like our Converted column)
   → Unsupervised: No labels, finds patterns (clustering, anomaly detection)

2. What is overfitting and how do you prevent it?
   → Model memorizes training data, fails on new data
   → Prevention: Train/test split, cross-validation, regularization

3. What is feature engineering?
   → Creating new features from raw data
   → Example: One-hot encoding Industry column

4. Why do we scale features?
   → Many algorithms assume features are on similar scales
   → Helps optimization converge faster

5. What is the difference between accuracy and precision/recall?
   → Accuracy: Overall correct predictions
   → Precision: Of predicted positives, how many are correct?
   → Recall: Of actual positives, how many did we find?

6. When would you use Logistic Regression vs Random Forest?
   → Logistic Regression: Simple, interpretable, baseline
   → Random Forest: Non-linear, handles feature interactions

7. How do you handle missing data?
   → Drop rows, impute with mean/median, use algorithms that handle it

8. What is cross-validation?
   → Rotate train/test splits to get more robust estimates
   → K-fold: Split data into K parts, train K times

9. How do you choose features?
   → Domain knowledge, correlation analysis, feature importance

10. How would you deploy this model?
    → Save with joblib/pickle, create API endpoint, integrate with app
""")


# ============================================================
# 🏆 SUMMARY
# ============================================================
print("\n" + "="*60)
print("🏆 ML FUNDAMENTALS COMPLETE!")
print("="*60)
print("""
You built a complete ML pipeline:
✅ Data preparation and feature engineering
✅ Train/test split
✅ Model training (Logistic Regression, Random Forest)
✅ Evaluation (accuracy, precision, recall, confusion matrix)
✅ Feature importance analysis
✅ Making predictions
✅ Saving models for production

KEY TAKEAWAYS:
• ML is about finding patterns in data
• Feature engineering is often more important than model choice
• Always evaluate on unseen data (test set)
• Interpretability matters in business contexts

NEXT: Move to GenAI where we'll use LLMs instead of traditional ML!
      The concepts you learned here (features, training, evaluation) 
      still apply, but the approach is different.
""")

# Cleanup
import os
if os.path.exists('lead_scorer_model.pkl'):
    os.remove('lead_scorer_model.pkl')
if os.path.exists('lead_scorer_scaler.pkl'):
    os.remove('lead_scorer_scaler.pkl')
