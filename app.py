import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)

# Получаем строку подключения к базе данных из переменной среды
db_uri = os.environ.get('DATABASE_URL', 'postgresql://gen_user:oBld4,bD8OZH:4@83.147.244.83:5432/default_db')

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    predicted_category = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())

# Создаем таблицу в базе данных (раскомментируйте при первом запуске для создания таблицы)
# db.create_all()
# фывфыввф
@app.route('/')
def index():
    categories_stats = db.session.query(Form.predicted_category, func.count().label('count')).group_by(Form.predicted_category).all()
    stats = [{'category': stat.predicted_category, 'count': stat.count} for stat in categories_stats]
    total_count = sum(stat['count'] for stat in stats)
    return render_template('index.html', stats=stats, total_count=total_count)

if __name__ == '__main__':
    app.run(debug=True)
