# EmELpp
This is the code for the SemRec challenge.

## Requirements      
Click 7.0    
cycler 0.10.0    
gast 0.2.2    
grpcio 1.18.0    
Keras-Applications 1.0.6    
Keras-Preprocessing 1.0.5    
numpy 1.16.0    
pandas 0.23.4    
pkg-resources 0.0.0         
pytz 2018.9    
scikit-learn 0.20.2    
scipy 1.2.0    
six 1.12.0     
sklearn 0.0     
tensorboard 1.15.0     
tensorflow-gpu 1.15.0     

The code is organized as follows:
- experiments: This contains separate folder for each ontology the experiment is carried out upon.
- The implementation of evaluation metrics - Evaluating_HITS.py

Implementation of the code is organised for classification task:

First place the test.owl files of every data in their separate folder. Then run the fixer.py script on the file. For example, for OWL2EL_5 data, we run the fixer.py on OWL2EL_5/test.owl file. In order to run on any other data, we change the filename in the fixer.py file.

Given an ontology OWL file we normalize it with Normalizer.groovy script using jcel jar in Experiments/data folder.
	Command to Normalize: groovy -cp jcel.jar Normalizer.groovy -i <Input OWL ontology> -o <Output normalized-ontology>

After we get the normalized files, run the extract_subclass.py script on the normalized file to get the final testing data.

Executing the code:
- Before executing the code you need CUDA installed to use a GPU and list of python libraries as provided in requirements.txt.
- Put the required pickled models in experiments/models folder.
- For evaluating the embeddings run python scripts Evaluating_HITS-semrec.py, provide the path of the pkl files(placed in the results folder).


The file used for training the model has also been provided in the Experiments/training folder.


