from odoo import models, fields, api


class FoodItem(models.Model):
    _name = 'food.item'
    _description = 'Food Item'

    food_name = fields.Char(string='Tên Món', required=True)
    food_price = fields.Float(string='Giá Món', required=True)
    member_id = fields.Many2one('res.users', string='Thành Viên', required=True)
    paid_status = fields.Boolean(string='Trạng Thái Thanh Toán')
    order_id = fields.Many2one('food.order', string='Order', required=True)
    discount_shared = fields.Float(string='Giảm giá', compute='_compute_shipping_fee_shared')
    shipping_fee_shared = fields.Float(string='Tiền Ship', compute='_compute_shipping_fee_shared')
    total_price = fields.Float(string='Tổng tiền phải trả', compute='_compute_total_price')

    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.company.currency_id.id)

    @api.depends('order_id.shipping_fee', 'order_id.food_item_ids.member_id', 'order_id.discount')
    def _compute_shipping_fee_shared(self):
        for order in self.mapped('order_id'):
            unique_members = set(item.member_id for item in order.food_item_ids)
            total_unique_members = len(unique_members)

            if total_unique_members > 0:
                shipping_fee_per_member = order.shipping_fee / total_unique_members
                discount_per_member = order.discount / total_unique_members
            else:
                shipping_fee_per_member = 0
                discount_per_member = 0

            for item in order.food_item_ids:
                member_items_count = sum(
                    1 for member_item in order.food_item_ids if member_item.member_id == item.member_id)

                if member_items_count > 0:
                    item.shipping_fee_shared = shipping_fee_per_member / member_items_count
                    item.discount_shared = discount_per_member / member_items_count
                else:
                    item.shipping_fee_shared = 0
                    item.discount_shared = 0

    @api.depends('food_price', 'shipping_fee_shared', 'discount_shared')
    def _compute_total_price(self):
        for item in self:
            item.total_price = item.food_price + item.shipping_fee_shared - item.discount_shared