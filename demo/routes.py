from .views import frontend


def setup_routes(app):
    app.router.add_route("GET", "/", frontend.index)
    app.router.add_route("POST", "/registration", frontend.reg_user)
    app.router.add_route("GET", "/login", frontend.login)
    app.router.add_route("GET", "/error", frontend.error)
    app.router.add_route("GET", '/logout', frontend.logout)
    app.router.add_route("GET", '/test', frontend.test)

