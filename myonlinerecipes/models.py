from myonlinerecipes import db

class User(db.Model):
    #schema for User model
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(40), unique=True, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)
    profile_image_url = db.Column(db.String(300), unique=True, nullable=True)
    recipes = db.relationship('Recipes', backref='owned_user_recipes')
    comments = db.relationship('Comments', backref='owned_user_comment')
  
    def __repr__(self):
        return self.username

class Recipes(db.Model):
    #schema for Recepes model
     __tablename__ = 'Recipes'
     id = db.Column(db.Integer, primary_key=True)
     user = db.Column(db.Integer, db.ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
     title = db.Column(db.String(201), unique=True, nullable=False)
     image_url = db.Column(db.String(300), unique=True, nullable=True)
     Ingredients = db.Column(db.Text, unique=True, nullable=True)
     method = db.Column(db.Text, unique=True, nullable=True)
     service_size = db.Column(db.Integer, nullable=True)
     cooking_time = db.Column(db.Integer, nullable=True)
     is_private = db.Column(db.Boolean, default=False, nullable=False)
     date_created = db.Column(db.DateTime, nullable=False)
     calories = db.Column(db.String(201), unique=True, nullable=True)
     fat = db.Column(db.String(201), unique=True, nullable=True)
     protein = db.Column(db.String(201), unique=True, nullable=True)
     carbohidrates = db.Column(db.String(201), unique=True, nullable=True)
     salt = db.Column(db.String(201), unique=True, nullable=True)
     comments = db.relationship('Comments', backref='recipes')

     def __repr__(self):
        return self.title


class Comments(db.Model):
     #schema for Recepes model
     __tablename__ = 'Comments'
     id = db.Column(db.Integer, primary_key=True)
     content = db.Column(db.Text, unique=True, nullable=False)
     title = db.Column(db.String(201), unique=True, nullable=False)
     recipes_id = db.Column(db.Integer, db.ForeignKey(Recipes.id, ondelete="CASCADE"), nullable=False)
     user = db.Column(db.Integer, db.ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
     created =  db.Column(db.Date, nullable=False)
     updated =  db.Column(db.Date, nullable=False)

     def __repr__(self):
        return self.title