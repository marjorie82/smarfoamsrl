# -*- coding: utf-8 -*-
# from odoo import http


# class PopularSupplierPaymentTxt(http.Controller):
#     @http.route('/popular_supplier_payment_txt/popular_supplier_payment_txt/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/popular_supplier_payment_txt/popular_supplier_payment_txt/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('popular_supplier_payment_txt.listing', {
#             'root': '/popular_supplier_payment_txt/popular_supplier_payment_txt',
#             'objects': http.request.env['popular_supplier_payment_txt.popular_supplier_payment_txt'].search([]),
#         })

#     @http.route('/popular_supplier_payment_txt/popular_supplier_payment_txt/objects/<model("popular_supplier_payment_txt.popular_supplier_payment_txt"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('popular_supplier_payment_txt.object', {
#             'object': obj
#         })
