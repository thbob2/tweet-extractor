from owlready2 import *

def ontology_classesNames(onto):
    ontol=get_ontology(onto).load()
    objects=ontol.classes()
    names_list=[]
    for obj in objects: 
        tuple=str(obj).split('.')
        name=tuple[1]
        if("_" in name):
            tuple1=name.split("_")
            name=" ".join(tuple1)
        names_list.append(name)
    return list(set(names_list))

if __name__ == '__main__':
    
    onto = ontology_classesNames(os.getcwd()+"/python/corp/assets/test.owx")
    print(onto)