from app import create_app
from instance.config import settings

app =  create_app(settings['testing'])

if __name__ == '__main__':
    app.run()