from odoo import http
from odoo.http import request

class DashboardController(http.Controller):
    @http.route('/dashboard/iframe_url', type='json', auth='user')
    def get_iframe_url(self):
        iframe_url = "https://app.powerbi.com/view?r=eyJrIjoiN2UyZDUzZTUtMTZmMi00YjMwLWFlZTEtZTk2NzQ1NjJhZ[...]6IjBiMTgwYjAyLTIzMTUtNDBjMS05ZWIxLTY0MDk4N2FmNDRkYyIsImMiOjl9"
        return {
            'iframe_url': iframe_url,
        }
