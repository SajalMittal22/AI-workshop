from flask import Flask, request, jsonify, send_file
import re

app = Flask(__name__)

user_state = {}

@app.route('/')
def home():
    return send_file("form.htm")

@app.route('/form', methods=['POST'])
def chatbot():
    global user_state

    data = request.get_json()
    user = data.get("message", "").lower()

    if not user_state:
        user_state = {
            "step": "start",
            "from": "",
            "to": "",
            "date": "",
            "passengers": "",
            "class": ""
        }

    # START
    if "book" in user:
        user_state["step"] = "route"
        return jsonify({"reply": "✈️ Enter route (e.g., Delhi to Mumbai)"})

    # ROUTE
    if user_state["step"] == "route":
        if "to" in user:
            try:
                parts = user.split("to")
                user_state["from"] = parts[0].strip().title()
                user_state["to"] = parts[1].strip().title()
                user_state["step"] = "date"
                return jsonify({"reply": f"📍 Route: {user_state['from']} ➝ {user_state['to']}\n📅 Enter date (e.g., 12 March 2026)"})
            except:
                return jsonify({"reply": "❌ Please enter like: Delhi to Mumbai"})

    # DATE (day + month + year)
    if user_state["step"] == "date":
        if re.search(r"\d{1,2}\s+\w+\s+\d{4}", user):
            user_state["date"] = user.title()
            user_state["step"] = "passengers"
            return jsonify({"reply": "👥 How many passengers?"})
        else:
            return jsonify({"reply": "❌ Enter full date like: 12 March 2026"})

    # PASSENGERS
    if user_state["step"] == "passengers":
        if user.isdigit():
            user_state["passengers"] = user
            user_state["step"] = "class"
            return jsonify({"reply": "💺 Choose class: Economy / Business / First"})
        else:
            return jsonify({"reply": "❌ Enter number of passengers (e.g., 2)"})

    # CLASS
    if user_state["step"] == "class":
        if "economy" in user:
            price = 50
            user_state["class"] = "Economy"
        elif "business" in user:
            price = 120
            user_state["class"] = "Business"
        elif "first" in user:
            price = 150
            user_state["class"] = "First"
        else:
            return jsonify({"reply": "❌ Choose: Economy / Business / First"})

        user_state["price"] = price
        user_state["step"] = "confirm"

        return jsonify({
            "reply": f"""
🧾 BOOKING SUMMARY:

✈️ Route: {user_state['from']} ➝ {user_state['to']}
📅 Date: {user_state['date']}
👥 Passengers: {user_state['passengers']}
💺 Class: {user_state['class']}
💰 Price per ticket: ${price}
💵 Total: ${int(price) * int(user_state['passengers'])}

👉 Type 'confirm' to book or 'cancel'
"""
        })

    # CONFIRM
    if "confirm" in user:
        final_details = f"""
🎉 BOOKING CONFIRMED!

✈️ {user_state['from']} ➝ {user_state['to']}
📅 {user_state['date']}
👥 {user_state['passengers']} passengers
💺 {user_state['class']}
💰 Total Paid: ${int(user_state['price']) * int(user_state['passengers'])}

🙏 Thank you for choosing FlyBot!
"""

        user_state = {}
        return jsonify({"reply": final_details})

    # CANCEL
    if "cancel" in user:
        user_state = {}
        return jsonify({"reply": "❌ Booking cancelled."})

    return jsonify({"reply": "🤖 Type 'book a flight' to start"})

if __name__ == "__main__":
    app.run(debug=True, port=5001)