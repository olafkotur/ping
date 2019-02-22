# Network Application Development
***


## Ping
```sudo python ping.py```

Ping 10 times (fixed) to host: `google.com`
```ping google.com```

Ping 25 times (custom) to host: `google.com`
```ping google.com -c 25```


***


## Traceroute
```sudo python traceroute.py```

Trace route of host: `google.com`
```ping google.com```

Trace route of host with a timoute of 2 seconds: `google.com`
```traceroute google.com -t 2```


***


## WebServer
```sudo python webserver.py```

The program will allow you to choose a `PORT number`, this must be greater than 1024. If you decide not to choose a PORT, the program will assume you use `PORT: 8080`. The program will use a different port if the selected port is already in use.

For testing, you may choose to use a random PORT, to do this set the fixed port value to false in `webserver.py line 15`
```
14  MAX_CONNECTIONS = 4		# Max number of refused connections
15  FIXED_PORT = True		 # Always attempt to use PORT 8080 if available
16  TIMEOUT = 100			  # Socket blocking value
```

To test the web server you can use any browser or `wget` to request the following pages:
* / (empty)
* /index.html
* /doggo.html

If the client requests any other pages the server will respond with a 404 Not Found and present the `404.html` file.

To exit the program and halt all server safely, use the default system interrupt on your operating system, the program will detect this and handle the request accordingly.

Mac: `CMD + C`

Literally anything else: `CTRL + C`


***


## WebProxy
```sudo python webproxy.py```

The program will allow you to choose a `PORT number`, this must be greater than 1024. If you decide not to choose a PORT, the program will assume you use `PORT: 8080`. The program will use a different port if the selected port is already in use.

For testing, you may choose to use a random PORT, to do this set the fixed port value to false in `webproxy.py line 15`
```
14  MAX_CONNECTIONS = 4		# Max number of refused connections
15  FIXED_PORT = True		 # Always attempt to use PORT 8080 if available
16  TIMEOUT = 100			  # Socket blocking value
```

To test the proxy you can use any browser provided you are able to set a manual proxy or the `wget` command. You should see terminal ouput for the related pages that are being requested. Note that this program will only work for `http://` websites, otherwise marked as `Not Secure` on some browsers.

```
wget thebigcb.com -e use_proxy=yes -e http_proxy=127.0.0.1:8080
```

To exit the program and halt all server safely, use the default system interrupt on your operating system, the program will detect this and handle the request accordingly.

Mac: `CMD + C`

Literally anything else: `CTRL + C`
