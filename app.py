from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# Establish database connection
db_connection = mysql.connector.connect(
    user="chanu",
    password="password",
    host="localhost",
    database="details",
    port= 3306
)
cursor = db_connection.cursor()
cursor.execute('use details')

@app.route('/')
def home():
    return render_template('index.html')  # Your form template


@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        # Log raw request data
        print("Request form data:", request.form)
        
        # Extract form data
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        print("Extracted Data:", name, email, message)  # Debugging extracted data

        # Insert data into the database
        insert_query = "INSERT INTO user_submissions (name, email, message) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (name, email, message))
        db_connection.commit()  # Commit the transaction

        # Send a response back
        return jsonify({"received_data": {"name": name, "email": email, "message": message}}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Something went wrong"}), 500

    


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5001)

