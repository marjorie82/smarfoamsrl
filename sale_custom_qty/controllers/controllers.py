# -*- coding: utf-8 -*-
# from odoo import http


# class SaleCustomQty(http.Controller):
#     @http.route('/sale_custom_qty/sale_custom_qty', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_custom_qty/sale_custom_qty/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_custom_qty.listing', {
#             'root': '/sale_custom_qty/sale_custom_qty',
#             'objects': http.request.env['sale_custom_qty.sale_custom_qty'].search([]),
#         })

#     @http.route('/sale_custom_qty/sale_custom_qty/objects/<model("sale_custom_qty.sale_custom_qty"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_custom_qty.object', {
#             'object': obj
#         })
