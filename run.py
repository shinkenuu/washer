from app import app

from app.views import vote

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
