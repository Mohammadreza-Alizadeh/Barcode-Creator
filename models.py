from database import db

class Student(db.Model):

    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    phone_number = db.Column(db.String(150), nullable=False)
    student_code = db.Column(db.String(150), nullable=False)
    payed = db.Column(db.Boolean, nullable=False)
    barcode = db.Column(db.String(32), nullable=False)
    ref_id = db.Column(db.String(150), nullable=False)
 
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.current_timestamp())