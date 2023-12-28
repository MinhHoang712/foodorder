from odoo import models, fields, api
from odoo.exceptions import ValidationError

class FoodOrder(models.Model):
    _name = 'food.order'
    _description = 'Food Order'
    _rec_name = 'title'

    title = fields.Char(string='Đơn order', required=True)
    order_creator_id = fields.Many2one('res.users', string='Người thanh toán', default=lambda self: self.env.user, readonly=True)
    total_price = fields.Float(string='Tổng thanh toán', compute='_compute_total_price')
    order_date = fields.Date(string='Ngày đặt', required=True)
    discount = fields.Float(string='Giảm Giá')
    shipping_fee = fields.Float(string='Phí Ship')
    food_item_ids = fields.One2many('food.item', 'order_id', string='Food Items', required=True)
    order_creator_qr = fields.Binary(related='order_creator_id.qr', string='QR Code', readonly=True)
    order_creator_stk = fields.Char(related='order_creator_id.stk', string='Số tài khoản', readonly=True)
    order_creator_nganhang = fields.Char(related='order_creator_id.nganhang', string='Ngân hàng', readonly=True)
    complete = fields.Boolean(string='Hoàn Thành', compute='_compute_complete', store=True)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.company.currency_id.id)

    @api.depends('food_item_ids.food_price', 'shipping_fee', 'discount')
    def _compute_total_price(self):
        for order in self:
            total = sum(item.food_price for item in order.food_item_ids)
            order.total_price = total + order.shipping_fee - order.discount

    @api.depends('food_item_ids.paid_status')
    def _compute_complete(self):
        for order in self:
            order.complete = all(item.paid_status for item in order.food_item_ids)

    @api.model
    def notify_unpaid_orders(self):
        orders = self.search([])
        for order in orders:
            unpaid_items = order.food_item_ids.filtered(lambda item: not item.paid_status and item.member_id)
            if unpaid_items:
                body = "<p>Bạn còn các mục chưa thanh toán trong đơn hàng: {}</p>".format(order.title)
                for item in unpaid_items:
                    formatted_price = "{:,.0f} VND".format(item.total_price)  # Định dạng số và thêm 'VND'
                    body += "<p>- Món ăn: {}: {}</p>".format(item.food_name, formatted_price)

                if order.order_creator_qr:
                    qr_src = "data:image/png;base64,{}".format(order.order_creator_qr.decode())
                    body += "<p>QR Code for Payment:</p><img src='{}'/>".format(qr_src)

                channel = self.env['mail.channel'].channel_get([order.order_creator_id.partner_id.id])
                channel_id = self.env['mail.channel'].browse(channel['id'])

                channel_id.with_context(mail_create_nosubscribe=True).message_post(
                    body=body,
                    author_id=self.env.ref('base.partner_root').id,
                    message_type='comment',
                    subtype_xmlid='mail.mt_comment',
                    content_subtype='html'
                )

    @api.constrains('food_item_ids')
    def _check_food_item_ids(self):
        for order in self:
            if not order.food_item_ids:
                raise ValidationError("Đơn hàng phải có ít nhất một món ăn.")

            for item in order.food_item_ids:
                if not item.food_name or item.food_price <= 0:
                    raise ValidationError("Mỗi món ăn phải có tên và giá hợp lệ.")
