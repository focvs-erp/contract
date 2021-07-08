from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError
from datetime import datetime


class ReceberFatura(models.TransientModel):
    _name = "contract.receber_fatura"
    _description = "Receber Fatura"

    name = fields.Char(readonly=True)
    contract_id = fields.Many2one("contract.contract", invisible=True)

    # AX4B - CPTM - RATEIO FORNECEDOR
    ativar_consorcio_fatura = fields.Boolean(string="Ativar consorcio")

    # AX4B - CPTM - RATEIO FORNECEDOR
    porcentagem = fields.Float(string="Porcentagem")

    partner_id = fields.Many2one("res.partner", string="Receber De")
    scheduled_date = fields.Date(string="Data Agendada", default=datetime.today())
    origin = fields.Char(related="contract_id.name", string="Documento de Origem")

    receber_fatura_line = fields.One2many(
        "contract.receber_fatura_line", "receber_fatura", string="Receber Fatura")

    def btn_validar_concluido(self):

        for products_line in self.receber_fatura_line:
            for concluido in products_line:
                if concluido.demanda < concluido.concluido:
                    raise UserError(
                        'O valor do campo Concluído não pode ser maior do que o campo Demanda')
                self._cr.execute(''' update contract_line set cd_recebido=%(concluido)s where id=%(contract_line_id)s ;''',
                                 {
                                     'contract_line_id': concluido.products_list.id,
                                     'concluido': concluido.concluido

                                 })

        self.criar_fatura_garantia()

    def action_close(self):
        return {'type': 'ir.actions.act_window_close'}

    @api.model
    def create(self, vals):
        obj = super(ReceberFatura, self).create(vals)
        sequence = self.env['ir.sequence'].get('receber_fatura_sequence')
        obj.write({'name': sequence})

    def criar_linha_na_fatura(self, move_id, contract, amount, type_bills):

        vals = {
            'move_id': move_id,
            'account_id': contract.cod_conta_contabil.id,
            'partner_id': contract.partner_id.id
        }

        vals['credit'] = amount if type_bills == "credit" else vals['debit'] = amount

        return (0, 0, vals)

    def criar_fatura_garantia(self):
        if self.contract_id.bt_reserva_garantia:

            fatura_line = self.receber_fatura_line

            contract = self.contract_id
            fatura = self.env['account.move'].create({
                'cd_empresa': self.env.user.company_id.id,
                'contract_garantia_id': contract.id,
                'invoice_origin': contract.name,
            })

            lines_ids_list = []
            amount_total = 0

            for item in fatura_line:
                amount = (item.products_list.price_unit
                          * (float(contract.cod_reserva_garantia) / 100)) * item.concluido
                amount_total += amount

                lines_ids_list.append(
                    self.criar_linha_na_fatura(fatura.id, contract, amount, 'debit')
                )

            # lines_ids_list.append(
            #     self.criar_linha_na_fatura(move_id=fatura.id,
            #                                account_id=contract.cod_conta_contabil.id,
            #                                partner_id=contract.partner_id.id,
            #                                credit=amount_total))
            lines_ids_list.append(
                self.criar_linha_na_fatura(fatura.id, contract, amount_total, 'credit')
            )

            fatura.line_ids = lines_ids_list
