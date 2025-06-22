#!/bin/bash
set -e  # stop if something goes wrong...

# vars
REPORT_REPO="/var/jenkins_home/parabank_tests_reports"
SOURCE_REPORT="/var/jenkins_home/workspace/parabank_API_and_Front/allure-report"
FECHA=$(date +'%Y%m%d_%H%M')

# move to reports repo
cd "$REPORT_REPO"

#clean old data except .git and .gitignore
find . -mindepth 1 ! -name '.git' ! -name '.gitignore' -exec rm -rf {} +

#copi new data
cp -r "$SOURCE_REPORT"/* "$REPORT_REPO"

# git add, commit and push
git add .
git commit -m "Actualización automática del reporte $FECHA"
git push
