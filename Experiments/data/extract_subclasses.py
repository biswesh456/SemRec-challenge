filename = "OWL2EL_5"
filename_train = filename + "/train_norm.owl"
filename_valid = filename + "/valid_norm.owl"
filename_test = filename + "/valid_test.owl"
train_subclass_file = filename + "/train.txt"
valid_subclass_file = filename + "/valid.txt"
test_subclass_file = filename + "/test.txt"

f = open(train_subclass_file, "w")

with open(filename_train, "r") as f_train:
    txt = ""
    for line in f_train:
            if line.startswith('SubClassOf'):
                line = line.replace('SubClassOf(', '')
                line = line.replace(')', '').split()
                if len(line) == 3:
                    if line[1].startswith('Object'):
                        print(line)
                        print(line[0] + " " + line[2].replace(')', ''))
                        txt += line[0] + " " + line[2].replace(')', '') + "\n"
                    elif line[0].startswith('Object'):  
                        print(line)
                        print(line[1].replace(')', '')  + " " + line[2])
                        txt += line[1].replace(')', '')  + " " + line[2] + "\n"
                if len(line) == 2:
                    txt += line[0] + " " + line[1] + "\n"

    f.write(txt)
    f.close()


f = open(valid_subclass_file, "w")                

with open(filename_valid, "r") as f_valid:
    txt = ""
    for line in f_valid:
            if line.startswith('SubClassOf'):
                line = line.replace('SubClassOf(', '')
                line = line.replace(')', '').split()
                if len(line) == 2:
                    txt += line[0] + " " + line[1] + "\n"

    f.write(txt)
    f.close()

f = open(test_subclass_file, "w")                

with open(filename_test, "r") as f_test:
    txt = ""
    for line in f_test:
            if line.startswith('SubClassOf'):
                line = line.replace('SubClassOf(', '')
                line = line.replace(')', '').split()
                if len(line) == 2:
                    txt += line[0] + " " + line[1] + "\n"

    f.write(txt)
    f.close()

