#!/usr/bin/env python
import pandas as pd
import sys
import os

# Load dataset
df = pd.read_csv('results/filt_surveys_format_category.tsv', sep='\t', index_col=0)

# Drop zone question
df = df.drop(columns=['Q2'])

# Define a custom order for responses (adding 'Ground Floor' and 'Higher than Ground Floor')
custom_order = [
    '18-34', '35-54', '55-74', '75-84', 
    'Yes', 'No', 'Unsure',
    'Not Worried', 'Partly Worried', 'Worried', 'Very Worried',
    'Not Urgent', 'Somewhat urgent', 'Moderately Urgent', 'Very urgent',
    'Male/Tāne', 'Female/Wahine', 'Another Gender/ He ira kē anō',
    'New Zealand European', 'Māori', 'Pacific', 'Asian', 'Middle Eastern/Latin American/Africa', 'Other (Please state)',
    'A (e.g. Apartment)', 'B (e.g. Row/Terrace home)', 'C (e.g. Detached house)',
    'Homeowner', 'Renter', 'Renter and homeowner on same property', 'Family Home', 'Other (please specify)',
    'Less than 1 year', '1-5 years', '6-10 years', '11-15 years', '16-20 years', '20 years+',
    'Ground Floor', 'Higher than Ground Floor', 'New Lynn', 'Mount Eden'
]

# Create an empty list to store formatted data
formatted_data = []

for col in df.columns:
    # Convert values to string and strip whitespace
    question = df[col].astype(str).str.strip()
    
    # Replace any value not in custom_order with "Unanswered"
    question = question.where(question.isin(custom_order), other="Unanswered")
    
    # Now count responses, including the replaced ones
    counts = question.value_counts(dropna=False)
    total = counts.sum()
    percentages = (counts / total) * 100

    col_df = pd.DataFrame({
        'Question': col,
        'Response': counts.index,
        'Count': [f"{x}/{total}" for x in counts],
        'Percentage': percentages.values
    })

    # Convert 'Response' to categorical with custom order
    full_order = custom_order.copy()
    if "Unanswered" not in full_order:
        full_order.append("Unanswered")

    # Apply categorical type to ensure custom order
    col_df['Response'] = pd.Categorical(col_df['Response'], categories=full_order, ordered=True)
    col_df['Response'] = col_df['Response'].astype(str)

    # Sort based on 'Response' column, ensuring the custom order is followed
    col_df = col_df.sort_values(by=['Question', 'Response'], key=lambda x: x.map({val: idx for idx, val in enumerate(full_order)}))

    # Append all other responses
    formatted_data.append(col_df)

# Combine all columns into a single DataFrame
result = pd.concat(formatted_data, ignore_index=True)

# Save
result.to_csv('results/proportions.tsv', sep='\t', index=False)
print("Proportions saved") 

