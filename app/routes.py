from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import Product, Transaction

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    products = Product.query.filter(
        Product.name.like(f'%{query}%') | Product.category.like(f'%{query}%')
    ).all()
    return render_template('search_results.html', products=products, query=query)

@app.route('/register', methods=['GET', 'POST'])
def register_product():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        quantity = int(request.form['quantity'])
        supplier = request.form['supplier']
        price = float(request.form['price'])

        new_product = Product(name=name, category=category, quantity=quantity, supplier=supplier, price=price)
        db.session.add(new_product)
        db.session.commit()

        flash('Product registered successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('register_product.html')

@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    products = Product.query.all()
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        action_type = request.form['action_type']
        quantity = int(request.form['quantity'])

        product = Product.query.get(product_id)
        if action_type == 'remove' and product.quantity < quantity:
            flash('Insufficient stock!', 'danger')
        else:
            if action_type == 'add':
                product.quantity += quantity
            elif action_type == 'remove':
                product.quantity -= quantity

            new_transaction = Transaction(product_id=product_id, action_type=action_type, quantity=quantity)
            db.session.add(new_transaction)
            db.session.commit()

            flash('Transaction recorded successfully!', 'success')
        return redirect(url_for('transactions'))
    return render_template('transactions.html', products=products)

@app.route('/reports')
def reports():
    products = Product.query.all()
    transactions = Transaction.query.all()
    return render_template('reports.html', products=products, transactions=transactions)
@app.route('/products')
def view_products():
    # Fetch all products from the database
    products = Product.query.all()
    return render_template('view_products.html', products=products)
