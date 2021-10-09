from flask import Flask, render_template
import connexion

# Local modules
import config

#app = Flask(__name__, template_folder="templates")

# Get the application instance
connex_app = config.connex_app


# read the swagger.yml file to configure the endpoints.
# containing all of the information necessary to configure your server to provide input parameter validation,
# output response data validation, URL endpoint definition
connex_app.add_api("swagger.yml")


@connex_app.route('/')
def hello_world():
    return render_template("home.html")


if __name__ == '__main__':
    connex_app.run(debug=True)
