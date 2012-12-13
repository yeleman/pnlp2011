#!/bin/bash

USERNAME="pnlp"
PASSWORD="pnlp"
DATABASE="pnlp"
BACKUP_FILE="pnlp_not_snisi.sql"
TMP_FILE="pnlp_not_snisi_modified.sql"

echo "Do you want to change DB ${DATABASE}? ^c if not."
read
clear

echo "Backing Up DB to ${BACKUP_FILE}"
mysqldump -u${USERNAME} -p${PASSWORD} ${DATABASE} > ${BACKUP_FILE}

echo "Creating a temporary ${TMP_FILE} file."
cp ${BACKUP_FILE} ${TMP_FILE}

echo "Replacing pnlp_* to snisi_* on ${TMP_FILE}"
sed -i 's/pnlp_core/snisi_core/g' ${TMP_FILE}
sed -i 's/pnlp_sms/snisi_sms/g' ${TMP_FILE}
sed -i 's/pnlp_web/snisi_web/g' ${TMP_FILE}

echo "Inserting modified DB dump into MySQL"
mysql -u${USERNAME} -p${PASSWORD} ${DATABASE} < ${TMP_FILE}