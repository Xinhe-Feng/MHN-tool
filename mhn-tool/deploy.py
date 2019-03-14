import sys
sys.path.append(r'/home/recovery/mhn/server')



import os
from config import DEPLOY_KEY, SERVER_BASE_URL


os.system('sudo pip install celery')
os.system('sudo bash ~/mhn/scripts/deploy_cowrie.sh '+ SERVER_BASE_URL +' '+ DEPLOY_KEY)
os.system('sudo bash ~/mhn/scripts/deploy_p0f.sh '+ SERVER_BASE_URL +' '+ DEPLOY_KEY)
#os.system('sudo ~/mhn/scripts/deploy_conpot.sh '+ SERVER_BASE_URL +' '+ DEPLOY_KEY)
#os.system('sudo ~/mhn/scripts/deploy_snort.sh '+ SERVER_BASE_URL +' '+ DEPLOY_KEY)
os.system('sudo bash ~/mhn/scripts/deploy_amun.sh '+ SERVER_BASE_URL +' '+ DEPLOY_KEY)
os.system('sudo bash ~/mhn/scripts/deploy_elastichoney.sh '+ SERVER_BASE_URL +' '+ DEPLOY_KEY)
os.system('sudo bash ~/mhn/scripts/deploy_wordpot.sh '+ SERVER_BASE_URL +' '+ DEPLOY_KEY)
os.system('sudo ~/mhn/scripts/deploy_glastopf.sh '+ SERVER_BASE_URL +' '+ DEPLOY_KEY)
