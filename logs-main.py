""" 
Reads audit log of guild and dumps it into a json file 
invoked with "$fetch_logs 100" in a discord chat
you need to create a file "output.json" first or it wont work
"""

import argparse
import asyncio
import json
import sys

import discord
from discord.ext import commands

try:
    from auth import token
except ImportError:
    token = None # add your discord api token here: looks like "abcdefghijklmnopqrstuvwx.abcdef.-abcdefghijklmnopqrstuvwxyz" can have integers in it

bot = commands.Bot(command_prefix = "$")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}, user_id = {bot.user.id}")


@bot.command()
async def fetch_logs(ctx, arg = 100):
    audit = []
    print("Fetching Logs...")
    async for entry in ctx.guild.audit_logs(limit = arg):
        log_entry = {
            "action": str(entry.action),
            "user": str(entry.user.name),
            "EntryID": int(entry.id),
            "Reason": str(entry.reason),
            "creation_time": str(entry.created_at),
            "target": str(entry.target)
        }
        audit.append(log_entry)
        print(log_entry)
    print("Dumping Logs...")
    json_object = json.dumps(audit, indent= 4)
    with open("output.json", "w") as outfile:
        outfile.write(json_object)

if __name__ == "__main__":
    try:
        bot.run(token)
    except discord.LoginFailure:
        sys.exit("Token doesnt work")
