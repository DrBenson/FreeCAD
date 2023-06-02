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
   if [ -f "ReverseEngineering_$lang.ts" ]; then
      echo -e '\033[1;32m\n     <<< Update translation for '$lang' language >>> \n\033[m';
      # Creation of uifiles.ts file from ../*.ui files with designation of language code
#      lupdate6 ../preferences/*.ui -ts uifiles.ts -source-language en_US -target-language $lang -no-obsolete
      lupdate6 ../../*.ui -ts uifiles.ts -source-language en_US -no-obsolete
      pylupdate6 ../../../*.py -ts pyfiles.ts --verbose
      # Join uifiles.ts and pyfiles.ts files to ReverseEngineering.ts
      lconvert -i uifiles.ts pyfiles.ts -o ReverseEngineering.ts --verbose
      # Join ReverseEngineering.ts to exist ReverseEngineering_(language).ts file ( -no-obsolete)
      lconvert -i ReverseEngineeringOrg.ts ReverseEngineering.ts ReverseEngineering_zh-TW.po -o ReverseEngineering_$lang.ts -target-language zh_TW -sort-contexts --verbose
#      lconvert -i ReverseEngineering.ts ReverseEngineering_$lang.ts -o ReverseEngineering_$lang.po -of po -target-language $lang -sort-contexts
      lconvert -i ReverseEngineering.ts -o ReverseEngineering.pot -of pot -target-language en-US
      lconvert -i title.ts ReverseEngineering_zh-TW.ts -o ReverseEngineering_zh-TW.po -of po -target-language zh_TW --verbose
      # (Release) Creation of *.qm file from ReverseEngineering_(language).ts
      lrelease ReverseEngineering_$lang.ts
      # Delete unused files
#      rm uifiles.ts
      cd ..
      dir2qrc ReverseEngineering
      cd translations
      rm pyfiles.ts uifiles.ts
      # rm ReverseEngineering.ts
#      lconvert -i ReverseEngineering_$lang.po -if po -o ReverseEngineering.pot -of pot -source-language en_US -sort-contexts
   else
      echo -e '\033[1;33m\n     <<< Create files for added '$lang' language >>> \n\033[m';
      # Creation of uifiles.ts file from ../*.ui files with designation of language code
      lupdate ../*.ui -ts uifiles.ts -source-language en_US -target-language $lang -no-obsolete
      # Creation of pyfiles.ts file from ../*.py files
      pylupdate5 ../*.py -ts pyfiles.ts -verbose -source-language en_US -target-language $lang -no-obsolete
      # Join uifiles.ts and pyfiles.ts files to ReverseEngineering_$lang.ts
      lconvert -i uifiles.ts pyfiles.ts -o ReverseEngineering_$lang.ts
      # Delete unused files
#      rm uifiles.ts
      rm pyfiles.ts
   fi
done
