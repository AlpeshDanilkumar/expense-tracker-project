from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://expense_user:password@db/expense_tracker'
db = SQLAlchemy(app)
metrics = PrometheusMetrics(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)

@app.route('/')
def index():
    expenses = Expense.query.all()
    total = sum(expense.price for expense in expenses)
    return render_template('index.html', expenses=expenses, total=total)

@app.route('/add', methods=['POST'])
def add_expense():
    category = request.form.get('category')
    price = request.form.get('price')
    new_expense = Expense(category=category, price=float(price))
    db.session.add(new_expense)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)

