# -*- coding: utf-8 -*-
from odoo import http

# class Objective(http.Controller):
#     @http.route('/objective/objective/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/objective/objective/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('objective.listing', {
#             'root': '/objective/objective',
#             'objects': http.request.env['objective.objective'].search([]),
#         })

#     @http.route('/objective/objective/objects/<model("objective.objective"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('objective.object', {
#             'object': obj
#         })