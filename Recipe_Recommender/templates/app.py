from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from ultralytics import YOLO
import requests
from PIL import Image
import io
import os

app = Flask(__name__)
CORS(app)

model = YOLO("yolov10s.pt")  
api_key = '19d094d105d340e7910fb7587fbf00fb'

food_classes = [
    "apple", "banana", "orange", "broccoli", "carrot"]

@app.route("/")
def index():
    return render_template("index.html")

def predict_image(file_bytes, confidence_threshold=0.5):
    image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    image_path = "temp.jpg"
    image.save(image_path)

    results = model(image_path)
    os.remove(image_path)

    detected = set()
    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        class_name = results[0].names[cls_id]
        confidence = float(box.conf[0])
        if class_name in food_classes and confidence > confidence_threshold:
            detected.add(class_name)

    return list(detected)

def get_recipes_from_ingredients(ingredients, number=5):
    if not ingredients:
        return []

    url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "ingredients": ",".join(ingredients),
        "number": number,
        "ranking": 1,
        "ignorePantry": True,
        "apiKey": api_key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        recipes = []
        for r in data:
            recipe_id = r.get("id")
            title = r.get("title")
            used_ingredients = [i["name"] for i in r.get("usedIngredients", [])]
            missed_ingredients = [i["name"] for i in r.get("missedIngredients", [])]
            link = f"https://spoonacular.com/recipes/{title.replace(' ', '-').lower()}-{recipe_id}"

            recipes.append({
                "title": title,
                "ingredients": used_ingredients,
                "missingIngredients": missed_ingredients,
                "link": link
            })

        return recipes
    except requests.exceptions.RequestException as e:
        print(f"API error: {e}")
        return []

@app.route("/api/recognize-image", methods=["POST"])
def recognize_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files['image']
    image_bytes = image_file.read()

    ingredients = predict_image(image_bytes)

    if not ingredients:
        return jsonify({"predictedIngredients": [], "recipes": []})

    recipes = get_recipes_from_ingredients(ingredients)
    return jsonify({
        "predictedIngredients": ingredients,
        "recipes": recipes
    })

if __name__ == "__main__":
    app.run(debug=True)
