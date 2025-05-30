from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
from datetime import datetime
import io
import qrcode 
import base64
import uuid
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing and session

# Simple in-memory "database" for demonstration (token -> data)
db = {}

@app.route('/')
def home():
    return redirect(url_for('welcome'))

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/form', methods=['GET', 'POST'])
def health_form():
    if request.method == 'POST':
        data = {
            "arrival_date": request.form.get('arrival-date'),
            "departure_date": request.form.get('departure-date'),
            "full_name": request.form.get('full-name'),
            "gender": request.form.get('gender'),
            "nationality": request.form.get('nationality'),
            "passport_number": request.form.get('passport-number'),
            "email": request.form.get('email'),
            "dob": request.form.get('dob'),
            "phone": request.form.get('phone'),
            "flight": request.form.get('flight'),
            "seat": request.form.get('seat'),
            "residence": request.form.get('residence'),
            "province": request.form.get('province'),
            "city": request.form.get('city'),
            "first_departure": request.form.get('first-departure'),
            "transit_airport": request.form.get('transit-airport'),
            "transit_country": request.form.get('transit-country'),
            "visited_country_1": request.form.get('visited-country-1'),
            "visited_country_2": request.form.get('visited-country-2'),
            "zimbabwe_address": request.form.get('zimbabwe-address'),
            "emergency_name": request.form.get('emergency-name'),
            "emergency_contact": request.form.get('emergency-contact'),
            "symptoms": request.form.getlist('symptoms[]'),
            "other_symptom": request.form.get('other-symptom'),
            "fever_temperature": request.form.get('fever-temperature'),
            "contact_symptoms": request.form.getlist('contact[]'),
            "contact_other": request.form.get('contact-other'),
            "health_conditions": request.form.getlist('health-conditions[]'),
            "vaccination_status": request.form.get('vaccination-status'),
            "last_vaccine_date": request.form.get('last-vaccine-date'),
            "consent": request.form.get('consent') == 'on'
        }

        token = str(uuid.uuid4())
        db[token] = data
        session['token'] = token

        flash('Form submitted successfully!', 'success')
        return redirect(url_for('confirmation'))

    return render_template('form.html')

@app.route('/confirmation')
def confirmation():
    token = session.get('token')
    if not token or token not in db:
        flash('No form data found. Please submit the form first.', 'error')
        return redirect(url_for('health_form'))

    qr_img = qrcode.make(token)
    buf = io.BytesIO()
    qr_img.save(buf, format='PNG')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('ascii')

    return render_template('confirmation.html', qr_code=img_base64, token=token)

@app.route('/scan/<token>', methods=['GET'])
def scan(token):
    data = db.get(token)
    if not data:
        return jsonify({"error": "Invalid or expired token"}), 404
    return jsonify(data)

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('.', 'sitemap.xml', mimetype='application/xml')

@app.route('/robots.txt')
def robots():
    return send_from_directory('.', 'robots.txt', mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
