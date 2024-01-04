from odoo import models, fields, api

class UserPaymentInfo(models.Model):
    _name = 'user.payment.info'
    _description = 'User Payment Information'
    _rec_name = 'user_id'

    user_id = fields.Many2one('res.users', string='Người dùng',default=lambda self: self.env.user ,required=True, ondelete='cascade')
    qr = fields.Binary(string='QR Code')
    stk = fields.Char(string='Số tài khoản')
    nganhang = fields.Char(string='Ngân hàng')

    _sql_constraints = [
        ('user_id_unique', 'UNIQUE(user_id)', 'Mỗi người dùng chỉ có thể có một bản ghi thông tin thanh toán.')
    ]

    @api.model
    def open_current_user_payment_info(self):
        payment_info = self.env['user.payment.info'].search([('user_id', '=', self.env.uid)], limit=1)
        if payment_info:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'user.payment.info',
                'view_mode': 'form',
                'res_id': payment_info.id,
                'target': 'current',
            }
        else:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'user.payment.info',
                'view_mode': 'form',
                'context': {'default_user_id': self.env.uid},
                'target': 'new',
            }
