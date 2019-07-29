"""
Return 4xx pages
"""
import Flask
import SUSOD
from SUSOD.util.login_permissions import get_username

@app.errorhandler(403)
def error_403():
	context = {
		username: get_username()
	}
	return render_template('./errors/403.html', **context), 403
