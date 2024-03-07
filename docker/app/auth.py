from flask import Flask, jsonify, request, session
import time

app = Flask(__name__)

# Set the secret key to enable sessions
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Dictionary to store login attempts and last failed attempt time for each IP
ip_login_attempts = {}

@app.route('/login', methods=['POST'])
def login():
    # Hardcoded valid credentials
    valid_email = 'aryalsubodh4@gmail.com'
    valid_password = 'subodh4444'

    # Get JSON data from the request
    data = request.get_json()

    # Get the IP address of the client making the request
    client_ip = request.remote_addr

    # Check if email, password, and app are provided in the request
    if 'email' not in data or 'password' not in data or 'app' not in data:
        return jsonify({'message': 'email, password, and app are required'}), 400

    # Check if the client IP is currently on cooldown
    if client_ip in ip_login_attempts and ip_login_attempts[client_ip]['cooldown_end'] > time.time():
        cooldown_remaining = int(ip_login_attempts[client_ip]['cooldown_end'] - time.time())
        return jsonify({'message': f'Cooldown active. Try again in {cooldown_remaining} seconds'}), 403

    # Check if the maximum number of failed attempts has been reached for the client IP
    if client_ip in ip_login_attempts and ip_login_attempts[client_ip]['failed_attempts'] >= 5:
        ip_login_attempts[client_ip]['cooldown_end'] = time.time() + 900  # Set cooldown for 15 minutes (900 seconds)
        return jsonify({'message': 'Maximum login attempts reached. Please try again later.'}), 403

    # Check if provided credentials match the valid credentials
    if data['email'] == valid_email and data['password'] == valid_password and data['app'] == 'svp_admin':
        # Reset failed attempts counter upon successful login
        if client_ip in ip_login_attempts:
            ip_login_attempts.pop(client_ip)
        return jsonify({'message': 'Login successful'}), 200
    else:
        # Increment failed attempts counter for the client IP
        if client_ip in ip_login_attempts:
            ip_login_attempts[client_ip]['failed_attempts'] += 1
        else:
            ip_login_attempts[client_ip] = {'failed_attempts': 1}
        return jsonify({'message': 'Invalid email, password, or app'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
