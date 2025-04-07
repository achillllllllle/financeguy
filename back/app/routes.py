from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from . import db
from .models import User, Category, Transaction, Reminder, RecurrenceFrequency
from .init_db import init_general_categories

main = Blueprint('main', __name__)

# Routes d'authentification
@main.route('/api/v1/token', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    
    if not user or not check_password_hash(user.hashed_password, data.get('password')):
        return jsonify({"error": "Invalid credentials"}), 401
    
    access_token = create_access_token(identity=user.email)
    return jsonify({"access_token": access_token, "token_type": "bearer"})

@main.route('/api/v1/users/', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({"error": "Email already registered"}), 400
    
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({"error": "Username already taken"}), 400
    
    user = User(
        email=data.get('email'),
        username=data.get('username'),
        hashed_password=generate_password_hash(data.get('password'))
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        "id": user.id,
        "email": user.email,
        "username": user.username
    }), 201

# Routes des catégories
@main.route('/api/v1/categories/', methods=['POST'])
@jwt_required()
def create_category():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    
    data = request.get_json()
    category = Category(
        name=data.get('name'),
        description=data.get('description'),
        is_general=data.get('is_general', False),
        user_id=user.id
    )
    
    db.session.add(category)
    db.session.commit()
    
    return jsonify({
        "id": category.id,
        "name": category.name,
        "description": category.description,
        "is_general": category.is_general
    }), 201

@main.route('/api/v1/categories/', methods=['GET'])
@jwt_required()
def get_categories():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    
    categories = Category.query.filter(
        (Category.is_general == True) | (Category.user_id == user.id)
    ).all()
    
    return jsonify([{
        "id": c.id,
        "name": c.name,
        "description": c.description,
        "is_general": c.is_general
    } for c in categories])

# Routes des transactions
@main.route('/api/v1/transactions/', methods=['POST'])
@jwt_required()
def create_transaction():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    
    data = request.get_json()
    
    # Vérifier la catégorie
    category = Category.query.filter_by(id=data.get('category_id')).first()
    if not category or (not category.is_general and category.user_id != user.id):
        return jsonify({"error": "Category not found"}), 404
    
    # Vérifier les champs de récurrence
    if data.get('is_recurrent'):
        if not data.get('recurrence_frequency'):
            return jsonify({"error": "Recurrence frequency is required"}), 400
        if not data.get('next_occurrence'):
            return jsonify({"error": "Next occurrence date is required"}), 400
    
    transaction = Transaction(
        amount=data.get('amount'),
        description=data.get('description'),
        type=data.get('type'),
        category_id=data.get('category_id'),
        user_id=user.id,
        is_recurrent=data.get('is_recurrent', False),
        recurrence_frequency=RecurrenceFrequency(data.get('recurrence_frequency')) if data.get('recurrence_frequency') else None,
        next_occurrence=datetime.fromisoformat(data.get('next_occurrence')) if data.get('next_occurrence') else None,
        is_confirmed=data.get('is_confirmed', True)
    )
    
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify({
        "id": transaction.id,
        "amount": transaction.amount,
        "description": transaction.description,
        "type": transaction.type,
        "date": transaction.date.isoformat(),
        "category_id": transaction.category_id,
        "is_recurrent": transaction.is_recurrent,
        "recurrence_frequency": transaction.recurrence_frequency.value if transaction.recurrence_frequency else None,
        "next_occurrence": transaction.next_occurrence.isoformat() if transaction.next_occurrence else None,
        "is_confirmed": transaction.is_confirmed
    }), 201

@main.route('/api/v1/transactions/', methods=['GET'])
@jwt_required()
def get_transactions():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    
    transactions = Transaction.query.filter_by(user_id=user.id).all()
    
    return jsonify([{
        "id": t.id,
        "amount": t.amount,
        "description": t.description,
        "type": t.type,
        "date": t.date.isoformat(),
        "category_id": t.category_id,
        "is_recurrent": t.is_recurrent,
        "recurrence_frequency": t.recurrence_frequency.value if t.recurrence_frequency else None,
        "next_occurrence": t.next_occurrence.isoformat() if t.next_occurrence else None,
        "is_confirmed": t.is_confirmed
    } for t in transactions])

@main.route('/api/v1/transactions/recurrent/', methods=['GET'])
@jwt_required()
def get_recurrent_transactions():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    
    transactions = Transaction.query.filter_by(
        user_id=user.id,
        is_recurrent=True
    ).all()
    
    return jsonify([{
        "id": t.id,
        "amount": t.amount,
        "description": t.description,
        "type": t.type,
        "date": t.date.isoformat(),
        "category_id": t.category_id,
        "recurrence_frequency": t.recurrence_frequency.value if t.recurrence_frequency else None,
        "next_occurrence": t.next_occurrence.isoformat() if t.next_occurrence else None,
        "is_confirmed": t.is_confirmed
    } for t in transactions])

@main.route('/api/v1/transactions/<int:transaction_id>/confirm/', methods=['PUT'])
@jwt_required()
def confirm_transaction(transaction_id):
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    
    transaction = Transaction.query.filter_by(
        id=transaction_id,
        user_id=user.id,
        is_recurrent=True
    ).first()
    
    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404
    
    # Calculer la prochaine date d'occurrence
    if transaction.recurrence_frequency == RecurrenceFrequency.DAILY:
        next_date = transaction.next_occurrence + timedelta(days=1)
    elif transaction.recurrence_frequency == RecurrenceFrequency.WEEKLY:
        next_date = transaction.next_occurrence + timedelta(weeks=1)
    elif transaction.recurrence_frequency == RecurrenceFrequency.MONTHLY:
        next_date = transaction.next_occurrence + timedelta(days=30)
    elif transaction.recurrence_frequency == RecurrenceFrequency.YEARLY:
        next_date = transaction.next_occurrence + timedelta(days=365)
    
    transaction.is_confirmed = True
    transaction.next_occurrence = next_date
    
    db.session.commit()
    
    return jsonify({
        "id": transaction.id,
        "next_occurrence": transaction.next_occurrence.isoformat(),
        "is_confirmed": transaction.is_confirmed
    })

@main.route('/api/v1/transactions/pending/', methods=['GET'])
@jwt_required()
def get_pending_transactions():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    
    now = datetime.utcnow()
    transactions = Transaction.query.filter_by(
        user_id=user.id,
        is_recurrent=True
    ).filter(
        Transaction.next_occurrence <= now,
        Transaction.is_confirmed == False
    ).all()
    
    return jsonify([{
        "id": t.id,
        "amount": t.amount,
        "description": t.description,
        "type": t.type,
        "next_occurrence": t.next_occurrence.isoformat(),
        "category_id": t.category_id
    } for t in transactions])

# Routes des rappels
@main.route('/api/v1/reminders/', methods=['POST'])
@jwt_required()
def create_reminder():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    
    data = request.get_json()
    reminder = Reminder(
        title=data.get('title'),
        description=data.get('description'),
        due_date=datetime.fromisoformat(data.get('due_date')),
        amount=data.get('amount'),
        user_id=user.id
    )
    
    db.session.add(reminder)
    db.session.commit()
    
    return jsonify({
        "id": reminder.id,
        "title": reminder.title,
        "description": reminder.description,
        "due_date": reminder.due_date.isoformat(),
        "amount": reminder.amount,
        "is_paid": reminder.is_paid
    }), 201

@main.route('/api/v1/reminders/', methods=['GET'])
@jwt_required()
def get_reminders():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    
    reminders = Reminder.query.filter_by(user_id=user.id).all()
    
    return jsonify([{
        "id": r.id,
        "title": r.title,
        "description": r.description,
        "due_date": r.due_date.isoformat(),
        "amount": r.amount,
        "is_paid": r.is_paid
    } for r in reminders])

@main.route('/api/v1/reminders/<int:reminder_id>/', methods=['PUT'])
@jwt_required()
def update_reminder(reminder_id):
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    
    reminder = Reminder.query.filter_by(
        id=reminder_id,
        user_id=user.id
    ).first()
    
    if not reminder:
        return jsonify({"error": "Reminder not found"}), 404
    
    data = request.get_json()
    reminder.title = data.get('title', reminder.title)
    reminder.description = data.get('description', reminder.description)
    reminder.due_date = datetime.fromisoformat(data.get('due_date')) if data.get('due_date') else reminder.due_date
    reminder.amount = data.get('amount', reminder.amount)
    
    db.session.commit()
    
    return jsonify({
        "id": reminder.id,
        "title": reminder.title,
        "description": reminder.description,
        "due_date": reminder.due_date.isoformat(),
        "amount": reminder.amount,
        "is_paid": reminder.is_paid
    })

@main.route('/api/v1/reminders/<int:reminder_id>/', methods=['DELETE'])
@jwt_required()
def delete_reminder(reminder_id):
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    
    reminder = Reminder.query.filter_by(
        id=reminder_id,
        user_id=user.id
    ).first()
    
    if not reminder:
        return jsonify({"error": "Reminder not found"}), 404
    
    db.session.delete(reminder)
    db.session.commit()
    
    return jsonify({"message": "Reminder deleted successfully"}) 