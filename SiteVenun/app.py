from flask import Flask, render_template, redirect, url_for, request, session, flash 
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Product 
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from flask import flash 

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Chave definida para cada sessão 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitevenun.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco com o app
db.init_app(app) 

# Render Index
@app.route('/')
def index(): 
    products = Product.query.all()
    return render_template('index.html', products=products)

# Render Login (exibe a página de login quando seleciona logout)
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

# Render Login
@app.route('/login')
def login():
    return render_template('login.html')

# Login Handler (processa o formulário de login)
@app.route('/login_handler', methods=['POST'])
def login_handler():
    email = request.form.get('login-form-email')
    password = request.form.get('login-form-password')

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.senha, password):
        # Armazena o ID do usuário na sessão
        session['user_id'] = user.id
        return redirect(url_for('index'))  # Login bem-sucedido
    return redirect(url_for('login'))  # Login mal-sucedido

# Render Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form.get('register-form-name')
        email = request.form.get('register-form-email')
        password = request.form.get('register-form-password')
        repassword = request.form.get('register-form-repassword')

        # Verifica se o e-mail já está cadastrado
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Este e-mail já está em uso!', 'error')
            return redirect(url_for('register'))
        
        # Verifica se as senhas coincidem
        if password != repassword:
            flash('As senhas não coincidem!', 'error')
            return redirect(url_for('register'))

        # Cria o novo usuário se tudo estiver válido
        try:
            senha_hash = generate_password_hash(password)
            user = User(
                nome=nome, 
                email=email, 
                username=nome,
                phone='', 
                senha=senha_hash
            )
            
            db.session.add(user)
            db.session.commit()
            flash('Registro realizado com sucesso! Faça login.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            flash('Erro ao registrar usuário. Tente novamente.', 'error')
            return redirect(url_for('register'))

    # Caso seja GET, exibe o formulário
    return render_template('register.html')

@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('login'))
    return render_template('profile.html', user_html=user)

"""# Render Cart
@app.route('/cart')
def cart():
    return render_template('cart.html')"""

""" # Render Cart
@app.route('/add_to_cart')
def add_to_cart():
    return render_template('cart.html') """

#Render shop_single
@app.route('/shop_single/<int:product_id>')
def shop_single(product_id):
    product = Product.query.get_or_404(product_id)
    print(product)
    return render_template('shop_single.html', product=product)

# Render shop
@app.route('/shop')
def shop():
    products = Product.query.all()
    return render_template('shop.html', products=products)

# Rota para adicionar um produto ao carrinho (POST)
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    # Obtém os dados do formulário
    product_id = request.form.get('product_id')
    quantity = request.form.get('quantity', 1)
    
    try:
        quantity = int(quantity)
    except ValueError:
        quantity = 1

    # Obtém o carrinho da sessão, ou inicializa um dicionário vazio se não existir
    cart = session.get('cart', {})

    # Se o produto já estiver no carrinho, atualiza a quantidade; senão, adiciona-o
    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity

    session['cart'] = cart  # Atualiza a sessão
    flash("Produto adicionado ao carrinho!", "success")
    return redirect(url_for('cart'))

# Rota para exibir o carrinho
@app.route('/cart')
def cart():
    cart = session.get('cart', {})  # Recupera o carrinho da sessão
    cart_items = []
    total = 0
    # Para cada item no carrinho, busca os dados do produto no banco
    for prod_id, qty in cart.items():
        product = Product.query.get(int(prod_id))
        if product:
            cart_items.append({'product': product, 'quantity': qty})
            total += product.preco * qty
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/remove-from-cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        session['cart'] = cart
    return redirect(url_for('cart'))

# Render 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Banco de dados criado com sucesso!")
    app.run(debug=True)
