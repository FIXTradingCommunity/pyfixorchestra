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

import xmltodict
import os

class FixDictionary:
    """

    Parameters
    ==========
    Type = String
           codeSets, datatypes, fields, components, groups, messages
    """

    version = "1.0"
    def __init__(self):
        # dictionary is intially empty, to be populated by read_xml
        self.FIX = {}

    def __checkType(self, name):
        ''' This is a check to make sure the user is generating a legal dictionary

        Returns
        =======
        name: String
                   accepted type

        '''
        accepted  = ["codeSets", "datatypes", "fields", "components", "groups", "messages"]
        if name not in accepted:
                    raise Exception("type not accepted")

        return(name)

    def getDocumentation(self, D):
        ''' Returns the documentation from a given element

        Returns
        =======
        returns documentation from a given element
        '''
        # this adds
        temp = [ ]
        if 'documentation' not in D['annotation'].keys():
            temp.append("No documentation found")
        else:
            d = D['annotation']['documentation']
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
        if 'fieldRef' not in Elem.keys( ):
            return([])
        E = Elem['fieldRef']
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
        if 'componentRef' not in Elem.keys( ):
            return([])
        E = Elem['componentRef']
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
        if 'groupRef' not in Elem.keys( ):
            return([])
        E = Elem['groupRef']
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
        if 'code' not in Elem.keys( ):
            return([])
        E = Elem['code']
        if type(E) != list:
            temp.append(E['@id'])
        else:
            for e in E:
                temp.append(e['@id'])

        return(temp)

    def generateDictionary(self, name):
        ''' Returns a dictionary of key = ID or name and appropriate values

        Returns
        =======
        dictionary:  dict
                     a dictionary of the aforementioned information

        '''
        name = self.__checkType(name)
        FIX = self.FIX['repository']
        parser = FIX[name][name[0:len(name) - 1]]
        dictionary = {}
        if name == 'fields':
            for field in parser:
                ID = field['@id']
                name = field['@name']
                type = field['@type']
                documentation = self.getDocumentation(field)
                dictionary[ID] = [name, type, documentation]
        elif name == 'components':
            for component in parser:
                ID = component['@id']
                name = component['@name']
                fieldRef = self.getFieldRef(component)
                groupRef = self.getGroupRef(component)
                componentRef = self.getComponentRef(component)
                documentation = self.getDocumentation(component)
                dictionary[ID] = [name, fieldRef, groupRef, componentRef, documentation]
        elif name == 'messages':
            for message in parser:
                ID = message['@msgType']
                name = message['@name']
                fieldRef = self.getFieldRef(message['structure'])
                groupRef = self.getGroupRef(message['structure'])
                componentRef = self.getComponentRef(message['structure'])
                documentation = self.getDocumentation(message)
                dictionary[ID] = [name, fieldRef, groupRef, componentRef, documentation]
        elif name == 'codeSets':
            for codeSet in parser:
                ID = codeSet['@id']
                name = codeSet['@name']
                fieldRef = self.getCodeSet(codeSet)
                documentation = self.getDocumentation(codeSet)
                dictionary[ID] = [name, fieldRef, documentation]
        elif name == 'groups':
            for group in parser:
                ID = group['@id']
                name = group['@name']
                numInGroup = group['numInGroup']['@id']
                fieldRef = self.getFieldRef(group)
                groupRef = self.getGroupRef(group)
                componentRef = self.getComponentRef(group)
                documentation = self.getDocumentation(group)
                dictionary[ID] = [name, numInGroup, fieldRef, groupRef, componentRef, documentation]
        elif name == 'datatypes':
            for datatype in parser:
                name = datatype['@name']
                documentation = self.getDocumentation(datatype)
                dictionary[name] = [name, documentation]

        return(dictionary)

    def read_xml(self, filepath="OrchestraFIXLatest.xml"):
        """
        Read the contents of an Orchestra XML file and convert it to a dictionary
        """
        namespaces = {
            "http://fixprotocol.io/2020/orchestra/repository": None, # skip this namespace so only localName is used
        }
        # present full namespace of metadata - Dublin Core Terms

        try:
            with open(filepath, "r", encoding="utf8") as f:
                self.FIX = xmltodict.parse(f.read(), process_namespaces=True, namespaces=namespaces)
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
        except Exception: #handle other exceptions such as attribute errors
            print("Unexpected error:", os.system.exc_info()[0])
