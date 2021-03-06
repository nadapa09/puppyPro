from flask import Flask, render_template
import extensions
import controllers
import config

# Initialize Flask app with the template folder address
app = Flask(__name__, template_folder='templates')

# Register the controllers
app.register_blueprint(controllers.offerHelp)
app.register_blueprint(controllers.requestHelp)
app.register_blueprint(controllers.results)
app.register_blueprint(controllers.user)
app.register_blueprint(controllers.main)

app.secret_key = 'nc67dihlltjron37vte29'

# Listen on external IPs
# For us, listen to port 3000 so you can just run 'python app.py' to start the server
if __name__ == '__main__':
    # listen on external IPs
    #app.run(host=config.env['host'], port=config.env['port'], debug=True)
    import os
    import os
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

