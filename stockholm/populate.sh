#!/bin/bash

TARGET_DIR=~/infection
mkdir -p "$TARGET_DIR"

rm -f "$TARGET_DIR"/*

file_extensions=(
    ".der" ".pfx" ".key" ".crt" ".csr" ".p12" ".pem" ".odt" ".ott" 
    ".sxw" ".stw" ".uot" ".3ds" ".max" ".3dm" ".ods" ".ots" ".sxc" 
    ".stc" ".dif" ".slk" ".wb2" ".odp" ".otp" ".sxd" ".std" ".uop" 
    ".odg" ".otg" ".sxm" ".mml" ".lay" ".lay6" ".asc" ".sqlite3" 
    ".sqlitedb" ".sql" ".accdb" ".mdb" ".db" ".dbf" ".odb" ".frm" 
    ".myd" ".myi" ".ibd" ".mdf" ".ldf" ".sln" ".suo" ".cs" ".c" 
    ".cpp" ".pas" ".h" ".asm" ".js" ".cmd" ".bat" ".ps1" ".vbs" 
    ".vb" ".pl" ".dip" ".dch" ".sch" ".brd" ".jsp" ".php" ".asp" 
    ".rb" ".java" ".jar" ".class" ".sh" ".mp3" ".wav" ".swf" ".fla" 
    ".wmv" ".mpg" ".vob" ".mpeg" ".asf" ".avi" ".mov" ".mp4" ".3gp" 
    ".mkv" ".3g2" ".flv" ".wma" ".mid" ".m3u" ".m4u" ".djvu" ".svg" 
    ".ai" ".psd" ".nef" ".tiff" ".tif" ".cgm" ".raw" ".gif" ".png" 
    ".bmp" ".jpg" ".jpeg" ".vcd" ".iso" ".backup" ".zip" ".rar" ".7z" 
    ".gz" ".tgz" ".tar" ".bak" ".tbk" ".bz2" ".PAQ" ".ARC" ".aes" 
    ".gpg" ".vmx" ".vmdk" ".vdi" ".sldm" ".sldx" ".sti" ".sxi" ".602" 
    ".hwp" ".snt" ".onetoc2" ".dwg" ".pdf" ".wk1" ".wks" ".123" ".rtf" 
    ".csv" ".txt" ".vsdx" ".vsd" ".edb" ".eml" ".msg" ".ost" ".pst" 
    ".potm" ".potx" ".ppam" ".ppsx" ".ppsm" ".pps" ".pot" ".pptm" 
    ".pptx" ".ppt" ".xltm" ".xltx" ".xlc" ".xlm" ".xlt" ".xlw" ".xlsb" 
    ".xlsm" ".xlsx" ".xls" ".dotx" ".dotm" ".dot" ".docm" ".docb" 
    ".docx" ".doc"
)

for ext in "${file_extensions[@]}"; do
    uuid=$(uuidgen)
    
    file_path="$TARGET_DIR/example$ext"
    echo -e "UUID: $uuid\nThis is a test file with extension $ext" > "$file_path"
done

echo "Files with UUIDs and messages have been created in $TARGET_DIR."
