import csv
import math

def calculate_poisson_probability(lmbda, k):
    """Calculates P(X = k) for a Poisson distribution."""
    return (math.pow(lmbda, k) * math.exp(-lmbda)) / math.factorial(k)

def main():
    print("--- Pest Sightings Data Analysis ---")
    
    filename = 'dataset.csv'
    total_pests = 0
    num_plots = 0
    
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                total_pests += int(row['Pest_Count'])
                num_plots += 1
                
        lmbda = total_pests / num_plots
        print(f"\n[+] Dataset loaded: {filename}")
        print(f"[+] Total plots analyzed: {num_plots}")
        print(f"[+] Calculated Average Sightings (λ): {lmbda:.2f} pests/plot")
        
        print("\nLet's calculate the probability of a plot needing treatment.")
        threshold_str = input("Enter the action threshold (minimum sightings for treatment) [e.g. 4]: ")
        
        if not threshold_str.strip():
            threshold = 4
        else:
            threshold = int(threshold_str)
        
        # P(X >= threshold) = 1 - P(X < threshold)
        prob_less_than = sum(calculate_poisson_probability(lmbda, i) for i in range(threshold))
        prob_requires_action = 1 - prob_less_than
        
        print("\n--- Results ---")
        print(f"Probability of finding {threshold} or more pests: {prob_requires_action:.2%}")
        
        if prob_requires_action >= 0.5:
            print("Risk Level: HIGH RISK")
        elif prob_requires_action >= 0.2:
            print("Risk Level: MODERATE RISK")
        else:
            print("Risk Level: LOW RISK")
            
    except FileNotFoundError:
        print(f"Error: Could not find '{filename}'. Make sure the dataset is in the same directory.")
    except ValueError:
        print("Error: Invalid input. Please enter a whole number for the threshold.")

if __name__ == "__main__":
    main()
