frappe.ui.form.on('BOM', {

    // ── Trigger on every input change ──
    custom_order_quantity:           function(frm) { calculate_carton_cost(frm); },
    custom_normal_loss:              function(frm) { calculate_carton_cost(frm); },
    custom_roll_size_mm:             function(frm) { calculate_carton_cost(frm); },
    custom_no_of_cutting:            function(frm) { calculate_carton_cost(frm); },
    custom_roll_size_gsm__t_top:     function(frm) { calculate_carton_cost(frm); },
    custom_roll_size_gsm__f_flute:   function(frm) { calculate_carton_cost(frm); },
    custom_roll_size_gsm__t_bottom:  function(frm) { calculate_carton_cost(frm); },
    custom_rate_of_paper:            function(frm) { calculate_carton_cost(frm); },
    custom_total_labor_hrs_required: function(frm) { calculate_carton_cost(frm); },
    custom_carton_length_mm_l:       function(frm) { calculate_carton_cost(frm); },
    custom_carton_width_mm_w:        function(frm) { calculate_carton_cost(frm); },
    custom_carton_height_mm_h:       function(frm) { calculate_carton_cost(frm); },
    custom_select_flute_size:        function(frm) { calculate_carton_cost(frm); },
    custom_sale_margin:              function(frm) { calculate_carton_cost(frm); },
    custom_total_kgs_ink_required:   function(frm) { calculate_carton_cost(frm); },

    refresh: function(frm) { calculate_carton_cost(frm); }
});


function calculate_carton_cost(frm) {
    let d = frm.doc;

    // ── Grab all inputs ──────────────────────────────────────
    let order_qty   = d.custom_order_quantity           || 0;
    let normal_loss = (d.custom_normal_loss             || 0) / 100;
    let roll_size   = d.custom_roll_size_mm             || 0;
    let no_cutting  = d.custom_no_of_cutting            || 1;
    let gsm_t       = d.custom_roll_size_gsm__t_top    || 0;
    let gsm_f       = d.custom_roll_size_gsm__f_flute  || 0;
    let gsm_t2      = d.custom_roll_size_gsm__t_bottom || 0;
    let rate_paper  = d.custom_rate_of_paper            || 0;
    let labor_hrs   = d.custom_total_labor_hrs_required || 0;
    let L           = d.custom_carton_length_mm_l       || 0;
    let W           = d.custom_carton_width_mm_w        || 0;
    let H           = d.custom_carton_height_mm_h       || 0;
    let sale_margin = (d.custom_sale_margin             || 0) / 100;
    let ink_kgs     = d.custom_total_kgs_ink_required   || 0;

    // ────────────────────────────────────────────────────────
    // 1. FLUTE FACTOR
    // =VLOOKUP(Select Flute Size, lookup table, 2, 0)
    // ────────────────────────────────────────────────────────
    let flute_factor = 0;
    if (d.custom_select_flute_size === 'Size - A Flute -5mm')   flute_factor = 1.55;
    if (d.custom_select_flute_size === 'Size - B Flute -3.5mm') flute_factor = 1.35;
    if (d.custom_select_flute_size === 'Size - E Flute -1.5mm') flute_factor = 1.25;
    frm.set_value('custom_flute_factor', flute_factor);

    // ────────────────────────────────────────────────────────
    // 2. GSM
    // = gsm_t + (gsm_f * flute_factor) + gsm_t2
    // ────────────────────────────────────────────────────────
    let gsm = gsm_t + (gsm_f * flute_factor) + gsm_t2;
    frm.set_value('custom_gsm', parseFloat(gsm.toFixed(2)));

    // ────────────────────────────────────────────────────────
    // 3. WEIGHT OF ONE CARTON (gm)
    // = (((30 + (2*(L+W))) * ((Roll Size mm / No Of Cutting) / 1000000))
    //    * GSM / 1000) * (1 + Normal Loss)
    // ────────────────────────────────────────────────────────
    let sheet_width  = roll_size / no_cutting;
    let sheet_length = 30 + (2 * (L + W));
    let area_m2      = (sheet_length * sheet_width) / 1000000;
    let weight_gm    = (area_m2 * gsm / 1000) * (1 + normal_loss);
    frm.set_value('custom_weight_of_one_carton_gm', parseFloat(weight_gm.toFixed(4)));

    // ────────────────────────────────────────────────────────
    // 4. MATERIAL COST
    // = Weight of One Carton (gm) * Rate of Paper
    // ────────────────────────────────────────────────────────
    let material_cost = weight_gm * rate_paper;
    frm.set_value('custom_material_cost', parseFloat(material_cost.toFixed(4)));

    // ────────────────────────────────────────────────────────
    // 5. LABOUR COST
    // = (Total Labor Hrs Required * 15 * 10) / Order Quantity
    // ────────────────────────────────────────────────────────
    let labour_cost = order_qty > 0
        ? (labor_hrs * 15 * 10) / order_qty
        : 0;
    frm.set_value('custom_labour_cost', parseFloat(labour_cost.toFixed(4)));

    // ────────────────────────────────────────────────────────
    // 6. OVERHEAD COST
    // = (Total Labor Hrs Required * 15 * 60) / Order Quantity
    // ────────────────────────────────────────────────────────
    let overhead_cost = order_qty > 0
        ? (labor_hrs * 15 * 60) / order_qty
        : 0;
    frm.set_value('custom_overhead_cost', parseFloat(overhead_cost.toFixed(4)));

    // ────────────────────────────────────────────────────────
    // 7. INK COST (per carton)
    // = (Total Kgs Ink Required * 15) / Order Quantity
    // ────────────────────────────────────────────────────────
    let ink_cost = order_qty > 0
        ? (ink_kgs * 15) / order_qty
        : 0;
    frm.set_value('custom_ink_cost', parseFloat(ink_cost.toFixed(4)));

    // ────────────────────────────────────────────────────────
    // 8. GLUE STD COST (fixed)
    // = 0.02
    // ────────────────────────────────────────────────────────
    let glue_std_cost = 0.02;
    frm.set_value('custom_glue_std_cost', glue_std_cost);

    // ────────────────────────────────────────────────────────
    // 9. STD SETUP COST
    // = 150 / Order Quantity
    // ────────────────────────────────────────────────────────
    let std_setup_cost = order_qty > 0
        ? 150 / order_qty
        : 0;
    frm.set_value('custom_std_setup_cost', parseFloat(std_setup_cost.toFixed(4)));

    // ────────────────────────────────────────────────────────
    // 10. COST PER CARTON
    // = Labour + Overhead + Glue + Setup + Ink + Material
    // ────────────────────────────────────────────────────────
    let cost_per_carton = labour_cost + overhead_cost + glue_std_cost
                        + std_setup_cost + ink_cost + material_cost;
    frm.set_value('custom_cost_per_carton', parseFloat(cost_per_carton.toFixed(4)));

    // ────────────────────────────────────────────────────────
    // 11. SALES PER CARTON
    // = Cost per Carton / (1 - Sale Margin)
    // ────────────────────────────────────────────────────────
    let sales_per_carton = (1 - sale_margin) > 0
        ? cost_per_carton / (1 - sale_margin)
        : 0;
    frm.set_value('custom_sales_per_carton', parseFloat(sales_per_carton.toFixed(4)));

    // ────────────────────────────────────────────────────────
    // 12. JOB ORDER TOTALS
    // ────────────────────────────────────────────────────────

    // Ink Cost Total = Total Kgs Ink Required * 15
    let ink_cost_total = ink_kgs * 15;
    frm.set_value('custom_ink_cost_total', parseFloat(ink_cost_total.toFixed(2)));

    // Material Cost Total = Order Qty * (1 + Normal Loss) * Rate of Paper * Weight(gm)
    let material_cost_total = order_qty * (1 + normal_loss) * rate_paper * weight_gm;
    frm.set_value('custom_material_cost_total', parseFloat(material_cost_total.toFixed(2)));

    // Labour Cost Total = Total Labor Hrs * (1 + Normal Loss) * 10 * 15
    let labour_cost_total = labor_hrs * (1 + normal_loss) * 10 * 15;
    frm.set_value('custom_labour_cost_total', parseFloat(labour_cost_total.toFixed(2)));

    // Overhead Cost Total = Total Labor Hrs * (1 + Normal Loss) * 60 * 15
    let overhead_cost_total = labor_hrs * (1 + normal_loss) * 60 * 15;
    frm.set_value('custom_overhead_cost_total_', parseFloat(overhead_cost_total.toFixed(2)));

    // Glue Std Cost Total = 100 (fixed)
    let glue_std_cost_total = 100;
    frm.set_value('custom_glue_std_cost_total', glue_std_cost_total);

    // Std Setup Cost Total = 100 (fixed)
    let std_setup_cost_total = 100;
    frm.set_value('custom_std_setup_cost_total', std_setup_cost_total);

    // Order Total Cost = Ink + Material + Labour + Overhead + Glue + Setup totals
    let order_total_cost = ink_cost_total + material_cost_total + labour_cost_total
                         + overhead_cost_total + glue_std_cost_total + std_setup_cost_total;
    frm.set_value('custom_order_total_cost', parseFloat(order_total_cost.toFixed(2)));

    // Total Material Weight = Weight of One Carton (gm) * Order Quantity
    let total_material_weight = weight_gm * order_qty;
    frm.set_value('custom_total_material_weight_kg', parseFloat(total_material_weight.toFixed(4)));

    // ────────────────────────────────────────────────────────
    // 13. TON RATE COST
    // = Order Total Cost / Total Material Weight
    // ────────────────────────────────────────────────────────
    let ton_rate_cost = total_material_weight > 0
        ? order_total_cost / total_material_weight
        : 0;
    frm.set_value('custom_ton_rate_cost', parseFloat(ton_rate_cost.toFixed(4)));

    // ────────────────────────────────────────────────────────
    // 14. TON RATE SALE
    // = Ton Rate Cost * 1.4
    // ────────────────────────────────────────────────────────
    let ton_rate_sale = ton_rate_cost * 1.4;
    frm.set_value('custom_ton_rate_sale', parseFloat(ton_rate_sale.toFixed(4)));
}