from __future__ import print_function 
import os, sys
import fileinput
import re

rootdir = './'
imagedir = '/images/'
exceptions = ['a', 'an', 'of', 'the', 'is']

def _removeCaption(filename):
    '''
    Removes the captions from figures
    '''
    leave_out = []
    out = open('tmpfile', 'w')
    with open(filename, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i not in leave_out:
                out.write(line)
                inp = line.split()
                if len(inp) == 3 and inp[1] == 'figure::':
                    # Scan the next 7 lines to look for a break indicating a caption
                    for j in range(i, i+7):
                        if len(lines[j].split()) == 0 and \
                        lines[j+1].startswith('   '):
                            # Add lines to the list of lines to skip
                            leave_out.append(j + 1)
                            leave_out.append(j + 2)
                            break
    out.close()
    cmd = 'mv tmpfile %s' % filename
    os.system(cmd)



def _makeLabel(filename):
    '''
    Adds a label at the top of the file
    '''
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        name = filename.split('/')[-1].split('.')[0]
        f.write('.. _%s:' % name + '\n' + '\n')
        heading = titleCase(name, exceptions)
        f.write('%s' % '=' * len(heading))
        f.write('\n')
        f.write('%s \n' % heading )
        f.write('%s' % '=' * len(heading))
        f.write('\n')
        f.write('\n')
        f.write(content)

def removeLines(file, pattern):
    '''
    Remove lines with a certain pattern
    '''
    for line in fileinput.input(file, inplace=1):
        if pattern not in line:
            sys.stdout.write(line)

def replaceAll(file, searchExp, replaceExp):
    '''
    A function to find and replace text in a file
    '''
    for line in fileinput.input(file, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)

def titleCase(string, exceptions):
    '''
    Converts a file name to a heading
    Args:
        string: the file name, expects underscore word separation
        exceptions: words not to capitalise if they are not first in the title
    '''

    string = re.sub(r'[^a-zA-Z_]+', '', string)         # Remove non-alphanumeric characters
    if len(string) > 0:
        word_list = re.split('_', string)       # re.split behaves as expected
        final = [word_list[0].capitalize()]
        for word in word_list[1:]:
            final.append(word if word in exceptions else word.capitalize())
        return " ".join(final)
    else:
        return "NULL"

def makeIndex(directory, header_text=""):
    '''
    Builds an index.rst file in a directory
    Args:
        directory: the target directory (string)
        header_text: Any free text that you want at the top of the page (string)
    '''

    files = [f for f in os.listdir(directory) if 
            os.path.isfile(os.path.join(directory, f)) and f.endswith('.rst')]

    indexfile = os.path.join(directory, 'index.rst')
    with open(indexfile, 'w') as f:
        heading = titleCase(directory, exceptions)
        f.write('.. _%s: \n' % directory[2:])
        f.write('\n')
        f.write('%s' % '='*len(heading))
        f.write('\n')
        f.write('%s \n' % heading)
        f.write('%s' % '='*len(heading))
        f.write('\n')
        f.write('\n')
        f.write('%s \n' % '.. toctree::')
        f.write('%s \n' % '   :hidden:')
        f.write('%s \n' % '   :glob:')
        f.write('%s \n' % '   :maxdepth: 1')
        f.write('\n')
        for file in sorted(files):
            f.write('   %s\n' % file.split('.')[0])
        f.write('\n')
        f.write('%s \n' % "**Sections**")
        f.write('\n')
        for file in sorted(files):
            f.write('* :ref:`%s`\n' % file.split('.')[0])
        f.write('\n')

# Build the list of the directories
directories = []
for subdir, dirs, files in os.walk(rootdir):
    if subdir not in directories:
        directories.append(subdir)

# Do pandoc conversion 

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file.endswith('.wiki'):
            outputfile = "%s.rst" % os.path.join(subdir, file.split('.')[0])
            inputfile = os.path.join(subdir, file)
            command = "pandoc %s -f mediawiki -t rst -s -o %s " % \
                      (inputfile, outputfile)
            os.system(command)
            replaceAll(outputfile, '.. figure:: ', '.. figure:: %s' % imagedir)
            replaceAll(outputfile, ' image:: ', ' image:: %s' % imagedir)
            _removeCaption(outputfile)
            _makeLabel(outputfile)


# Create an index.rst in each directory
for directory in directories:
    makeIndex(directory) 
