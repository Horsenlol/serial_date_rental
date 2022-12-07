from datetime import datetime
from odoo import models, fields, api


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"
    _order = "last_rent_date asc"

    last_rent_date = fields.Date(compute="_compute_last_rent_date")

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, f"{rec.name}, {rec.last_rent_date}"))
        return result

    @api.depends("sale_order_count")
    def _compute_last_rent_date(self):
        for rec in self:
            context = {
                "model": "stock.production.lot",
                "active_id": rec.id,
            }
            res = self.env["stock.traceability.report"].with_context(context).get_lines()
            if res:
                for line in res:
                    columns = line.get("columns")
                    if columns and columns[4] == "Stock" and columns[5] == "Rental":
                        rec.last_rent_date = datetime.strptime(columns[2], "%d/%m/%Y %H:%M:%S")
                        break
            else:
                rec.last_rent_date = False
