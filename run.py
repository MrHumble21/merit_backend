from app import app, db
from app.models import User


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # manager.run()
    app.run(host='0.0.0.0', port=8000, debug=True)






# python run.py

# to make changes db  
    # python run.py db migrate
    # python run.py db upgrade
