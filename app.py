# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, url_for, redirect, flash, session
from zeep.client import Client
from database import db
from models import Student
import uuid

# app
app = Flask(__name__)
app.secret_key = 'Secret-key' # Required

# db
db_name = 'students.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# zarinpal
MMERCHANT_ID = '##########################'  # Required - Merchant code
ZARINPAL_WEBSERVICE = 'https://www.zarinpal.com/pg/services/WebGate/wsdl'  # Required
amount = 1000  # Amount will be based on Toman  Required
description = u'همایش مسیر موفقیت'  # Required


@app.route('/')
def index():
    return render_template('home/home.html')


@app.route('/register/', methods=['POST'])
def register():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    student_code = request.form.get('student_code')
    phone_number = request.form.get('phone_number')

    if (not first_name) or (not last_name) or (not student_code) or (not phone_number):
        flash('تمام فیلد ها اجباری هستند', 'error')
        return redirect('/#register-form')
    
    if Student.query.filter(Student.student_code==student_code).scalar():
        flash('ثبت نام با شماره دانشجویی وارد شده قبلا انجام شده. برای دریافت بارکد با این شماره دانشجویی به انتهای صفحه مراجعه کنید ')
        return redirect('/#register-form')
    
    session['first_name'] = first_name
    session['last_name'] = last_name
    session['student_code'] = student_code
    session['phone_number'] = phone_number
    
    client = Client(ZARINPAL_WEBSERVICE)
    result = client.service.PaymentRequest(
        MMERCHANT_ID,
        Amount = amount,
        Description=description,
        CallbackURL = str(url_for('verify', _external=True))
    )
    
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + result.Authority)
    else:
        flash('خطایی از طرف درگاه بوجود آمده است. لطفا بعدا امتحان کنید. درصورتی که مشکل همچنان پابرجا بود با پشتیبانی سایت تماس بگیرید')
        return redirect('/#register-form')


@app.route('/verify/', methods=['GET', 'POST'])
def verify():
    client = Client(ZARINPAL_WEBSERVICE)
    if request.args.get('Status') == 'OK':
        
        result = client.service.PaymentVerification(
            MMERCHANT_ID,
            request.args['Authority'],
            amount
        )
        
        if result.Status == 100:
            barcode = generate_barcode()
            s = Student(
                first_name = session['first_name'],
                last_name = session['last_name'],
                student_code = session['student_code'],
                phone_number = session['phone_number'],
                payed = True,
                barcode = barcode,
                ref_id = str(result.RefID)
            )
            db.session.add(s)
            db.session.commit()
            flash('ثبت نام شما با موفقیت انجام شد')
            return render_template('home/success.html', barcode=barcode)
        
        elif result.Status == 101:
            flash('تراکنش موفق')
            return render_template('home/home.html')
        
        else:
            flash('پرداخت با خطا رو برو شد , کد خطا : ' + str(result.Status))
            return  redirect('/#register-form')
    else:
        flash('پرداخت توسط کاربر لغو شد')
        return  redirect('/#register-form')

@app.route('/test/')
def test():
    flash('ثبت نام شما با موفقیت انجام شد')
    return render_template('home/success.html', barcode='123456789')

@app.route('/barcode/', methods=['POST'])
def barcode():
    student_code = request.form.get('barcode_student_code')
    if not student_code:
        flash('مقدار وارد شده مجاز نیست')
        return redirect('/#register-form')

    student = Student.query.filter(Student.student_code==student_code).scalar()
    if student is None:
        flash('هیچ کاربری با این شماره دانشجویی ثبت نام نکرده')
        return redirect('/#register-form')
    
    return render_template('home/home.html/', barcode=student.barcode)

def generate_barcode():
    return uuid.uuid4().hex