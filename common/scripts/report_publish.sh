#!/bin/bash
set -e  # stop if something goes wrong...

# vars
REPORT_REPO="/var/jenkins_home/parabank_tests_reports"
SOURCE_REPORT="/var/jenkins_home/workspace/parabank_API_and_Front/allure-report"
FECHA=$(date +'%Y%m%d_%H%M')
echo "varaibles declaradas"

# move to reports repo
cd "$REPORT_REPO"
pwd

#clean old data except .git and .gitignore
rsync -av --delete --exclude='.git' --exclude='.gitignore' "$SOURCE_REPORT"/ .

echo "data cleaned"
#ls -las

#copi new data
cp -r "$SOURCE_REPORT"/* "$REPORT_REPO"
echo "new data copieda"
#ls -las

# git add, commit and push
pwd
#git status
git add .
git commit -m "Actualización automática del reporte $FECHA"
git push

echo "publish reports script finish"
