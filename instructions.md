# Problem statement 

You will build a simple HTTP proxy server with caching. A proxy acts like a middleman: instead of your browser talking directly to a website, it talks to the proxy, which either fetches the data for you or serves a saved copy from its own storage. Your proxy will listen on a local port, accept client requests, check if the response is already cached, and either serve it immediately or fetch it from the origin server. This shows you how web traffic can be controlled, optimized, and sped up by an intermediary, just like how real- world proxies and CDNs work.

Think of your proxy as a librarian. When someone asks for a book, the librarian first checks if a copy is already on the shelf. If it’s there, you get it right away, which is a cache hit. If not, the librarian goes to the main library, makes a photocopy, hands you the book, and then keeps that copy for next time, which is a cache miss.

Your proxy server will behave the same way with web pages. When the client requests a resource:

- If the resource is already cached locally, the proxy returns it immediately.
- If the resource is not cached, the proxy forwards the request to the origin server, retrieves the response, sends it back to the client, and stores a copy in the cache for future requests.

Beyond caching, proxies are widely used in real networks. They can filter requests, block unwanted content, or log usage for traffic control. They improve efficiency by serving cached responses, reducing bandwidth consumption, and speeding up response times. They also enhance security and privacy by hiding client details from servers or enforcing access rules.

In this task, your proxy will be simple: handle client HTTP requests, forward them to the appropriate server when needed, and maintain a cache folder for faster responses on repeated requests. Through this simplified version, you will gain practical experience with how proxies enforce policies, reduce network load, and speed up content delivery.

# Instructions 

1. Create a Python file called ProxyServer.py and run it using: `python ProxyServer.py localhost`. The file has already been made.
2. Ensure the program creates a folder named cache/ if it does not exist. Cached files must follow the naming format:

`cache/<host><path with '/' replaced by '_'>`

Examples: 
- `http://httpforever.com/ -> cache/httpforever.com`
- `http://httpforever.com/css/style.css -> cache/httpforever.com_css_style.css`

3. When a client connects, read the HTTP request. If the method is not GET, respond with:

```
HTTP/1.0 405 Method Not Allowed
Content-Type: text/plain
content-Length: 22
405 Method Not Allowed
```

4. Parse the URL from the request. The default port is 80 unless a custom port is specified. If no path is given, use /.

Examples: 
- `http://example.com/ → host = example.com, port = 80, path = /`
- `http://example.com:8080/foo → host = example.com, port = 8080, path = /foo`

5. If the cache file exists, return its contents to the client. Otherwise, open a connection to the origin server and send:

```
GET /path HTTP/1.0
Host: host
Connection: close
User-Agent: SimpleProxy/1.0
```
Forward the server’s response to the client as it arrives, and save the entire response into the cache file.

6. If the proxy cannot connect to the origin server, reply with:

```
HTTP/1.0 502 Bad Gateway
Content-Type: text/plain
Content-Length: 15
502 Bad Gateway
```

# Testing

1. Test with a local HTTP server:

- Create a folder named server with an index.html file inside. This step has already been done.

- in the first terminal, start a simple HTTP server in that folder: `python -m http.server 8080`
- in the second terminal, start the proxy server: `python ProxyServer.py localhost`
- in a third terminal, fetch the file through your proxy using curl: `curl -x localhost:8888 http://localhost:8080/server/index.html`

2. Test with a real website:

- configure Chrome to use the proxy at localhost:8888
- visit `http://httpforever.com` and watch the proxy fetch and cache the response 
- delete the cached file and reload to see a cache miss, followed by another fetch from the server 


3. Verify cache hits and misses
- the first request should be a cache miss, fetched from the original server
- running the same request again should be a cache hit, served directly from your cache folder

# Sample Run 

Proxy terminal:

```
Proxy server running... Press Ctrl+C to stop.
Ready to serve...
Received a connection from: ('127.0.0.1', 58962)
Raw request:
GET http://localhost:8080/index.html HTTP/1.1
Host: localhost:8080
User-Agent: curl/8.7.1
Accept: */*
Proxy-Connection: Keep-Alive
Extracted:
Host: localhost, Port:8080, Path: /index.html
<<< CACHE MISS >>>
Connecting to Server...
Connection successful to localhost:8080
Saved 230 bytes to cache
```

On the second request:
```
>>> CACHE HIT <<<
Served from Local Cache: cache/localhost_index.html
```


