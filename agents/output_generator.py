import json
import os

def save_and_display_results(final_data, output_path="outputs/result.json"):
    """Saves the final JSON and prints a summary."""
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # FIX: Ensure 'f' is the second argument
    with open(output_path, "w") as f:
        json.dump(final_data, f, indent=2) 
    
    print("\n" + "✅ PROCESSING COMPLETE")
    print(f"📍 Final Route: {final_data.get('recommendedRoute', 'N/A')}")
    print(f"📝 Reason: {final_data.get('reasoning', 'N/A')}")
    print(f"📂 Saved to: {output_path}\n")