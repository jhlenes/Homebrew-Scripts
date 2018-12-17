# Homebrew-Scripts

## Install Django in a virtual environment
```
mkdir homebrew-django
cd homebrew-django
python3 -m venv homebrew-env
source homebrew-env/bin/activate
python3 -m pip install --upgrade pip
echo "Django~=2.0.6" >> requirements.txt
echo "requests" >> requirements.txt
pip install -r requirements.txt
```

## Clone website and give access to database
```
cd ~/homebrew-django
git clone https://github.com/jhlenes/Homebrew-Django.git
sudo chown www-data:www-data Homebrew-Django/
sudo chown www-data:www-data Homebrew-Django/db.sqlite3
```
Collect static files (do this every time you make changes to static files)
```
cd Homebrew-Django
python3 manage.py collectstatic
```

## Install apache
```
sudo apt install -y apache2 apache2-dev
```

## Install modwsgi
See [here](https://modwsgi.readthedocs.io/en/develop/user-guides/quick-installation-guide.html).
```
wget https://github.com/GrahamDumpleton/mod_wsgi/archive/4.6.4.tar.gz -P ~/Downloads
cd ~/Downloads
tar xvfz 4.6.4.tar.gz
cd mod_wsgi-4.6.4
./configure --with-python=/usr/bin/python3
make
sudo make install
make clean
```

## Configure apache
See [here.](https://docs.djangoproject.com/pl/2.1/howto/deployment/wsgi/modwsgi/)

At bottom of ```/etc/apache2/apache2.conf```, add this:
```
LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so

WSGIDaemonProcess homebrew python-home=/home/henrik/homebrew-django/homebrew-env python-path=/home/henrik/homebrew-django/Homebrew-Django
WSGIProcessGroup homebrew
WSGIApplicationGroup %{GLOBAL}

WSGIScriptAlias / /home/henrik/homebrew-django/Homebrew-Django/Homebrew/wsgi.py process-group=homebrew
WSGIPythonHome /home/henrik/homebrew-django/homebrew-env
WSGIPythonPath /home/henrik/homebrew-django/Homebrew-Django

Alias /favicon.ico /home/henrik/homebrew-django/Homebrew-Django/main/static/main/favicon.ico
Alias /static/ /home/henrik/homebrew-django/Homebrew-Django/Homebrew/static/

<Directory /home/henrik/homebrew-django/Homebrew-Django/Homebrew/static>
Require all granted
</Directory>

<Directory /home/henrik/homebrew-django/Homebrew-Django/Homebrew>
<Files wsgi.py>
Require all granted
</Files>
</Directory>
```

## Run Arduino communication script on boot

Install tmux with:
```
sudo apt install -y tmux
```

Add this line to ```/etc/rc.local``` before ```exit 0```:
```
tmux new-session -d -s homebrew-connection \; send-keys "python3 /home/pi/Homebrew-Scripts/connection.py" Enter
```
