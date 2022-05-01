from flaskDemo import app

if __name__ == '__main__':
    app.config['SQLALCHEMY_POOL_SIZE'] = 1000
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 2800
    app.run(debug=True)
