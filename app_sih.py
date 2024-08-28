from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')  # Ensure you have an index.html in the templates folder

# Route for handling chatbot messages
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    # Process the user message and generate a response
    bot_response = generate_response(user_message)
    return jsonify({'response': bot_response})

# Function to generate a chatbot response
def generate_response(message):
    # Implement your chatbot logic here
    return "Hello! How can I assist you today?"

# Route for favicon (optional, prevents 404 errors for favicon requests)
@app.route('/favicon.ico')
def favicon():
    return '', 204  # Return a 'No Content' response for the favicon request

if __name__ == '__main__':
    app.run(debug=True)
