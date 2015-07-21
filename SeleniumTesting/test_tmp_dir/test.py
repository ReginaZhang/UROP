import sys
import ConfigParser

Config = ConfigParser.ConfigParser()
Config.read("./test_config.cfg")
print "sections"
print Config.sections()
print "options"
print Config.options("SectionOne")
print "value to age"
print Config.get("SectionOne", "age")
print Config.options("SectionTwo")
print Config.get("SectionTwo", "favorite color")
print >>sys.stderr, "A lovely error"