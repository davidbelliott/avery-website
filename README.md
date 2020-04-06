# Avery Website

This is the official Avery House website. The branch `master` contains a very bare-bones version of the website which does not depend on any external APIs. The branch `maximal` contains a number of other features which are more maintenance-intensive, such as a music queue, a gallery which pulls photos from Facebook using the Facebook API, and an events page which pulls events from the Google calendar using the Google Calendar API.

## Setup

To get a web server up and running using `nginx` with the default configuration:

### nginx installation and configuration

1. Install nginx (Ubuntu: `sudo apt install nginx`)
2. Copy the basic configuration file `avery-website.nginx.conf` to `/etc/nginx/sites-available`
3. Symlink the nginx configuration file to `sites-enabled`: `ln -s /etc/nginx/sites-available/avery-website.nginx.conf /etc/nginx/sites-enabled/`
4. Start and enable `nginx` (Ubuntu: `systemctl start nginx; systemctl enable nginx`)

### Python virtual environment (recommended)

If you choose not to use a virtual environment, you will need to install the dependencies in `requirements.txt` globally. Otherwise, proceed as follows (assuming `python` is Python 3)

1. `python -m venv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`

### Running the web app

Finally, run `./run.sh` to start the web app.
