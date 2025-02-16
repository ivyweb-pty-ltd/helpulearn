# -*- coding: utf-8 -*-
# from odoo import http


# class Bit(http.Controller):
#     @http.route('/bit/bit', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bit/bit/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('bit.listing', {
#             'root': '/bit/bit',
#             'objects': http.request.env['bit.bit'].search([]),
#         })

#     @http.route('/bit/bit/objects/<model("bit.bit"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bit.object', {
#             'object': obj
#         })

