from odoo import models, fields


class RentalOrderWizardLine(models.TransientModel):
    _inherit = "rental.order.wizard.line"

    stock_production_lot_id = fields.Many2one("stock.production.lot", domain="[('product_id', '=', product_id)]")
