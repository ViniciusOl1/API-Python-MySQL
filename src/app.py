from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
api = Api(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db =  SQLAlchemy(app)
ma = Marshmallow(app)


# Models
class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)

    category = db.relationship('Category', backref=db.backref('products', lazy=True))
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

#Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'category_id', 'price')
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

class CategorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)

db.create_all()

# Resources
class CategoriesResource(Resource):
    def get(self):
        return categories_schema.dump(Category.query.all())
    def post(self):
        data = request.json
        category = Category(name=data['name'])
        db.session.add(category)
        db.session.commit()
        return category_schema.dump(category)


class ProductsResource(Resource):
    def get(self):
        return products_schema.dump(Products.query.all())
    def post(self):
        data = request.json
        product = Products(title=data['title'], description=data['description'], category_id=data['category_id'], price=data['price'])
        db.session.add(product)
        db.session.commit()
        
        return product_schema.dump(product)

api.add_resource(CategoriesResource, '/categories')
api.add_resource(ProductsResource, '/products')

if __name__ == '__main__':
    app.run(debug=True)