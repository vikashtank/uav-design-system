"""
file for athena vortext lattice interface
"""

def create_mass_file(file_name: str, structural_model: "StructuralModel",
                                     properties):

    title_string = """# Plane Name: {0}
Lunit = 1.0 m
Munit = 1.0 kg
Tunit = 1.0 s

g   = {1}
rho = {2}
""".format(structural_model.name,
           properties["gravity"],
           properties["density"])

    mass_string = "\n".join(structural_model.avl_mass_list)
    with open(file_name, "w") as open_file:
        open_file.write(title_string + mass_string)



if __name__ == "__main__":
    pass
