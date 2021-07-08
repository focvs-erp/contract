# Copyright 2016 Tecnativa - Carlos Dauden
# Copyright 2018 ACSONE SA/NV.
# Copyright 2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    # We keep this field for migration purpose
    old_contract_id = fields.Many2one("contract.contract")

    # Reserva de Garantia
    contract_garantia_id = fields.Many2one("contract.contract")

    # def _check_balanced(self):
    #     # !IMPORTANTE esse metodo foi sobreescrito para que possa ser possivel
    #     # a inserção em receber_fatura.py na linha 42 sem a necessidade de
    #     # ter uma contrapartida.
    #     ''' Assert the move is fully balanced debit = credit.
    #     An error is raised if it's not the case.
    #     '''
    #     return True


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    contract_line_id = fields.Many2one(
        "contract.line", string="Contract Line", index=True
    )
