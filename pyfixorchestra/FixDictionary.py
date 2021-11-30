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

import os
import xmltodict


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

    def __check_type(self, name):
        """ This is a check to make sure the user is generating a legal dictionary

        Returns
        =======
        name: String
                   accepted type

        """
        accepted = ["codeSets", "datatypes", "fields",
                    "components", "groups", "messages", "metadata"]
        if name not in accepted:
            raise Exception("type not accepted")

        return name

    def documentation(self, elem):
        """ Returns the documentation from a given element

        Returns
        =======
        returns documentation from a given element
        """
        # this adds
        temp = []
        if 'annotation' not in elem or 'documentation' not in elem['annotation'].keys():
            temp.append({"text": ""})
        else:
            d = elem['annotation']['documentation']
            if d is None:
                temp.append({"text": ""})
            elif type(d) == list:
                for d in d:
                    if '#text' in d.keys():
                        temp.append({k[1:]: v for k, v in d.items()
                                     if k in ['#text', '@purpose', '@contentType']})
            elif type(d) == str:
                temp.append({'text', d})
            elif '#text' in d.keys():
                temp.append({k[1:]: v for k, v in d.items()
                             if k in ['#text', '@purpose', '@contentType']})
            else:
                temp.append({"text": ""})
        return temp

    def field_ref(self, elem):
        """ Returns the field tags for field references in other components

        Returns
        =======
        returns field references for a given element
        """
        temp = []
        if 'fieldRef' not in elem.keys():
            return []
        e = elem['fieldRef']
        if type(e) != list:
            documentation = self.documentation(e)
            kv = {k[1:]: v for k, v in e.items() if k in [
                '@id', '@presence', '@scenario']}
            kv['documentation'] = documentation
            temp.append(kv)
        else:
            for e in e:
                documentation = self.documentation(e)
                kv = {k[1:]: v for k, v in e.items() if k in [
                    '@id', '@presence', '@scenario']}
                kv['documentation'] = documentation
                temp.append(kv)
        return temp

    def component_ref(self, elem):
        """ Returns the component tags for component references in other components

        Returns
        =======
        returns component references for a given element
        """
        temp = []
        if 'componentRef' not in elem.keys():
            return []
        e = elem['componentRef']
        if type(e) != list:
            documentation = self.documentation(e)
            kv = {k[1:]: v for k, v in e.items() if k in [
                '@id', '@presence', '@scenario']}
            kv['documentation'] = documentation
            temp.append(kv)
        else:
            for e in e:
                documentation = self.documentation(e)
                kv = {k[1:]: v for k, v in e.items() if k in [
                    '@id', '@presence', '@scenario']}
                kv['documentation'] = documentation
                temp.append(kv)
        return temp

    def group_ref(self, elem):
        """ Returns the group tags for group references in other components

        Returns
        =======
        returns group references for a given element
        """
        temp = []
        if 'groupRef' not in elem.keys():
            return []
        e = elem['groupRef']
        if type(e) != list:
            documentation = self.documentation(e)
            kv = {k[1:]: v for k, v in e.items() if k in [
                '@id', '@presence', '@scenario']}
            kv['documentation'] = documentation
            temp.append(kv)
        else:
            for e in e:
                documentation = self.documentation(e)
                kv = {k[1:]: v for k, v in e.items() if k in [
                    '@id', '@presence', '@scenario']}
                kv['documentation'] = documentation
                temp.append(kv)
        return temp

    def codes(self, elem):
        """ Returns the values in a codeSet

        Returns
        =======
        returns values in a code set
        """
        temp = []
        if 'code' not in elem.keys():
            return []
        e = elem['code']
        if type(e) != list:
            documentation = self.documentation(e)
            kv = {k[1:]: v for k, v in e.items() if k in [
                '@id', '@name', '@value']}
            kv['documentation'] = documentation
            temp.append(kv)
        else:
            for e in e:
                documentation = self.documentation(e)
                kv = {k[1:]: v for k, v in e.items() if k in [
                    '@id', '@name', '@value']}
                kv['documentation'] = documentation
                temp.append(kv)
        return temp

    def generate_dictionary(self, name):
        """ Extracts the requested category of Orchestra elements

        Returns
        =======
        an array of dictionary elements or a dictionary of metadata

        """
        name = self.__check_type(name)
        fix = self.FIX['repository']
        if name == 'metadata':
            # return a dictionary of Dublin Core Terms
            return fix['metadata']
        else:
            parser = fix[name][name[0:len(name) - 1]]
            array = []

            if name == 'fields':
                for field in parser:
                    dictionary = {'id': field['@id'], 'name': field['@name'], 'type': field['@type'],
                                  'scenario': field.get('@scenario', 'base'),
                                  'documentation': self.documentation(field)}
                    array.append(dictionary)
            elif name == 'components':
                for component in parser:
                    dictionary = {'id': component['@id'], 'name': component['@name'],
                                  'scenario': component.get('@scenario', 'base'),
                                  'fieldRef': self.field_ref(component), 'groupRef': self.group_ref(component),
                                  'componentRef': self.component_ref(
                                      component), 'documentation': self.documentation(
                            component)}
                    array.append(dictionary)
            elif name == 'messages':
                for message in parser:
                    dictionary = {'id': message['@id'], 'name': message['@name'],
                                  'scenario': message.get('@scenario', 'base'),
                                  'fieldRef': self.field_ref(message['structure']),
                                  'groupRef': self.group_ref(message['structure']),
                                  'componentRef': self.component_ref(message['structure']),
                                  'documentation': self.documentation(
                                      message)}
                    array.append(dictionary)
            elif name == 'codeSets':
                for codeSet in parser:
                    dictionary = {'id': codeSet['@id'], 'name': codeSet['@name'], 'type': codeSet['@type'],
                                  'scenario': codeSet.get('@scenario', 'base'), 'codes': self.codes(codeSet),
                                  'documentation': self.documentation(
                                      codeSet)}
                    array.append(dictionary)
            elif name == 'groups':
                for group in parser:
                    dictionary = {'id': group['@id'], 'name': group['@name'],
                                  'scenario': group.get('@scenario', 'base'), 'numInGroup': group['numInGroup']['@id'],
                                  'fieldRef': self.field_ref(group), 'groupRef': self.group_ref(group),
                                  'componentRef': self.component_ref(group),
                                  'documentation': self.documentation(group)}
                    array.append(dictionary)
            elif name == 'datatypes':
                for datatype in parser:
                    dictionary = {'name': datatype['@name'], 'documentation': self.documentation(
                        datatype)}
                    array.append(dictionary)

            return array

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
