# Instructions to get project up and running

## Create an account on SendGrid
  1. Create an account on [SendGrid](https://www.sendgrid.com)
  2. Copy your SendGrid username
  3. Log into your new SendGrid account
  4. Navigate to Settings >> API Keys in the left-hand pane
  5. Click Create API Key >> General API Key
  6. Give your new API Key a name and full access to Mail Send, then save
  7. Copy your newly created API Key ID
  
## Get started with pythonanywhere
  1. Create an account on [pythonanywhere](https://www.pythonanywhere.com)
  2. Enter your new account. Navigate to the Consoles tab, and start a bash session
  3. Run these commands to load your information into the environment:
  
  `cd ~ && echo "export SENDGRID_API_KEY='<SENDGRID API KEY HERE>'" >>.bashrc && . ~/.bashrc`
  
  `cd ~ && echo "export EMAIL='<EMAIL HERE>'" >>.bashrc && . ~/.bashrc`

  4. In the bash session run this command to download the repo from github: 
  
  `cd ~ && git clone <git clone link> && cd ~/<project folder>`
  
  5. To run the script manually, type this into the bash terminal:
  `cd ~/<project folder> && python run.py`
  
  6. To schedule the script to run manually, click the Schedule tab and insert this path:
  
  `~/<project folder>/run.py`
  
   For more information on scheduled tasks, [click here](https://help.pythonanywhere.com/pages/ScheduledTasks/)
  
## Troubleshooting
  * You must be in the folder PROJ FOLDER to run the script.  If you run the script and you get this error:
  
  `python: can't open file 'run.py': [Errno 2] No such file or directory`
  
   It's because you're in the wrong directory.  Enter this command:
  
  `cd ~/<project folder>/ && python run.py`
