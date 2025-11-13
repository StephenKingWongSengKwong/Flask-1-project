from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Temporary in-memory storage for tasks
tasks = []

def calculate_remaining_days(deadline):
    deadline_date = datetime.strptime(deadline, '%Y-%m-%d')
    today = datetime.now()
    remaining_days = (deadline_date - today).days
    return max(0, remaining_days)

def classify_urgency(task):
    if task['remaining_days'] == 0:
        task['urgency'] = 'overdue'
    elif task['remaining_days'] <= 1:
        task['urgency'] = 'high'
    elif task['remaining_days'] <= 3:
        task['urgency'] = 'medium'
    else:
        task['urgency'] = 'low'

@app.route('/')
def index():
    for task in tasks:
        task['remaining_days'] = calculate_remaining_days(task['deadline'])
        classify_urgency(task)
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        deadline = datetime.strptime(request.form['deadline'], '%Y-%m-%d')
        task = {
            'title': request.form['title'],
            'description': request.form['description'],
            'deadline': request.form['deadline'],
            'priority': 'high' if 'priority' in request.form else 'normal',
            'remaining_days': calculate_remaining_days(request.form['deadline']),
        }
        classify_urgency(task)
        tasks.append(task)
        return redirect(url_for('index'))
    return render_template('add_task.html')

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = tasks[task_id]
    if request.method == 'POST':
        task['title'] = request.form['title']
        task['description'] = request.form['description']
        task['deadline'] = request.form['deadline']
        task['remaining_days'] = calculate_remaining_days(task['deadline'])
        classify_urgency(task)
        return redirect(url_for('index'))
    return render_template('edit_task.html', task=task, task_id=task_id)

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    del tasks[task_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
