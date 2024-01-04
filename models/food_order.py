from odoo import models, fields, api
from odoo.exceptions import ValidationError

class FoodOrder(models.Model):
    _name = 'food.order'
    _description = 'Food Order'
    _rec_name = 'title'

    title = fields.Char(string='Đơn hàng', required=True)
    order_creator_id = fields.Many2one('res.users', string='Người thanh toán', default=lambda self: self.env.user, readonly=True)
    total_price = fields.Float(string='Tổng thanh toán', compute='_compute_total_price')
    order_date = fields.Date(string='Ngày đặt', required=True,  default=lambda self: fields.Date.context_today(self))
    discount = fields.Float(string='Giảm Giá')
    shipping_fee = fields.Float(string='Phí Ship')
    payment_info_id = fields.Many2one('user.payment.info', string='Thông tin thanh toán',  compute='_compute_payment_info', store=True, readonly=True)
    food_item_ids = fields.One2many('food.item', 'order_id', string='Food Items', required=True)
    order_creator_qr = fields.Binary(related='payment_info_id.qr', string='QR Code', readonly=True)
    order_creator_stk = fields.Char(related='payment_info_id.stk', string='Số tài khoản', readonly=True)
    order_creator_nganhang = fields.Char(related='payment_info_id.nganhang', string='Ngân hàng', readonly=True)
    complete = fields.Boolean(string='Hoàn Thành', compute='_compute_complete', store=True)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.company.currency_id.id)
    amount_paid = fields.Float(string='Số Tiền Đã Thanh Toán', compute='_compute_amount_paid')
    amount_due = fields.Float(string='Số Tiền Còn Thiếu', compute='_compute_amount_due')
    @api.depends('food_item_ids.food_price', 'food_item_ids.paid_status')
    def _compute_amount_paid(self):
        for order in self:
            order.amount_paid = sum(item.total_price for item in order.food_item_ids if item.paid_status)
    @api.depends('order_creator_id')
    def _compute_payment_info(self):
        for record in self:
            payment_info = self.env['user.payment.info'].search([('user_id', '=', record.order_creator_id.id)], limit=1)
            record.payment_info_id = payment_info

    @api.depends('total_price', 'amount_paid')
    def _compute_amount_due(self):
        for order in self:
            order.amount_due = order.total_price - order.amount_paid
    @api.depends('food_item_ids.food_price', 'shipping_fee', 'discount')
    def _compute_total_price(self):
        for order in self:
            total = sum(item.food_price for item in order.food_item_ids)
            order.total_price = total + order.shipping_fee - order.discount

    @api.depends('food_item_ids.paid_status')
    def _compute_complete(self):
        for order in self:
            order.complete = all(item.paid_status for item in order.food_item_ids) if order.food_item_ids else False

    @api.model
    def notify_unpaid_orders(self):
        orders = self.search([])
        for order in orders:
            unpaid_items = order.food_item_ids.filtered(lambda item: not item.paid_status and item.member_id)
            if unpaid_items:
                for item in unpaid_items:
                    formatted_price = "{:,.0f} VND".format(item.total_price)
                    body = "<p>Bạn còn một mục chưa thanh toán trong đơn hàng: {}</p>".format(order.title)
                    body += "<p>- Món ăn: {}: {}</p>".format(item.food_name, formatted_price)

                    if order.order_creator_qr:
                        qr_src = "data:image/png;base64,{}".format(order.order_creator_qr.decode())
                        body += "<p>QR Code for Payment:</p><img src='{}'/>".format(qr_src)

                    channel = self.env['mail.channel'].channel_get([item.member_id.partner_id.id])
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

    def write(self, vals):
        restricted_fields = ['title', 'order_date', 'discount', 'shipping_fee']

        if any(field in vals for field in restricted_fields):
            for record in self:
                if record.create_uid != self.env.user:
                    raise ValidationError(
                        "Bạn không có quyền chỉnh sửa các quyền này ")

        return super(FoodOrder, self).write(vals)
