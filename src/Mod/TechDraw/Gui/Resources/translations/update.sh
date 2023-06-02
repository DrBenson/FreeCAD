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
   if [ -f "TechDraw_$lang.ts" ]; then
      echo -e '\033[1;32m\n     <<< Update translation for '$lang' language >>> \n\033[m';
      # Creation of uifiles.ts file from ../*.ui files with designation of language code
#      lupdate6 ../preferences/*.ui -ts uifiles.ts -source-language en_US -target-language $lang -no-obsolete
      lupdate6 ../../*.ui -ts uifiles.ts -source-language en_US -target-language zh_TW -no-obsolete
      pylupdate6 ../../../*.py ../../../TDTest/*.py ../../../TechDrawTools/*.py -ts pyfiles.ts --verbose
      # Join uifiles.ts and pyfiles.ts files to TechDraw.ts
      lconvert -i uifiles.ts pyfiles.ts -o TechDraw.ts --verbose
      # Join TechDraw.ts to exist TechDraw_(language).ts file ( -no-obsolete)
      lconvert -i TechDrawOrg.ts TechDraw.ts TechDraw_zh-TW.po -o TechDraw_$lang.ts -target-language zh_TW -sort-contexts --verbose
#      lconvert -i TechDraw.ts TechDraw_$lang.ts -o TechDraw_$lang.po -of po -target-language $lang -sort-contexts
      lconvert -i TechDraw.ts -o TechDraw.pot -of pot -target-language en-US
      lconvert -i title.ts TechDraw_zh-TW.ts -o TechDraw_zh-TW.po -of po -target-language zh_TW --verbose
      # (Release) Creation of *.qm file from TechDraw_(language).ts
      lrelease TechDraw_$lang.ts
      # Delete unused files
#      rm uifiles.ts
      cd ..
      dir2qrc TechDraw
      cd translations
      rm pyfiles.ts uifiles.ts
      # rm TechDraw.ts
#      lconvert -i TechDraw_$lang.po -if po -o TechDraw.pot -of pot -source-language en_US -sort-contexts
   else
      echo -e '\033[1;33m\n     <<< Create files for added '$lang' language >>> \n\033[m';
      # Creation of uifiles.ts file from ../*.ui files with designation of language code
      lupdate ../*.ui -ts uifiles.ts -source-language en_US -target-language $lang -no-obsolete
      # Creation of pyfiles.ts file from ../*.py files
      pylupdate5 ../*.py -ts pyfiles.ts -verbose -source-language en_US -target-language $lang -no-obsolete
      # Join uifiles.ts and pyfiles.ts files to TechDraw_$lang.ts
      lconvert -i uifiles.ts pyfiles.ts -o TechDraw_$lang.ts
      # Delete unused files
#      rm uifiles.ts
      rm pyfiles.ts
   fi
done
