"""
============================================================
MODULE 1: PYTHON ESSENTIALS FOR JS/APEX DEVELOPERS
============================================================
Time: 30-45 minutes
Goal: Get comfortable with Python syntax for AI development

HOW TO RUN THIS FILE:
1. Open terminal in this folder
2. Activate venv: source ../venv/bin/activate
3. Run: python3 01_python_for_js_devs.py

Or run section by section in VS Code/Cursor
============================================================
"""

# ============================================================
# SECTION 1: VARIABLES & DATA TYPES
# ============================================================
# JavaScript:  let name = "Arsh"; const age = 30;
# Python:      No let/const, just assign directly

print("\n=== SECTION 1: Variables ===")

name = "Arsh"
age = 30
is_developer = True  # Note: True/False are capitalized in Python

# Multiple assignment (Python superpower)
x, y, z = 1, 2, 3
first, *rest = [1, 2, 3, 4, 5]  # first=1, rest=[2,3,4,5]

print(f"Name: {name}, Age: {age}")  # f-strings = template literals
print(f"Multiple assignment: x={x}, y={y}, z={z}")
print(f"Unpacking: first={first}, rest={rest}")

# YOUR TURN: Create variables for your Salesforce experience
# sf_experience = ???
# technologies = ???  (make it a list)


# ============================================================
# SECTION 2: LISTS (JavaScript Arrays)
# ============================================================
print("\n=== SECTION 2: Lists ===")

# JavaScript: const arr = [1, 2, 3]; arr.push(4); arr.map(x => x * 2)
# Python: Much more powerful!

numbers = [1, 2, 3, 4, 5]
numbers.append(6)  # like push()

# List comprehension (THIS IS HUGE IN AI/ML CODE!)
# JavaScript: numbers.map(x => x * 2)
# Python:
doubled = [x * 2 for x in numbers]
print(f"Doubled: {doubled}")

# Filtered list comprehension
# JavaScript: numbers.filter(x => x > 3).map(x => x * 2)
# Python:
filtered_doubled = [x * 2 for x in numbers if x > 3]
print(f"Filtered & doubled: {filtered_doubled}")

# Slicing (super common in AI for data manipulation)
print(f"First 3: {numbers[:3]}")      # [1, 2, 3]
print(f"Last 3: {numbers[-3:]}")      # [4, 5, 6]
print(f"Every 2nd: {numbers[::2]}")   # [1, 3, 5]
print(f"Reversed: {numbers[::-1]}")   # [6, 5, 4, 3, 2, 1]

# YOUR TURN: Create a list of Salesforce objects and:
# 1. Add a new object
# 2. Get only objects starting with 'A' (hint: use list comprehension with if)
sf_objects = ["Account", "Contact", "Lead", "Opportunity"]


# ============================================================
# SECTION 3: DICTIONARIES (JavaScript Objects)
# ============================================================
print("\n=== SECTION 3: Dictionaries ===")

# JavaScript: { name: "John", age: 30 }
# Python: Keys must be strings (usually), values can be anything

person = {
    "name": "Arsh",
    "role": "Salesforce Architect",
    "skills": ["Apex", "LWC", "Integration"],
    "experience": 10
}

# Access values
print(f"Name: {person['name']}")
print(f"Skills: {person.get('skills')}")  # .get() is safer (returns None if missing)

# Dictionary comprehension (very common in AI)
skills_upper = {k: v.upper() if isinstance(v, str) else v for k, v in person.items()}
print(f"Uppercase strings: {skills_upper}")

# Nested dictionaries (you'll see this A LOT in API responses)
api_response = {
    "status": "success",
    "data": {
        "accounts": [
            {"id": "001", "name": "Acme Corp"},
            {"id": "002", "name": "Tech Inc"}
        ]
    }
}

# Access nested data
accounts = api_response["data"]["accounts"]
print(f"First account: {accounts[0]['name']}")

# YOUR TURN: Create a dictionary representing a Salesforce Lead
# Include: firstName, lastName, company, status, isConverted


# ============================================================
# SECTION 4: FUNCTIONS
# ============================================================
print("\n=== SECTION 4: Functions ===")

# JavaScript: function greet(name) { return `Hello ${name}`; }
# JavaScript: const greet = (name) => `Hello ${name}`;
# Python:

def greet(name):
    return f"Hello {name}"

# With type hints (very common in modern Python, helps with AI libraries)
def greet_typed(name: str) -> str:
    return f"Hello {name}"

# Default parameters
def create_lead(name: str, company: str, status: str = "Open"):
    return {"name": name, "company": company, "status": status}

print(create_lead("John", "Acme"))  # Uses default status
print(create_lead("Jane", "Tech", "Qualified"))  # Override status

# *args and **kwargs (you'll see these in AI libraries)
def flexible_function(*args, **kwargs):
    print(f"Args: {args}")      # Tuple of positional args
    print(f"Kwargs: {kwargs}")  # Dict of keyword args

flexible_function(1, 2, 3, name="Arsh", role="Developer")

# Lambda functions (like arrow functions)
# JavaScript: const double = x => x * 2
# Python:
double = lambda x: x * 2
print(f"Lambda double(5): {double(5)}")

# YOUR TURN: Create a function that takes a Salesforce record dict
# and returns a formatted string like "Account: Acme Corp (ID: 001)"


# ============================================================
# SECTION 5: CLASSES (Similar to Apex!)
# ============================================================
print("\n=== SECTION 5: Classes ===")

class SalesforceRecord:
    """Base class for Salesforce records - similar to Apex classes!"""
    
    def __init__(self, id: str, name: str):  # Constructor like Apex
        self.id = id
        self.name = name
        self.created_date = "2024-01-01"  # Instance variable
    
    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name}
    
    def __str__(self) -> str:  # Like Apex toString()
        return f"{self.__class__.__name__}: {self.name} ({self.id})"


class Account(SalesforceRecord):
    """Account class extending SalesforceRecord"""
    
    def __init__(self, id: str, name: str, industry: str = None):
        super().__init__(id, name)  # Call parent constructor
        self.industry = industry
        self.contacts = []
    
    def add_contact(self, contact_name: str):
        self.contacts.append(contact_name)
    
    def to_dict(self) -> dict:
        base = super().to_dict()
        base["industry"] = self.industry
        base["contacts"] = self.contacts
        return base


# Using the classes
acc = Account("001ABC", "Acme Corp", "Technology")
acc.add_contact("John Smith")
acc.add_contact("Jane Doe")

print(acc)
print(f"As dict: {acc.to_dict()}")

# YOUR TURN: Create a Lead class with:
# - Properties: id, firstName, lastName, company, status
# - Method: qualify() that changes status to "Qualified"
# - Method: full_name() that returns "FirstName LastName"


# ============================================================
# SECTION 6: ERROR HANDLING
# ============================================================
print("\n=== SECTION 6: Error Handling ===")

# JavaScript: try { } catch (e) { } finally { }
# Python: try: except: finally:

def safe_divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("Cannot divide by zero!")
        return None
    except TypeError as e:
        print(f"Type error: {e}")
        return None
    finally:
        print("Division attempted")

print(f"10/2 = {safe_divide(10, 2)}")
print(f"10/0 = {safe_divide(10, 0)}")

# Raising exceptions (like throw in JS)
def validate_lead(lead: dict):
    if not lead.get("company"):
        raise ValueError("Lead must have a company!")
    return True


# ============================================================
# SECTION 7: MODULES & IMPORTS
# ============================================================
print("\n=== SECTION 7: Imports ===")

# Python import styles (you'll use ALL of these in AI)
import json  # Import entire module
from datetime import datetime  # Import specific item
from typing import List, Dict, Optional  # Type hints

# Common AI imports you'll see:
# import numpy as np
# import pandas as pd
# from langchain import LLM
# from anthropic import Anthropic

# Using imports
data = {"name": "Arsh", "skills": ["AI", "Salesforce"]}
json_string = json.dumps(data, indent=2)
print(f"JSON:\n{json_string}")

now = datetime.now()
print(f"Current time: {now}")


# ============================================================
# SECTION 8: FILE OPERATIONS (Used in AI for data loading)
# ============================================================
print("\n=== SECTION 8: File Operations ===")

# Writing to file
sample_data = [
    {"name": "Account 1", "type": "Customer"},
    {"name": "Account 2", "type": "Partner"}
]

# Context manager (with) automatically closes file
with open("sample_data.json", "w") as f:
    json.dump(sample_data, f, indent=2)
print("Wrote sample_data.json")

# Reading from file
with open("sample_data.json", "r") as f:
    loaded_data = json.load(f)
print(f"Loaded: {loaded_data}")

# Clean up
import os
os.remove("sample_data.json")
print("Cleaned up sample file")


# ============================================================
# SECTION 9: ASYNC/AWAIT (For API calls in AI)
# ============================================================
print("\n=== SECTION 9: Async (Preview) ===")

import asyncio

async def fetch_data(name: str) -> dict:
    """Simulates an async API call"""
    await asyncio.sleep(0.1)  # Simulate network delay
    return {"name": name, "status": "fetched"}

async def main():
    # Run multiple async operations concurrently
    results = await asyncio.gather(
        fetch_data("Account"),
        fetch_data("Contact"),
        fetch_data("Lead")
    )
    return results

# Run async code
results = asyncio.run(main())
print(f"Async results: {results}")


# ============================================================
# 🎯 PRACTICE EXERCISES
# ============================================================
print("\n" + "="*60)
print("🎯 PRACTICE EXERCISES")
print("="*60)

print("""
EXERCISE 1: Data Transformation
--------------------------------
Given this list of leads, create a new list with only qualified leads,
and transform each to have only 'name' and 'company' fields.

leads = [
    {"name": "John", "company": "Acme", "status": "Qualified"},
    {"name": "Jane", "company": "Tech", "status": "Open"},
    {"name": "Bob", "company": "Corp", "status": "Qualified"},
]

Expected output: [{"name": "John", "company": "Acme"}, {"name": "Bob", "company": "Corp"}]

YOUR CODE HERE:
qualified = ???


EXERCISE 2: API Response Parser
-------------------------------
Write a function that takes a Salesforce API response and returns
a simplified list of records.

def parse_sf_response(response: dict) -> list:
    '''
    Input: {"totalSize": 2, "done": True, "records": [{"Id": "001", "Name": "A"}, {"Id": "002", "Name": "B"}]}
    Output: [{"id": "001", "name": "A"}, {"id": "002", "name": "B"}]
    '''
    pass


EXERCISE 3: Create a Lead Qualifier Class
-----------------------------------------
Create a LeadQualifier class that:
- Takes a lead dict in constructor
- Has method score() that returns 0-100 based on criteria
- Has method qualify() that returns "Hot", "Warm", or "Cold"

Scoring criteria (make up your own!):
- Has email: +30 points
- Has phone: +20 points
- Company size > 100: +30 points
- Industry is "Technology": +20 points

""")


# ============================================================
# 🏆 SUMMARY
# ============================================================
print("\n" + "="*60)
print("🏆 PYTHON ESSENTIALS COMPLETE!")
print("="*60)
print("""
You now know enough Python to:
✅ Read and write AI/ML code
✅ Work with data structures
✅ Create classes (similar to Apex)
✅ Handle errors
✅ Work with files and JSON
✅ Use async/await for API calls

NEXT: Run this file, complete the exercises, then move to:
      02_numpy_pandas_basics.py
""")
