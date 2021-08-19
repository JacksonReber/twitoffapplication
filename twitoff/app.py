from flask import Flask, render_template, request
from .models import DB, User, Tweet
from os import getenv
from .twitter import add_or_update_user, insert_example_users
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from .predict import predict_user

# Creates application
def create_app():
    
    app = Flask(__name__)
#    app_dir = os.path.dirname(os.path.abspath(__file__))
#    database = "sqlite:///{}".format(os.path.join(app_dir, "twitoff.sqlite3"))

    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite3'#getenv('DATABASE_URI')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB.init_app(app)

    with app.app_context():
        DB.create_all()
        insert_example_users() 

       

    @app.route("/")
    def root():
        users = User.query.all()
        return render_template('home.html', title="Home", users=users)

    @app.route('/compare', methods=['POST'])
    def compare():
        user0, user1 = sorted(
            [request.values['user0'], request.values['user1']])
        
        if user0 == user1:
            message = 'Cannot compare users to themselves!'
        else:
            prediction = predict_user(
                user0, user1, request.values['tweet_text'])
            message = "'{}' is more likely to be said by {} than {}".format(
                request.values['tweet_text'],
                user1 if prediction else user0,
                user0 if prediction else user1
            )

        return render_template('prediction.html', title='Prediction', message=message)    
    
    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        name = name or request.values['user_name']

        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = 'User {} succesfully added!'.format(name)
            
            tweets = User.query.filter(User.name == name).one().tweets

        except Exception as e:
            message = 'Error handling {}: {}'.format(name, e)
            
            tweets = []
        return render_template('user.html', title=name, tweets=tweets, message=message)
        
    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return "This DB has been reset!"
    
    @app.route('/update')
    def update():
        users = User.query.all()
        for user in users:
            add_or_update_user(user.name)
        users = User.query.all()
        return render_template('home.html', title="Home", users=users)
        
    
    return app