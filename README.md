# workflowtrigger_bot
Discord bot to trigger a github workflow

Setup this your server host or ur own server if u have. Am currently using [Serv00](https://www.serv00.com/). replit offers 20hrs per month, didn't try aws and oracle(they give free plan but ask credit card details) 

### Setup
#### Changes to be done to bot.py
(Don't remove double quotes, change content in it)

DISCORD_TOKEN = "MTM0NT1234567890"        # Create a bot in developer.discord there u will get it

GITHUB_TOKEN = "github_pat_1234567890"    # Go to  settings in profile > developer settings > personal access token > fine grain (there a image below if don't know what to set in it)

OWNER = "githubusername"                  # Change to ur username 

REPO = "mcserverstarter"                  # Change to the forked repo name

WORKFLOW_FILE = "selenium.yml"            # Maybe the file name is same if not then change


ALLOWED_SERVER_ID = 1234567890123456789  # Replace with your Discord server ID

NOTIFY_CHANNEL_ID = 1234567890123456789  # Channel where notification is sent (for workflow trigger logs) or just comment it out if not needed

#### Cooldown & daily limit system (in bot.py as well)
COOLDOWN_TIME = 600  # 600 seconds (10 minutes) cooldown per user

MAX_USES_PER_DAY = 6  # Limit per user per day

### Commands

run_mc        # Triggers REPO

users_usage   # Displays Usage of that day 

reset_usage   # Resets usage (it resets every 24 hrs but incase u need to)

#### Creating Personal access token
1) Expiration : no expiration

2) Repository access : all repositories (or the repo u want) 

3) Permissions : Actions (read and write); Workflow(read and write)
        
![PAT1](https://github.com/dibope/workflowtrigger_bot/blob/main/PAT1.jpg)
![PAT2](https://github.com/dibope/workflowtrigger_bot/blob/main/PAT2.jpg)
