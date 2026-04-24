class NutritionChatbot:
    def __init__(self):
        # We can implement a simple rule-based bot or use a local LLM later.
        # For offline speed and reliability in this prototype, we'll use rule-based logic
        # combined with simple string matching.
        pass
        
    def generate_response(self, user_message, context):
        """
        Generates a response based on the user's message and the current context (detected food, calories).
        """
        msg = user_message.lower()
        
        if not context:
            return "I don't have any food image context right now. Please upload an image first!"
            
        food_name = context.get('food_item', 'this food')
        calories = context.get('calories', 'unknown')
        protein = context.get('protein', 'unknown')
        
        if "calorie" in msg or "energy" in msg:
            if calories == 'unknown':
                return f"I couldn't estimate the calories for {food_name} as it's not in my database."
            return f"Based on my estimation, {food_name} contains approximately {calories} kcal per {context.get('weight_g', 100)}g."
        elif "protein" in msg or "macros" in msg or "carb" in msg or "fat" in msg:
            if calories == 'unknown':
                return f"I don't have macro information for {food_name}."
            return f"The {food_name} has about {protein}g of protein, {context.get('carbs', 'unknown')}g of carbs, and {context.get('fat', 'unknown')}g of fat."
        elif "healthy" in msg or "good for me" in msg:
            if calories != 'unknown' and float(calories) > 300:
                return f"{food_name.capitalize()} is a bit calorie-dense ({calories} kcal per 100g). Enjoy it in moderation!"
            elif calories != 'unknown':
                return f"{food_name.capitalize()} seems like a relatively light choice ({calories} kcal per 100g)!"
            else:
                return f"I'm not sure about the nutritional profile of {food_name}."
        elif "weight" in msg or "portion" in msg or "size" in msg:
            return "My estimates are based on a standard 100g portion. If your portion is larger or smaller, you'll need to multiply the calories accordingly."
        else:
            return f"I'm your AI Nutrition Assistant. I detected {food_name} in your image. Feel free to ask me about its calories, macros, or healthiness!"
