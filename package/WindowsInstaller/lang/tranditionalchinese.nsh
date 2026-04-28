!macro LANG LANG_NAME
  # NSIS language file
  !insertmacro MUI_LANGUAGE "${LANG_NAME}"
  # FreeCAD language file
  !insertmacro LANGFILE_INCLUDE_WITHDEFAULT "lang\${LANG_NAME}.nsh" "lang\english.nsh"
!macroend

# list of all languages the installer is translated to
!insertmacro LANG "tranditionalchinese"
!insertmacro LANGFILE_EXT "繁體中文 (Tranditional-Chinese)"

${LangFileString} TEXT_INSTALL_CURRENTUSER "(為目前使用者安裝)"

${LangFileString} TEXT_WELCOME "此精靈將引導您完成安裝 $(^NameDA). $\r$\n\
				$\r$\n\
				$_CLICK"

#${LangFileString} TEXT_CONFIGURE_PYTHON "編譯 Python 腳本..."

${LangFileString} TEXT_FINISH_DESKTOP "建立桌面捷徑"
${LangFileString} TEXT_FINISH_WEBSITE "請造訪 freecad.org/ 獲取最新消息、技術支援與實用技巧"

#${LangFileString} FileTypeTitle "FreeCAD-文件"

#${LangFileString} SecAllUsersTitle "為所有使用者安裝?"
${LangFileString} SecFileAssocTitle "檔案關聯"
${LangFileString} SecDesktopTitle "桌面圖示"

${LangFileString} SecCoreDescription "FreeCAD 檔案."
#${LangFileString} SecAllUsersDescription "為所有使用者安裝 FreeCAD，或僅安裝給目前的使用者."
${LangFileString} SecFileAssocDescription "副檔名為 .FCStd 的檔案將自動在 FreeCAD 中開啟."
${LangFileString} SecDesktopDescription "桌面上的 FreeCAD 圖示."
#${LangFileString} SecDictionaries "字典"
#${LangFileString} SecDictionariesDescription "可下載並安裝的拼字檢查字典."

#${LangFileString} PathName '檔案路徑 $\"xxx.exe$\"'
#${LangFileString} InvalidFolder '檔案 $\"xxx.exe$\" 不在指定的路徑中.'

#${LangFileString} DictionariesFailed '無法下載語言 $\"$R3$\" 字典.'

#${LangFileString} ConfigInfo "以下 FreeCAD 的設定可能需要一些時間."

#${LangFileString} RunConfigureFailed "無法執行 參數設定(configure) 腳本."
${LangFileString} InstallRunning "安裝程式已經在執行中!"
${LangFileString} AlreadyInstalled "FreeCAD ${APP_SERIES_KEY2} 已安裝!$\r$\n\
				若您目前安裝的版本為測試版，或現有 FreeCAD 安裝出現問題，則不建議直接覆蓋安裝.$\r$\n\
				在這些情況下，建議重新安裝 FreeCAD.$\r$\n\
				您是否仍要覆蓋安裝現有版本 FreeCAD?"
${LangFileString} NewerInstalled "Y您正嘗試安裝比現有版本更舊的 FreeCAD 版本.$\r$\n\
				  若您確實需要這樣做，必須先解除安裝現有的 FreeCAD $OldVersionNumber 版本."

#${LangFileString} FinishPageMessage "恭喜您! FreeCAD 已成功安裝.$\r$\n\
#					$\r$\n\
#					(首次啟動 FreeCAD 可能需要一點點時間.)"
${LangFileString} FinishPageRun "啟動 FreeCAD"

${LangFileString} UnNotInRegistryLabel "無法在登錄檔中找到 FreeCAD.$\r$\n\
					桌面及「開始」選單中的捷徑將不會被移除."
${LangFileString} UnInstallRunning "您必須先關閉 FreeCAD!"
${LangFileString} UnNotAdminLabel "您必須具備管理員權限才能解除安裝 FreeCAD!"
${LangFileString} UnReallyRemoveLabel "您確定要完全移除 FreeCAD 及其所有元件嗎?"
${LangFileString} UnFreeCADPreferencesTitle 'FreeCAD 的使用者偏好設定'

#${LangFileString} SecUnProgDescription "解除安裝 xxx."
${LangFileString} SecUnPreferencesDescription '刪除 FreeCAD 的設定$\r$\n\
						(目錄 $\"$AppPre\username\$\r$\n\
						$AppSuff\$\r$\n\
						${APP_DIR_USERDATA}$\")$\r$\n\
						針對您，或針對所有使用者(如果您是管理員).'
${LangFileString} DialogUnPreferences '您選擇刪除 FreeCAD 使用者設定.$\r$\n\
						此操作也會刪除所有已安裝的 FreeCAD 外掛程式，並會影響所有版本 FreeCAD 的偏好設定.$\r$\n\
						您確定要繼續?'
${LangFileString} SecUnProgramFilesDescription "解除安裝 FreeCAD 及其所有元件."
