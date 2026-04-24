import pandas as pd
import os

class CalorieEstimator:
    def __init__(self, db_path="data/food_database.csv"):
        self.db_path = db_path
        if os.path.exists(self.db_path):
            self.db = pd.read_csv(self.db_path)
        else:
            self.db = pd.DataFrame(columns=["food_item", "calories_per_100g", "protein_per_100g", "carbs_per_100g", "fat_per_100g", "category"])
            
    def estimate_calories(self, food_label, weight_g=100):
        # basic text matching. The food label from the model might have underscores or be multiple words.
        food_label = food_label.lower().replace("_", " ")
        
        # Check for partial matches
        # e.g., if label is "apple pie", and we have "apple" in db
        match = self.db[self.db['food_item'].apply(lambda x: x in food_label or food_label in x)]
        
        if not match.empty:
            # Sort by length of match to get the most specific one if multiple exist
            # Or just take the first
            row = match.iloc[0]
            multiplier = weight_g / 100.0
            return {
                "food_item": row["food_item"],
                "calories": round(row["calories_per_100g"] * multiplier, 1),
                "protein": round(row["protein_per_100g"] * multiplier, 1),
                "carbs": round(row["carbs_per_100g"] * multiplier, 1),
                "fat": round(row["fat_per_100g"] * multiplier, 1),
                "weight_g": weight_g,
                "found": True
            }
        else:
            return {
                "food_item": food_label,
                "calories": 0,
                "protein": 0,
                "carbs": 0,
                "fat": 0,
                "weight_g": weight_g,
                "found": False
            }
