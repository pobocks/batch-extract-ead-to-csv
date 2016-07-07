from lxml import etree
import os, glob

def lenTest(path,tree):
  return len(tree.xpath(path))

def multipleParts(partsPath,tree):
    global creator
    partsList = tree.xpath(partsPath)
    for part in partsList:
        creator = creator + etree.tostring(part, encoding='unicode_escape', method='text').strip() + "|"

def multipleCreators(genPath,tree):
    global creator
    num = lenTest(genPath,tree)
    increment = 1
    while increment <= num:
        parts = genPath + "[" + str(increment) + "]" + "/part"
        if lenTest(parts,tree) > 1:
            multipleParts(parts,tree)
        elif lenTest(parts,tree) == 1:
            partsVal = tree.xpath(parts)[0]
            creator = creator + etree.tostring(partsVal, encoding='unicode_escape', method='text').strip() + "|"
        increment += 1

def getOrigination(corpXPath, famXPath, nameXPath, persXPath,tree):
    global creator
    if lenTest(corpXPath,tree) > 1:
        multipleCreators(corpXPath,tree)
    elif lenTest(corpXPath,tree) == 1:
        parts = corpXPath + "[1]/part"
        partsVal = tree.xpath(parts)[0]
        creator = creator + etree.tostring(partsVal, encoding='unicode_escape', method='text').strip() + "|"
    if lenTest(famXPath,tree) > 1:
        multipleCreators(famXPath,tree)
    elif lenTest(famXPath,tree) == 1:
        parts = famXPath + "[1]/part"
        partsVal = tree.xpath(parts)[0]
        creator = creator + etree.tostring(partsVal, encoding='unicode_escape', method='text').strip() + "|"
    if lenTest(nameXPath,tree) > 1:
        multipleCreators(nameXPath,tree)
    elif lenTest(nameXPath,tree) == 1:
        parts = nameXPath + "[1]/part"
        partsVal = tree.xpath(parts)[0]
        creator = creator + etree.tostring(partsVal, encoding='unicode_escape', method='text').strip() + "|"
    if lenTest(persXPath,tree) > 1:
        multipleCreators(persXPath,tree)
    elif lenTest(persXPath,tree) == 1:
        parts = persXPath + "[1]/part"
        partsVal = tree.xpath(parts)[0]
        creator = creator + etree.tostring(partsVal, encoding='unicode_escape', method='text').strip() + "|"

def getScopeContent(genPath,tree):
    global scopeAndContent
    scopeParagraphPath = genPath + "[1]" + "/p"
    scopeParagraphs = tree.xpath(scopeParagraphPath)
    for para in scopeParagraphs:
        scopeAndContent = scopeAndContent + etree.tostring(para, encoding='unicode_escape', method='text').strip() + "\u000a\u000a"

# Use os and glob.glob to pickup every single *.xml file and then run a full process on it. Maybe take just directory as input?

directory="/Users/rtillman/Documents/Code/FindingAidsWork_Apparently_Dont_Batch_Ingest/samples"

# Of course gonna have to clear variables between groups

titleXPath = "/ead/control/filedesc/titlestmt/titleproper"
scopeXPath = "/ead/archdesc/scopecontent"
corpXPath = "/ead/archdesc/did/origination/corpname"
persXPath = "/ead/archdesc/did/origination/persname"
famXPath = "/ead/archdesc/did/origination/famname"
nameXPath = "/ead/archdesc/did/origination/name"
creator = ""
scopeAndContent = ""

# Actually Running It This Will Become a Function #
def createCSV(directory, outputFile):
    global creator, scopeAndContent
    os.chdir(directory)
    f = open(outputFile, 'w')
    f.write("type,owner,access,files,dc:title,dc:abstract,dc:creator\n")
    files = glob.glob("*.xml")
    for each in files:
        tree = etree.parse(each)
        titleString = etree.tostring(tree.xpath(titleXPath)[0], method='text').strip()
        creator = ""
        scopeAndContent = ""
        typeString = "Work-FindingAid"
        ownerString = "rtillman"
        accessString = "public;edit=rtillman"
        titleString = titleString.replace('"', '\u0022')
        getOrigination(corpXPath, famXPath, nameXPath, persXPath,tree)
        creator = creator.replace('"', '\u0022')
        getScopeContent(scopeXPath,tree)
        scopeAndContent = scopeAndContent.replace('"', '\u0022')
        creator = '"' + creator + '"'
        titleString = '"' + titleString + '"'
        scopeAndContent = '"' + scopeAndContent + '"'
        #line = typeString + "," + ownerString  + "," + accessString + "," + each + "," + titleString + "," + scopeAndContent + "," + creator + "\n"
        f.write(typeString)
        f.write(",")
        f.write(ownerString)
        f.write(",")
        f.write(accessString)
        f.write(",")
        f.write(each)
        f.write(",")
        f.write(titleString)
        f.write(",")
        f.write(scopeAndContent)
        f.write(",")
        f.write(creator)
        f.write("\n")

output = raw_input("What do you want to call the file? ")
createCSV(directory,output)
