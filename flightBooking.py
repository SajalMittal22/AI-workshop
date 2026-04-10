from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

@app.route('/')
def home():
    return send_file("form.htm", as_attachment=False)

@app.route('/form', methods=['POST'])
def airWays():
    data = request.get_json()
    user = data.get("message", "").lower()

    # greetings
    if any(x in user for x in ["hello", "hey"]):
        reply = "Hello! 👋 How can I assist you today?"

    # start booking
    elif "book" in user or "flight" in user:
        reply = "Sure! Where would you like to travel? ✈️"

    # route detection
    elif "from" in user and "to" in user:
        reply = "Great! When would you like to fly?"

    # city mention
    elif any(city in user for city in ["delhi", "mumbai", "chennai", "bangalore", "kolkata"]):
        reply = "Please provide full route (e.g., Delhi to Mumbai)"

    # date
    elif any(x in user for x in ["today", "tomorrow", "next week", "next month"]):
        reply = "How many passengers will be traveling?"

    # passengers
    elif any(x in user for x in ["1", "one", "2", "two", "3", "three"]):
        reply = "Which class would you prefer? Economy, Business, or First Class?"

    # class selection
    elif "economy" in user:
        reply = "Economy class selected 💺 Ticket price: $50. Type 'confirm' to proceed."

    elif "business" in user:
        reply = "Business class selected 💼 Ticket price: $120. Type 'confirm' to proceed."

    elif "first" in user:
        reply = "First Class selected 🛫 Ticket price: $150. Type 'confirm' to proceed."

    # confirmation
    elif "confirm" in user:
        reply = "✅ Booking confirmed! Your ticket has been successfully booked."

    # cancel
    elif "cancel" in user:
        reply = "❌ Your booking has been cancelled."

    # help
    elif "help" in user:
        reply = "You can say things like 'book a flight', 'Delhi to Mumbai', 'next week', etc."
    else:
        reply = "🤔 Sorry, I didn't understand. Try saying 'book a flight'"

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)