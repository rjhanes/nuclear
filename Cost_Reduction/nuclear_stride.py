import marimo

__generated_with = "0.15.0"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    <center><table>
        <tr>
            <th><img src="./INL1.png",align="middle",height="10000"/></th>
            <th><img src="./MIT1.png",align="middle",height="10"\></th>
            <th><img src="./ANL.png",align="middle",height="10"/></th>
        </tr>
    </table>
    </center>
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# <center>Cost Reduction Framework for Nuclear Reactor Power Plants</center>""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""###  Importing the libraries""")
    return


@app.cell
def _():
    import pandas as pd
    import numpy as np
    from src import prettify, update_high_level_costs, ITC_reduction_factor

    import warnings
    warnings.simplefilter(action='ignore', category=FutureWarning)

    pd.set_option('display.max_rows', None)
    return ITC_reduction_factor, np, pd, prettify, update_high_level_costs


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Section 1 : Reading the Baseline reactor Cost Summary Table""")
    return


@app.cell
def _(pd):

    def reactor_data_read(reactor_type):
        if reactor_type == 'Concept A':
            raise NotImplementedError
        elif reactor_type == 'Concept B':
            Reactor_data_0 = pd.read_excel('Cost_Reduction/conceptb-inputs.xlsx',
                                           sheet_name = 'Costs')
            _reactor_power = 310.8 * 1000
        db = pd.DataFrame()
        db = Reactor_data_0[['Account', 'Title',
                             'Total Cost (USD)', 'Factory Equipment Cost',
                             'Site Labor Hours', 'Site Labor Cost',
                             'Site Material Cost']].copy()
        Reactor_data = db
        return (Reactor_data, _reactor_power)

    # Check function
    reactor_data = reactor_data_read('Concept B')[0]
    _reactor_power = reactor_data_read('Concept B')[1]

    reactor_data

    return (reactor_data_read,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Section - 2 : User Inputs""")
    return


@app.cell
def _():
    # User specified parameters

    # DO NOT CHANGE this one
    reactor_type_1 = 'Concept B'

    # OK to change the rest of these
    n_th = 1
    num_orders = 13
    land_cost_per_acre_0 = 22000
    startup_0 = 16
    interest_rate_0 = 0.06
    design_completion_0 = 0.8
    Design_Maturity_0 = 1
    proc_exp_0 = 0.5
    ae_exp_0 = 0.5
    ce_exp_0 = 1
    N_proc = 3
    N_AE = 4
    N_cons = 5
    mod_0 = 'modularized'
    standardization_0 = 0.8
    BOP_grade_0 = 'non_nuclear'
    RB_grade_0 = 'nuclear'
    ITC_0 = 0
    n_ITC = 3
    f_22 = 250000000
    f_2321 = 150000000
    return (
        BOP_grade_0,
        Design_Maturity_0,
        ITC_0,
        N_AE,
        N_cons,
        N_proc,
        RB_grade_0,
        ae_exp_0,
        ce_exp_0,
        design_completion_0,
        f_22,
        f_2321,
        interest_rate_0,
        land_cost_per_acre_0,
        mod_0,
        n_ITC,
        n_th,
        num_orders,
        proc_exp_0,
        reactor_type_1,
        standardization_0,
        startup_0,
    )


@app.cell
def _(
    BOP_grade_0,
    Design_Maturity_0,
    ITC_0,
    RB_grade_0,
    ae_exp_0,
    ce_exp_0,
    design_completion_0,
    interest_rate_0,
    land_cost_per_acre_0,
    mod_0,
    pd,
    proc_exp_0,
    standardization_0,
    startup_0,
):
    global_levers = pd.read_csv('Cost_Reduction/global_levers_baselines.csv')

    global_levers.loc[:, 'User-Input Value'] = [Design_Maturity_0,
                                                design_completion_0,
                                                proc_exp_0,
                                                ae_exp_0,
                                                ce_exp_0,
                                                land_cost_per_acre_0,
                                                ITC_0,
                                                interest_rate_0,
                                                BOP_grade_0,
                                                RB_grade_0,
                                                mod_0,
                                                standardization_0,
                                                startup_0]

    global_levers
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### The Cost reduction framework: levers and variables impact the costs as shown in the figure (below)

    <center><table>
        <tr>
            <th><img src="./framework_diagram.png",align="middle",height="10000"/></th>
        </tr>
    </table>
    </center>
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Section - 3 : Updating the Cost Summary based on user inputs""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Section - 3-0 : Adding the factory cost to accounts 22 and 232.1""")
    return


@app.cell
def _(num_orders, pd, update_high_level_costs):
    def add_factory_cost(Reactor_data_0, power, f_22, f_2321):
        db = pd.DataFrame()
        db = Reactor_data_0[['Account', 'Title', 'Total Cost (USD)', 'Factory Equipment Cost', 'Site Labor Hours', 'Site Labor Cost', 'Site Material Cost']].copy()
        db.loc[db.Account == 22, 'Factory Equipment Cost'] = None
        db.loc[db.Account == 232.1, 'Factory Equipment Cost'] = None
        db.loc[db.Account == 22, 'Factory Equipment Cost'] = Reactor_data_0.loc[Reactor_data_0.Account == 22, 'Factory Equipment Cost'] + f_22 / num_orders
        db.loc[db.Account == 232.1, 'Factory Equipment Cost'] = Reactor_data_0.loc[Reactor_data_0.Account == 232.1, 'Factory Equipment Cost'] + f_2321 / num_orders
        Reactor_data_fac = update_high_level_costs(db, power)
        Reactor_data_fac_ = pd.DataFrame()
        Reactor_data_fac_ = Reactor_data_fac[['Account', 'Title', 'Total Cost (USD)', 'Factory Equipment Cost', 'Site Labor Hours', 'Site Labor Cost', 'Site Material Cost']].copy()
        return Reactor_data_fac_

    return (add_factory_cost,)


@app.cell
def _(
    add_factory_cost,
    f_22,
    f_2321,
    np,
    prettify,
    reactor_data_1,
    reactor_type_1,
):


    _Reactor_data_factory = add_factory_cost(reactor_data_1, _reactor_power, f_22, f_2321)

    Reactor_data_factory_pretty = prettify(_Reactor_data_factory, f' The {reactor_type_1} {np.round(_reactor_power / 1000, 1)} MWe Reactor <br> Capital Cost Summary - Factories Cost Included  <br> Displaying Direct Cost only<br><br> ', 'no_subsidies')
    list1 = list(range(0, 11))
    list2 = list(range(29, 69))
    hidden_list1 = list1 + list2
    Reactor_data_factory_pretty#.hide(subset=hidden_list1, axis=0)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Section 3-1 : The land cost & Taxes""")
    return


@app.cell
def _(
    add_factory_cost,
    f_22,
    f_2321,
    land_cost_per_acre_0,
    np,
    pd,
    prettify,
    reactor_data_read,
    reactor_type_1,
    update_high_level_costs,
):
    def add_land_cost(Reactor_data_fac, land_cost_per_acre, power):
        db = pd.DataFrame()
        db = Reactor_data_fac[['Account', 'Title', 'Total Cost (USD)', 'Factory Equipment Cost', 'Site Labor Hours', 'Site Labor Cost', 'Site Material Cost']].copy()
        db.loc[db.Account == 11, 'Total Cost (USD)'] = None
        db.loc[db.Account == 12, 'Total Cost (USD)'] = None
        db.loc[db.Account == 51, 'Total Cost (USD)'] = None
        db.loc[db.Account == 11, 'Total Cost (USD)'] = land_cost_per_acre / 22000 * Reactor_data_fac.loc[Reactor_data_fac.Account == 11, 'Total Cost (USD)'].values
        db.loc[db.Account == 12, 'Total Cost (USD)'] = land_cost_per_acre / 22000 * Reactor_data_fac.loc[Reactor_data_fac.Account == 12, 'Total Cost (USD)'].values
        db.loc[db.Account == 51, 'Total Cost (USD)'] = land_cost_per_acre / 22000 * Reactor_data_fac.loc[Reactor_data_fac.Account == 51, 'Total Cost (USD)'].values
        db.loc[db.Account == 51, 'Total Cost (USD)']
        Reactor_data_updated_1 = update_high_level_costs(db, power)
        Reactor_data_updated_1_ = pd.DataFrame()
        Reactor_data_updated_1_ = Reactor_data_updated_1[['Account', 'Title', 'Total Cost (USD)', 'Factory Equipment Cost', 'Site Labor Hours', 'Site Labor Cost', 'Site Material Cost']].copy()
        return Reactor_data_updated_1_
    reactor_data_2 = reactor_data_read(reactor_type_1)[0]
    _reactor_power = reactor_data_read(reactor_type_1)[1]
    _Reactor_data_factory = add_factory_cost(reactor_data_2, _reactor_power, f_22, f_2321)
    _Reactor_data_factory_land_taxes = add_land_cost(_Reactor_data_factory, land_cost_per_acre_0, _reactor_power)
    Reactor_data_factory_land_taxes_pretty = prettify(_Reactor_data_factory_land_taxes, f' The {reactor_type_1} {np.round(_reactor_power / 1000, 1)} MWe Reactor <br> Capital Cost Summary - Factories Cost, land cost and taxes Included  <br><br> ', 'no_subsidies')
    hidden_list2 = list(range(46, 69))
    Reactor_data_factory_land_taxes_pretty#.hide(subset=hidden_list2, axis=0)
    return (add_land_cost,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Section 3-2 : Whether the Reactor Building and BOP are nuclear grade equipment""")
    return


@app.cell
def _(
    BOP_grade_0,
    RB_grade_0,
    add_factory_cost,
    add_land_cost,
    f_22,
    f_2321,
    land_cost_per_acre_0,
    np,
    pd,
    prettify,
    reactor_data_read,
    reactor_type_1,
    update_high_level_costs,
):
    def add_BOP_RP_grades(Reactor_data_updated_1, RB_grade_0, BOP_grade_0, power):
        RB_grade = RB_grade_0
        BOP_grade = BOP_grade_0
        db = pd.DataFrame()
        db = Reactor_data_updated_1[['Account', 'Title', 'Total Cost (USD)', 'Factory Equipment Cost', 'Site Labor Hours', 'Site Labor Cost', 'Site Material Cost']].copy()
        db.loc[db.Account == 212, 'Site Material Cost'] = None
        db.loc[db.Account == 212, 'Site Labor Cost'] = None
        db.loc[db.Account == 212, 'Site Labor Hours'] = None
        db.loc[db.Account == 212, 'Factory Equipment Cost'] = None
        db.loc[db.Account == 213, 'Site Material Cost'] = None
        db.loc[db.Account == 213, 'Site Labor Cost'] = None
        db.loc[db.Account == 213, 'Site Labor Hours'] = None
        db.loc[db.Account == 213, 'Factory Equipment Cost'] = None
        db.loc[db.Account == 232.1, 'Factory Equipment Cost'] = None
        db.loc[db.Account == 232.1, 'Site Labor Cost'] = None
        db.loc[db.Account == 232.1, 'Site Labor Hours'] = None
        if RB_grade == 'non_nuclear':
            db.loc[db.Account == 212, 'Site Material Cost'] = 0.6 * Reactor_data_updated_1.loc[Reactor_data_updated_1.Account == 212, 'Site Material Cost'].values
            db.loc[db.Account == 212, 'Site Labor Cost'] = 0.6 * Reactor_data_updated_1.loc[Reactor_data_updated_1.Account == 212, 'Site Labor Cost'].values
            db.loc[db.Account == 212, 'Site Labor Hours'] = 0.6 * Reactor_data_updated_1.loc[Reactor_data_updated_1.Account == 212, 'Site Labor Hours'].values
            db.loc[db.Account == 212, 'Factory Equipment Cost'] = 0.6 * Reactor_data_updated_1.loc[Reactor_data_updated_1.Account == 212, 'Factory Equipment Cost'].values
        else:
            db.loc[db.Account == 212, 'Site Material Cost'] = Reactor_data_updated_1.loc[Reactor_data_updated_1.Account == 212, 'Site Material Cost'].values
            db.loc[db.Account == 212, 'Site Labor Cost'] = Reactor_data_updated_1.loc[Reactor_data_updated_1.Account == 212, 'Site Labor Cost'].values
            db.loc[db.Account == 212, 'Site Labor Hours'] = Reactor_data_updated_1.loc[Reactor_data_updated_1.Account == 212, 'Site Labor Hours'].values
            db.loc[db.Account == 212, 'Factory Equipment Cost'] = Reactor_data_updated_1.loc[Reactor_data_updated_1.Account == 212, 'Factory Equipment Cost'].values
        if BOP_grade == 'non_nuclear':
            db.loc[db.Account == 213, 'Site Material Cost'] = 0.6 * Reactor_data_updated_1.loc[Reactor_data_updated_1.Account == 213, 'Site Material Cost'].values
            db.loc[db.Account == 213, 'Site Labor Cost'] = 0.6 * Reactor_data_updated_1.loc[Reactor_data_updated_1.Account == 213, 'Site Labor Cost'].values
            db.loc[db.Account == 213, 'Site Labor Hours'] = 0.6 * Reactor_data_updated_1.loc[Reactor_data_updated_1.Account == 213, 'Site Labor Hours'].values
            db.loc[db.Account == 213, 'Factory Equipment Cost'] = 0.6 * Reactor_data_updated_1.loc[Reactor_data_updated_1.Account == 213, 'Factory Equipment Cost'].values
            db.loc[db.Account == 232.1, 'Factory Equipment Cost'] = 0.6 * Reactor_data_updated_1.loc[Reactor_data_updated_1.Account == 232.1, 'Factory Equipment Cost'].values
            db.loc[db.Account == 232.1, 'Site Labor Hours'] = 0.6 * Reactor_data_updated_1.loc[Reactor_data_updated_1.Account == 232.1, 'Site Labor Hours'].values
            db.loc[db.Account == 232.1, 'Site Labor Cost'] = 0.6 * Reactor_data_updated_1.loc[Reactor_data_updated_1.Account == 232.1, 'Site Labor Cost'].values
        else:
            db.loc[db.Account == 213, 'Site Material Cost'] = Reactor_data_updated_1.loc[Reactor_data_updated_1.Account == 213, 'Site Material Cost'].values
            db.loc[db.Account == 213, 'Site Labor Cost'] = Reactor_data_updated_1.loc[Reactor_data_updated_1.Account == 213, 'Site Labor Cost'].values
            db.loc[db.Account == 213, 'Site Labor Hours'] = Reactor_data_updated_1.loc[Reactor_data_updated_1.Account == 213, 'Site Labor Hours'].values
            db.loc[db.Account == 213, 'Factory Equipment Cost'] = Reactor_data_updated_1.loc[Reactor_data_updated_1.Account == 213, 'Factory Equipment Cost'].values
            db.loc[db.Account == 232.1, 'Factory Equipment Cost'] = Reactor_data_updated_1.loc[Reactor_data_updated_1.Account == 232.1, 'Factory Equipment Cost'].values
            db.loc[db.Account == 232.1, 'Site Labor Hours'] = Reactor_data_updated_1.loc[Reactor_data_updated_1.Account == 232.1, 'Site Labor Hours'].values
            db.loc[db.Account == 232.1, 'Site Labor Cost'] = Reactor_data_updated_1.loc[Reactor_data_updated_1.Account == 232.1, 'Site Labor Cost'].values
        Reactor_data_updated_2 = update_high_level_costs(db, power)
        Reactor_data_updated_2_ = pd.DataFrame()
        Reactor_data_updated_2_ = Reactor_data_updated_2[['Account', 'Title', 'Total Cost (USD)', 'Factory Equipment Cost', 'Site Labor Hours', 'Site Labor Cost', 'Site Material Cost']].copy()
        return Reactor_data_updated_2_
    reactor_data_3 = reactor_data_read(reactor_type_1)[0]
    _reactor_power = reactor_data_read(reactor_type_1)[1]
    _Reactor_data_factory = add_factory_cost(reactor_data_3, _reactor_power, f_22, f_2321)
    _Reactor_data_factory_land_taxes = add_land_cost(_Reactor_data_factory, land_cost_per_acre_0, _reactor_power)
    _Reactor_data_factory_land_taxes_BOP_RP_grades = add_BOP_RP_grades(_Reactor_data_factory_land_taxes, RB_grade_0, BOP_grade_0, _reactor_power)
    Reactor_data_factory_land_taxes_BOP_RP_grades_pretty = prettify(_Reactor_data_factory_land_taxes_BOP_RP_grades, f' The {reactor_type_1} {np.round(_reactor_power / 1000, 1)} MWe Reactor <br> Capital Cost Summary - Factories Cost, land cost, taxes and BOP/RP grades Included  <br> Displaying Direct Cost only<br><br> ', 'no_subsidies')
    Reactor_data_factory_land_taxes_BOP_RP_grades_pretty#.hide(subset=hidden_list1, axis=0)
    return (add_BOP_RP_grades,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Section 3-3 : Bulk Ordering""")
    return


@app.cell
def _(
    BOP_grade_0,
    RB_grade_0,
    add_BOP_RP_grades,
    add_factory_cost,
    add_land_cost,
    f_22,
    f_2321,
    land_cost_per_acre_0,
    np,
    num_orders,
    pd,
    prettify,
    reactor_data_read,
    reactor_type_1,
    update_high_level_costs,
):
    def add_bulk_ordering(Reactor_data_updated_3, num_orders, f_22, f_2321, power):
        db = pd.DataFrame()
        db = Reactor_data_updated_3[['Account', 'Title', 'Total Cost (USD)', 'Factory Equipment Cost', 'Site Labor Hours', 'Site Labor Cost', 'Site Material Cost']].copy()
        lr22 = 0.180234165929142
        lr2321 = 0.260746237204082
        reduction_factor_22 = 0
        reduction_factor_2321 = 0
        for ith_unit in range(1, num_orders + 1):
            reduction_factor_22 = reduction_factor_22 + (1 - lr22) ** np.log2(ith_unit) / num_orders
            reduction_factor_2321 = reduction_factor_2321 + (1 - lr2321) ** np.log2(ith_unit) / num_orders
        for x in [22, 232.1]:
            db.loc[db.Account == x, 'Factory Equipment Cost'] = None
        db.loc[db.Account == 22, 'Factory Equipment Cost'] = reduction_factor_22 * (Reactor_data_updated_3.loc[Reactor_data_updated_3.Account == 22, 'Factory Equipment Cost'] - f_22 / num_orders) + f_22 / num_orders
        db.loc[db.Account == 232.1, 'Factory Equipment Cost'] = reduction_factor_2321 * (Reactor_data_updated_3.loc[Reactor_data_updated_3.Account == 232.1, 'Factory Equipment Cost'] - f_2321 / num_orders) + f_2321 / num_orders
        Reactor_data_updated_4 = update_high_level_costs(db, power)
        Reactor_data_updated_4_ = pd.DataFrame()
        Reactor_data_updated_4_ = Reactor_data_updated_4[['Account', 'Title', 'Total Cost (USD)', 'Factory Equipment Cost', 'Site Labor Hours', 'Site Labor Cost', 'Site Material Cost']].copy()
        return Reactor_data_updated_4_
    reactor_data_4 = reactor_data_read(reactor_type_1)[0]
    _reactor_power = reactor_data_read(reactor_type_1)[1]
    _Reactor_data_factory = add_factory_cost(reactor_data_4, _reactor_power, f_22, f_2321)
    _Reactor_data_factory_land_taxes = add_land_cost(_Reactor_data_factory, land_cost_per_acre_0, _reactor_power)
    _Reactor_data_factory_land_taxes_BOP_RP_grades = add_BOP_RP_grades(_Reactor_data_factory_land_taxes, RB_grade_0, BOP_grade_0, _reactor_power)
    _Reactor_data_factory_land_taxes_BOP_RP_grades_bulkOrder = add_bulk_ordering(_Reactor_data_factory_land_taxes_BOP_RP_grades, num_orders, f_22, f_2321, _reactor_power)
    Reactor_data_factory_land_taxes_BOP_RP_grades_bulkOrder_pretty = prettify(_Reactor_data_factory_land_taxes_BOP_RP_grades_bulkOrder, f' The {reactor_type_1} {np.round(_reactor_power / 1000, 1)} MWe Reactor <br> Capital Cost Summary - Factories Cost, land cost, taxes, BOP/RP grades , bulk ordering Included  <br> Displaying Direct Cost only<br><br> ', 'no_subsidies')
    Reactor_data_factory_land_taxes_BOP_RP_grades_bulkOrder_pretty#.hide(subset=hidden_list1, axis=0)
    return (add_bulk_ordering,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Section 3-4 : Reworking and labor productivity""")
    return


@app.cell
def _(
    BOP_grade_0,
    N_AE,
    N_cons,
    RB_grade_0,
    add_BOP_RP_grades,
    add_bulk_ordering,
    add_factory_cost,
    add_land_cost,
    ae_exp_0,
    ce_exp_0,
    design_completion_0,
    f_22,
    f_2321,
    land_cost_per_acre_0,
    n_th,
    np,
    num_orders,
    pd,
    prettify,
    reactor_data_read,
    reactor_type_1,
    update_high_level_costs,
):
    def add_reworking_productivity(Reactor_data_updated_4, reactor_type, n_th, design_completion_0, ae_exp_0, N_AE, ce_exp_0, N_cons, power):
        if n_th == 1:
            design_completion = design_completion_0
            ae_exp = ae_exp_0
            ce_exp = ce_exp_0
        elif n_th > 1:
            design_completion = 1
            ae_exp = min(ae_exp_0 + 2 / N_AE * (n_th - 1), 2)
            ce_exp = min(ce_exp_0 + 2 / N_cons * (n_th - 1), 2)
        productivity = 0.145 * ce_exp + 0.71
        if reactor_type == 'Concept B':
            reworking_factor = (-0.9 * design_completion + 1.9) * (-0.15 * ae_exp + 1.3) * (-0.15 * ce_exp + 1.3)
        if reactor_type == 'Concept A':
            reworking_factor = (-0.69 * design_completion + 1.69) * (-0.125 * ae_exp + 1.25) * (-0.125 * ce_exp + 1.25)
        db = pd.DataFrame()
        db = Reactor_data_updated_4[['Account', 'Title', 'Total Cost (USD)', 'Factory Equipment Cost', 'Site Labor Hours', 'Site Labor Cost', 'Site Material Cost']].copy()
        for x in [212, 213, '211 plus 214 to 219', 22, 232.1, 233, 24, 26]:
            db.loc[db.Account == x, 'Factory Equipment Cost'] = None
            db.loc[db.Account == x, 'Site Labor Hours'] = None
            db.loc[db.Account == x, 'Site Labor Cost'] = None
            db.loc[db.Account == x, 'Site Material Cost'] = None
        for x in [212, 213, '211 plus 214 to 219', 22, 232.1, 233, 24, 26]:
            db.loc[db.Account == x, 'Factory Equipment Cost'] = Reactor_data_updated_4.loc[Reactor_data_updated_4.Account == x, 'Factory Equipment Cost'].values[0] * reworking_factor
            db.loc[db.Account == x, 'Site Labor Hours'] = Reactor_data_updated_4.loc[Reactor_data_updated_4.Account == x, 'Site Labor Hours'].values[0] * reworking_factor / productivity
            db.loc[db.Account == x, 'Site Labor Cost'] = Reactor_data_updated_4.loc[Reactor_data_updated_4.Account == x, 'Site Labor Cost'].values[0] * reworking_factor / productivity
            db.loc[db.Account == x, 'Site Material Cost'] = Reactor_data_updated_4.loc[Reactor_data_updated_4.Account == x, 'Site Material Cost'].values[0] * reworking_factor
        Reactor_data_updated_5 = update_high_level_costs(db, power)
        Reactor_data_updated_5_ = pd.DataFrame()
        Reactor_data_updated_5_ = Reactor_data_updated_5[['Account', 'Title', 'Total Cost (USD)', 'Factory Equipment Cost', 'Site Labor Hours', 'Site Labor Cost', 'Site Material Cost']].copy()
        return Reactor_data_updated_5_
    reactor_data_5 = reactor_data_read(reactor_type_1)[0]
    _reactor_power = reactor_data_read(reactor_type_1)[1]
    _Reactor_data_factory = add_factory_cost(reactor_data_5, _reactor_power, f_22, f_2321)
    _Reactor_data_factory_land_taxes = add_land_cost(_Reactor_data_factory, land_cost_per_acre_0, _reactor_power)
    _Reactor_data_factory_land_taxes_BOP_RP_grades = add_BOP_RP_grades(_Reactor_data_factory_land_taxes, RB_grade_0, BOP_grade_0, _reactor_power)
    _Reactor_data_factory_land_taxes_BOP_RP_grades_bulkOrder = add_bulk_ordering(_Reactor_data_factory_land_taxes_BOP_RP_grades, num_orders, f_22, f_2321, _reactor_power)
    Reactor_data_factory_land_taxes_BOP_RP_grades_bulkOrder_rework_productivity = add_reworking_productivity(_Reactor_data_factory_land_taxes_BOP_RP_grades_bulkOrder, reactor_type_1, n_th, design_completion_0, ae_exp_0, N_AE, ce_exp_0, N_cons, _reactor_power)
    Reactor_data_factory_land_taxes_BOP_RP_grades_bulkOrder_rework_productivity_pretty = prettify(Reactor_data_factory_land_taxes_BOP_RP_grades_bulkOrder_rework_productivity, f' The {reactor_type_1} {np.round(_reactor_power / 1000, 1)} MWe Reactor Capital Cost Summary <br> Factories Cost, land cost, taxes, BOP/RP grades , bulk ordering, reworking and productivity Included  <br> Displaying Direct Cost only<br><br> ', 'no_subsidies')
    Reactor_data_factory_land_taxes_BOP_RP_grades_bulkOrder_rework_productivity_pretty#.hide(subset=hidden_list1, axis=0)
    return (add_reworking_productivity,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""#### Combine the previous functions in one function""")
    return


@app.cell
def _(
    BOP_grade_0,
    N_AE,
    N_cons,
    RB_grade_0,
    add_BOP_RP_grades,
    add_bulk_ordering,
    add_factory_cost,
    add_land_cost,
    add_reworking_productivity,
    ae_exp_0,
    ce_exp_0,
    design_completion_0,
    f_22,
    f_2321,
    land_cost_per_acre_0,
    n_th,
    np,
    num_orders,
    prettify,
    reactor_data_read,
    reactor_type_1,
):
    def update_direct_cost(reactor_type, n_th, f_22, f_2321, land_cost_per_acre_0, RB_grade_0, BOP_grade_0, num_orders, design_completion_0, ae_exp_0, N_AE, ce_exp_0, N_cons):
        reactor_data = reactor_data_read(reactor_type)[0]
        _reactor_power = reactor_data_read(reactor_type)[1]
        _Reactor_data_factory = add_factory_cost(reactor_data, _reactor_power, f_22, f_2321)
        _Reactor_data_factory_land_taxes = add_land_cost(_Reactor_data_factory, land_cost_per_acre_0, _reactor_power)
        _Reactor_data_factory_land_taxes_BOP_RP_grades = add_BOP_RP_grades(_Reactor_data_factory_land_taxes, RB_grade_0, BOP_grade_0, _reactor_power)
        _Reactor_data_factory_land_taxes_BOP_RP_grades_bulkOrder = add_bulk_ordering(_Reactor_data_factory_land_taxes_BOP_RP_grades, num_orders, f_22, f_2321, _reactor_power)
        Reactor_data_factory_land_taxes_BOP_RP_grades_bulkOrder_rework_productivity = add_reworking_productivity(_Reactor_data_factory_land_taxes_BOP_RP_grades_bulkOrder, reactor_type, n_th, design_completion_0, ae_exp_0, N_AE, ce_exp_0, N_cons, _reactor_power)
        return Reactor_data_factory_land_taxes_BOP_RP_grades_bulkOrder_rework_productivity
    reactor_data_6 = reactor_data_read(reactor_type_1)[0]
    _reactor_power = reactor_data_read(reactor_type_1)[1]
    _direct_cost_updated = update_direct_cost(reactor_type_1, n_th, f_22, f_2321, land_cost_per_acre_0, RB_grade_0, BOP_grade_0, num_orders, design_completion_0, ae_exp_0, N_AE, ce_exp_0, N_cons)
    direct_cost_updated_pretty = prettify(_direct_cost_updated, f' The {reactor_type_1} {np.round(_reactor_power / 1000, 1)} MWe Reactor <br> Capital Cost Summary - Direct Cost Updated <br><br> ', 'no_subsidies')
    direct_cost_updated_pretty#.hide(subset=hidden_list1, axis=0)
    return reactor_data_6, update_direct_cost


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Section 3-5 :Update construction duration from labor hours""")
    return


@app.cell
def _(
    BOP_grade_0,
    N_AE,
    N_cons,
    RB_grade_0,
    ae_exp_0,
    ce_exp_0,
    design_completion_0,
    f_22,
    f_2321,
    land_cost_per_acre_0,
    mod_0,
    n_th,
    num_orders,
    reactor_data_6,
    reactor_type_1,
    update_direct_cost,
):
    def update_cons_dur(Reactor_data_0, db, mod_0):
        sum_old_lab_hrs = Reactor_data_0.loc[Reactor_data_0.Account == 21, 'Site Labor Hours'].values + Reactor_data_0.loc[Reactor_data_0.Account == 22, 'Site Labor Hours'].values + Reactor_data_0.loc[Reactor_data_0.Account == 23, 'Site Labor Hours'].values + Reactor_data_0.loc[Reactor_data_0.Account == 24, 'Site Labor Hours'].values + Reactor_data_0.loc[Reactor_data_0.Account == 26, 'Site Labor Hours'].values
        sum_new_lab_hrs = db.loc[db.Account == 21, 'Site Labor Hours'].values + db.loc[db.Account == 22, 'Site Labor Hours'].values + db.loc[db.Account == 23, 'Site Labor Hours'].values + db.loc[db.Account == 24, 'Site Labor Hours'].values + db.loc[db.Account == 26, 'Site Labor Hours'].values
        labor_hour_ratio = sum_new_lab_hrs / sum_old_lab_hrs
        labor_hour_ratio
        mod = mod_0
        if mod == 'stick_built':
            mod_factor = 0.8
        elif mod == 'modularized':
            mod_factor = 1
        if reactor_type_1 == 'Concept B':
            baseline_construction_duration = 64 / mod_factor
        elif reactor_type_1 == 'Concept A':
            baseline_construction_duration = 100 / mod_factor
        actual_construction_duration = baseline_construction_duration * (0.3 * labor_hour_ratio + 0.7)
        return actual_construction_duration
    _direct_cost_updated = update_direct_cost(reactor_type_1, n_th, f_22, f_2321, land_cost_per_acre_0, RB_grade_0, BOP_grade_0, num_orders, design_completion_0, ae_exp_0, N_AE, ce_exp_0, N_cons)
    _act_con_duration = update_cons_dur(reactor_data_6, _direct_cost_updated, mod_0)
    return (update_cons_dur,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Section 3-6 Learning by doing effect on the cost""")
    return


@app.cell
def _(
    BOP_grade_0,
    N_AE,
    N_cons,
    RB_grade_0,
    ae_exp_0,
    ce_exp_0,
    design_completion_0,
    f_22,
    f_2321,
    land_cost_per_acre_0,
    n_th,
    np,
    num_orders,
    pd,
    prettify,
    reactor_data_read,
    reactor_type_1,
    standardization_0,
    update_direct_cost,
    update_high_level_costs,
):
    def learning_effect(Reactor_data_updated_5, n_th, standardization_0, power):
        if n_th == 1:
            standardization = 0.7
        elif n_th > 1:
            standardization = standardization_0
        fitted_LR = pd.DataFrame()
        fitted_LR.loc[:, 'Account'] = Reactor_data_updated_5.loc[:, 'Account']
        fitted_LR.loc[:, 'Title'] = Reactor_data_updated_5.loc[:, 'Title']
        fitted_LR = fitted_LR.loc[fitted_LR['Account'].isin([212, 213, '211 plus 214 to 219', 22, 232.1, 233, 24, 26])]
        fitted_LR['Mat LR'] = np.array([0.099588665391, 0.099588665391, 0.099588665391, 0.080817992281, 0.0, 0.099588665391, 0.099588665391, 0.099588665391]) * standardization / 0.7
        fitted_LR['Lab LR'] = np.array([0.180678729399, 0.180678729399, 0.180678729399, 0.146555539499, 0.137148574884, 0.180678729399, 0.180678729399, 0.180678729399]) * standardization / 0.7
        db = pd.DataFrame()
        db = Reactor_data_updated_5[['Account', 'Title', 'Total Cost (USD)', 'Factory Equipment Cost', 'Site Labor Hours', 'Site Labor Cost', 'Site Material Cost']].copy()
        for x in [212, 213, '211 plus 214 to 219', 22, 232.1, 233, 24, 26]:
            db.loc[db.Account == x, 'Site Labor Hours'] = None
            db.loc[db.Account == x, 'Site Labor Cost'] = None
            db.loc[db.Account == x, 'Site Material Cost'] = None
        for x in [212, 213, '211 plus 214 to 219', 22, 232.1, 233, 24, 26]:
            mat_cost_reduction_multiplier = (1 - fitted_LR.loc[fitted_LR.Account == x, 'Mat LR'].values[0]) ** np.log2(n_th)
            lab_cost_reduction_multiplier = (1 - fitted_LR.loc[fitted_LR.Account == x, 'Lab LR'].values[0]) ** np.log2(n_th)
            db.loc[db.Account == x, 'Site Material Cost'] = Reactor_data_updated_5.loc[Reactor_data_updated_5.Account == x, 'Site Material Cost'] * mat_cost_reduction_multiplier
            db.loc[db.Account == x, 'Site Labor Hours'] = Reactor_data_updated_5.loc[Reactor_data_updated_5.Account == x, 'Site Labor Hours'] * lab_cost_reduction_multiplier
            db.loc[db.Account == x, 'Site Labor Cost'] = Reactor_data_updated_5.loc[Reactor_data_updated_5.Account == x, 'Site Labor Cost'] * lab_cost_reduction_multiplier
        Reactor_data_updated_6 = update_high_level_costs(db, power)
        Reactor_data_updated_6_ = pd.DataFrame()
        Reactor_data_updated_6_ = Reactor_data_updated_6[['Account', 'Title', 'Total Cost (USD)', 'Factory Equipment Cost', 'Site Labor Hours', 'Site Labor Cost', 'Site Material Cost']].copy()
        return Reactor_data_updated_6_
    _reactor_power = reactor_data_read(reactor_type_1)[1]
    _direct_cost_updated = update_direct_cost(reactor_type_1, n_th, f_22, f_2321, land_cost_per_acre_0, RB_grade_0, BOP_grade_0, num_orders, design_completion_0, ae_exp_0, N_AE, ce_exp_0, N_cons)
    _direct_cost_updated_plus_learning = learning_effect(_direct_cost_updated, n_th, standardization_0, _reactor_power)
    direct_cost_updated_plus_learning_pretty = prettify(_direct_cost_updated_plus_learning, f' The {reactor_type_1} {np.round(_reactor_power / 1000, 1)} MWe Reactor <br> Capital Cost Summary - Direct Cost Updated plus learning effect <br> Displaying Direct Cost only<br><br> ', 'no_subsidies')
    direct_cost_updated_plus_learning_pretty#.hide(subset=hidden_list1, axis=0)
    return (learning_effect,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Section 3-7 supply chain delays""")
    return


@app.cell
def _(
    BOP_grade_0,
    Design_Maturity_0,
    N_AE,
    N_cons,
    N_proc,
    RB_grade_0,
    ae_exp_0,
    ce_exp_0,
    design_completion_0,
    f_22,
    f_2321,
    land_cost_per_acre_0,
    mod_0,
    n_th,
    num_orders,
    proc_exp_0,
    reactor_data_read,
    reactor_type_1,
    update_cons_dur,
    update_direct_cost,
):
    def act_cons_duration_plus_delay(reactor_type, n_th, Design_Maturity_0, proc_exp_0, N_proc, cons_duration_no_delay):
        if n_th == 1:
            Design_Maturity = Design_Maturity_0
            proc_exp = proc_exp_0
        elif n_th > 1:
            Design_Maturity = 2
            proc_exp = min(proc_exp_0 + 2 / N_proc * (n_th - 1), 2)
        if reactor_type == 'Concept B':
            task_length_multiplier = 1
            ref_construction_duration = 64
        elif reactor_type == 'Concept A':
            task_length_multiplier = 100 / 64
            ref_construction_duration = 100
        B_21 = 42.1 * task_length_multiplier
        B_22 = 60.2 * task_length_multiplier
        B_23 = 14.8 * task_length_multiplier
        B_24 = 3.6 * task_length_multiplier
        B_25 = 10.1 * task_length_multiplier
        B_26 = 43.9 * task_length_multiplier
        D_21 = -6 * Design_Maturity - 3 * proc_exp + 18
        D_22 = -6 * Design_Maturity - 3 * proc_exp + 18
        D_23 = -6 * Design_Maturity - 3 * proc_exp + 18
        D_24 = -6 * Design_Maturity - 3 * proc_exp + 18
        D_25 = -6 * Design_Maturity - 3 * proc_exp + 18
        D_26 = -6 * Design_Maturity - 3 * proc_exp + 18
        T_21 = B_21 + D_21
        T_22 = 0.09 * (B_21 + D_21) + B_22 + D_22
        T_23 = 0.24 * (B_21 + D_21) + B_23 + D_23
        T_24 = 0.24 * (B_21 + D_21) + 0.34 * (B_23 + D_23) + B_24 + D_24
        T_25 = 0.18 * (B_21 + D_21) + B_25 + D_25
        T_26 = 0.21 * (B_21 + D_21) + B_26 + D_26
        T_end = max(T_21, T_22, T_23, T_24, T_25, T_26)
        supply_chain_delay = max(T_end - ref_construction_duration, 0)
        actual_construction_duration_plus_delay = cons_duration_no_delay + supply_chain_delay
        return actual_construction_duration_plus_delay
    reactor_data_7 = reactor_data_read(reactor_type_1)[0]
    _reactor_power = reactor_data_read(reactor_type_1)[1]
    _direct_cost_updated = update_direct_cost(reactor_type_1, n_th, f_22, f_2321, land_cost_per_acre_0, RB_grade_0, BOP_grade_0, num_orders, design_completion_0, ae_exp_0, N_AE, ce_exp_0, N_cons)
    _act_con_duration = update_cons_dur(reactor_data_7, _direct_cost_updated, mod_0)
    _cons_duration_plus_delay = act_cons_duration_plus_delay(reactor_type_1, n_th, Design_Maturity_0, proc_exp_0, N_proc, _act_con_duration)
    return (act_cons_duration_plus_delay,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Section 3-8 Learning by doing effect on the construction duration""")
    return


@app.cell
def _(
    BOP_grade_0,
    Design_Maturity_0,
    N_AE,
    N_cons,
    N_proc,
    RB_grade_0,
    act_cons_duration_plus_delay,
    ae_exp_0,
    ce_exp_0,
    design_completion_0,
    f_22,
    f_2321,
    land_cost_per_acre_0,
    mod_0,
    n_th,
    np,
    num_orders,
    proc_exp_0,
    reactor_data_read,
    reactor_type_1,
    standardization_0,
    update_cons_dur,
    update_direct_cost,
):
    def duration_learning_effect(n_th, standardization_0, actual_construction_duration_plus_delay):
        if n_th == 1:
            standardization = 0.7
        elif n_th > 1:
            standardization = standardization_0
        fitted_LR_duration = 0.15 * standardization / 0.7
        duration_multiplier = (1 - fitted_LR_duration) ** np.log2(n_th)
        _final_construction_duration = duration_multiplier * actual_construction_duration_plus_delay
        return _final_construction_duration
    reactor_data_8 = reactor_data_read(reactor_type_1)[0]
    _reactor_power = reactor_data_read(reactor_type_1)[1]
    _direct_cost_updated = update_direct_cost(reactor_type_1, n_th, f_22, f_2321, land_cost_per_acre_0, RB_grade_0, BOP_grade_0, num_orders, design_completion_0, ae_exp_0, N_AE, ce_exp_0, N_cons)
    _act_con_duration = update_cons_dur(reactor_data_8, _direct_cost_updated, mod_0)
    _cons_duration_plus_delay = act_cons_duration_plus_delay(reactor_type_1, n_th, Design_Maturity_0, proc_exp_0, N_proc, _act_con_duration)
    _final_con_duration = duration_learning_effect(n_th, standardization_0, _cons_duration_plus_delay)
    return (duration_learning_effect,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Section 3-9 Calculate the Indirect Cost and the standardization impact""")
    return


@app.cell
def _(
    BOP_grade_0,
    Design_Maturity_0,
    N_AE,
    N_cons,
    N_proc,
    RB_grade_0,
    act_cons_duration_plus_delay,
    ae_exp_0,
    ce_exp_0,
    design_completion_0,
    duration_learning_effect,
    f_22,
    f_2321,
    land_cost_per_acre_0,
    learning_effect,
    mod_0,
    n_th,
    np,
    num_orders,
    pd,
    prettify,
    proc_exp_0,
    reactor_data_read,
    reactor_type_1,
    standardization_0,
    update_cons_dur,
    update_direct_cost,
    update_high_level_costs,
):
    def update_indirect_cost(n_th, standardization_0, Reactor_data_updated_6, final_construction_duration, power):
        if n_th == 1:
            standardization = 0.7
        elif n_th > 1:
            standardization = standardization_0
        factor_35 = -3.33 * standardization + 3.331
        db = pd.DataFrame()
        db = Reactor_data_updated_6[['Account', 'Title', 'Total Cost (USD)', 'Factory Equipment Cost', 'Site Labor Hours', 'Site Labor Cost', 'Site Material Cost']].copy()
        for x in [31, 32, 33, 34, 35]:
            db.loc[db.Account == x, 'Total Cost (USD)'] = None
        sum_new_mat_cost = 0
        sum_new_lab_cost = 0
        sum_new_lab_hrs = 0
        for x in [21, 22, 23, 24, 26]:
            sum_new_mat_cost = sum_new_mat_cost + db.loc[db.Account == x, 'Site Material Cost'].values
            sum_new_lab_cost = sum_new_lab_cost + db.loc[db.Account == x, 'Site Labor Cost'].values
            sum_new_lab_hrs = sum_new_lab_hrs + db.loc[db.Account == x, 'Site Labor Hours'].values
        db.loc[db.Account == 31, 'Total Cost (USD)'] = sum_new_mat_cost * 0.785 * sum_new_lab_hrs / final_construction_duration / 160 / 1058 + sum_new_lab_cost * 0.36
        db.loc[db.Account == 32, 'Total Cost (USD)'] = sum_new_lab_cost * 0.36 * 3.661 * final_construction_duration / 72
        db.loc[db.Account == 33, 'Total Cost (USD)'] = 0.042 * db.loc[db.Account == 32, 'Total Cost (USD)'].values[0]
        db.loc[db.Account == 34, 'Total Cost (USD)'] = 0.0035 * db.loc[db.Account == 32, 'Total Cost (USD)'].values[0]
        db.loc[db.Account == 35, 'Total Cost (USD)'] = 0.27 * db.loc[db.Account == 32, 'Total Cost (USD)'].values[0] * factor_35
        Reactor_data_updated_7 = update_high_level_costs(db, power)
        Reactor_data_updated_7_ = pd.DataFrame()
        Reactor_data_updated_7_ = Reactor_data_updated_7[['Account', 'Title', 'Total Cost (USD)', 'Factory Equipment Cost', 'Site Labor Hours', 'Site Labor Cost', 'Site Material Cost']].copy()
        return Reactor_data_updated_7_
    reactor_data_9 = reactor_data_read(reactor_type_1)[0]
    _reactor_power = reactor_data_read(reactor_type_1)[1]
    _direct_cost_updated = update_direct_cost(reactor_type_1, n_th, f_22, f_2321, land_cost_per_acre_0, RB_grade_0, BOP_grade_0, num_orders, design_completion_0, ae_exp_0, N_AE, ce_exp_0, N_cons)
    _act_con_duration = update_cons_dur(reactor_data_9, _direct_cost_updated, mod_0)
    _cons_duration_plus_delay = act_cons_duration_plus_delay(reactor_type_1, n_th, Design_Maturity_0, proc_exp_0, N_proc, _act_con_duration)
    _final_con_duration = duration_learning_effect(n_th, standardization_0, _cons_duration_plus_delay)
    _direct_cost_updated_plus_learning = learning_effect(_direct_cost_updated, n_th, standardization_0, _reactor_power)
    direct_cost_updated_plus_learning_with_indirect_cost = update_indirect_cost(n_th, standardization_0, _direct_cost_updated_plus_learning, _final_con_duration, _reactor_power)
    direct_cost_updated_plus_learning_with_indirect_cost_pretty = prettify(direct_cost_updated_plus_learning_with_indirect_cost, f' The {reactor_type_1} {np.round(_reactor_power / 1000, 1)} MWe Reactor <br> Capital Cost Summary - Base Cost updated (Direct and Indirect costs) <br><br> ', 'no_subsidies')
    #list3 = list(range(38, 69))
    #hidden_list3 = list1 + list3
    direct_cost_updated_plus_learning_with_indirect_cost_pretty#.hide(subset=hidden_list3, axis=0)
    return (update_indirect_cost,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""#### Combine the previous functions in one function""")
    return


@app.cell
def _(
    act_cons_duration_plus_delay,
    duration_learning_effect,
    learning_effect,
    reactor_data_read,
    update_cons_dur,
    update_direct_cost,
    update_indirect_cost,
):
    def calculate_base_cost(reactor_type, n_th, f_22, f_2321, land_cost_per_acre_0, RB_grade_0, BOP_grade_0, num_orders, design_completion_0, ae_exp_0, N_AE, ce_exp_0, N_cons, mod_0, Design_Maturity_0, proc_exp_0, N_proc, standardization_0):
        reactor_data = reactor_data_read(reactor_type)[0]
        _reactor_power = reactor_data_read(reactor_type)[1]
        _direct_cost_updated = update_direct_cost(reactor_type, n_th, f_22, f_2321, land_cost_per_acre_0, RB_grade_0, BOP_grade_0, num_orders, design_completion_0, ae_exp_0, N_AE, ce_exp_0, N_cons)
        _act_con_duration = update_cons_dur(reactor_data, _direct_cost_updated, mod_0)
        _cons_duration_plus_delay = act_cons_duration_plus_delay(reactor_type, n_th, Design_Maturity_0, proc_exp_0, N_proc, _act_con_duration)
        _final_con_duration = duration_learning_effect(n_th, standardization_0, _cons_duration_plus_delay)
        _direct_cost_updated_plus_learning = learning_effect(_direct_cost_updated, n_th, standardization_0, _reactor_power)
        direct_cost_updated_plus_learning_with_indirect_cost = update_indirect_cost(n_th, standardization_0, _direct_cost_updated_plus_learning, _final_con_duration, _reactor_power)
        return (direct_cost_updated_plus_learning_with_indirect_cost, _final_con_duration)
    return (calculate_base_cost,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Section 3-10 :  Insurance""")
    return


@app.cell
def _(
    BOP_grade_0,
    Design_Maturity_0,
    N_AE,
    N_cons,
    N_proc,
    RB_grade_0,
    ae_exp_0,
    calculate_base_cost,
    ce_exp_0,
    design_completion_0,
    f_22,
    f_2321,
    land_cost_per_acre_0,
    mod_0,
    n_th,
    np,
    num_orders,
    pd,
    prettify,
    proc_exp_0,
    reactor_data_read,
    reactor_type_1,
    standardization_0,
    update_high_level_costs,
):
    def insurance_cost_update(Reactor_data_0, Reactor_data_updated_7, power):
        db = pd.DataFrame()
        db = Reactor_data_updated_7[['Account', 'Title', 'Total Cost (USD)', 'Factory Equipment Cost', 'Site Labor Hours', 'Site Labor Cost', 'Site Material Cost']].copy()
        db0 = Reactor_data_0
        db.loc[db.Account == 52, 'Total Cost (USD)'] = None
        change_in_insuance_cost = (db.loc[db.Title == '20s - Subtotal', 'Total Cost (USD)'].values + db.loc[db.Title == '30s - Subtotal', 'Total Cost (USD)'].values) / (db0.loc[db0.Title == '20s - Subtotal', 'Total Cost (USD)'].values + db0.loc[db0.Title == '30s - Subtotal', 'Total Cost (USD)'].values)
        db.loc[db.Account == 52, 'Total Cost (USD)'] = change_in_insuance_cost[0] * Reactor_data_updated_7.loc[db.Account == 52, 'Total Cost (USD)']
        Reactor_data_updated_8 = update_high_level_costs(db, power)
        Reactor_data_updated_8_ = pd.DataFrame()
        Reactor_data_updated_8_ = Reactor_data_updated_8[['Account', 'Title', 'Total Cost (USD)', 'Factory Equipment Cost', 'Site Labor Hours', 'Site Labor Cost', 'Site Material Cost']].copy()
        return Reactor_data_updated_8_
    reactor_data_10 = reactor_data_read(reactor_type_1)[0]
    _reactor_power = reactor_data_read(reactor_type_1)[1]
    _tot_base_cost = calculate_base_cost(reactor_type_1, n_th, f_22, f_2321, land_cost_per_acre_0, RB_grade_0, BOP_grade_0, num_orders, design_completion_0, ae_exp_0, N_AE, ce_exp_0, N_cons, mod_0, Design_Maturity_0, proc_exp_0, N_proc, standardization_0)[0]
    _tot_base_cost_wz_insurance = insurance_cost_update(reactor_data_10, _tot_base_cost, _reactor_power)
    tot_base_cost_wz_insurance_pretty = prettify(_tot_base_cost_wz_insurance, f' The {reactor_type_1} {np.round(_reactor_power / 1000, 1)} MWe Reactor <br> Capital Cost Summary - Base Cost updated (Direct and Indirect costs) plus insurance <br><br> ', 'no_subsidies')
    #list4 = list(range(46, 69))
    #hidden_list4 = list1 + list4
    tot_base_cost_wz_insurance_pretty#.hide(subset=hidden_list4, axis=0)
    return (insurance_cost_update,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Section 3-11 :  Interest""")
    return


@app.cell
def _(
    BOP_grade_0,
    Design_Maturity_0,
    N_AE,
    N_cons,
    N_proc,
    RB_grade_0,
    ae_exp_0,
    calculate_base_cost,
    ce_exp_0,
    design_completion_0,
    f_22,
    f_2321,
    insurance_cost_update,
    interest_rate_0,
    land_cost_per_acre_0,
    mod_0,
    n_th,
    np,
    num_orders,
    pd,
    prettify,
    proc_exp_0,
    reactor_data_read,
    reactor_type_1,
    standardization_0,
    startup_0,
    update_high_level_costs,
):
    def update_interest_cost(Reactor_data_updated_8, final_construction_duration, interest_rate, startup_0, n_th, power):
        sp = pd.read_excel('Cost_Reduction\conceptb-inputs.xlsx', sheet_name='Ref Spending Curve', usecols='A : D')
        Months = sp['Month'].tolist()
        CDFs = sp['CDF'].tolist()
        annual_periods = np.linspace(12, 12 * int(final_construction_duration / 12), int(final_construction_duration / 12))
        if max(annual_periods) < int(final_construction_duration) - 1:
            annual_periods_1 = np.append(annual_periods, final_construction_duration - 1)
        else:
            annual_periods_1 = annual_periods
        annual_cum_spend = []
        for period in annual_periods_1:
            new_period = 103 * period / int(final_construction_duration)
            annual_cum_spend.append(np.interp(new_period, Months, CDFs))
        annual_cum_spend1 = np.append(annual_cum_spend[0], np.diff(annual_cum_spend))
        tot_overnight_cost = Reactor_data_updated_8.loc[Reactor_data_updated_8.Title == 'Total Overnight Cost (Accounts 10 to 50)', 'Total Cost (USD)'].values[0]
        annual_loan_add = annual_cum_spend1 * tot_overnight_cost
        interest_exp = (1 + interest_rate) ** ((final_construction_duration - annual_periods_1) / 12) * annual_loan_add - annual_loan_add
        tot_int_exp_construction = sum(interest_exp)
        if n_th == 1:
            startup = startup_0
        elif n_th > 1:
            startup = max(7, startup_0 * (1 - 0.3) ** np.log2(n_th))
        int_exp_startup = (tot_int_exp_construction + tot_overnight_cost) * (1 + interest_rate) ** (startup / 12) - (tot_int_exp_construction + tot_overnight_cost)
        db = pd.DataFrame()
        db = Reactor_data_updated_8[['Account', 'Title', 'Total Cost (USD)', 'Factory Equipment Cost', 'Site Labor Hours', 'Site Labor Cost', 'Site Material Cost']].copy()
        db.loc[db.Account == 62, 'Total Cost (USD)'] = None
        db.loc[db.Account == 62, 'Total Cost (USD)'] = int_exp_startup + tot_int_exp_construction
        Reactor_data_updated_9 = update_high_level_costs(db, power)
        Reactor_data_updated_9_ = pd.DataFrame()
        Reactor_data_updated_9_ = Reactor_data_updated_9[['Account', 'Title', 'Total Cost (USD)', 'Factory Equipment Cost', 'Site Labor Hours', 'Site Labor Cost', 'Site Material Cost']].copy()
        tot_cap_investment = Reactor_data_updated_9.loc[Reactor_data_updated_9.Title == 'Total Capital Investment Cost (All Accounts)', 'Total Cost (USD)'].values
        return (Reactor_data_updated_9_, tot_overnight_cost, tot_cap_investment)
    reactor_data_11 = reactor_data_read(reactor_type_1)[0]
    _reactor_power = reactor_data_read(reactor_type_1)[1]
    _tot_base_cost_results = calculate_base_cost(reactor_type_1, n_th, f_22, f_2321, land_cost_per_acre_0, RB_grade_0, BOP_grade_0, num_orders, design_completion_0, ae_exp_0, N_AE, ce_exp_0, N_cons, mod_0, Design_Maturity_0, proc_exp_0, N_proc, standardization_0)
    _tot_base_cost = _tot_base_cost_results[0]
    final_construction_duration = _tot_base_cost_results[1]
    _tot_base_cost_wz_insurance = insurance_cost_update(reactor_data_11, _tot_base_cost, _reactor_power)
    _tot_base_cost_wz_insurance_interest = update_interest_cost(_tot_base_cost_wz_insurance, final_construction_duration, interest_rate_0, startup_0, n_th, _reactor_power)[0]
    tot_base_cost_wz_insurance_interest_pretty = prettify(_tot_base_cost_wz_insurance_interest, f' The {reactor_type_1} {np.round(_reactor_power / 1000, 1)} MWe Reactor <br> Capital Cost Summary - Base Cost updated (Direct and Indirect costs) plus insurance and interest <br><br> ', 'no_subsidies')
    tot_base_cost_wz_insurance_interest_pretty
    return (update_interest_cost,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""### Section 3 - 12 :  ITC Subsidies""")
    return


@app.cell
def _(
    BOP_grade_0,
    Design_Maturity_0,
    ITC_0,
    ITC_reduction_factor,
    N_AE,
    N_cons,
    N_proc,
    RB_grade_0,
    ae_exp_0,
    calculate_base_cost,
    ce_exp_0,
    design_completion_0,
    f_22,
    f_2321,
    insurance_cost_update,
    interest_rate_0,
    land_cost_per_acre_0,
    mod_0,
    n_ITC,
    n_th,
    np,
    num_orders,
    pd,
    prettify,
    proc_exp_0,
    reactor_data_read,
    reactor_type_1,
    standardization_0,
    startup_0,
    update_high_level_costs,
    update_interest_cost,
):
    def update_itc(Reactor_data_updated_9, tot_overnight_cost, tot_cap_investment, n_th, ITC_0, n_ITC, reactor_power):
        if n_th <= n_ITC:
            ITC = ITC_0
        else:
            ITC = 0
        db1 = pd.DataFrame()
        db1 = Reactor_data_updated_9[['Account', 'Title', 'Total Cost (USD)', 'Factory Equipment Cost', 'Site Labor Hours', 'Site Labor Cost', 'Site Material Cost']].copy()
        ITC_cost_reduction_factor = ITC_reduction_factor(ITC)
        ITC_reduced_OCC = tot_overnight_cost * ITC_cost_reduction_factor
        OCC_cost_reduction_due_to_TCI = tot_overnight_cost - ITC_reduced_OCC
        db1.loc[db1.Title == 'Total Overnight Cost - ITC reduced', 'Total Cost (USD)'] = None
        db1.loc[db1.Title == 'Total Overnight Cost -ITC reduced (US$/kWe)', 'Total Cost (USD)'] = None
        db1.loc[db1.Title == 'Total Capital Investment Cost - ITC reduced', 'Total Cost (USD)'] = None
        db1.loc[db1.Title == 'Total Capital Investment Cost - ITC reduced (US$/kWe)', 'Total Cost (USD)'] = None
        db1.loc[db1.Title == 'Total Overnight Cost - ITC reduced', 'Total Cost (USD)'] = ITC_reduced_OCC
        db1.loc[db1.Title == 'Total Overnight Cost -ITC reduced (US$/kWe)', 'Total Cost (USD)'] = ITC_reduced_OCC / reactor_power
        db1.loc[db1.Title == 'Total Capital Investment Cost - ITC reduced', 'Total Cost (USD)'] = tot_cap_investment - OCC_cost_reduction_due_to_TCI
        levelized_NCI = db1.loc[db1.Title == 'Total Capital Investment Cost - ITC reduced', 'Total Cost (USD)'].values[0] / reactor_power
        db1.loc[db1.Title == 'Total Capital Investment Cost - ITC reduced (US$/kWe)', 'Total Cost (USD)'] = levelized_NCI
        Reactor_data_updated_10 = update_high_level_costs(db1, reactor_power)
        Reactor_data_updated_10_ = pd.DataFrame()
        Reactor_data_updated_10_ = Reactor_data_updated_10[['Account', 'Title', 'Total Cost (USD)', 'Factory Equipment Cost', 'Site Labor Hours', 'Site Labor Cost', 'Site Material Cost']].copy()
        return (Reactor_data_updated_10_, ITC_reduced_OCC / reactor_power, levelized_NCI)
    reactor_data_12 = reactor_data_read(reactor_type_1)[0]
    reactor_power = reactor_data_read(reactor_type_1)[1]
    _tot_base_cost_results = calculate_base_cost(reactor_type_1, n_th, f_22, f_2321, land_cost_per_acre_0, RB_grade_0, BOP_grade_0, num_orders, design_completion_0, ae_exp_0, N_AE, ce_exp_0, N_cons, mod_0, Design_Maturity_0, proc_exp_0, N_proc, standardization_0)
    _tot_base_cost = _tot_base_cost_results[0]
    _final_construction_duration = _tot_base_cost_results[1]
    _tot_base_cost_wz_insurance = insurance_cost_update(reactor_data_12, _tot_base_cost, reactor_power)
    tot_base_cost_wz_insurance_interest_results = update_interest_cost(_tot_base_cost_wz_insurance, _final_construction_duration, interest_rate_0, startup_0, n_th, reactor_power)
    _tot_base_cost_wz_insurance_interest = tot_base_cost_wz_insurance_interest_results[0]
    tot_overnight_cost = tot_base_cost_wz_insurance_interest_results[1]
    tot_cap_investment = tot_base_cost_wz_insurance_interest_results[2]
    Final_Result = update_itc(_tot_base_cost_wz_insurance_interest, tot_overnight_cost, tot_cap_investment, n_th, ITC_0, n_ITC, reactor_power)
    Final_Result_COA = Final_Result[0]
    Final_Result_pretty = prettify(Final_Result_COA, f' The {reactor_type_1} {np.round(reactor_power / 1000, 1)} MWe Reactor <br> Capital Cost Summary  <br><br> ', 'subsidies')
    Final_Result_pretty
    return (update_itc,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""#### A Python function to combine all the previous ones""")
    return


@app.cell
def _(
    ITC_0,
    calculate_base_cost,
    insurance_cost_update,
    n_ITC,
    reactor_data_read,
    update_interest_cost,
    update_itc,
):
    def calculate_final_result(reactor_type, n_th, f_22, f_2321, land_cost_per_acre_0, RB_grade_0, BOP_grade_0, num_orders, design_completion_0, ae_exp_0, N_AE, ce_exp_0, N_cons, mod_0, Design_Maturity_0, proc_exp_0, N_proc, standardization_0, interest_rate_0, startup_0):
        reactor_data = reactor_data_read(reactor_type)[0]
        _reactor_power = reactor_data_read(reactor_type)[1]
        _tot_base_cost_results = calculate_base_cost(reactor_type, n_th, f_22, f_2321, land_cost_per_acre_0, RB_grade_0, BOP_grade_0, num_orders, design_completion_0, ae_exp_0, N_AE, ce_exp_0, N_cons, mod_0, Design_Maturity_0, proc_exp_0, N_proc, standardization_0)
        _tot_base_cost = _tot_base_cost_results[0]
        _final_construction_duration = _tot_base_cost_results[1]
        _tot_base_cost_wz_insurance = insurance_cost_update(reactor_data, _tot_base_cost, _reactor_power)
        tot_base_cost_wz_insurance_interest_results = update_interest_cost(_tot_base_cost_wz_insurance, _final_construction_duration, interest_rate_0, startup_0, n_th, _reactor_power)
        _tot_base_cost_wz_insurance_interest = tot_base_cost_wz_insurance_interest_results[0]
        tot_overnight_cost = tot_base_cost_wz_insurance_interest_results[1]
        tot_cap_investment = tot_base_cost_wz_insurance_interest_results[2]
        Final_Result = update_itc(_tot_base_cost_wz_insurance_interest, tot_overnight_cost, tot_cap_investment, n_th, ITC_0, n_ITC, _reactor_power)
        Final_Result_COA = Final_Result[0]
        levelized_net_OCC = Final_Result[1]
        levelized_NCI = Final_Result[2]
        return (Final_Result_COA, levelized_net_OCC, levelized_NCI, _final_construction_duration)
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
