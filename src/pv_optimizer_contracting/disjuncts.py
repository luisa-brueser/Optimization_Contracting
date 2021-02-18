from pyomo.environ import *
from pyomo.gdp import Disjunct, Disjunction


def create_list_disjuncts(model):
    model.only_contractor_supplies = Disjunct()
    model.only_contractor_supplies.no_grid=Constraint(expr=sum(model.supply[t, 'Grid_Only'] for t in model.time) <= 0)
    model.only_contractor_supplies.no_pv=Constraint(expr=sum(model.supply[t, 'PV'] for t in model.time)  <= 0)
    model.only_contractor_supplies.no_grid_cap=Constraint(expr=model.capacity['Grid_Only'] <= 0)
    model.only_contractor_supplies.no_pv_cap=Constraint(expr=model.capacity['PV']  <= 0)
    
    model.only_grid_supplies = Disjunct()
    model.only_grid_supplies.no_contractor=Constraint(expr=sum(model.supply[t, 'Pv_Contractor'] for t in model.time)<= 0)
    model.only_grid_supplies.no_pv=Constraint(expr=sum(model.supply[t, 'PV'] for t in model.time)<= 0)
    model.only_grid_supplies.no_grid_cap=Constraint(expr=model.capacity['Pv_Contractor'] <= 0)
    model.only_grid_supplies.no_pv_cap=Constraint(expr=model.capacity['PV'] <= 0)


    model.only_pv_supplies = Disjunct()
    model.only_pv_supplies.no_contractor=Constraint(expr=sum(model.supply[t, 'Pv_Contractor'] for t in model.time)<= 0)
    model.only_pv_supplies.no_grid=Constraint(expr=sum(model.supply[t, 'Grid_Only'] for t in model.time)<= 0)
    model.only_pv_supplies.no_grid_cap=Constraint(expr=model.capacity['Pv_Contractor'] <= 0)
    model.only_pv_supplies.no_pv_cap=Constraint(expr=model.capacity['Grid_Only']  <= 0)

    return [model.only_contractor_supplies,model.only_grid_supplies,model.only_pv_supplies]
     



# def create_list_disjuncts(model):

#     def create_contractor_only_disjunct(model):
#         """
#         In case the supply gets delivered exclusively by the contractor, then a constraint that sets the supply from grid and pv to less or equal than zero, for every timeperiod, needs to be applied.
#         """
#         model.only_contractor_supplies = Disjunct()
#         model.only_contractor_supplies.no_grid=Constraint(expr=sum(model.supply[t, "Grid_Only"] for t in model.time)<= 0)
#         model.only_contractor_supplies.no_pv=Constraint(expr=sum(model.supply[t, "PV"] for t in model.time)<= 0)
#         return model.only_contractor_supplies

#     def create_grid_only_disjunct(model):
#         """
#         In case the supply gets delivered exclusively by the grid operator, then a constraint that sets the supply from contractor and pv to less or equal than zero, for every timeperiod, needs to be applied.
#         """
#         model.only_grid_supplies = Disjunct()
#         model.only_grid_supplies.no_contractor=Constraint(expr=sum(model.supply[t, "Pv_Contractor"] for t in model.time)<= 0)
#         model.only_grid_supplies.no_pv=Constraint(expr=sum(model.supply[t, "PV"] for t in model.time)<= 0)
#         return model.only_grid_supplies


#     def create_pv_only_disjunct(model):
#         """
#         In case the supply gets delivered exclusively by the grid operator, then a constraint that sets the supply from contractor and pv to less or equal than zero, for every timeperiod, needs to be applied.
#         """
#         model.only_pv_supplies = Disjunct()
#         model.only_pv_supplies.no_contractor=Constraint(expr=sum(model.supply[t, "Pv_Contractor"] for t in model.time)<= 0)
#         model.only_pv_supplies.no_grid=Constraint(expr=sum(model.supply[t, "Grid_Only"] for t in model.time)<= 0)
#         return model.only_pv_supplies
#     return [model.only_contractor_supplies,model.only_grid_supplies,model.only_pv_supplies]

# list_disjuncts=create_list_disjuncts()
# print(list_disjuncts)
 