from pyomo.environ import *
from pyomo.gdp import Disjunct, Disjunction

def create_disjunction(model):
    '''
    Creates disjuncts for each option, that ensure that supply gets delivered exclusively by the option chosen. 
    If binary variable is True for one option, then the possible capacity of all other options is set to zero.
    '''

    model.number_options = (['Pv_Contractor','Grid_Only','PV'])
    model.number_disjunction = RangeSet(1)
    model.d = Disjunct(model.number_options)
    model.djn = Disjunction(model.number_disjunction)
    model.djn[1] = [model.d['Pv_Contractor'], model.d['Grid_Only'],model.d['PV']]

    model.d['Pv_Contractor'].no_grid = Constraint(expr=model.capacity['Grid_Only'] == 0)
    model.d['Pv_Contractor'].no_pv = Constraint(expr=model.capacity['PV'] == 0)
    #model.d['Pv_Contractor'].pv_area_cap = Constraint(expr=model.capacity['Pv_Contractor'] <= (model.area_roof/model.specific_area_pv))

    model.d['Grid_Only'].no_contracting = Constraint(expr=model.capacity['Pv_Contractor'] == 0)
    model.d['Grid_Only'].no_pv = Constraint(expr=model.capacity['PV'] == 0)

    model.d['PV'].no_contracting = Constraint(expr=model.capacity['Pv_Contractor'] == 0)
    model.d['PV'].no_grid_cap = Constraint(expr=model.capacity['Grid_Only'] == 0)
    #model.d['PV'].pv_area_cap=Constraint(expr=model.capacity['PV'] <= (model.area_roof/model.specific_area_pv))

def create_boolean_var(model):
    model.option_binary_var = BooleanVar(model.number_options)
    for idx in model.option_binary_var:
        model.option_binary_var[idx].associate_binary_var(model.d[idx].indicator_var)
    return model.option_binary_var


def update_boolean_vars_from_binary(model, integer_tolerance=1e-5):
    """Updates all Boolean variables based on the value of their linked binary variables."""
    for boolean_var in model.component_data_objects(BooleanVar, descend_into=(Block, Disjunct)):
        binary_var = boolean_var.get_associated_binary()
        if binary_var is not None and binary_var.value is not None:
            if abs(binary_var.value - 1) <= integer_tolerance:
                boolean_var.value = True
            elif abs(binary_var.value) <= integer_tolerance:
                boolean_var.value = False
            else:
                raise ValueError("Binary variable has non-{0,1} value: %s = %s" % (binary_var.name, binary_var.value))
            boolean_var.stale = binary_var.stale