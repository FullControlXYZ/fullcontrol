import os
import subprocess

# usage: run this script in the bin directory with 'python tutorials_to_py.py'
# this script converts all the .ipynb files into .py files in the tutorials directory and combines them as a single .py files before deleting the individual .py files
# it also replaces the 'fig.show()' line in one tutorial with code that saves the figure as a .png file
# this is only required for the single demo where the plot is manually created
# all other plots are created using fc.transform which is automatically modified during CICD testing to output figures as .png files

def convert_ipynb_to_py():
    files = os.listdir('../tutorials/')
    ipynb_files = list(filter(lambda x: x.endswith('.ipynb'), files))
    ipynb_files.sort()  # Sort the files by filename
    print(ipynb_files)

    for ipynb_file in ipynb_files:
        subprocess.run(['jupyter', 'nbconvert', '--to', 'python', '--output-dir=../tests/', '../tutorials/' + ipynb_file])
        print(f'converted {ipynb_files} to .py')
    py_files = list(map(lambda x: x.replace('.ipynb', '.py'), ipynb_files))
    return py_files


def combine_py_files(py_files):
    combined_file = '../tests/combined_tutorials.py'
    combined_content = ''
    # Read the content of each .py file and append it to the combined_content string
    for py_file in py_files:
        with open('../tests/' + py_file, 'r') as infile:
            for line in infile:
                # If the line is 'fig.show()\n', replace it with the new code
                if line == '    fig.show()\n':
                    combined_content += '    import plotly.io as pio\n'
                    combined_content += '    from datetime import datetime\n'
                    combined_content += '    pio.write_image(fig, datetime.now().strftime("figure__%d-%m-%Y__%H-%M-%S.png"))\n'
                    print("changed 'fig.show()' to write a png image")
                else:
                    # Otherwise, append the line as is to the combined_content string
                    combined_content += line
    # Write the combined content to the new file
    with open(combined_file, 'w') as outfile: outfile.write(combined_content)
    print(f'Combined {len(py_files)} .py files into {combined_file}')

def delete_py_files(py_files):
    # Delete the individual .py files
    for py_file in py_files:
        os.remove('../tests/' + py_file)
    print(f'Deleted {len(py_files)} .py files')

py_files = convert_ipynb_to_py()
combine_py_files(py_files)
delete_py_files(py_files)
