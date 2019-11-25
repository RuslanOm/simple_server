import aiohttp
from demo import create_app
from demo.settings import load_config


app = create_app(config=load_config())

if __name__ == "__main__":
    aiohttp.web.run_app(app, )


