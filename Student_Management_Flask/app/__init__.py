from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

    # Register Blueprints
    from app.features.students.routes import students_bp
    
    # Prefixing with /students is optional but good practice for feature isolation
    app.register_blueprint(students_bp, url_prefix='/students')

    # Add a simple root route that redirects to the students feature
    @app.route('/')
    def index():
        from flask import redirect, url_for
        return redirect(url_for('students.list_students'))

    return app
