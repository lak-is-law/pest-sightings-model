import pandas as pd
import math
import os
import sys

def calculate_poisson_probability(lmbda, k):
    """Calculates P(X = k) for a Poisson distribution."""
    return (math.pow(lmbda, k) * math.exp(-lmbda)) / math.factorial(k)

def main():
    print("======================================================")
    print("   AGRICULTURAL PEST SIGHTINGS - DATASET ANALYSIS")
    print("======================================================\n")
    
    filename = 'dataset.csv'
    
    if not os.path.exists(filename):
        print(f"[!] Error: {filename} not found in the current directory.")
        return

    try:
        # Load dataset using pandas
        df = pd.read_csv(filename)
        print(f"[*] Successfully loaded formal dataset: '{filename}'")
        print(f"[*] Total records: {len(df)}")
        print(f"[*] Columns: {', '.join(df.columns)}")
        print("-" * 54)
        
        # Display a quick preview
        print("\nData Preview (First 5 rows):")
        # Show subset of interesting columns to fit terminal
        cols_to_show = ['observation_id', 'crop_type', 'avg_temperature_c', 'pest_count_per_plot']
        if all(c in df.columns for c in cols_to_show):
            print(df[cols_to_show].head().to_string(index=False))
        else:
            print(df.head().to_string())
        print("-" * 54)
        
        # Detect the pest count column
        pest_col = 'pest_count_per_plot'
        if pest_col not in df.columns:
            # Fallback
            for col in df.columns:
                if 'pest' in col.lower() and ('count' in col.lower() or 'num' in col.lower()):
                    pest_col = col
                    break
                    
        # Overall Analysis
        overall_lambda = df[pest_col].mean()
        print(f"\n[GLOBAL] Overall Average Pest Sightings (λ): {overall_lambda:.2f} pests/plot")
        
        # Crop-specific Analysis if available
        if 'crop_type' in df.columns:
            print("\n[ANALYSIS] Average Sightings (λ) by Crop Type:")
            crop_stats = df.groupby('crop_type')[pest_col].mean().reset_index()
            for _, row in crop_stats.iterrows():
                print(f"  - {row['crop_type'].ljust(10)}: {row[pest_col]:.2f}")
                
        print("\n" + "=" * 54)
        
        # Interactive Probability Calculation
        print("PROBABILITY CALCULATOR")
        
        crop_choice = ""
        target_lambda = overall_lambda
        scope = "Global"
        
        if 'crop_type' in df.columns:
            crop_choice = input("Enter a Crop Type (e.g. Wheat, Corn, Tomato) or press Enter for Global: ").strip().capitalize()
            if crop_choice and crop_choice in df['crop_type'].unique():
                target_lambda = df[df['crop_type'] == crop_choice][pest_col].mean()
                scope = crop_choice
                
        print(f"Using λ = {target_lambda:.2f} ({scope})")
        
        threshold_str = input("Enter the action threshold (k) [default=4]: ")
        threshold = int(threshold_str) if threshold_str.strip() else 4
        
        # P(X >= threshold) = 1 - P(X < threshold)
        prob_less_than = sum(calculate_poisson_probability(target_lambda, i) for i in range(threshold))
        prob_requires_action = 1 - prob_less_than
        
        print("\n--- Final Results ---")
        print(f"Probability of finding {threshold} or more pests for {scope}: {prob_requires_action:.2%}")
        
        if prob_requires_action >= 0.5:
            print("Risk Level: HIGH RISK 🚨")
        elif prob_requires_action >= 0.2:
            print("Risk Level: MODERATE RISK ⚠️")
        else:
            print("Risk Level: LOW RISK ✅")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
