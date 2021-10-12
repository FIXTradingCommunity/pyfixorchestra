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
        if 'annotation' not in Elem or 'documentation' not in Elem['annotation'].keys():
            temp.append("No documentation found")
        else:
            D = Elem['annotation']['documentation']
            if D is None:
                temp.append("No documentation found")
            elif type(D) == list:
                for d in D:
                    if '#text' in d.keys():
                        temp.append({k[1:]: v for k, v in d.items()
                                     if k in ['#text', '@purpose', '@contentType']})
            elif type(D) == str:
                temp.append({'text', D})
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
            documentation = self.getDocumentation(E)
            kv = {k[1:]: v for k, v in E.items() if k in [
                '@id', '@presence', '@scenario']}
            kv['documentation'] = documentation
            temp.append(kv)
        else:
            for e in E:
                documentation = self.getDocumentation(e)
                kv = {k[1:]: v for k, v in e.items() if k in [
                    '@id', '@presence', '@scenario']}
                kv['documentation'] = documentation
                temp.append(kv)
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
            documentation = self.getDocumentation(E)
            kv = {k[1:]: v for k, v in E.items() if k in [
                '@id', '@presence', '@scenario']}
            kv['documentation'] = documentation
            temp.append(kv)
        else:
            for e in E:
                documentation = self.getDocumentation(e)
                kv = {k[1:]: v for k, v in e.items() if k in [
                    '@id', '@presence', '@scenario']}
                kv['documentation'] = documentation
                temp.append(kv)
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
            documentation = self.getDocumentation(E)
            kv = {k[1:]: v for k, v in E.items() if k in [
                '@id', '@presence', '@scenario']}
            kv['documentation'] = documentation
            temp.append(kv)
        else:
            for e in E:
                documentation = self.getDocumentation(e)
                kv = {k[1:]: v for k, v in e.items() if k in [
                    '@id', '@presence', '@scenario']}
                kv['documentation'] = documentation
                temp.append(kv)
        return(temp)

    def getCodes(self, Elem):
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
            documentation = self.getDocumentation(E)
            kv = {k[1:]: v for k, v in E.items() if k in [
                '@id', '@name', '@value']}
            kv['documentation'] = documentation
            temp.append(kv)
        else:
            for e in E:
                documentation = self.getDocumentation(e)
                kv = {k[1:]: v for k, v in e.items() if k in [
                    '@id', '@name', '@value']}
                kv['documentation'] = documentation
                temp.append(kv)
        return(temp)

    def generateDictionary(self, name):
        ''' Extracts the requested category of Orchestra elements

        Returns
        =======
        an array of dictionary elements or a dictionary of metadata

        '''
        name = self.__checkType(name)
        FIX = self.FIX['repository']
        if name == 'metadata':
            # return a dictionary of Dublin Core Terms
            return FIX['metadata']
        else:
            parser = FIX[name][name[0:len(name) - 1]]
            array = []

            if name == 'fields':
                for field in parser:
                    dictionary = {}
                    dictionary['id'] = field['@id']
                    dictionary['name'] = field['@name']
                    dictionary['type'] = field['@type']
                    dictionary['scenario'] = field.get('@scenario', 'base')
                    dictionary['documentation'] = self.getDocumentation(field)
                    array.append(dictionary)
            elif name == 'components':
                for component in parser:
                    dictionary = {}
                    dictionary['id'] = component['@id']
                    dictionary['name'] = component['@name']
                    dictionary['scenario'] = component.get('@scenario', 'base')
                    dictionary['fieldRef'] = self.getFieldRef(component)
                    dictionary['groupRef'] = self.getGroupRef(component)
                    dictionary['componentRef'] = self.getComponentRef(
                        component)
                    dictionary['documentation'] = self.getDocumentation(
                        component)
                    array.append(dictionary)
            elif name == 'messages':
                for message in parser:
                    dictionary = {}
                    dictionary['id'] = message['@id']
                    dictionary['name'] = message['@name']
                    dictionary['scenario'] = message.get('@scenario', 'base')
                    dictionary['fieldRef'] = self.getFieldRef(message['structure'])
                    dictionary['groupRef'] = self.getGroupRef(message['structure'])
                    dictionary['componentRef'] = self.getComponentRef(message['structure'])
                    dictionary['documentation'] = self.getDocumentation(
                        message)
                    array.append(dictionary)
            elif name == 'codeSets':
                for codeSet in parser:
                    dictionary = {}
                    dictionary['id'] = codeSet['@id']
                    dictionary['name'] = codeSet['@name']
                    dictionary['scenario'] = codeSet.get('@scenario', 'base')
                    dictionary['codes'] = self.getCodes(codeSet)
                    dictionary['documentation'] = self.getDocumentation(
                        codeSet)
                    array.append(dictionary)
            elif name == 'groups':
                for group in parser:
                    dictionary = {}
                    dictionary['id'] = group['@id']
                    dictionary['name'] = group['@name']
                    dictionary['scenario'] = group.get('@scenario', 'base')
                    dictionary['numInGroup'] = group['numInGroup']['@id']
                    dictionary['fieldRef'] = self.getFieldRef(group)
                    dictionary['groupRef'] = self.getGroupRef(group)
                    dictionary['componentRef'] = self.getComponentRef(group)
                    dictionary['documentation'] = self.getDocumentation(group)
                    array.append(dictionary)
            elif name == 'datatypes':
                for datatype in parser:
                    dictionary = {}
                    dictionary['name'] = datatype['@name']
                    dictionary['documentation'] = self.getDocumentation(
                        datatype)
                    array.append(dictionary)

            return(array)

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
