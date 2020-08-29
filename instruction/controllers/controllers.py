# -*- coding: utf-8 -*-
from odoo import http

# class Instruction(http.Controller):
#     @http.route('/instruction/instruction/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/instruction/instruction/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('instruction.listing', {
#             'root': '/instruction/instruction',
#             'objects': http.request.env['instruction.instruction'].search([]),
#         })

#     @http.route('/instruction/instruction/objects/<model("instruction.instruction"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('instruction.object', {
#             'object': obj
#         })