import sys
import ConfigParser

Config = ConfigParser.ConfigParser()
Config.optionxform=str
Config.read("./test_config.cfg")
print "sections"
print Config.sections()
print "options"
print Config.options("SectionOne")
print "value to age"
print Config.get("SectionOne", "Age")
print Config.options("SectionTwo")
print Config.get("SectionTwo", "Favorite Color")
print >>sys.stderr, "A lovely error"
print Config.get("SectionOne", "a")
print "hey" + Config.get("SectionOne", "b") + "hello"