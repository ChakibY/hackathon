from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, jsonify

import json
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
db = SQLAlchemy(app)

delimiter_word = "specific_word"

# Define models
class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    dob = db.Column(db.Date)
    gender = db.Column(db.Enum('Male', 'Female'))
    contact_info = db.Column(db.String(100))

    def to_dict(self, delimiter_word=delimiter_word):
        data = {col.name: getattr(self, col.name) for col in self.__table__.columns}
        data["delimiter"] = delimiter_word
        return data

class Doctor(db.Model):
    __tablename__ = 'doctor'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    specialty = db.Column(db.String(100))
    contact_info = db.Column(db.String(100))

    def to_dict(self, delimiter_word=delimiter_word):
        data = {col.name: getattr(self, col.name) for col in self.__table__.columns}
        data["delimiter"] = delimiter_word
        return data

class MedicalHistory(db.Model):
    __tablename__ = 'medicalhistories'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    date = db.Column(db.Date)
    diagnosis = db.Column(db.Text)
    treatment = db.Column(db.Text)
    patient = db.relationship('Patient', backref=db.backref('medical_history', lazy=True))
    doctor = db.relationship('Doctor', backref=db.backref('medical_history', lazy=True))

    def to_dict(self, delimiter_word=delimiter_word):
        data = {col.name: getattr(self, col.name) for col in self.__table__.columns}
        data["delimiter"] = delimiter_word
        return data

class Allergy(db.Model):
    __tablename__ = 'allergies'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    patient = db.relationship('Patient', backref=db.backref('allergies', lazy=True))

    def to_dict(self, delimiter_word=delimiter_word):
        data = {col.name: getattr(self, col.name) for col in self.__table__.columns}
        data["delimiter"] = delimiter_word
        return data

class Medication(db.Model):
    __tablename__ = 'medications'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    name = db.Column(db.String(100))
    dosage = db.Column(db.String(50))
    frequency = db.Column(db.String(50))
    patient = db.relationship('Patient', backref=db.backref('medications', lazy=True))

    def to_dict(self, delimiter_word=delimiter_word):
        data = {col.name: getattr(self, col.name) for col in self.__table__.columns}
        data["delimiter"] = delimiter_word
        return data

class Visit(db.Model):
    __tablename__ = 'visits'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    date = db.Column(db.Date)
    purpose = db.Column(db.Text)
    notes = db.Column(db.Text)
    patient = db.relationship('Patient', backref=db.backref('visits', lazy=True))
    doctor = db.relationship('Doctor', backref=db.backref('visits', lazy=True))

    def to_dict(self, delimiter_word=delimiter_word):
        data = {col.name: getattr(self, col.name) for col in self.__table__.columns}
        data["delimiter"] = delimiter_word
        return data

with app.app_context():
    db.create_all()

@app.route('/add_sample_data')
def add_sample_data():
    # Adding sample patients
    patient1 = Patient(first_name="John", last_name="Doe", dob=date(1980, 5, 21), gender='Male', contact_info="john@example.com")
    patient2 = Patient(first_name="Jane", last_name="Smith", dob=date(1990, 7, 15), gender='Female', contact_info="jane@example.com")
    patient3 = Patient(first_name="Alice", last_name="Johnson", dob=date(2000, 9, 30), gender='Female', contact_info="alice@example.com")

    # Adding sample doctors
    doctor1 = Doctor(first_name="Gregory", last_name="House", specialty="Diagnostics", contact_info="house@example.com")
    doctor2 = Doctor(first_name="Meredith", last_name="Grey", specialty="General Surgery", contact_info="grey@example.com")
    doctor3 = Doctor(first_name="John", last_name="Watson", specialty="Family Medicine", contact_info="watson@example.com")

    # Adding sample medical histories
    history1 = MedicalHistory(patient=patient1, doctor=doctor1, date=date(2020, 1, 10), diagnosis="Flu", treatment="Rest and hydration")
    history2 = MedicalHistory(patient=patient2, doctor=doctor2, date=date(2021, 3, 22), diagnosis="Appendicitis", treatment="Appendectomy")
    history3 = MedicalHistory(patient=patient3, doctor=doctor3, date=date(2022, 5, 18), diagnosis="Migraine", treatment="Pain management")

    # Adding sample allergies
    allergy1 = Allergy(patient=patient1, name="Peanuts", description="Severe anaphylactic reaction")
    allergy2 = Allergy(patient=patient2, name="Penicillin", description="Rash and swelling")
    allergy3 = Allergy(patient=patient3, name="Bee stings", description="Mild swelling")

    # Adding sample medications
    medication1 = Medication(patient=patient1, name="Ibuprofen", dosage="200mg", frequency="Twice a day")
    medication2 = Medication(patient=patient2, name="Amoxicillin", dosage="500mg", frequency="Three times a day")
    medication3 = Medication(patient=patient3, name="Aspirin", dosage="100mg", frequency="Once a day")

    # Adding sample visits
    visit1 = Visit(patient=patient1, doctor=doctor1, date=date(2023, 1, 20), purpose="Routine check-up", notes="All good")
    visit2 = Visit(patient=patient2, doctor=doctor2, date=date(2023, 2, 25), purpose="Post-surgery follow-up", notes="Recovery is going well")
    visit3 = Visit(patient=patient3, doctor=doctor3, date=date(2023, 3, 15), purpose="Consultation", notes="Discussed migraine management")

    db.session.add_all([patient1, patient2, patient3, doctor1, doctor2, doctor3, history1, history2, history3, allergy1, allergy2, allergy3, medication1, medication2, medication3, visit1, visit2, visit3])
    db.session.commit()

    # Dump data to JSON file after adding sample data
    dump_all_models_to_file('data.json')

    return "Sample data added successfully"


@app.route('/doctors')
def doctors():
    doctors = Doctor.query.all()
    return render_template('doctors.html', doctors=doctors)

@app.route('/medical_histories')
def medical_histories():
    histories = MedicalHistory.query.all()
    return render_template('medical_histories.html', histories=histories)

@app.route('/allergies')
def allergies():
    allergies = Allergy.query.all()
    return render_template('allergies.html', allergies=allergies)

@app.route('/medications')
def medications():
    medications = Medication.query.all()
    return render_template('medications.html', medications=medications)

@app.route('/visits')
def visits():
    visits = Visit.query.all()
    return render_template('visits.html', visits=visits)

# Function to dump all models to a file
def dump_all_models_to_file(file_path):
    data = {}
    for table in db.metadata.tables.values():
        model_name = table.name
        model_class = db.Model._decl_class_registry.get(model_name)
        if model_class:
            model_data = [dict(row) for row in db.session.query(model_class).all()]
            data[model_name] = model_data
    with open(file_path, 'w') as file:  # 'w' mode will overwrite the file
        json.dump(data, file, default=str)  # default=str to handle non-serializable types like datetime

# Example route to trigger dumping data to a file
@app.route('/dump_data')
def dump_data():
    file_path = 'data.json'
    dump_all_models_to_file(file_path)
    return f"Data dumped to {file_path}"

if __name__ == '__main__':
    app.run(debug=True)