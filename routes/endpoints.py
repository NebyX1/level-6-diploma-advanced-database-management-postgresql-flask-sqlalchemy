from flask import Flask, render_template, redirect, url_for, flash
from helpers.forms import LoginForm, GameForm
from flask_login import login_user, logout_user, login_required, LoginManager
from database.models import Admin, Game
from database.db import db

login_manager = LoginManager()


def init_app(app: Flask):

    login_manager.init_app(app)

    @app.route("/")
    @app.route("/index")
    @app.route("/home")
    def home_page():
        games = Game.query.all()
        return render_template('index.html', games=games)

    @app.route("/login", methods=['GET', 'POST'])
    def login_page():
        form = LoginForm()
        if form.validate_on_submit():
            attempted_user = Admin.query.filter_by(name=form.name.data).first()
            if attempted_user and attempted_user.check_password(password_attempt=form.password.data):
                login_user(attempted_user)
                flash(f'You are logeed in as: {attempted_user.name}', category='success')
                return redirect(url_for('home_page'))
            else:
                flash('Username or password incorrect', category='danger')
        return render_template('login.html', form=form)

    @app.route("/logout")
    def logout_page():
        logout_user()
        flash('You are now Logged Out, See you soon!', category='info')
        return redirect(url_for('home_page'))

    @app.route("/admin", methods=['GET', 'POST'])
    @login_required
    def admin_page():
        form = GameForm()
        # ! Endpoint para crear un juego
        if form.validate_on_submit():
            try:
                new_game = Game(
                    game_name=form.game_name.data,
                    genre=form.genre.data,
                    price=form.price.data
                )
                db.session.add(new_game)
                db.session.commit()
                flash('Game created successfully', category='success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error creating game: {str(e)}', category='error')
            return redirect(url_for('admin_page'))

        games = Game.query.all()
        return render_template('admin.html', form=form, games=games)

    @app.errorhandler(404)
    def not_found(e):
        return render_template('notfound.html')

    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        return render_template('forbiden.html')

# ! Endpoint para eliminar un juego
    @app.route("/admin/delete_game/<int:game_id>", methods=['POST'])
    @login_required
    def delete_game(game_id):
        game = Game.query.get(game_id)
        if game:
            db.session.delete(game)
            db.session.commit()
            flash('Game deleted successfully', category='success')
        else:
            flash('Game not found', category='error')
        return redirect(url_for('admin_page'))
