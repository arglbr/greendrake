# TODOs

* Generate a git flow
* Tests
* Documentation
* Scalability, etc...
* OFXProcessor needs to generate the output CSV without the headers;
  - No, it is not. Actually the table generated at Athena must. It can be achieved if use 'TBLPROPERTIES ("skip.header.line.count"='1');' on the table definition.

