from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from prometheus_client import Counter, generate_latest
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://expense_user:password@db/expense_tracker'
db = SQLAlchemy(app)
metrics = PrometheusMetrics(app)

# Define a custom metric for data entries
data_entry_counter = Counter('data_entries_total', 'Total number of data entries')

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    expenses = Expense.query.all()
    total = sum(expense.price for expense in expenses)
    return render_template('index.html', expenses=expenses, total="{:.2f}".format(total / 100))

@app.route('/add', methods=['POST'])
def add_expense():
    name = request.form.get('name')    
    category = request.form.get('category')
    price_pounds = float(request.form.get('price'))
    price_pence = int(price_pounds * 100)
    new_expense = Expense(name=name, category=category, price=price_pence)
    db.session.add(new_expense)
    db.session.commit()
    data_entry_counter.inc()  # Increment the custom metric
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update_expense(id):
    expense = Expense.query.get_or_404(id)
    expense.name = request.form.get('name')
    expense.category = request.form.get('category')
    price_pounds = float(request.form.get('price'))
    expense.price = int(price_pounds * 100)  # Convert pounds to pence
    
    try:
        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)})

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(expense)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('delete.html', expense=expense)

@app.route('/metrics')
def metrics_route():
    return generate_latest()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)

