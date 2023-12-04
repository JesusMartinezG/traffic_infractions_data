from flask_app import create_app

create_app(run_config='dev').run(debug=True)
# create_app(run_config='dev_database').run(host='0.0.0.0')