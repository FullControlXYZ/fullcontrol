# CICD testing

## quick test:
- copy tutorial or model notebooks from their respective directories into the repo home directory so that, upon execution, they import the correct version of fullcontrol (in case fullcontrol is installed multiple times, etc.)
- run the notebook copies to check everything works
- delete the notebook copies
- explain tests done on any pull request to github

## extensive testing:
- note: this method has only been tested on ubuntu in WSL
- navigate to fullcontrol repo directory
- `cd tests`
- `python CICD_test.py`
    - this will take a few minutes becuase it runs through all tutorial notebooks and models to generate the text outputs and save plots as png images
- follows prompts to:
    - check text outputs look similar to the reference outputs
    - check plot iamges outputs look similar to the reference images
    - any changes should be justified in the pull request comment

## update testing script if tutorials or models are modified:
if the tutorial notebooks are modified, the overall test script (combination of all notebooks) should be recreated to include the modifications
- navigate to fullcontrol repo directory
- `cd bin`
- `python tutorials_to_py.py`
- do 'extensive testing' above and check that text outputs and plots change as expected
- in tests directory:
    - copy test_print_output.txt to overwrite test_print_output_reference.txt
    - copy collage.png to overwrite collage_reference.png
    - leave test_result.txt as it is, to highlight (expected) changes resulting from notebook modifications
- submit pull request with clear explanation that tests were completely correctly and reference files in the tests directory were overwritten and all differences were expected