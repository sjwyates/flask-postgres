from flask import render_template
from portal.plotlydash import portal_dash as portal_dash_obj
from portal.plotlydash import dash
from flask_login import login_required


@dash.route('/dashboard')
@login_required
def portal_dashboard():
    return render_template(
        'dashapps/dash_app.html',
        title='Welcome',
        dash_url=portal_dash_obj.URL_BASE,
        min_height=portal_dash_obj.MIN_HEIGHT
    )
