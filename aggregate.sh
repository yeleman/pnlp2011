#!/bin/bash

source /home/reg/src/envs/pnlp/bin/activate


# importer la base PNLP
# supprimer Alerts: 11, 12, 01 ()
# Supprimer:
# - CIV: tous
# - CV: tous
# Bamako: tous
# Mali: tous
# lancer import excel
# lancer agregate

# 16/08
date `python -c "import datetime; print datetime.datetime.now().strftime('0816%H%M2011')"`
./manage.py pnlp_daily_tasks

# 26/08
date `python -c "import datetime; print datetime.datetime.now().strftime('0826%H%M2011')"`
./manage.py pnlp_daily_tasks
./manage.py pnlp_daily_tasks

# 16/09
date `python -c "import datetime; print datetime.datetime.now().strftime('0916%H%M2011')"`
./manage.py pnlp_daily_tasks

# 26/09
date `python -c "import datetime; print datetime.datetime.now().strftime('0926%H%M2011')"`
./manage.py pnlp_daily_tasks
./manage.py pnlp_daily_tasks

# 16/10
date `python -c "import datetime; print datetime.datetime.now().strftime('1016%H%M2011')"`
./manage.py pnlp_daily_tasks

# 26/10
date `python -c "import datetime; print datetime.datetime.now().strftime('1026%H%M2011')"`
./manage.py pnlp_daily_tasks
./manage.py pnlp_daily_tasks

# 16/11
date `python -c "import datetime; print datetime.datetime.now().strftime('1116%H%M2011')"`
./manage.py pnlp_daily_tasks

# 26/11
date `python -c "import datetime; print datetime.datetime.now().strftime('1126%H%M2011')"`
./manage.py pnlp_daily_tasks
./manage.py pnlp_daily_tasks

# 16/12
date `python -c "import datetime; print datetime.datetime.now().strftime('1216%H%M2011')"`
./manage.py pnlp_daily_tasks

# 26/12
date `python -c "import datetime; print datetime.datetime.now().strftime('1226%H%M2011')"`
./manage.py pnlp_daily_tasks
./manage.py pnlp_daily_tasks

# 16/01
date `python -c "import datetime; print datetime.datetime.now().strftime('0116%H%M2012')"`
./manage.py pnlp_daily_tasks

# 26/01
date `python -c "import datetime; print datetime.datetime.now().strftime('0126%H%M2012')"`
./manage.py pnlp_daily_tasks
./manage.py pnlp_daily_tasks

# 16/02
date `python -c "import datetime; print datetime.datetime.now().strftime('0216%H%M2012')"`
./manage.py pnlp_daily_tasks

# 26/02
date `python -c "import datetime; print datetime.datetime.now().strftime('0226%H%M2012')"`
./manage.py pnlp_daily_tasks
./manage.py pnlp_daily_tasks

echo "FIN."
ntpdate-debian