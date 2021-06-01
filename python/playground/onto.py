from owlready2 import *
import os
onto_path.append(os.getcwd()+"/python/corp/assets/")
onto = get_ontology(os.getcwd()+"/python/corp/assets/techpunsh.owl").load()
objects = onto.classes()
print(onto.get_namespace())
    