import pandas as pd
import math
import os
import sys

def calculate_poisson_probability(lmbda, k):
    """Calculates P(X = k) for a Poisson distribution."""
    return (math.pow(lmbda, k) * math.exp(-lmbda)) / math.factorial(k)

def main():
    print("======================================================")
    print("   AGRICULTURAL PEST SIGHTINGS - KAGGLE DATASET ANALYSIS")
    print("======================================================\n")
    
    filename = 'dataset.csv'
    
    # 1. Inform the user to download a dataset from Kaggle if it doesn't exist
    if not os.path.exists(filename):
        print("[!] Dataset not found locally.")
        print("    Please download a formal Pest Detection dataset from Kaggle.")
        print("\n    👉 KAGGLE LINK: https://www.kaggle.com/datasets/vigneshwarans10/smart-pest-detection-agriculture-dataset")
        print(f"\n    Once downloaded, extract the CSV, rename it to '{filename}', place it in this folder, and run this script again.\n")
        return

    try:
        # Load dataset using pandas
        df = pd.read_csv(filename)
        print(f"[*] Successfully loaded dataset: '{filename}'")
        print(f"[*] Total records: {len(df)}")
        print(f"[*] Columns: {', '.join(df.columns)}")
        print("-" * 54)
        
        # Display a quick preview
        print("\nData Preview (First 5 rows):")
        print(df.head().to_string())
        print("-" * 54)
        
        # We need to find the column that represents pest sightings/count
        pest_col = None
        for col in df.columns:
            if 'pest' in col.lower() and ('count' in col.lower() or 'num' in col.lower() or 'severity' in col.lower()):
                pest_col = col
                break
                
        # Fallback to the first numeric column if no obvious 'pest' column exists
        if not pest_col:
            numeric_cols = df.select_dtypes(include='number').columns
            if len(numeric_cols) > 0:
                pest_col = numeric_cols[-1] # Usually the target variable is at the end
            else:
                print("Error: Could not find any numeric column to calculate pest sightings.")
                return
                
        print(f"\n[ANALYSIS] Using column '{pest_col}' as the Pest Sightings variable.")
        
        # Overall Analysis
        overall_lambda = df[pest_col].mean()
        print(f"[GLOBAL] Overall Average Pest Sightings (λ): {overall_lambda:.2f}")
        print("\n" + "=" * 54)
        
        # Interactive Probability Calculation
        print("PROBABILITY CALCULATOR")
        
        threshold_str = input("Enter the action threshold (k) [default=4]: ")
        threshold = int(threshold_str) if threshold_str.strip() else 4
        
        # P(X >= threshold) = 1 - P(X < threshold)
        prob_less_than = sum(calculate_poisson_probability(overall_lambda, i) for i in range(threshold))
        prob_requires_action = 1 - prob_less_than
        
        print("\n--- Final Results ---")
        print(f"Probability of finding {threshold} or more pests: {prob_requires_action:.2%}")
        
        if prob_requires_action >= 0.5:
            print("Risk Level: HIGH RISK 🚨")
        elif prob_requires_action >= 0.2:
            print("Risk Level: MODERATE RISK ⚠️")
        else:
            print("Risk Level: LOW RISK ✅")
            
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{filename}' is empty.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
