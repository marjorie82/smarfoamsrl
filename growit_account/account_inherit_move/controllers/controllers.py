# -*- coding: utf-8 -*-
# from odoo import http


# class AccountInheritMove(http.Controller):
#     @http.route('/account_inherit_move/account_inherit_move/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_inherit_move/account_inherit_move/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_inherit_move.listing', {
#             'root': '/account_inherit_move/account_inherit_move',
#             'objects': http.request.env['account_inherit_move.account_inherit_move'].search([]),
#         })

#     @http.route('/account_inherit_move/account_inherit_move/objects/<model("account_inherit_move.account_inherit_move"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_inherit_move.object', {
#             'object': obj
#         })
