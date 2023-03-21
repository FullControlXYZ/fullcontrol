# FullControl lab


FullControl lab exists for things that aren't suitable for the main FullControl package yet, typically due to complexity in terms of their concept, code, hardware requirements, computational requirements, etc.

FullControl features/functions/classes in the lab may be more experimental in nature and should be used with more caution than the regular FullControl package

at present, both the lab and the regular FullControl packages are under active development and the code and package structures may change considerably. some aspects currently in FullControl may move to the lab and vice versa

the lab currently has two main aspects:
- geometry functions that supplement existing geometry functions in FullControl
- a five-axis demo

some aspects in the lab supplement the existing FullControl package (e.g. extra geometric functions) whereas some aspects overwrite existing functions/classes (e.g. Point objects changing to have XYZBC attributes instead of XYZ)

## installation

the lab is installed automatically with FullControl (this may change in the future)

## using FullControl lab

### *complimentary additional capabilities*

complimentary additional capabilities in the lab are imported in addition to the regular FullControl package:

```
import fullcontrol as fc
import lab.fullcontrol as fclab
```

### *modified capabilities*
some capabilities in the lab are imported **instead** of the regular FullControl package. the following import statement automatically imports everything in the regular FullControl package, but modifies some aspects to be fiveaxis:
```
import lab.fullcontrol.fiveaxis as fc5
```