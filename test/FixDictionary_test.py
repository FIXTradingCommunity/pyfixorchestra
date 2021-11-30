import pytest
from pyfixorchestra import FixDictionary

METADATA = "metadata"
FIELDS = "fields"
GROUPS = "groups"
COMPONENTS= "components"
MESSAGES="messages"
CODESETS="codeSets"
DATATYPES="datatypes"
typez = [METADATA, FIELDS, COMPONENTS, GROUPS, MESSAGES, CODESETS, DATATYPES]

fd = FixDictionary()
fd.read_xml("test/resource_dir/OrchestraFIXLatest.xml")
dd = {t:print(fd.generate_dictionary(t)) for t in typez}