import discord

def get_server_settings(cursor, server_id):
    cursor.execute("SELECT * FROM server_settings WHERE server_id = ?", (server_id,))
    return cursor.fetchone()

def update_server_settings(cursor, db, server_id, **kwargs):
    current = get_server_settings(cursor, server_id)
    if current:
        for key, value in kwargs.items():
            if value is not None:
                cursor.execute(f"UPDATE server_settings SET {key} = ? WHERE server_id = ?", (value, server_id))
    else:
        cursor.execute("""
            INSERT INTO server_settings (
                server_id, owner, repo, workflow_file, github_token, notify_channel, max_uses_per_day, cooldown_time, use_session_cache
            ) VALUES (?, 'None', 'mcserverstarter', 'selenium.yml', '', 0, 3, 600, 0)
        """, (server_id,))
        update_server_settings(cursor, db, server_id, **kwargs)
    db.commit()

async def update_presence(bot):
    count = len(bot.guilds)
    activity = discord.Activity(
        type=discord.ActivityType.listening,
        name=f"{count} servers"
    )
    await bot.change_presence(activity=activity)
