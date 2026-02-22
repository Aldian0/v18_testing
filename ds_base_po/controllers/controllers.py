# -*- coding: utf-8 -*-
# from odoo import http


# class DsBasePo(http.Controller):
#     @http.route('/ds_base_po/ds_base_po', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ds_base_po/ds_base_po/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ds_base_po.listing', {
#             'root': '/ds_base_po/ds_base_po',
#             'objects': http.request.env['ds_base_po.ds_base_po'].search([]),
#         })

#     @http.route('/ds_base_po/ds_base_po/objects/<model("ds_base_po.ds_base_po"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ds_base_po.object', {
#             'object': obj
#         })

