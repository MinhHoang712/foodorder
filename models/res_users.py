
from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    qr = fields.Binary(string='QR Code Image')
    stk = fields.Char(string='Số tài khoản')
    nganhang = fields.Char(string='Ngân hàng')





