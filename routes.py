import calendar
import logging
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, send_file, abort, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash

from app import app, db
from models import User, Diary, DiaryEntry, ChatLink
from services.pdf_generator import generate_diary_pdf
from services.question_generator import generate_questions

# Home route
@app.route('/')
def index():
    return render_template('index.html', now=datetime.now())

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html', now=datetime.now())

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_by_username = User.query.filter_by(username=username).first()
        user_by_email = User.query.filter_by(email=email).first()
        
        if user_by_username:
            flash('Username already exists', 'danger')
        elif user_by_email:
            flash('Email already registered', 'danger')
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Account created successfully!', 'success')
            return redirect(url_for('index'))
    
    return render_template('signup.html', now=datetime.now())

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

# Diary generation routes
@app.route('/generate-diary', methods=['POST'])
@login_required
def generate_diary():
    try:
        # Get month and year from form
        month = int(request.form.get('month', datetime.now().month))
        year = int(request.form.get('year', datetime.now().year))
        
        # Validate month and year
        if month < 1 or month > 12 or year < 2000 or year > 2100:
            flash('Invalid month or year', 'danger')
            return redirect(url_for('index'))
        
        # Generate questions for the month, passing the user_id for personalization
        questions = generate_questions(month, year, user_id=current_user.id)
        
        # Create diary in database
        diary = Diary(month=month, year=year, user_id=current_user.id)
        db.session.add(diary)
        db.session.flush()  # Get diary ID without committing
        
        # Create diary entries for each day
        days_in_month = calendar.monthrange(year, month)[1]
        for day in range(1, days_in_month + 1):
            # Use the question for this day, or a default if none exists
            question = questions.get(day, f"What was most meaningful to you today?")
            entry = DiaryEntry(day=day, question=question, diary_id=diary.id)
            db.session.add(entry)
        
        db.session.commit()
        
        # Generate PDF
        pdf_path = generate_diary_pdf(diary.id)
        
        # Return the PDF file
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'reflection_diary_{month}_{year}.pdf'
        )
    except Exception as e:
        logging.error(f"Error generating diary: {str(e)}")
        flash(f'Error generating diary: {str(e)}', 'danger')
        return redirect(url_for('index'))

# API routes for AJAX calls
@app.route('/api/diary/<int:diary_id>', methods=['GET'])
@login_required
def get_diary(diary_id):
    diary = Diary.query.get_or_404(diary_id)
    
    # Check if diary belongs to current user
    if diary.user_id != current_user.id:
        abort(403)
    
    entries = [
        {
            'id': entry.id,
            'day': entry.day,
            'question': entry.question,
            'answer': entry.answer
        }
        for entry in diary.entries.order_by(DiaryEntry.day).all()
    ]
    
    return jsonify({
        'id': diary.id,
        'month': diary.month,
        'year': diary.year,
        'entries': entries
    })

# ChatGPT Links Management
@app.route('/chat-links')
@login_required
def chat_links():
    user_links = ChatLink.query.filter_by(user_id=current_user.id).order_by(ChatLink.created_at.desc()).all()
    return render_template('chat_links.html', chat_links=user_links, now=datetime.now())

@app.route('/chat-links/add', methods=['POST'])
@login_required
def add_chat_link():
    url = request.form.get('url')
    title = request.form.get('title')
    
    if not url:
        flash('URL is required', 'danger')
        return redirect(url_for('chat_links'))
    
    # Validate the URL format (basic check)
    if not url.startswith('https://chat.openai.com/share/'):
        flash('Invalid ChatGPT share URL. URL must start with https://chat.openai.com/share/', 'danger')
        return redirect(url_for('chat_links'))
    
    # Create new chat link
    chat_link = ChatLink(url=url, title=title, user_id=current_user.id)
    db.session.add(chat_link)
    db.session.commit()
    
    flash('ChatGPT conversation link added successfully', 'success')
    return redirect(url_for('chat_links'))

@app.route('/chat-links/delete/<int:link_id>', methods=['POST'])
@login_required
def delete_chat_link(link_id):
    link = ChatLink.query.get_or_404(link_id)
    
    # Check if the link belongs to the current user
    if link.user_id != current_user.id:
        abort(403)
    
    db.session.delete(link)
    db.session.commit()
    
    flash('ChatGPT conversation link deleted successfully', 'success')
    return redirect(url_for('chat_links'))
