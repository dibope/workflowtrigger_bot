import discord
import requests
import os
from discord.ext import commands, tasks
from collections import defaultdict
from datetime import datetime, timedelta

# Load tokens from environment variables (replace these with real values)
DISCORD_TOKEN = "MTM0NT1234567890"        #yo bot token
GITHUB_TOKEN = "github_pat_1234567890"    #yo personal access token
OWNER = "dibope"
REPO = "mcserverstarter"
WORKFLOW_FILE = "selenium.yml"

# Allowed server ID
ALLOWED_SERVER_ID = 1234567890123456789  # Replace with your Discord server ID
NOTIFY_CHANNEL_ID = 1234567890123456789  # Channel where notification is sent (for workflow trigger logs) or just comment it out if not needed

# Intents for the bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Cooldown & daily limit system
COOLDOWN_TIME = 600  # 600 seconds (10 minutes) cooldown per user
MAX_USES_PER_DAY = 6  # Limit per user per day
user_cooldowns = {}  # Tracks last use time
user_usage = defaultdict(int)  # Tracks daily usage count
last_reset = datetime.utcnow()  # Track when the usage was last reset

def reset_daily_usage():
    """Resets the usage count every 24 hours."""
    global last_reset, user_usage
    now = datetime.utcnow()
    if now - last_reset >= timedelta(days=1):
        user_usage.clear()
        last_reset = now

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    reset_usage_task.start()  # Start automatic daily reset
    
    try:
        await bot.tree.sync()  # ✅ Await the sync command
        print("✅ Slash commands synced!")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

@tasks.loop(hours=24)
async def reset_usage_task():
    """Scheduled task to reset daily usage every 24 hours."""
    reset_daily_usage()
    print("✅ Daily usage count has been reset.")

@bot.tree.command(name="reset_usage", description="Reset all users' usage count")
async def reset_usage(ctx: discord.Interaction):
    if ctx.guild is None or ctx.guild.id != ALLOWED_SERVER_ID:
        await ctx.response.send_message("🚫 This command can only be used in the authorized server.", ephemeral=True)
        return
    
    user_usage.clear()
    await ctx.response.send_message("🔄 All users' usage counts have been reset.", ephemeral=True)
    print("✅ Manual usage reset triggered.")

@bot.tree.command(name="users_usage", description="View all users' usage count")
async def users_usage(ctx: discord.Interaction):
    if ctx.guild is None or ctx.guild.id != ALLOWED_SERVER_ID:
        await ctx.response.send_message("🚫 This command can only be used in the authorized server.", ephemeral=False)
        return
    
    usage_report = "\n".join([f"<@{user_id}>: {count} uses" for user_id, count in user_usage.items()])
    if not usage_report:
        usage_report = "No usage data available."
    
    await ctx.response.send_message(f"📊 **Users' Usage Counts:**\n{usage_report}", ephemeral=True)

@bot.tree.command(name="run_mc", description="Trigger a GitHub Actions workflow to start the MC server")
async def run_mc(ctx: discord.Interaction):
    user_id = ctx.user.id

    # Ensure command is only used in the allowed server
    if ctx.guild is None or ctx.guild.id != ALLOWED_SERVER_ID:
        await ctx.response.send_message("🚫 This command can only be used in the authorized server.", ephemeral=True)
        return

    # Reset usage count if needed
    reset_daily_usage()

    # Check if user exceeded daily limit
    if user_usage[user_id] >= MAX_USES_PER_DAY:
        await ctx.response.send_message("🚫 You have reached the daily limit for this command (6 times per day).", ephemeral=True)
        return

    # Check cooldown
    last_used = user_cooldowns.get(user_id, 0)
    remaining_time = COOLDOWN_TIME - (discord.utils.utcnow().timestamp() - last_used)
    
    if remaining_time > 0:
        await ctx.response.send_message(f"⏳ You must wait {int(remaining_time)} more seconds before using this command again.", ephemeral=True)
        return

    # Call GitHub Actions API
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{WORKFLOW_FILE}/dispatches"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"ref": "main"}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 204:
        user_cooldowns[user_id] = discord.utils.utcnow().timestamp()  # Apply cooldown
        user_usage[user_id] += 1  # Count this usage
        await ctx.response.send_message(f"✅ Will be started in 50 secs You have {MAX_USES_PER_DAY - user_usage[user_id]} uses left today.", ephemeral=True)
        notify_channel = bot.get_channel(NOTIFY_CHANNEL_ID)
        if notify_channel:
            await notify_channel.send(f"{ctx.user.name} has invoked **run_mc** command")
        else:
            print("unable to send logs")

    else:
        await ctx.response.send_message(f"❌ Failed to trigger workflow: {response.text}", ephemeral=True)

bot.run(DISCORD_TOKEN)
