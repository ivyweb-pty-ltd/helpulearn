# -*- coding: utf-8 -*-
from odoo import http

# class Grading(http.Controller):
#     @http.route('/grading/grading/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/grading/grading/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('grading.listing', {
#             'root': '/grading/grading',
#             'objects': http.request.env['grading.grading'].search([]),
#         })

#     @http.route('/grading/grading/objects/<model("grading.grading"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('grading.object', {
#             'object': obj
#         })