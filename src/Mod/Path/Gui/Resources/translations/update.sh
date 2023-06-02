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
   if [ -f "Path_$lang.ts" ]; then
      echo -e '\033[1;32m\n     <<< Update translation for '$lang' language >>> \n\033[m';
      # Creation of uifiles.ts file from ../*.ui files with designation of language code
      lupdate6 ../preferences/*.ui ../../*.ui -ts uifiles.ts -source-language en_US -no-obsolete
      pylupdate6  ../../../*.py ../../../Path/*.py ../../../Path/Base/*.py ../../../Path/Base/Generator/*.py \
                 ../../../Path/Base/Gui/*.py ../../../Path/Dressup/*.py ../../../Path/Dressup/Gui/*.py \
                 ../../../Path/Main/*.py ../../../Path/Main/Gui/*.py ../../../Path/Op/*.py \
                 ../../../Path/Op/Gui/*.py ../../../Path/Post/*.py ../../../Path/Post/scripts/*.py \
                 ../../../Path/Tool/*.py ../../../Path/Tool/Gui/*.py ../../../PathPythonGui/*.py \
                 ../../../PathScripts/*.py ../../../PathTests/*.py ../../../Tools/*.py -ts pyfiles.ts  -no-obsolete --verbose
      # Join uifiles.ts and pyfiles.ts files to Path.ts
      lconvert -i uifiles.ts pyfiles.ts -o Path.ts --verbose
      # Join Path.ts to exist Path_(language).ts file ( -no-obsolete)
      lconvert -i PathOrg.ts Path.ts Path_zh-TW.po -o Path_$lang.ts -target-language zh_TW -sort-contexts --verbose
#      lconvert -i Path.ts Path_$lang.ts -o Path_$lang.po -of po -target-language $lang -sort-contexts
      lconvert -i Path.ts -o Path.pot -of pot -target-language en-US
      lconvert -i title.ts Path_zh-TW.ts  -o Path_zh-TW.po -of po -target-language zh_TW --verbose
      # (Release) Creation of *.qm file from Path_(language).ts
      lrelease Path_$lang.ts
      # Delete unused files
#      rm uifiles.ts
      cd ..
#      dir2qrc Path
      cd translations
      rm pyfiles.ts uifiles.ts
      # rm Path.ts
#      lconvert -i Path_$lang.po -if po -o Path.pot -of pot -source-language en_US -sort-contexts
   else
      echo -e '\033[1;33m\n     <<< Create files for added '$lang' language >>> \n\033[m';
      # Creation of uifiles.ts file from ../*.ui files with designation of language code
      lupdate ../*.ui -ts uifiles.ts -source-language en_US -target-language $lang -no-obsolete
      # Creation of pyfiles.ts file from ../*.py files
      pylupdate5 ../*.py -ts pyfiles.ts -verbose -source-language en_US -target-language $lang -no-obsolete
      # Join uifiles.ts and pyfiles.ts files to Path_$lang.ts
      lconvert -i uifiles.ts pyfiles.ts -o Path_$lang.ts
      # Delete unused files
#      rm uifiles.ts
      rm pyfiles.ts
   fi
done
