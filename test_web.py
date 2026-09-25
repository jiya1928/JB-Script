from framework.web import web


app = web()


def home(request):
    return "Hello from JB Framework!"


app.get("/", home)

app.run(8080)