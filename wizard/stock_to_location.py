# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class TransferStockToLocation(models.TransientModel):
    _name = 'wave.stock.to.location'
    _description = 'Move selected stock to a location'
    dest_location_id = fields.Many2one('stock.location', 'Destination Location', help='All selected products will be moved to this location')

    @api.multi
    def transfer_stock(self):
        # This method transfers all selected products in active ids to the destination location
        # @param: self
        # @return: view of the created picks

        quants = self.env['stock.quant'].browse(self.env.context['active_ids'])
        picking_ids = []
        location_ids = []

        # Get source locations
        for stock in quants:
            if stock.location_id not in location_ids:
                location_ids.append(stock.location_id)
        
        # Create Picks based on source locations
        for location in location_ids:
            move_vals = []
            picking_vals = {
                 'location_dest_id': self.dest_location_id.id,
                 'picking_type_id': self.env['stock.picking.type'].search([('name','=','Internal Transfers')]).id
            }

            for quant in quants:
                if quant.location_id == location and quant.quantity - quant.reserved_quantity > 0:
                    move_dict = {
                        'product_id': quant.product_id.id,
                        'name': "LOC_CHANGE / " + quant.display_name,
                        'product_uom': quant.product_id.uom_id.id,
                        'product_uom_qty': quant.quantity - quant.reserved_quantity,
                        'location_id': location.id,
                        'location_dest_id': self.dest_location_id.id,
                    }
                    move_vals.append((0,0,move_dict))
            
            if len(move_vals) > 0:
                picking_vals['location_id'] = location.id
                picking_vals['move_lines'] = move_vals
                # Create and assign stock to the picking
                pick = self.env['stock.picking'].create(picking_vals)
                pick.action_confirm()
                pick.action_assign()
                picking_ids.append(pick.id)

        domain = [('id','in',picking_ids)]
        return { 'type': 'ir.actions.act_window', 'res_model': 'stock.picking', 'res_id': picking_ids, 'view_type': 'form', 'view_mode': 'tree,form', 'domain': domain}

