from framework.web import JBWebServer

server = JBWebServer(
    host="localhost",
    port=8080
)

server.run()