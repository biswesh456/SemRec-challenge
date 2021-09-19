filename = "OWL2EL_5"
filename_train = filename + "/train.owl"
filename_valid = filename + "/valid.owl"
filename_test = filename + "/test.owl"
train_subclass_file = filename + "/train_fixed.owl"
valid_subclass_file = filename + "/valid_fixed.owl"
test_subclass_file = filename + "/test_fixed.owl"

f = open(train_subclass_file, "w")

with open(filename_train, "r") as f_train:
    txt = ""
    for line in f_train:
        bl = True
        if line.find("FunctionalDataProperty") != -1:
            bl = False
        if line.find("DataPropertyRange") != -1:
            bl = False
        if line.find("DataPropertyDomain") != -1:
            bl = False    
        if line.find("HasKey") != -1:
            bl = False  
        if line.find("ObjectHasValue") != -1:
            bl = False    
        if line.find("ObjectHasSelf") != -1:
            bl = False                  
        if bl == True:         
            txt += line
                
    f.write(txt)
    f.close()


f = open(valid_subclass_file, "w")                

with open(filename_valid, "r") as f_valid:
    txt = ""
    for line in f_valid:
        bl = True
        if line.find("FunctionalDataProperty") != -1:
            bl = False
        if line.find("DataPropertyRange") != -1:
            bl = False
        if line.find("DataPropertyDomain") != -1:
            bl = False    
        if line.find("HasKey") != -1:
            bl = False  
        if line.find("ObjectHasValue") != -1:
            bl = False  
        if line.find("ObjectHasSelf") != -1:
            bl = False                   
        if bl == True:         
            txt += line

    f.write(txt)
    f.close()

f = open(test_subclass_file, "w")                

with open(filename_test, "r") as f_test:
    txt = ""
    for line in f_test:
        bl = True
        if line.find("FunctionalDataProperty") != -1:
            bl = False
        if line.find("DataPropertyRange") != -1:
            bl = False
        if line.find("DataPropertyDomain") != -1:
            bl = False    
        if line.find("HasKey") != -1:
            bl = False  
        if line.find("ObjectHasValue") != -1:
            bl = False  
        if line.find("ObjectHasSelf") != -1:
            bl = False                   
        if bl == True:         
            txt += line

    f.write(txt)
    f.close()

