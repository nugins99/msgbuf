# msgbuf

Sort of like protobuf, but nothing like it at all at the same time. 

Protobuf is a well thought out design and implemention.  This is a quick hack
just to prove that I could quickly define a message in a yaml format, and using
a little python + Jinja2 templates to create a message definition and generate
code that could serialize/deserialize messages with minimal effort.

Some minimal support handle network endianess.   Not fully tested...

Look at the example file in msg/msg.yaml for an example file format.

Look in the test directory for test code and infrastructure to support 
serialization/deserialization. 

YMMV...



