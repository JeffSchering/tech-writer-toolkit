# Set up a web service that provides readability scores

The web service exposes the Readability API to the network. To expose an API that's written in Python, you need a Web Services Gateway Interface (WSGI) server. The instructions here show you how to install and use the Gunicorn WSGI server.

You can expose Gunicorn directly to the network, but it's best to put it behind a proxy. You can use a web server such as Apache or Nginx for the proxy. When you use a proxy, you get all the features of the web server such as the ability to handle multiple hosts, virtual servers, logging, HTTPS connections, and more. The instructions here show you how to use Nginx as the proxy.

The API relies on the Flask web development framework. It handles routing from the API endpoints to the functions that handle the API calls. Flask also has a WSGI server that you can use during development and testing, but not for production.

## API endpoints

<table>
    <thead>
    <tr>
        <th>Endpoint</th>
        <th>Method</th>
        <th>Content-Type</th>
        <th>Description</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>/</td>
        <td>GET</td>
        <td>N/A</td>
        <td><p>Returns a page that contains this table.</p></td>
    </tr>
    <tr>
        <td>/word-count</td>
        <td>POST</td>
        <td>text/plain</td>
        <td><p>Returns the number of words in the submitted text.</p>
        <p>Body of the POST request is a string.</p>
        <p>Returns JSON. For example: <code>{count: "77", message: "OK", status: "OK"}</code></p></td>
    </tr>
    <tr>
        <td>/fkgl</td>
        <td>POST</td>
        <td>text/plain</td>
        <td><p>Returns the <b>Flesch-Kincaid Grade Level</b>.</p>
        <p>Body of the POST request is a string.</p>
        <p>Returns JSON. For example: <code>{grade: "10.77", message: "OK", status: "OK"}</code></p></td>
    </tr>
    <tr>
        <td>/fres</td>
        <td>POST</td>
        <td>text/plain</td>
        <td><p>Returns the <b>Flesch Reading Ease Score</b>.</p>
        <p>Body of the POST request is a string.</p>
        <p>Returns JSON. For example: <code>{score: "52.16", message: "OK", status: "OK"}</code></p></td>
    </tr>
    </tbody>
</table>

## Prerequisites

1. Linux server. You can also run it on Windows, but the instructions here are specific to Linux.
2. Your server firewall exposes port 80 to the Internet. If you plan to use HTTPS, expose port 443 too.
3. Your service provider allows traffic from the Internet to your server over port 80 and 443.

## Install Python 3 and pip

On systems that use `yum`, such as RedHat, Fedora, CentOS, Oracle Linux, and others that are based on RedHat, open a terminal window and issue the following command:

    sudo yum install python3 python3-pip

On systems that use `apt`, such as Debian, Ubuntu, Mint, Linux Lite, and others that are based on Debian or Ubuntu, use the following command in a terminal window:

    sudo apt-get install python3 python3-pip

## Install the API files

You install the API files into a Python virtual environment. You also install Flask. Flask is the API's only external dependency.

1. Create a directory for your project and cd into it. Let's call it `api`.

        mkdir api
        cd api

2. Download this repo to get the following files:

    + `readability_api.py`
    + `toolkit.py`
    + `wsgi.py`

    You can clone the repo, or you can grab the zip file from GitHub and extract what you need, or you can run these three commands to get each file individually:

        wget https://raw.githubusercontent.com/JeffSchering/tech-writer-toolkit/master/readability_api.py
        wget https://raw.githubusercontent.com/JeffSchering/tech-writer-toolkit/master/toolkit.py
        wget https://raw.githubusercontent.com/JeffSchering/tech-writer-toolkit/master/wsgi.py

    Make sure the files end up in the `api` directory that you created.

3. Create a Python 3 virtual environment.

        python3 -m venv venv

4. Activate the virtual environment.

        source venv/bin/activate

5. Make sure your virtual environment has the latest `pip`, which you'll use to install Flask.

        python -m pip install --upgrade pip

6. Install Flask.

        pip install flask

You can test the API now to make sure everything so far is working. Because Flask comes with a basic WSGI server, you can use that. Just be aware that it's only good for testing and shouldn't be used in production.

## Test the API with the Flask WSGI server

This test is optional, but you might want to do it just to confirm that all the files are in the right place and the API can load and run.

1. Run Flask. By default, Flask loads the `wsgi.py` file.

        flask run

    By default Flask listens on port 5000 and allows connections only from the machine on which it's running.

2. Use cURL to test the `/` endpoint with a GET method. Open another terminal on the server and run the following command:

        curl http://localhost:5000/

    You should get a bunch of HTML returned.

3. Type **Ctrl-C** to shut down the Flask server.

## Install and configure Gunicorn

After you install Gunicorn, start it up to test that it's installed ok and can load the API. For the test, Gunicorn accepts connections only from the server that it's running on.

You'll also configure Gunicorn to use `systemd` for managing its life cycle. This allows you to set it to start on system boot. If you follow the instructions below, Gunicorn will use a Unix domain socket for communicating with the proxy instead of an open port on the server. This has better performance and is more secure.

1. Make sure you're in the `api` directory and the virtual environment is activated.
2. Install Gunicorn.

        pip install gunicorn

3. Test Gunicorn to make sure that it installed ok.

    1. Start Gunicorn

            gunicorn --bind 127.0.0.1:5000 wsgi:app

    2. Open another terminal on the server and run the following command:

            curl http://localhost:5000/

        You should get a bunch of HTML returned.

4. Type **Ctrl-C** to shut down the Gunicorn server.

5. Set Gunicorn to use `systemd` for managing its life cycle. This allows you to set Gunicorn to start on boot. To do that, you'll have to create a systemd service file. Most systems have `nano` text editor, so we'll use that.

    1. Create a new service file.

            sudo nano /etc/systemd/system/gunicorn.service

    2. Paste the following contents into the file and then replace each instance of the text `USER_NAME` with your own user name (4 places).

            [Unit]
            Description=Gunicorn for Readability API
            After=network.target

            [Service]
            User=USER_NAME
            Group=nginx
            WorkingDirectory=/home/USER_NAME/api
            Environment="PATH=/home/USER_NAME/api/venv/bin"
            ExecStart=/home/USER_NAME/api/venv/bin/gunicorn --workers 3 --bind unix:api.sock -m 007 wsgi:app

            [Install]
            WantedBy=multi-user.target

    3. Enable Gunicorn to start on boot.

            sudo systemctl enable gunicorn

Gunicorn is not ready to start yet. The `gunicorn.service` file puts Gunicorn in the `nginx` group, but we haven't installed Nginx yet.

## Install and configure Nginx

Because Nginx is not a Python program, it won't be installed in the virtual environment.

1. Install Nginx

    On systems that use `yum`, such as RedHat, Fedora, CentOS, Oracle Linux, and others that are based on RedHat, open a terminal window and issue the following command:

        sudo yum install nginx

    On systems that use `apt`, such as Debian, Ubuntu, Mint, Linux Lite, and others that are based on Debian or Ubuntu, use the following command in a terminal window:

        sudo apt-get install nginx

2. Optional: Configure Nginx to start on reboot.

        sudo systemctl enable nginx

3. Start Nginx.

        sudo systemctl start nginx

4. Make sure that Nginx is working ok and is accessible to the Internet. Open a browser and go to http://YOUR_SERVER/. You should get an Nginx welcome page.

    If you get a connection refused message:
    1. run `systemctl status nginx` and examine the output.
    2. Check to make sure that port 80 is open on your firewall.
    3. Check to make sure that the network that connects your server to the Internet is allowing traffic over port 80.

4. Start Gunicorn

        sudo systemctl start gunicorn

    To test that Gunicorn is running, use the following command in a terminal window on your server: `systemctl status gunicorn`. If Gunicorn failed to start for some reason, this command will tell you why, although sometimes the messages can be a little cryptic. You can also check for the existence of `/home/USER_NAME/api/api.sock`. This is the socket that Gunicorn and Nginx use to communicate with each other. When it starts up, Gunicorn creates the socket. When it shuts down, Gunicorn deletes the socket.

5. Configure Nginx to proxy Gunicorn.

    1. Create an Nginx configuration file with the name api.conf.

            sudo nano /etc/nginx/conf.d/api.conf

    2. Paste in the following contents. Make sure you replace `SERVER_IP_ADDRESS` with your server's IP address. Also replace `USER_NAME` with your own user name.

            server {
                listen 80;
                server_name SERVER_IP_ADDRESS;

                location / {
                    proxy_set_header Host $http_host;
                    proxy_set_header X-Real-IP $remote_addr;
                    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                    proxy_set_header X-Forwarded-Proto $scheme;
                    proxy_pass http://unix:/home/USER_NAME/api/api.sock;
                }
            }

    3. Add the nginx user to your group. Replace `USER_NAME` with your own user name.

            sudo usermod -a -G USER_NAME nginx
            chmod 710 /home/USER_NAME

6. Restart Nginx to make sure the configuration is loaded.

        sudo systemctl reload nginx

In theory, you're all set to go. Open a browser and goto http://YOUR_SERVER/. You should see a table that shows the endpoints that the API provides.

If you get a bad gateway error, this means that Nginx is running but for some reason it can't connect to the Gunicorn socket. Run the following command in a terminal window on your server:

    sudo tail /var/log/nginx/error.log

This will give one or more hints about why it's not working. If the messages indicate that permission was denied, then most likely your server has SELinux. To verify, run the following command:

    sestatus

With any luck, you'll get output that indicates that SELinux is enabled. If not, I have no idea what's going on and you're on your own.

## SELinux

If your system has SELinux, you must make further changes to allow Nginx access to the Unix socket.

1. Create an SELinux Type Enforcement rule in a file called `nginx.te`. The file can be anywhere on your system that you have write access to.

        nano nginx.te

2. Paste the following contents into it:

        module nginx 1.0;

        require {
            type httpd_t;
            type user_home_t;
            type httpd_sys_content_t;
            type init_t;
            class sock_file write;
            class unix_stream_socket connectto;
        }

        #============= httpd_t ==============
        allow httpd_t httpd_sys_content_t:sock_file write;
        allow httpd_t init_t:unix_stream_socket connectto;
        allow httpd_t user_home_t:sock_file write;

3. Create a policy module called nginx.mod:

        checkmodule -M -m -o nginx.mod nginx.te

4. Compile the policy module into a policy package called `nginx.pp`:

        semodule_package -o nginx.pp -m nginx.mod

5. Load the policy module. This can take 15 seconds or so:

        sudo semodule -i nginx.pp

The API should be ready to use now.