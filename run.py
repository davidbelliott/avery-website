#!./venv/bin/python3

from avery_website import create_app

if __name__ == '__main__'
    app = create_app()
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
