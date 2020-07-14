"""
Created on Mon Jul 13 19:20:15 2020

@author: 12699
"""



class GeneratorPrettyPrinter:

    def getLists(self):
        ''' Returns the list of dictionaries need for Fix prett printer

        Returns
        =======
        master_list: list
                     list of dictionaries in alphabetical order

        '''
        from .FixDictionary import FixDictionary
        T  = ["fixr:codeSets", "fixr:fields", "fixr:components", "fixr:groups", "fixr:messages"]
        master_list = [ ]
        for t in T:
            temp = FixDictionary(t)
            master_list.append(temp.generateDictionary( ))
        return(master_list)
