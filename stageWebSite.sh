#!/bin/bash
# (use "chmod +rx scriptname" to make script executable)
#
# This script builds the HTML pages for the complete SKIRT project web site,
# including the documentation for SKIRT and PTS versions 8 and 9, as well as
# information common to both versions. The resulting directory and file tree
# can be copied (published) directly to the SKIRT web site server.
#
# This script DOES NOT stage downloadable/viewable data files (other than images
# that form an integral part of the documentation). Because of size restrictions
# on the UGent web site server and in GitHub repositories, these data files are
# provided for download from a seperate server.
#
# Instructions:
#   - use on Mac OS X only
#   - check out the relevant repositories next to this one (see below)
#   - run this script with the directory in which it resides as the current directory
#
# The script requires that the most recent version of the following repositories
# are checked out, next to each other in a common parent directory:
#  - PTS
#  - PTS9
#  - SKIRT8
#  - SKIRT9
#  - Web8
#  - Web9
#
# This script resides in the Web9/git directory and should be executed with that
# directory as the current directory. The resulting HTML pages are placed inside
# the Web9/stage directory (which is created if necessary). All internal links are
# relative so they can be tested locally on the staged copy before pulishing.
# Links to downloadable/viewable data files are absolute because these files are
# provided on a seperate server. Assuming the data files are properly published to
# that server, these links can be tested locally on the staged copy as well.
#

# Generate html documentation in the staging area next to our git folder
mkdir -p ../stage
/Applications/Doxygen.app/Contents/Resources/doxygen staging/html_root.doxygen
/Applications/Doxygen.app/Contents/Resources/doxygen staging/html_version8.doxygen
/Applications/Doxygen.app/Contents/Resources/doxygen staging/html_skirt8.doxygen
/Applications/Doxygen.app/Contents/Resources/doxygen staging/html_pts8.doxygen
/Applications/Doxygen.app/Contents/Resources/doxygen staging/html_version9.doxygen
/Applications/Doxygen.app/Contents/Resources/doxygen staging/html_skirt9.doxygen
/Applications/Doxygen.app/Contents/Resources/doxygen staging/html_pts9.doxygen

# Copy the 'mouse over' SKIRT logo
cp staging/SkirtLogoSmall-home.png ../stage/root/
cp staging/SkirtLogoSmall-home.png ../stage/version8/
cp staging/SkirtLogoSmall-home.png ../stage/skirt8/
cp staging/SkirtLogoSmall-home.png ../stage/pts8/
cp staging/SkirtLogoSmall-home.png ../stage/version9/
cp staging/SkirtLogoSmall-home.png ../stage/skirt9/
cp staging/SkirtLogoSmall-home.png ../stage/pts9/

# Copy redirecting index.html file
cp staging/index_root.html ../stage/index.html

# Obtain the MathJax repository if it is not yet present
if [ ! -d ../stage/mathjax ]; then

    # Clone the repository and checkout version 2.4
    git clone git://github.com/mathjax/MathJax.git ../stage/mathjax
    git -C ../stage/mathjax checkout -b v2.4-latest origin/v2.4-latest

    # Remove unnecessary files and folders
    xargs -I fname rm -r fname < staging/mathjax_delete.txt

fi
