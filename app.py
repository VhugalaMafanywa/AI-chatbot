from flask import Flask, render_template, request, session, redirect, url_for
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def get_bot_response(user_input):
    user_input = user_input.lower()

    # If starting fresh (no state), expect greeting to begin conversation
    if session.get('state') is None:
        if 'hi' in user_input or 'hello' in user_input:
            session['state'] = 'awaiting_request'
            return "Hi! How can I help you today? You can ask for career guidance."
        else:
            return "Please say 'hi' to start."

   
    elif session['state'] == 'awaiting_request':
        if 'career' in user_input or 'guidance' in user_input:
            session['state'] = 'ask_interests'
            return "Great! Let's start. What are your interests?"
        else:
            return "I can help with career guidance. Please say something like 'I want career guidance'."

    
    elif session['state'] == 'ask_interests':
        session['interests'] = user_input
        session['state'] = 'ask_skills'
        return "Thanks! Now, what skills do you have?"

    
    elif session['state'] == 'ask_skills':
        session['skills'] = user_input
        session['state'] = 'ask_subjects'
        return "Awesome. Lastly, what are your favorite subjects?"

    # Asking for favorite subjects
    elif session['state'] == 'ask_subjects':
        session['subjects'] = user_input
        session['state'] = 'completed'

        interests = session.get('interests', '')
        skills = session.get('skills', '')
        subjects = session.get('subjects', '')

        combined_text = f"{interests} {skills} {subjects}"

        if any(word in combined_text for word in ['tech', 'technology', 'programming', 'coding', 'computers', 'math']):
            recommendation = "Software Developer, Data Analyst, or Cybersecurity Specialist."
        elif any(word in combined_text for word in ['helping', 'care', 'people', 'life science', 'biology']):
            recommendation = "Doctor, Nurse, or Social Worker."
        elif any(word in combined_text for word in ['art', 'drawing', 'design', 'creative']):
            recommendation = "Graphic Designer, Animator, or Architect."
        elif any(word in combined_text for word in ['business', 'economics', 'entrepreneur']):
            recommendation = "Business Analyst, Accountant, or Marketing Manager."
        elif any(word in combined_text for word in ['history', 'writing', 'reading', 'communication']):
            recommendation = "Journalist, Teacher, or Lawyer."
        else:
            recommendation = "Project Manager, HR Officer, or Consultant."

        return f"Based on your answers, you might enjoy a career as: <strong>{recommendation}</strong>"

    # After completion, prompt user to start new chat or reset
    elif session['state'] == 'completed':
        return "If you'd like to start over, please click the 'Start New Chat' button."

    # Default fallback
    else:
        session['state'] = None
        return "Please say 'hi' to start a new conversation."

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'chat' not in session:
        session['chat'] = []
        session['state'] = None
        session['session_id'] = str(uuid.uuid4())

    if request.method == 'POST':
        user_input = request.form['user_input'].strip()
        if user_input == "":
            bot_response = "Please enter a message."
        else:
            bot_response = get_bot_response(user_input.lower())

        # Save conversation history
        session['chat'].append(('You', user_input))
        session['chat'].append(('Bot', bot_response))

    return render_template('index.html', chat=session['chat'])

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
