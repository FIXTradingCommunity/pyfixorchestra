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
        accepted = ["codeSets", "datatypes", "fields",
                    "components", "groups", "messages", "metadata"]
        if name not in accepted:
            raise Exception("type not accepted")

        return(name)

    def getDocumentation(self, Elem):
        ''' Returns the documentation from a given element

        Returns
        =======
        returns documentation from a given element
        '''
        # this adds
        temp = []
        if 'documentation' not in Elem['annotation'].keys():
            temp.append("No documentation found")
        else:
            D = Elem['annotation']['documentation']
            if type(D) == list:
                for d in D:
                    if '#text' in d.keys():
                        temp.append({k[1:]: v for k, v in d.items()
                                     if k in ['#text', '@purpose', '@contentType']})
            elif '#text' in D.keys():
                temp.append({k[1:]: v for k, v in D.items()
                             if k in ['#text', '@purpose', '@contentType']})
            else:
                temp.append("No documentation found")
        return(temp)

    def getFieldRef(self, Elem):
        ''' Returns the field tags for field references in other components

        Returns
        =======
        returns field references for a given element
        '''
        temp = []
        if 'fieldRef' not in Elem.keys():
            return([])
        E = Elem['fieldRef']
        if type(E) != list:
            temp.append({k[1:]: v for k, v in E.items() if k in [
                        '@id', '@presence', '@scenario']})
        else:
            for e in E:
                temp.append({k[1:]: v for k, v in e.items() if k in [
                            '@id', '@presence', '@scenario']})
        return(temp)

    def getComponentRef(self, Elem):
        ''' Returns the component tags for component references in other components

        Returns
        =======
        returns component references for a given element
        '''
        temp = []
        if 'componentRef' not in Elem.keys():
            return([])
        E = Elem['componentRef']
        if type(E) != list:
            temp.append({k[1:]: v for k, v in E.items() if k in [
                        '@id', '@presence', '@scenario']})
        else:
            for e in E:
                temp.append({k[1:]: v for k, v in e.items() if k in [
                            '@id', '@presence', '@scenario']})
        return(temp)

    def getGroupRef(self, Elem):
        ''' Returns the group tags for group references in other components

        Returns
        =======
        returns group references for a given element
        '''
        temp = []
        if 'groupRef' not in Elem.keys():
            return([])
        E = Elem['groupRef']
        if type(E) != list:
            temp.append({k[1:]: v for k, v in E.items() if k in [
                        '@id', '@presence', '@scenario']})
        else:
            for e in E:
                temp.append({k[1:]: v for k, v in e.items() if k in [
                            '@id', '@presence', '@scenario']})
        return(temp)

    def getCodeSet(self, Elem):
        ''' Returns the values in a codeSet

        Returns
        =======
        returns values in a code set
        '''
        temp = []
        if 'code' not in Elem.keys():
            return([])
        E = Elem['code']
        if type(E) != list:
            temp.append(E['@id'])
        else:
            for e in E:
                temp.append(e['@id'])

        return(temp)

    def generateDictionary(self, name):
        ''' Returns a dictionary of key = id or name and appropriate values

        Returns
        =======
        dictionary:  dict
                     a dictionary of the aforementioned information

        '''
        name = self.__checkType(name)
        dictionary = {}
        FIX = self.FIX['repository']
        if name == 'metadata':
            dictionary = FIX['metadata']
        else:
            parser = FIX[name][name[0:len(name) - 1]]

            if name == 'fields':
                for field in parser:
                    id = field['@id']
                    name = field['@name']
                    type = field['@type']
                    scenario = field.get('@scenario', 'base')
                    documentation = self.getDocumentation(field)
                    dictionary[id] = [name, type, scenario, documentation]
            elif name == 'components':
                for component in parser:
                    id = component['@id']
                    name = component['@name']
                    scenario = component.get('@scenario', 'base')
                    fieldRef = self.getFieldRef(component)
                    groupRef = self.getGroupRef(component)
                    componentRef = self.getComponentRef(component)
                    documentation = self.getDocumentation(component)
                    dictionary[id] = [name, scenario, fieldRef,
                                      groupRef, componentRef, documentation]
            elif name == 'messages':
                for message in parser:
                    id = message['@msgType']
                    name = message['@name']
                    scenario = message.get('@scenario', 'base')
                    fieldRef = self.getFieldRef(message['structure'])
                    groupRef = self.getGroupRef(message['structure'])
                    componentRef = self.getComponentRef(message['structure'])
                    documentation = self.getDocumentation(message)
                    dictionary[id] = [name, scenario, fieldRef,
                                      groupRef, componentRef, documentation]
            elif name == 'codeSets':
                for codeSet in parser:
                    id = codeSet['@id']
                    name = codeSet['@name']
                    scenario = codeSet.get('@scenario', 'base')
                    fieldRef = self.getCodeSet(codeSet)
                    documentation = self.getDocumentation(codeSet)
                    dictionary[id] = [name, scenario, fieldRef, documentation]
            elif name == 'groups':
                for group in parser:
                    id = group['@id']
                    name = group['@name']
                    scenario = group.get('@scenario', 'base')
                    numInGroup = group['numInGroup']['@id']
                    fieldRef = self.getFieldRef(group)
                    groupRef = self.getGroupRef(group)
                    componentRef = self.getComponentRef(group)
                    documentation = self.getDocumentation(group)
                    dictionary[id] = [name, scenario, numInGroup, fieldRef,
                                      groupRef, componentRef, documentation]
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
            # skip this namespace so only localName is used
            "http://fixprotocol.io/2020/orchestra/repository": None,
        }
        # present full namespace of metadata - Dublin Core Terms

        try:
            with open(filepath, "r", encoding="utf8") as f:
                self.FIX = xmltodict.parse(
                    f.read(), process_namespaces=True, namespaces=namespaces)
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
        except Exception:  # handle other exceptions such as attribute errors
            print("Unexpected error:", os.system.exc_info()[0])
