# Creates default files for SUSOD 

import sys
from pathlib import Path

def generate_controller(page_name):
	p = Path("./SUSOD/controller/" + page_name)

	if not (p.exists() or p.is_dir()):
		p.mkdir()

		q = p / '__init__.py'
		with q.open('w', encoding = "utf-8") as f:
			f.write("# Make sure to import any .py files added to SUSOD/controller/" + page_name)
			f.close()

	else: 
		raise ValueError("There exists an object named " + page_name + " in ./SUSOD/controller/")


def generate_js(page_name):
	p = Path("./SUSOD/js/" + page_name + "_index")

	if not (p.exists() or p.is_dir()):
		p.mkdir()

		q = p / 'index.jsx'
		with q.open('w', encoding = "utf-8") as f:
			f.write("""import React, {Component} from 'react';
import PropTypes from 'prop-types';

class Index extends Component {
	render() {
		return (
			<h1>
				Change me
			</h1>
		);
	}
}

Index.propTypes = {
	url: PropTypes.string.isRequired,
}

export default Index;

				""")
			f.close()

		p = Path("./SUSOD/js/_routes/" + page_name + "_index.jsx")
		with p.open('w', encoding = "utf-8") as f:
			f.write("""import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import Index from '""" + page_name + """_index/index';



ReactDOM.render(
	<Index url="/api/""" + page_name + """/" />,
	document.getElementById('reactEntry')
);
				""")


	else: 
		raise ValueError("There exists an object named " + page_name + "_index" + " in ./SUSOD/js/")



def generate_model(page_name):
	p = Path("./SUSOD/model/" + page_name + ".py")

	if not (p.exists()):

		with p.open('w', encoding = "utf-8") as f:
			f.write("""import flask
import SUSOD

from SUSOD import util
from .db import get_db

# Add any database related functions here
				""")
			f.close()

	else: 
		raise ValueError("There exists an object named " + page_name + ".py in ./SUSOD/model/")



def generate_templates(page_name):
	p = Path("./SUSOD/templates/" + page_name)

	if not (p.exists() or p.is_dir()):
		p.mkdir()

		q = p / 'index.html'
		with q.open('w', encoding = "utf-8") as f:
			f.write("""{% extends "header.html" %}
{% block content %}
	<div id="reactEntry"/>
	<script src="{{ url_for('static', filename='./js/""" + page_name + """_index.js') }}"></script>
{% endblock %}


				""")
			f.close()

	else: 
		raise ValueError("There exists an object named " + page_name + " in ./SUSOD/templates/")

def generate_views(page_name):
	p = Path("./SUSOD/views/" + page_name)

	if not (p.exists() or p.is_dir()):
		p.mkdir()

		q = p / (page_name + '.py')
		with q.open('w', encoding = "utf-8") as f:
			f.write("""#""" + page_name + """ view
import flask
import SUSOD
from SUSOD import util

@SUSOD.app.route('/""" + page_name + """/')
@util.has_permissions
def show_""" + page_name + """_index():
	context = util.get_login_context()
	
	return flask.render_template('""" + page_name + """/index.html', **context)
""")
			f.close()

		q = p / '__init__.py'
		with q.open('w', encoding = "utf-8") as f:
			f.write("from ." + page_name + " import show_" + page_name + "_index")
			f.close()

		# Add necessary line to 
		path_views_init = Path("./SUSOD/views/__init__.py")
		with path_views_init.open('a') as f:
			f.write("\nfrom ." + page_name + " import *\n")
	else: 
		raise ValueError("There exists an object named " + page_name + " in ./SUSOD/views/")

def __main__():
	if (len(sys.argv) == 2):
		page_name = sys.argv[1]

		try:
			generate_controller(page_name)
			generate_js(page_name)
			generate_model(page_name)
			generate_templates(page_name)
			generate_views(page_name)
		except ValueError as ex:
			print(ex)

	else:
		print("""
This tool is here to generate the initial files required 
to build the initial files for adding a new page. 		

Please Run: python3 generate_page.py <new_page_name>
""")


__main__()