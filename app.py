from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "foodapp123"

# ---------- MENU ----------
menu = {
    "Pizza": [
        ("Margherita Pizza", 200),
        ("Cheese Burst Pizza", 250),
        ("Farmhouse Pizza", 220)
    ],
    "Burger": [
        ("Veg Burger", 80),
        ("Cheese Burger", 120),
        ("Chicken Burger", 150)
    ],
    "Pasta": [
        ("White Sauce Pasta", 180),
        ("Red Sauce Pasta", 170)
    ],
    "Indian": [
        ("Paneer Butter Masala", 200),
        ("Chicken Biryani", 250)
    ],
    "Sweet": [
        ("Ice Cream", 60),
        ("Chocolate Cake", 150),
        ("Gulab Jamun", 80)
    ],
    "Snacks": [
        ("French Fries", 90),
        ("Chicken Nuggets", 130)
    ]
}

# ---------- HOME ----------
@app.route("/", methods=["GET", "POST"])
def home():
    suggestion = ""

    if request.method == "POST":
        food = request.form["food"].lower()

        # all items list (safe fallback)
        all_items = sum(menu.values(), [])

        if "sweet" in food:
            suggestion = "Try " + ", ".join([i[0] for i in menu["Sweet"]])

        elif "spicy" in food:
            suggestion = "Try " + ", ".join([i[0] for i in menu["Indian"]])

        elif "burger" in food:
            suggestion = "Try " + ", ".join([i[0] for i in menu["Burger"]])

        elif "pizza" in food:
            suggestion = "Try " + ", ".join([i[0] for i in menu["Pizza"]])

        elif "pasta" in food:
            suggestion = "Try " + ", ".join([i[0] for i in menu["Pasta"]])

        elif "snacks" in food:
            suggestion = "Try " + ", ".join([i[0] for i in menu["Snacks"]])

        else:
            suggestion = "Try " + random.choice(all_items)[0]

    return render_template("index.html", menu=menu, suggestion=suggestion)


# ---------- ADD TO CART ----------
@app.route("/add/<item>/<int:price>")
def add_to_cart(item, price):

    if "cart" not in session:
        session["cart"] = []

    session["cart"].append({"item": item, "price": price})
    session.modified = True

    return redirect(url_for("home"))


# ---------- CART ----------
@app.route("/cart")
def cart():

    cart = session.get("cart", [])
    total = sum(i["price"] for i in cart)

    return render_template("cart.html", cart=cart, total=total)


# ---------- REMOVE ----------
@app.route("/remove/<int:index>")
def remove(index):

    cart = session.get("cart", [])

    if 0 <= index < len(cart):
        cart.pop(index)

    session["cart"] = cart

    return redirect(url_for("cart"))


# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)