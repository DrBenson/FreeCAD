#!/bin/bash
#
# Tested in Ubuntu 20.04.2 LTS.
# This script must strictly contain line endings in Linux format for correct work.
# Install QT5 dev tools packages before run this script, by the following commands:
#
# sudo apt update
# sudo apt install -y qttools5-dev-tools
# sudo apt install -y pyqt5-dev-tools
#
# This is array of supported languages. New languages, must be added to it.
languages=(zh-TW)
for lang in ${languages[*]}
do
   # Check if fastners_$lang.ts exist
   if [ -f "Mesh_$lang.ts" ]; then
      echo -e '\033[1;32m\n     <<< Update translation for '$lang' language >>> \n\033[m';
      # Creation of uifiles.ts file from ../*.ui files with designation of language code
      pylupdate6 ../../*.ui -ts uifiles.ts --verbose
      pylupdate6 ../../../*.py ../../../App/*.py -ts pyfiles.ts --verbose
      lconvert -i uifiles.ts pyfiles.ts -o Mesh.ts --verbose
      # Join Mesh.ts to exist Mesh_(language).ts file ( -no-obsolete)
      lconvert -i MeshOrg.ts Mesh.ts Mesh_$lang.po -o Mesh_$lang.ts -target-language zh_TW -sort-contexts --verbose
#      lconvert -i Mesh.ts Mesh_$lang.ts -o Mesh_$lang.po -of po -target-language $lang -sort-contexts
      lconvert -i title.ts Mesh_zh-TW.ts -o Mesh_zh-TW.po -of po -target-language zh_TW --verbose
      # (Release) Creation of *.qm file from Mesh_(language).ts
      lrelease Mesh_$lang.ts
      # Delete unused files
#      rm uifiles.ts
      cd ..
#      dir2qrc Mesh
      cd translations
      rm pyfiles.ts uifiles.ts
      # rm Mesh.ts
#      lconvert -i Mesh_$lang.po -if po -o Mesh.pot -of pot -source-language en_US -sort-contexts
   else
      echo -e '\033[1;33m\n     <<< Create files for added '$lang' language >>> \n\033[m';
      # Creation of uifiles.ts file from ../*.ui files with designation of language code
      lupdate ../*.ui -ts uifiles.ts -source-language en_US -target-language $lang -no-obsolete
      # Creation of pyfiles.ts file from ../*.py files
      lupdate ../../../*.py -ts pyfiles.ts -verbose -source-language en_US -no-obsolete
      # Join uifiles.ts and pyfiles.ts files to Mesh_$lang.ts
      lconvert -i uifiles.ts pyfiles.ts -o Mesh_$lang.ts
      # Delete unused files
#      rm uifiles.ts
      rm pyfiles.ts
   fi
done
