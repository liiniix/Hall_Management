- Firstly create virtualenv using python-3.6.9
- Activate virtualenv
- pip install -r requirements.txt
- run by command ./run
http://www.blog.pythonlibrary.org/2017/12/14/flask-101-adding-editing-and-displaying-data/
```
<VirtualHost *:80>
     # Add machine's IP address (use ifconfig command)
     ServerName 103.28.121.19
     # Give an alias to to start your website url with
     WSGIScriptAlias /hall_management /var/www/Hall_Management/Hall_Management.wsgi
     <Directory /var/www/Hall_Management/Hall_Management>
            # set permissions as per apache2.conf file
            Options FollowSymLinks
            AllowOverride None
            Require all granted
     </Directory>
     ErrorLog ${APACHE_LOG_DIR}/error.log
     LogLevel warn
     CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>```
