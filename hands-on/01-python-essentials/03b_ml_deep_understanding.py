"""
============================================================
ML FUNDAMENTALS - DEEP UNDERSTANDING SESSION
============================================================
Run this file section by section in VS Code/Cursor
Use: Shift+Enter to run selected lines (or copy to Python REPL)

This is INTERACTIVE - modify values, experiment, break things!
============================================================
"""

# ============================================================
# CONCEPT 1: WHAT IS MACHINE LEARNING REALLY?
# ============================================================
"""
🧠 THE CORE IDEA:

Machine Learning = Finding patterns in data to make predictions

Think of it like this (Salesforce analogy):

TRADITIONAL PROGRAMMING (Apex):
    IF lead.Employees > 500 AND lead.Industry = 'Technology' THEN
        lead.Rating = 'Hot'
    
    → YOU write the rules manually
    → Rules are fixed
    → You need domain expertise to write good rules

MACHINE LEARNING:
    → You give examples: "These leads converted, these didn't"
    → Algorithm FINDS the patterns automatically
    → Patterns can be complex (combinations you'd never think of)
    → Model can find: "Leads with 200-500 employees in Finance 
       who responded within 24 hours convert 3x more"

KEY INSIGHT: ML doesn't replace your expertise - it finds patterns
in data that are too complex for humans to manually code.
"""

print("="*60)
print("CONCEPT 1: What is ML?")
print("="*60)

# Let's prove this with real code
import numpy as np
import pandas as pd

# Simple data: [employees, response_time_hours]
# Label: 1 = converted, 0 = didn't convert
data = [
    [100, 48, 0],   # Small company, slow response → No
    [500, 12, 1],   # Medium company, fast response → Yes
    [50, 72, 0],    # Tiny company, very slow → No
    [1000, 6, 1],   # Large company, very fast → Yes
    [200, 24, 1],   # Medium company, decent response → Yes
    [75, 60, 0],    # Small company, slow → No
    [800, 8, 1],    # Large company, fast → Yes
    [150, 36, 0],   # Small-medium, medium response → No
]

df = pd.DataFrame(data, columns=['employees', 'response_hours', 'converted'])
print("\nSample Lead Data:")
print(df)

# What patterns do YOU see?
print("""
❓ EXERCISE 1: Look at the data above.
   What patterns do you notice?
   
   Think about it, then scroll down...
   
   
   
   
   
   
   
   
   
   
PATTERNS:
- Larger companies (>200 employees) tend to convert
- Faster response times (<24 hours) tend to convert
- Combination matters: 200 employees + 24hr response = Yes
                       150 employees + 36hr response = No

ML finds these patterns AUTOMATICALLY from thousands of examples!
""")


# ============================================================
# CONCEPT 2: FEATURES AND LABELS (X and y)
# ============================================================
print("\n" + "="*60)
print("CONCEPT 2: Features (X) vs Labels (y)")
print("="*60)

"""
🎯 THE VOCABULARY:

FEATURES (X) = The information you use to make predictions
    → Employees, ResponseTime, Industry, HasEmail, etc.
    → Like the fields on a Lead record
    → INPUT to the model

LABELS (y) = What you're trying to predict
    → Converted (Yes/No)
    → Also called: target, outcome, dependent variable
    → OUTPUT of the model

TRAINING = Show the model examples with known labels
PREDICTION = Use trained model on new data without labels
"""

# Separate features and labels
X = df[['employees', 'response_hours']]  # Features
y = df['converted']                       # Label

print("\nFeatures (X) - what we use to predict:")
print(X)
print("\nLabels (y) - what we're predicting:")
print(y.tolist())

print("""
❓ EXERCISE 2: In Salesforce terms...

If you wanted to predict Opportunity Win/Loss:

FEATURES (X) would be:
- Amount
- Stage duration
- Number of competitors
- Product count
- Account industry
- etc.

LABEL (y) would be:
- IsWon (True/False)

What features would you use to predict Lead Conversion?
Think of 5 fields from your Lead object...
""")


# ============================================================
# CONCEPT 3: TRAIN/TEST SPLIT - WHY IT MATTERS
# ============================================================
print("\n" + "="*60)
print("CONCEPT 3: Train/Test Split")
print("="*60)

"""
🎓 THE PROBLEM:

If you train a model on ALL your data, how do you know it works?

Imagine a student who memorizes all the answers:
- They score 100% on practice tests
- But they FAIL on the real exam with new questions

This is called OVERFITTING - the model memorized, didn't learn.

THE SOLUTION:

Split your data:
- TRAINING SET (80%): Model learns from this
- TEST SET (20%): Model never sees this during training
                  Used only to evaluate performance

If model does well on TEST set → It learned real patterns!
If model does poorly on TEST set → It just memorized training data.
"""

from sklearn.model_selection import train_test_split

# Create a larger dataset for demonstration
np.random.seed(42)
n = 100

# Generate fake lead data
employees = np.random.randint(50, 2000, n)
response_hours = np.random.randint(1, 72, n)

# Create a realistic conversion pattern
# Higher employees + lower response time = more likely to convert
conversion_score = (employees / 500) + (50 / response_hours) + np.random.randn(n) * 0.5
converted = (conversion_score > 2).astype(int)

X = pd.DataFrame({'employees': employees, 'response_hours': response_hours})
y = pd.Series(converted)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2,      # 20% for testing
    random_state=42     # For reproducibility
)

print(f"Total samples: {len(X)}")
print(f"Training samples: {len(X_train)} ({len(X_train)/len(X)*100:.0f}%)")
print(f"Test samples: {len(X_test)} ({len(X_test)/len(X)*100:.0f}%)")

print("""
❓ EXERCISE 3: Why can't we evaluate on training data?

Think about it:
- Model sees training data during learning
- If we test on training data, it's like giving same test twice
- High score doesn't mean model is good, just that it memorized

Real test: How well does it do on data it's NEVER seen?
""")


# ============================================================
# CONCEPT 4: HOW THE MODEL ACTUALLY LEARNS
# ============================================================
print("\n" + "="*60)
print("CONCEPT 4: How Models Learn")
print("="*60)

"""
🔧 LOGISTIC REGRESSION - The Simplest Classification Model

Think of it as finding the best "line" to separate classes:

        Converted
           │
         1 ●  ●  ●    ← These converted
           │    ────── Best dividing line
         0 ●  ●  ●    ← These didn't
           └──────────
             Employees →

The model learns:
- Each feature gets a WEIGHT (importance)
- Weights are adjusted until predictions are most accurate
- Final formula: P(convert) = sigmoid(w1*employees + w2*response + ...)

LEARNING PROCESS:
1. Start with random weights
2. Make predictions
3. Calculate error (how wrong we are)
4. Adjust weights to reduce error
5. Repeat 1000s of times
6. Stop when error stops improving
"""

from sklearn.linear_model import LogisticRegression

# Create and train model
model = LogisticRegression()
model.fit(X_train, y_train)  # This is where learning happens!

print("Model trained!")
print(f"\nLearned weights:")
print(f"  employees coefficient: {model.coef_[0][0]:.4f}")
print(f"  response_hours coefficient: {model.coef_[0][1]:.4f}")
print(f"  intercept (bias): {model.intercept_[0]:.4f}")

print("""
📊 INTERPRETING WEIGHTS:

Positive weight → Feature INCREASES conversion probability
Negative weight → Feature DECREASES conversion probability
Larger absolute value → Stronger effect

From above:
- Employees has POSITIVE weight → More employees = more likely to convert
- Response hours has NEGATIVE weight → Longer response = less likely to convert

This matches our intuition!
""")


# ============================================================
# CONCEPT 5: MAKING PREDICTIONS
# ============================================================
print("\n" + "="*60)
print("CONCEPT 5: Making Predictions")
print("="*60)

# New leads to score
new_leads = pd.DataFrame([
    {'employees': 1000, 'response_hours': 4},   # Big, fast
    {'employees': 50, 'response_hours': 60},    # Small, slow
    {'employees': 300, 'response_hours': 24},   # Medium, medium
])

print("New leads to score:")
print(new_leads)

# Predict class (0 or 1)
predictions = model.predict(new_leads)
print(f"\nPredicted class: {predictions}")

# Predict probability
probabilities = model.predict_proba(new_leads)
print(f"\nPredicted probabilities:")
for i, (row, prob) in enumerate(zip(new_leads.values, probabilities)):
    print(f"  Lead {i+1}: {prob[1]*100:.1f}% chance of conversion")

print("""
❓ EXERCISE 4: Make your own predictions!

Modify the new_leads DataFrame above with different values:
- What happens with 5000 employees and 1 hour response?
- What happens with 10 employees and 100 hour response?
- Find the "boundary" where prediction flips from 0 to 1

Try it! Change the values and re-run this cell.
""")


# ============================================================
# CONCEPT 6: EVALUATING THE MODEL
# ============================================================
print("\n" + "="*60)
print("CONCEPT 6: Evaluation Metrics")
print("="*60)

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Predictions on TEST set (data model never saw!)
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy*100:.1f}%")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print(f"""
Confusion Matrix:
                 Predicted
                 No    Yes
Actual No      [{cm[0,0]:3d}   {cm[0,1]:3d}]
       Yes     [{cm[1,0]:3d}   {cm[1,1]:3d}]

Reading this:
- Top-left ({cm[0,0]}): Correctly predicted "No" (True Negatives)
- Top-right ({cm[0,1]}): Predicted "Yes" but was "No" (False Positives)
- Bottom-left ({cm[1,0]}): Predicted "No" but was "Yes" (False Negatives)  
- Bottom-right ({cm[1,1]}): Correctly predicted "Yes" (True Positives)
""")

print("""
🎯 KEY METRICS EXPLAINED:

ACCURACY = (Correct predictions) / (Total predictions)
    → Simple but can be misleading with imbalanced data
    
PRECISION = (True Positives) / (All Positive Predictions)
    → "Of the leads I said would convert, how many actually did?"
    → Important when FALSE POSITIVES are costly (wasting sales time)
    
RECALL = (True Positives) / (All Actual Positives)
    → "Of all leads that converted, how many did I catch?"
    → Important when FALSE NEGATIVES are costly (missing hot leads)
    
F1 SCORE = Balance between Precision and Recall
    → Use when you care about both equally

SALESFORCE EXAMPLE:
- High Precision: Don't waste sales reps' time on bad leads
- High Recall: Don't miss any potential customers
- Usually you need to balance both!
""")


# ============================================================
# CONCEPT 7: PUTTING IT ALL TOGETHER
# ============================================================
print("\n" + "="*60)
print("CONCEPT 7: The Complete Picture")
print("="*60)

print("""
🔄 THE ML WORKFLOW:

    ┌─────────────────┐
    │   RAW DATA      │  ← Export from Salesforce
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │  PREPARE DATA   │  ← Clean, encode, feature engineering
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │   SPLIT DATA    │  ← 80% train, 20% test
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │  TRAIN MODEL    │  ← Algorithm learns patterns
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │   EVALUATE      │  ← Test on held-out data
    └────────┬────────┘
             │
    ┌────────┴────────┐
    │  Good enough?   │
    └────────┬────────┘
         No  │  Yes
             │    │
    ┌────────▼─┐  │
    │  Improve │  │
    │  (tune,  │  │
    │  features│  │
    │   etc.)  │  │
    └──────────┘  │
             ┌───▼───────────┐
             │    DEPLOY     │  ← Use in production
             └───────────────┘


HOW THIS CONNECTS TO YOUR EXISTING WORK:

Your current API server could:
1. Export Lead data from Salesforce (you have sf_query!)
2. Train a model on historical conversions
3. Score new leads in real-time
4. Claude could explain WHY a lead scored high/low

That's AI-powered lead scoring in Salesforce!
""")


# ============================================================
# FINAL EXERCISES - TEST YOUR UNDERSTANDING
# ============================================================
print("\n" + "="*60)
print("📝 FINAL EXERCISES")
print("="*60)

print("""
Complete these to confirm understanding:

1. VOCABULARY CHECK:
   Match the terms:
   a) Features       ___  What you're trying to predict
   b) Labels         ___  Input data (columns)
   c) Training set   ___  Data used to evaluate
   d) Test set       ___  Data used to learn

   (Answers: a-Input data, b-What you predict, c-Learn, d-Evaluate)

2. EXPLAIN TO A COLLEAGUE:
   Imagine explaining to a Salesforce Admin:
   "What is machine learning and how could we use it for leads?"
   
   Write 3-4 sentences in plain English.

3. CODE EXERCISE:
   Using the code above, answer:
   - What's the accuracy of our model? ____%
   - Which feature is more important for prediction?
   - If a lead has 500 employees and 12hr response, will it convert?

4. CRITICAL THINKING:
   - Why do we split data into train/test?
   - What would happen if we only had 10 training examples?
   - When would high Recall be more important than Precision?

5. SALESFORCE APPLICATION:
   List 5 things you could predict with ML in Salesforce:
   - Lead conversion (we did this!)
   - Opportunity win probability
   - ??? (think of 3 more)
""")


# ============================================================
# ANSWERS
# ============================================================
print("""
When ready, scroll down for answers...
















ANSWERS:

1. VOCABULARY:
   a) Features → Input data (columns)
   b) Labels → What you're trying to predict  
   c) Training set → Data used to learn
   d) Test set → Data used to evaluate

2. EXPLANATION EXAMPLE:
   "Machine learning lets us find patterns in our historical data 
   automatically. Instead of writing rules like 'if company > 500 
   employees, mark as Hot', we show the computer thousands of past 
   leads and it figures out what made them convert. Then it can 
   score new leads based on those patterns."

3. CODE EXERCISE:
   - Accuracy: Check the output above (varies, ~70-80%)
   - employees has higher absolute coefficient = more important
   - 500 employees + 12hr response → Likely converts (run the code!)

4. CRITICAL THINKING:
   - Split: To test on data model hasn't memorized
   - 10 examples: Model would overfit, wouldn't generalize
   - High Recall: When missing a lead is worse than wasting time 
     (e.g., high-value enterprise deals)

5. SALESFORCE ML USE CASES:
   - Case escalation prediction
   - Churn risk scoring
   - Deal amount prediction
   - Support ticket routing
   - Customer lifetime value
   - Optimal send time for emails
   - Product recommendations
""")

print("\n" + "="*60)
print("✅ ML DEEP UNDERSTANDING COMPLETE!")
print("="*60)
print("""
You now truly understand:
✅ What ML is (pattern finding, not rule writing)
✅ Features vs Labels (inputs vs output)
✅ Train/Test split (prevent memorization)
✅ How models learn (weights, optimization)
✅ Making predictions (class + probability)
✅ Evaluation metrics (accuracy, precision, recall)
✅ When to use which metric

NEXT: Move to GenAI fundamentals!
      python3 hands-on/02-genai-fundamentals/01_how_llms_work.py
""")
