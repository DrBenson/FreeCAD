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
   if [ -f "Drawing_$lang.ts" ]; then
      echo -e '\033[1;32m\n     <<< Update translation for '$lang' language >>> \n\033[m';
      # Creation of uifiles.ts file from ../*.ui files with designation of language code
      pylupdate6 ../../*.ui -ts uifiles.ts --verbose
      pylupdate6 ../../../*.py -ts pyfiles.ts --verbose
      lconvert -i uifiles.ts pyfiles.ts -o Drawing.ts --verbose
      # Join Drawing.ts to exist Drawing_(language).ts file ( -no-obsolete)
      lconvert -i DrawingOrg.ts Drawing.ts Drawing_$lang.po -o Drawing_$lang.ts -target-language zh_TW -sort-contexts --verbose
#      lconvert -i Drawing.ts Drawing_$lang.ts -o Drawing_$lang.po -of po -target-language $lang -sort-contexts
      lconvert -i title.ts Drawing_zh-TW.ts -o Drawing_zh-TW.po -of po -target-language zh_TW --verbose
      # (Release) Creation of *.qm file from Drawing_(language).ts
      lrelease Drawing_$lang.ts
      # Delete unused files
#      rm uifiles.ts
      cd ..
      dir2qrc Drawing
      cd translations
      rm pyfiles.ts uifiles.ts
      # rm Drawing.ts
#      lconvert -i Drawing_$lang.po -if po -o Drawing.pot -of pot -source-language en_US -sort-contexts
   else
      echo -e '\033[1;33m\n     <<< Create files for added '$lang' language >>> \n\033[m';
      # Creation of uifiles.ts file from ../*.ui files with designation of language code
      lupdate ../*.ui -ts uifiles.ts -source-language en_US -target-language $lang -no-obsolete
      # Creation of pyfiles.ts file from ../*.py files
      pylupdate5 ../*.py -ts pyfiles.ts -verbose -source-language en_US -target-language $lang -no-obsolete
      # Join uifiles.ts and pyfiles.ts files to Drawing_$lang.ts
      lconvert -i uifiles.ts pyfiles.ts -o Drawing_$lang.ts
      # Delete unused files
#      rm uifiles.ts
      rm pyfiles.ts
   fi
done
