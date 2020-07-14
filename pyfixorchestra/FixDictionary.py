# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 09:32:49 2020

@author: Nathanael Judge
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 09:32:49 2020

@author: Nathanael Judge
"""

class FixDictionary:
    """

    Parameters
    ==========
    Type = String
           codeSets, datatypes, fields, components, groups, messages
    """

    version = "1.0"
    def __init__(self, Type:str ):
            self.Type = Type


    def printType(self):
        """ prints the type submitted

        Returns
        =======


        """
        print(self.Type)


    def __checkString(self):
        """ checks if the string is formated correctly.

        Returns
        =======
        Type: string
               Formatted string to be used
        """
        if not self.Type[0:5] == "fixr:":
            self.Type = "fixr:" + self.Type
        return(self.Type)
    def __checkType(self):
        ''' This is a check to make sure the user is generating a legal dictionary and ensures the string is in a good format.

        Returns
        =======
        formatted: String
                   formatted user input to generate the dictionary

        '''
        accepted  = ["fixr:codeSets", "fixr:datatypes", "fixr:fields", "fixr:components", "fixr:groups", "fixr:messages"]
        formatted = self.__checkString()
        if formatted not in accepted:
            print("Formatting needs to be 'fixr:+'")
            print("For example, FixDictionary('fixr:fields')")
            raise Exception("type needs to be one of the 6 accepted")

        return(formatted)
    def getDocumentation(self, D):
        ''' Returns the documentation from a given element

        Returns
        =======
        returns documentation from a given element
        '''
        # this adds
        temp = [ ]
        if 'fixr:documentation' not in D['fixr:annotation'].keys():
            temp.append("No documentation found")
        else:
            d = D['fixr:annotation']['fixr:documentation']
            if type(d) == list:
                check = d[0]
                if '#text' not in check.keys():
                    temp.append("No documentation found")
                else:
                    temp.append(d[0]['#text'])
            elif '#text' in d.keys():
                temp.append(d['#text'])
            else:
                temp.append("No documentation found")
        return(temp)
    def getFieldRef(self, Elem):
        ''' Returns the field tags for field references in other components

        Returns
        =======
        returns field references for a given element
        '''
        temp = [ ]
        if 'fixr:fieldRef' not in Elem.keys( ):
            return([])
        E = Elem['fixr:fieldRef']
        if type(E) != list:
            temp.append(E['@id'])
        else:
            for e in E:
                temp.append(e['@id'])
        return(temp)

    def getComponentRef(self, Elem):
        ''' Returns the component tags for component references in other components

        Returns
        =======
        returns component references for a given element
        '''
        temp = [ ]
        if 'fixr:componentRef' not in Elem.keys( ):
            return([])
        E = Elem['fixr:componentRef']
        if type(E) != list:
            temp.append(E['@id'])
        else:
            for e in E:
                temp.append(e['@id'])
        return(temp)
    def getGroupRef(self, Elem):
        ''' Returns the group tags for group references in other components

        Returns
        =======
        returns group references for a given element
        '''
        temp = [ ]
        if 'fixr:groupRef' not in Elem.keys( ):
            return([])
        E = Elem['fixr:groupRef']
        if type(E) != list:
            temp.append(E['@id'])
        else:
            for e in E:
                temp.append(e['@id'])
        return(temp)
    def getCodeSet(self, Elem):
        ''' Returns the values in a codeSet

        Returns
        =======
        returns values in a code set
        '''
        temp = [ ]
        if 'fixr:code' not in Elem.keys( ):
            return([])
        E = Elem['fixr:code']
        if type(E) != list:
            temp.append(E['@id'])
        else:
            for e in E:
                temp.append(e['@id'])

        return(temp)

    def generateDictionary(self):
        ''' Returns a dictionary of key = ID or name and appropriate values

        Returns
        =======
        dictionary:  dict
                     a dictionary of the aforementioned information

        '''
        name = self.__checkType( )
        import xmltodict
        # get the XML content
        f = open("OrchestraEP257.xml", "r", encoding="utf8")
        # convert to dictionary
        FIX = xmltodict.parse(f.read())
        f.close()
        FIX = FIX['fixr:repository']
        parser = FIX[name][name[0:len(name) - 1]]
        dictionary = {}
        if name == 'fixr:fields':
            for field in parser:
                ID = field['@id']
                name = field['@name']
                documentation = self.getDocumentation(field)
                dictionary[ID] = [name, documentation]
        elif name == 'fixr:components':
            for component in parser:
                ID = component['@id']
                fieldRef = self.getFieldRef(component)
                groupRef = self.getGroupRef(component)
                componentRef = self.getComponentRef(component)
                documentation = self.getDocumentation(component)
                dictionary[ID] = [fieldRef, groupRef, componentRef, documentation]
        elif name == 'fixr:messages':
            for message in parser:
                ID = message['@id']
                fieldRef = self.getFieldRef(message)
                groupRef = self.getGroupRef(message)
                componentRef = self.getComponentRef(message)
                documentation = self.getDocumentation(message)
                dictionary[ID] = [fieldRef, groupRef, componentRef, documentation]
        elif name == 'fixr:codeSets':
            for codeSet in parser:
                ID = codeSet['@id']
                name = codeSet['@name']
                fieldRef = self.getCodeSet(codeSet)
                documentation = self.getDocumentation(codeSet)
                dictionary[ID] = [name, fieldRef, documentation]
        elif name == 'fixr:groups':
            for group in parser:
                ID = group['@id']
                numInGroup = group['fixr:numInGroup']['@id']
                fieldRef = self.getFieldRef(group)
                groupRef = self.getGroupRef(group)
                componentRef = self.getComponentRef(group)
                documentation = self.getDocumentation(group)
                dictionary[ID] = [numInGroup, fieldRef, groupRef, componentRef, documentation]
        elif name == 'fixr:datatypes':
            for datatype in parser:
                name = datatype['@name']
                documentation = self.getDocumentation(datatype)
                dictionary[name] = [documentation]

        return(dictionary)
