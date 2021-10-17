import discord
import re

from discord.ext import commands

# color constants

COLOR_GREEN = 0x739957
COLOR_YELLOW = 0xedb313
COLOR_RED = 0xed1b2e
COLOR_BLUE = 0x0096FF


class FirstAid(commands.Cog):
    # constructor
    def __init__(self, bot):
        self.bot = bot
        self.conditions = [
            [
                "Heart Attack",
                [
                    "Fast heart rate", "Pale skin", "Blue/Purple Spots",
                    "Hyperventilation", "Weak Pulse", "Weakness", "Nausea",
                    "Vomiting", "Yawning", "Chest Pain", "Chest Tightness"
                ],
                [
                    "Phone EMS Immediately",
                    "Position Into a Semi-Sitting Position",
                    "Loosen Tight Clothing Around the Neck and Chest",
                    "Take Prescribed Medication (like Nitroglycerin) If Available",
                    "If No Prescription Medications are Available, 1 Adult Tablet or 2 Low Dose Tablets of Aspirin Can Be Used"
                ]
            ],
            [
                "Stroke",
                [
                    "Headache", "Numbness on one Side of Body",
                    "Slurred Speech", "Dizziness", "Blurred Vision"
                ],
                [
                    "Phone EMS Immediately",
                    "Don't do Anything and Wait Until EMS Arrives",
                    "Take Note of Time Since Stroke Start",
                    "Perform CPR If Necassary"
                ]
            ],
            [
                "Seizure",
                [
                    "Staring", "Jerky Movements", "Rapid Blinking",
                    "Loss of Bladder Control", "Loss of Bowel Control"
                ],
                [
                    "Semi-Prone Position",
                    "Phone EMS Immediately If Victim's not Breathing for More Than 30 Seconds",
                    "Phone EMS if Seizure is Longer than 5 Minutes",
                    "https://youtu.be/Ovsw7tdneqE?t=61"
                ]
            ],
            [
                "Anaphylaxis",
                [
                    "Hives", "Itching", "Pale Skin", "Hypotension",
                    "Swollen Tongue", "Swollen Throat", "Fast Heart Rate",
                    "Nausea", "Vomiting", "Diarrhea", "Dizziness"
                ],
                [
                    "Phone EMS Immediately", "Epipen",
                    "Blue to the Sky, Orange to the Thigh",
                    "https://youtu.be/K7QyCMNDHAs?t=35"
                ]
            ],
            [
                "Choking",
                [
                    "Coughing", "Throat Pain", "Neck Pain", "Gagging",
                    "Chest Pain", "Red Face", "Inability to Speak",
                    "Blue/Purple Spots"
                ],
                [
                    "Encourage Coughing",
                    "Give 5 Back Blows, 5 J Thrusts If Airway is Fully OBstructed",
                    "Phone EMS Immediately If Victim Goes Unconcious"
                ]
            ],
            [
                "Hypothermia",
                [
                    "Shivering", "Slurred Speech", "Fatigue", "Shock",
                    "Blurred Vision", "Cold"
                ],
                [
                    "Bring Victim to Dry, Sheltered Place",
                    "Remove Wet Clothing", "Give Warm Beverages",
                    "Get Into Huddle Position: (Hugs)",
                    "Do Not Rub Victims Body Surfaces"
                ]
            ]
        ]

    # Command to add new conditions.
    @commands.command(
        description="Add a new condition to the list of conditions",
        aliases=["add", "ac"])
    async def addCondition(self, ctx, *, input=None):
        embed_title = "New condition added."
        embed_desc = ""
        embed_color = COLOR_GREEN
        add_symptom = True

        if input == None:
            embed_title = "Error adding new condition."
            embed_desc  = "Invalid command usage.\n" + \
                          "Usage: `.add (Condition Name); (List of Symptoms); (List of Treatment)`"
            embed_color = COLOR_YELLOW
            await ctx.send(embed=discord.Embed(
                title=embed_title, description=embed_desc, color=embed_color))
            return

        if input.count(";") != 2:
            embed_title = "Error adding new condition."
            embed_desc  = "Invalid command usage.\n" + \
                          "Usage: `.add (Condition Name); (List of Symptoms); (List of Treatment)`"
            embed_color = COLOR_YELLOW
            add_symptom = False

        toAdd = ["", [], []]
        section = input.split("; ")

        for i in self.conditions:
            if re.search(section[0], i[0], re.IGNORECASE):
                embed_title = "Error adding new condition."
                embed_desc = "**{}** already exists.".format(i[0])
                embed_color = COLOR_YELLOW
                add_symptom = False

        if add_symptom:

            # Getting Symptoms From String
            listOfSymptoms = section[1].split(", ")

            # Getting Treatments from String
            listOfTreatment = section[2].split(", ")

            toAdd[0] = section[0]
            toAdd[1] = listOfSymptoms
            toAdd[2] = listOfTreatment

            embed_desc = "**{0}**\n\n".format(toAdd[0]) + \
                         "*Symptoms:*\n"

            for i in toAdd[1]:
                embed_desc += "- {}\n".format(i)

            embed_desc += "\n*Treatment:*\n"

            for i in toAdd[2]:
                embed_desc += "- {}\n".format(i)

            self.conditions.append(toAdd)

        await ctx.send(embed=discord.Embed(
            title=embed_title, description=embed_desc, color=embed_color))

    # Command to remove conditions from the list
    @commands.command(
        description="Remove a condition from the list of conditions",
        aliases=["rm", "remove", "delete"])
    async def removeCondition(self, ctx, *, input=None):
        embed_title = "Error deleting condition."
        embed_desc = "Condition not found in list."
        embed_color = COLOR_YELLOW

        if input == None:
            embed_title = "Error deleting condition."
            embed_desc = "Invalid command usage.\n" + \
                         "Usage: `.remove (Condition Name)`"
            embed_color = COLOR_YELLOW
        else:
            for i in self.conditions:
                if re.search(input, i[0], re.IGNORECASE):
                    embed_title = "Condition deleted."
                    embed_desc = "Deleted entry: {}".format(i[0])
                    embed_color = COLOR_RED
                    self.conditions.remove(i)
                    break

        await ctx.send(embed=discord.Embed(
            title=embed_title, description=embed_desc, color=embed_color))

    # Command to list all conditions
    @commands.command(description="List all conditions.", aliases=["ls"])
    async def list(self, ctx):
        embed_title = "Current list of conditions:"
        embed_desc = ""
        embed_color = COLOR_BLUE

        if len(self.conditions) == 0:
            embed_title = "Error viewing list."
            embed_desc = "List is empty."
            embed_color = COLOR_YELLOW
        else:
            for i in self.conditions:
                embed_desc += "- {}\n".format(i[0])

        await ctx.send(embed=discord.Embed(
            title=embed_title, description=embed_desc, color=embed_color))

    # Command to search for a condition
    @commands.command(
        description="Search for a condition from the list of conditions.",
        aliases=[])
    async def search(self, ctx, *, input=None):
        embed_title = "Error searching for condition."
        embed_desc = "Condition not found in list."
        embed_color = COLOR_YELLOW

        if input == None:
            embed_title = "Error searching for condition."
            embed_desc = "Invalid command usage.\n" + \
                          "Usage: `.search (Condition Name)`"
            embed_color = COLOR_YELLOW
        else:
            for i in self.conditions:
                if re.search(input, i[0], re.IGNORECASE):
                    embed_title = "**{}**".format(i[0])

                    embed_desc = "**Symptoms:**\n"
                    for j in i[1]:
                        embed_desc += "- {}\n".format(j)

                    embed_desc += "\n**Treatment:**\n"
                    for j in i[2]:
                        embed_desc += "- {}\n".format(j)

                    embed_color = COLOR_BLUE
                    break

        await ctx.send(embed=discord.Embed(
            title=embed_title, description=embed_desc, color=embed_color))

    # Command to show CPR instructions
    @commands.command(description="Show instructions for CPR.", aliases=[])
    async def cpr(self, ctx):
        await ctx.send(embed=discord.Embed(color=COLOR_RED).set_image(
            url=
            "https://cdn.discordapp.com/attachments/899062169033920523/899110545247064114/adult-cpr-aed.png"
        ))

    # Command to Compare Symptoms to Symptom in the Database
    @commands.command(
        description="Compare Symptoms to Database to Find Conditions",
        aliases=["c", "comp"])
    async def compare(self, ctx, *, input=None):
        embed_title = "Error comparing symptoms."
        embed_desc = ""
        embed_color = COLOR_YELLOW

        if input == None:
            embed_title = "Error comparing symptoms."
            embed_desc  = "Invalid command usage\n"  + \
                          "Usage: `.compare (Symptom Name)`"
            embed_color = COLOR_YELLOW
        else:
            for i in self.conditions:
                for j in i[1]:
                    if re.search(input, j, re.IGNORECASE):
                        embed_title = "Possible conditions:\n\n"
                        embed_desc += "- {}\n".format(i[0])
                        embed_color = COLOR_BLUE

        if embed_desc == "":
            embed_desc = "No conditions match the given symptom."

        await ctx.send(embed=discord.Embed(
            title=embed_title, description=embed_desc, color=embed_color))

def setup(bot):
    bot.add_cog(FirstAid(bot))
