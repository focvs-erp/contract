# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ReajustePreco(models.Model):
    _name = 'contract.reajuste_preco'
    _description = 'Reajuste de Preço'

    name = fields.Char(string='Name', required=True)
    moeda = fields.Many2one('res.currency')
    empresa = fields.Many2one('res.company', 'Company')
    items = fields.One2many("contract.reajuste_preco_item", "reajuste_preco", string="Item")
