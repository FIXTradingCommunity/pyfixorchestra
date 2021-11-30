# pyfixorchestra
FIX Orchestra hand built language binding for Python

## Usage

Example to retrieve all parts of an Orchestra file:

```python
from pyfixorchestra import FixDictionary

METADATA = "metadata"
FIELDS = "fields"
GROUPS = "groups"
COMPONENTS = "components"
MESSAGES = "messages"
CODESETS = "codeSets"
DATATYPES = "datatypes"
typez = [METADATA, FIELDS, COMPONENTS, GROUPS, MESSAGES, CODESETS, DATATYPES]

fd = FixDictionary()
fd.read_xml("OrchestraFIXLatest.xml")
dd = {t: print(fd.generate_dictionary(t)) for t in typez}
```

## Output format

### Metadata

The metadata section of an Orchestra file describes the artifact using [Dublin Core Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/).

The metadata terms are return as a dictionary. The keys are Dublin Core Terms with their XML namespace.

Example:

```python
OrderedDict([('http://purl.org/dc/elements/1.1/:title', 'Orchestra'), ('http://purl.org/dc/elements/1.1/:creator', 
'unified2orchestra.xslt script'), ('http://purl.org/dc/elements/1.1/:publisher', 'FIX Trading Community'), ('http://purl.org/dc/elements/1.1/:date', '2021-08-14T22:38:48.950856Z'), ('http://purl.org/dc/elements/1.1/:format', 'Orchestra schema'), ('http://purl.org/dc/elements/1.1/:source', 'FIX Unified Repository'), ('http://purl.org/dc/elements/1.1/:rights', 'Copyright (c) FIX Protocol Ltd. All Rights Reserved.')])
```

### Fields

Fields are return as an array where each element reprsents a field. Each field is a dictionary with entries for id (tag) name, type (datatype name or codeset name), scenario, and documentation. See below for scenario and documentation.

```python
[{'id': '1', 'name': 'Account', 'type': 'String', 'scenario': 'base', 'documentation': [{'purpose': 'SYNOPSIS', 'text': 'Account mnemonic as agreed between buy and sell sides, e.g. broker and institution or investor/intermediary and fund manager.'}]}, {'id': '2', 'name': 'AdvId', 'type': 'String', 'scenario': 'base', 'documentation': [{'purpose': 'SYNOPSIS', 'text': 'Unique identifier of advertisement message.\n         (Prior to FIX 4.1 this field was of type int)'}]}, {'id': '3', 'name': 'AdvRefID', 'type': 'String', 'scenario': 'base', 'documentation': [{'purpose': 'SYNOPSIS', 'text': 'Reference identifier used with CANCEL and REPLACE transaction types.\n         (Prior to FIX 4.1 this field was of type int)'}]}, {'id': '4', 'name': 'AdvSide', 'type': 'AdvSideCodeSet', 'scenario': 'base', 'documentation': [{'purpose': 'SYNOPSIS', 'text': "Broker's side of advertised trade"}]}, {'id': '5', 'name': 'AdvTransType', 'type': 'AdvTransTypeCodeSet', 'scenario': 'base', 'documentation': [{'purpose': 'SYNOPSIS', 'text': 'Identifies advertisement message transaction type'}]}, 
...
```

### Scenario

In Orchestra, every message and message element has a scenario name. The default scenario is 'base'.


### Documentation

The documenation of all elements, including fields, are in the same format. Each element has array of documentation objects. Each object optionally has an optional `purpose` attribute and a `text` attribute. If an element has no documentation, then the literal 'No documentation found' is generated.

```python
[{'purpose': 'SYNOPSIS', 'text': 'The CommissionData component block is used to carry commission information such as the type of commission and the rate. Use the CommissionDataGrp component as an alternative if multiple commissions or enhanced attributes are needed.'}, {'purpose': 'ELABORATION', 'text': 'This component may be used to provide aggregated commission data of a given CommType(13) where the CommissionDataGrp maybe used to include the detail splits ...'}]
```

### Components

Components are returned as an array where each element represents a component. Each component is a dictionary with entries for id, name,  scenario, a fieldRef array, groupRef array, an array of nested componentRef , and documentation. See above for scenario and documentation. The fieldRef, groupRef, and componentRef are the members of the top-level component.

```python
[{'id': '1000', 'name': 'CommissionData', 'scenario': 'base', 'fieldRef': [{'id': '12', 'documentation': ['No documentation found']}, {'id': '13', 'documentation': ['No documentation found']}, {'id': '479', 'documentation': ['No documentation found']}, {'id': '1233', 'documentation': ['No documentation found']}, {'id': '1238', 'documentation': ['No documentation found']}, {'id': '497', 'documentation': ['No documentation found']}], 'groupRef': [], 'componentRef': [], 'documentation': [{'purpose': 'SYNOPSIS', 'text': 'The CommissionData component block is used to carry commission information such as the type of commission and the rate. Use the CommissionDataGrp component as an alternative if multiple commissions or enhanced attributes are needed.'}, {'purpose': 'ELABORATION', 'text': 'This component may be used to provide aggregated commission data of a given CommType(13) where the CommissionDataGrp maybe used to include the detail splits provided the commission is of the same commission basis type. For example, CommissionData may contain CommType(13) of 3 (Absolute) and a Commission(12) value of "15". CommissionDataGrp may be used to show how this Commission(12) value of "15" is split up as long as the CommissionBasis(2642) is also 3 (Absolute) for each of the instances added together. This method of aggregated commission data may also be applied to this component to provide a total when the instances of the detail splits in CommissionDataGrp contain leg level information (indicated by the usage of CommissionLegRefID(2649) in CommissionDataGrp). Note that it is only possible to aggregate values for a single commission basis type.'}]}, {'id': '1001', 'name': 'DiscretionInstructions', 'scenario': 'base', 'fieldRef': [{'id': '388', 'documentation': [{'text', 'What the discretionary price is related to (e.g. primary price, display price etc)'}]}, {'id': '389', 'documentation': [{'Amount (signed) added to the "related to" price specified via DiscretionInst, in the context of DiscretionOffsetType', 'text'}]}, {'id': '841', 'documentation': [{'text', 'Describes whether discretion price is static/fixed or floats'}]}, {'id': '842', 'documentation': [{'text', 'Type of Discretion Offset (e.g. price offset, tick offset etc)'}]}, {'id': '843', 'documentation': [{'Specifies the nature of the resulting discretion price (e.g. or better limit, strict limit etc)', 'text'}]}, {'id': '844', 'documentation': [{'If the calculated discretion price is not a valid tick price, specifies how to round the price (e.g. to be more or less aggressive)', 'text'}]}, {'id': '846', 'documentation': [{'text', 'The scope of "related to" price of the discretion (e.g. local, global etc)'}]}], 'groupRef': [], 'componentRef': [], 'documentation': [{'purpose': 'SYNOPSIS', 'text': 'The presence of DiscretionInstructions component block on an order indicates that the trader wishes to display one price but will accept trades at another price.'}]}, 
...
```
### Groups

Groups follows the same format as components described above, with addition of a `numInGroup` attribute. It specifies the field id that conveys the size of a repeating group.

### Messages

Messages follows the same format as components described above.

### Codesets

Codesets are return as an array where each element reprsents a codeset. Each codeset is a dictionary with entries for id, name,  scenario, an array of codes, and documentation. Each code is a dictionary of id, name, and value, and documentation.

```python
[{'id': '4', 'name': 'AdvSideCodeSet', 'scenario': 'base', 'codes': [{'name': 'Buy', 'id': '4001', 'value': 'B', 'documentation': [{'purpose': 'SYNOPSIS', 'text': 'Buy'}]}, {'name': 'Sell', 'id': '4002', 'value': 'S', 'documentation': [{'purpose': 'SYNOPSIS', 'text': 'Sell'}]}, {'name': 'Trade', 'id': '4003', 'value': 'T', 'documentation': [{'purpose': 'SYNOPSIS', 'text': 'Trade'}]}, {'name': 'Cross', 'id': '4004', 'value': 'X', 'documentation': [{'purpose': 'SYNOPSIS', 'text': 'Cross'}]}], 'documentation': [{'purpose': 'SYNOPSIS', 'text': "Broker's side of advertised trade"}]}, {'id': '5', 'name': 'AdvTransTypeCodeSet', 'scenario': 'base', 'codes': [{'name': 'New', 'id': '5001', 'value': 'N', 'documentation': [{'purpose': 'SYNOPSIS', 'text': 'New'}]}, {'name': 'Cancel', 'id': '5002', 'value': 'C', 'documentation': [{'purpose': 'SYNOPSIS', 'text': 'Cancel'}]}, {'name': 'Replace', 'id': '5003', 'value': 'R', 'documentation': [{'purpose': 'SYNOPSIS', 'text': 'Replace'}]}], 'documentation': [{'purpose': 'SYNOPSIS', 'text': 'Identifies advertisement message transaction type'}]},
...
```

### Datatypes

Datatypes are return as an array where each element reprsents a datatype. Each datatype is a dictionary with entries for name and documentation.

```python
[{'name': 'int', 'documentation': [{'purpose': 'SYNOPSIS', 'text': 'Sequence of digits without commas or decimals and optional sign character (ASCII characters "-" and "0" - "9" ). The sign character utilizes one byte (i.e. positive int is "99999" while negative int is "-99999"). Note that int values may contain leading zeros (e.g. "00023" = "23").'}, {'purpose': 'EXAMPLE', 'text': '723 in field 21 would be mapped int as |21=723|. -723 in field 12 would be mapped int as |12=-723|.'}]}, {'name': 'Length', 'documentation': [{'purpose': 'SYNOPSIS', 'text': 'int field representing the length in bytes. Value must be positive.'}]},
...
```

## License
© Copyright 2020-2021 FIX Protocol Limited

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.