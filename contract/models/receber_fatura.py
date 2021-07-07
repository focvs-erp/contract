from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError
from datetime import datetime

class ReceberFatura(models.TransientModel):
    _name = "contract.receber_fatura"
    _description = "Receber Fatura"

    name = fields.Char(readonly=True)
    contract_id = fields.Many2one("contract.contract", invisible=True)

    ativar_consorcio_fatura = fields.Boolean(compute= "set_ativar_consorcio_fatura")


    def _get_domain_fornecedores(self):
        fornecedores_ids = []
        if self.env.context.get('ativar_consorcio'):
            consorcio = self.env['contract.contrato_consorcio'].search([("id", "=", self.env.context.get("cod_consorcio"))])
            for contract in consorcio.contratos:
                if contract.cd_ativo:
                    fornecedores_ids.append(contract.cd_fornecedores.id)
        else:
            fornecedores_ids.append(self.env.context.get('partner_id'))

        return [('id', 'in', fornecedores_ids)]



    partner_id = fields.Many2one("res.partner", string="Receber De", domain=_get_domain_fornecedores)
    porcentagem = fields.Float(string="Porcentagem")

    scheduled_date = fields.Date(string="Data Agendada", default=datetime.today())
    origin = fields.Char(related="contract_id.name", string="Documento de Origem")

    receber_fatura_line = fields.One2many("contract.receber_fatura_line","receber_fatura",string="Receber Fatura")


    def btn_validar_concluido(self):
        produtos_solicitados = self.receber_fatura_line.filtered(lambda x: x.concluido > 0)

        for solicitado in produtos_solicitados:
            total_recebido = solicitado.concluido + solicitado.recebido
            if solicitado.demanda < total_recebido :
                raise UserError('O valor do campo Concluído não pode ser maior do que o campo Demanda')

            self._cr.execute(''' update contract_line set cd_recebido=%(concluido)s where id=%(contract_line_id)s ;''',
                {
                    'contract_line_id': solicitado.products_list.id,
                    'concluido': total_recebido
                })

    def action_close(self):
        return {'type': 'ir.actions.act_window_close'}


    @api.model
    def create(self, vals):
        obj = super(ReceberFatura, self).create(vals)
        sequence = self.env['ir.sequence'].get('receber_fatura_sequence')
        obj.write({'name': sequence})
        return obj

    def set_ativar_consorcio_fatura(self):
        for rec in self:
            rec.ativar_consorcio_fatura = self.env.context.get('ativar_consorcio')


    @api.onchange("partner_id")
    def preencher_porncetagem(self):
        consorcio = self.env['contract.contrato_consorcio'].browse(self.env.context.get("cod_consorcio"))

        fornecedor_selecionado = consorcio.contratos.filtered(lambda x: x.cd_fornecedores.id == self.partner_id.id)
        self.porcentagem = fornecedor_selecionado.cd_participacao
