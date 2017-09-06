#!./venv/bin/python3
from avery_website import create_app

application = create_app()

if __name__ == '__main__':
    import os
    application.debug = True
    port = int(os.environ.get("PORT", 5000))
    application.run(host='0.0.0.0', port=port)
