from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError
from datetime import datetime
import math
from datetime import datetime, date

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
            novo_recebido = solicitado.concluido + solicitado.recebido
            if self.env.context.get('ativar_consorcio'):

                total_fornecedor_recebido = self.get_recebido_por_fornecedor_consorcio(solicitado.products_list.id, self.partner_id.id)
                quantidade_total_permitida = math.ceil((solicitado.demanda / 100) * self.get_porcentagem_fornecedor())
                quantidade_atual_permitida = quantidade_total_permitida - total_fornecedor_recebido

                if solicitado.concluido > quantidade_atual_permitida:
                    raise UserError('Quantidade ultrapassa o permitido para este fornecedor, atualmente é permitido ' + str(quantidade_atual_permitida))

                self.criar_fatura_consorcio(solicitado.products_list.id, solicitado.concluido, quantidade_atual_permitida - solicitado.concluido)

            else:
                if solicitado.demanda < novo_recebido:
                    raise UserError('Quantidade ultrapassa o permitido para este fornecedor, atualmente é permitido ' + str(solicitado.demanda - solicitado.recebido))

            self.atualizar_recebido_contrato_line(solicitado.products_list.id, novo_recebido)
            self.env['contract.contract'].browse(self.contract_id.id).write({"houve_recebimento": True})
            self.env.cr.commit()
            self.criar_pedido()


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
        self.write({'porcentagem': self.get_porcentagem_fornecedor()})


    def get_porcentagem_fornecedor(self):
        consorcio = self.env['contract.contrato_consorcio'].browse(self.env.context.get("cod_consorcio"))
        fornecedor_selecionado = consorcio.contratos.filtered(lambda x: x.cd_fornecedores.id == self.partner_id.id)

        porcentagem = fornecedor_selecionado.cd_participacao if fornecedor_selecionado.cd_participacao else 0
        return porcentagem


    def get_recebido_por_fornecedor_consorcio(self, contract_line_id, fornecedor_id):
        produtos_recebidos = self.env["contract.fatura_consorcio"].search(['&', ("contract_line", "=", contract_line_id), ("cd_contrato", "=", self.contract_id.id), ("cd_fornecedor", "=", fornecedor_id)])

        total_recebido_produto = 0
        for produto in produtos_recebidos:
            total_recebido_produto += produto.total_concluido

        return total_recebido_produto


    def atualizar_recebido_contrato_line(self, contract_line_id, concluido):
        self._cr.execute(''' update contract_line set cd_recebido=%(concluido)s where id=%(contract_line_id)s ;''',
                {
                    'contract_line_id': contract_line_id,
                    'concluido': concluido
                })
#         self.env.cr.commit()

    def criar_fatura_consorcio(self, contract_line_id, total_recebido, disponivel):
        vals = {
            "cd_fornecedor": self.partner_id.id,
            "contract_line": contract_line_id,
            "total_concluido": total_recebido,
            "valor_disponivel_concluir": disponivel,
            "data_recebimento": date.today(),
        }
        self.env["contract.fatura_consorcio"].create(vals)


    def criar_pedido(self):
        pass
