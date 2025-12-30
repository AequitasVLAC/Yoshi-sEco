# Advanced Features Guide - Custom Tokens & Games

**Platform:** Streamer.bot (v0.2.0+)  
**Last Updated:** December 2025

This guide teaches you how to extend the Yoshi's Eggonomy system with your own custom tokens, games, and features. Perfect for streamers who want to create unique experiences for their community.

---

## Table of Contents

1. [Adding Custom Token Types](#adding-custom-token-types)
2. [Creating New Games](#creating-new-games)
3. [Advanced Payout Systems](#advanced-payout-systems)
4. [Team-Based Features](#team-based-features)
5. [Achievement System](#achievement-system)
6. [Season Pass System](#season-pass-system)
7. [Custom Rank Tiers](#custom-rank-tiers)
8. [Integration with Other Systems](#integration-with-other-systems)

---

## Adding Custom Token Types

### Understanding the Token System

The base system includes three token types:
- **Mystery Egg** (20 eggs) → Chomp Tunnel
- **Dice Egg** (10 eggs) → Hatch Roll
- **Duel Egg** (5 eggs) → Duel Nest

You can add unlimited custom tokens following this pattern.

---

### Example: Adding "Lucky Egg" Token

Let's create a new token type called "Lucky Egg" that costs 15 eggs and is used for a lottery game.

#### Step 1: Update Buy Token Action

**Edit Action:** `[ECON] Buy Token`

**Find this section in the code:**

```csharp
Dictionary<string, int> tokenCosts = new Dictionary<string, int>
{
    {"MysteryEgg", 20},
    {"DiceEgg", 10},
    {"DuelEgg", 5}
};
```

**Add your new token:**

```csharp
Dictionary<string, int> tokenCosts = new Dictionary<string, int>
{
    {"MysteryEgg", 20},
    {"DiceEgg", 10},
    {"DuelEgg", 5},
    {"LuckyEgg", 15}  // NEW TOKEN
};
```

**That's it for purchasing!** The rest of the buy logic automatically handles it.

---

#### Step 2: Update Inventory Command

**Edit Action:** `[USER] View Inventory`

**Add Lucky Egg to the display:**

```csharp
int mysteryEggs = CPH.GetGlobalVar<int>($"{userId}_MysteryEgg", true);
int diceEggs = CPH.GetGlobalVar<int>($"{userId}_DiceEgg", true);
int duelEggs = CPH.GetGlobalVar<int>($"{userId}_DuelEgg", true);
int luckyEggs = CPH.GetGlobalVar<int>($"{userId}_LuckyEgg", true); // NEW

CPH.SendMessage($"@{userName}'s Egg Pack 🎒 | {pouchEggs} 🥚 | {mysteryEggs} Mystery 🔮 | {diceEggs} Dice 🎲 | {duelEggs} Duel ⚔️ | {luckyEggs} Lucky 🍀");
```

---

#### Step 3: Create a Game for the Token

**Action Name:** `[GAME] Lucky Draw`

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        string userId = args["userId"].ToString();
        string userName = args["userName"].ToString();
        
        // Check for Lucky Egg
        string tokenVar = $"{userId}_LuckyEgg";
        int luckyEggs = CPH.GetGlobalVar<int>(tokenVar, true);
        
        // Check for free entry event
        bool freeEntry = CPH.GetGlobalVar<bool>("freeEntryTokensActive", true);
        
        if (luckyEggs < 1 && !freeEntry)
        {
            CPH.SendMessage($"@{userName}, you need 1 Lucky Egg! Use: !buy LuckyEgg 1");
            return false;
        }
        
        // Deduct token (if not free entry)
        if (!freeEntry && luckyEggs >= 1)
        {
            CPH.SetGlobalVar(tokenVar, luckyEggs - 1, true);
        }
        
        // Lucky Draw mechanics: Pull from a deck of prizes
        Random rnd = new Random();
        int draw = rnd.Next(1, 101); // 1-100
        
        int payout = 0;
        string message = "";
        
        if (draw <= 40)
        {
            // 40% chance - Small prize
            payout = 10;
            message = $"🍀 @{userName} drew: Common! +{payout} 🥚";
        }
        else if (draw <= 70)
        {
            // 30% chance - Medium prize
            payout = 25;
            message = $"🍀✨ @{userName} drew: Uncommon! +{payout} 🥚";
        }
        else if (draw <= 90)
        {
            // 20% chance - Good prize
            payout = 50;
            message = $"🍀🌟 @{userName} drew: Rare! +{payout} 🥚";
        }
        else if (draw <= 98)
        {
            // 8% chance - Great prize
            payout = 100;
            message = $"🍀💎 @{userName} drew: EPIC! +{payout} 🥚";
        }
        else
        {
            // 2% chance - Jackpot
            payout = 250;
            message = $"🍀👑✨ @{userName} drew: LEGENDARY! +{payout} 🥚";
        }
        
        // Apply event multipliers
        double multiplier = CPH.GetGlobalVar<double>("rewardMultiplier", true);
        if (multiplier == 0) multiplier = 1.0;
        
        if (multiplier > 1.0)
        {
            payout = (int)(payout * multiplier);
            message += $" [{multiplier}X EVENT]";
        }
        
        // Award eggs
        CPH.AddPoints(userId, payout, "Lucky Draw Win");
        
        // Update stats
        int draws = CPH.GetGlobalVar<int>($"{userId}_luckyDraws", true);
        CPH.SetGlobalVar($"{userId}_luckyDraws", draws + 1, true);
        
        int totalWon = CPH.GetGlobalVar<int>($"{userId}_totalEggsWon", true);
        CPH.SetGlobalVar($"{userId}_totalEggsWon", totalWon + payout, true);
        
        CPH.SendMessage(message);
        
        return true;
    }
}
```

**Command:** `!luckydraw` (10 second cooldown, everyone)

---

#### Testing Your New Token

1. Buy some Lucky Eggs: `!buy LuckyEgg 3`
2. Check inventory: `!eggpack` (should show Lucky Eggs)
3. Play the game: `!luckydraw`
4. Verify tokens decrease and eggs are awarded

---

### Token Creation Template

Use this template for ANY new token type:

```csharp
// 1. Add to Buy Token dictionary
{"YourTokenName", COST_IN_EGGS}

// 2. Create game action
string tokenVar = $"{userId}_YourTokenName";
int tokens = CPH.GetGlobalVar<int>(tokenVar, true);

// 3. Check and deduct token
bool freeEntry = CPH.GetGlobalVar<bool>("freeEntryTokensActive", true);
if (tokens < 1 && !freeEntry) {
    CPH.SendMessage($"@{userName}, you need 1 YourTokenName!");
    return false;
}
if (!freeEntry && tokens >= 1) {
    CPH.SetGlobalVar(tokenVar, tokens - 1, true);
}

// 4. Implement game logic
// ... your game code ...

// 5. Award payout with multiplier
double multiplier = CPH.GetGlobalVar<double>("rewardMultiplier", true);
if (multiplier == 0) multiplier = 1.0;
payout = (int)(payout * multiplier);

CPH.AddPoints(userId, payout, "Your Game Win");
```

---

### More Token Ideas

**Battle Egg (30 eggs)** → Boss Battle game  
**Mystery Egg variants** → Common/Rare/Epic tiers  
**Season Egg (50 eggs)** → Exclusive to current season  
**Guild Egg (100 eggs)** → Team-based gameplay  
**Time Egg (25 eggs)** → Speed-based mini-game  

---

## Creating New Games

### Game Design Principles

**Good Economy Games:**
1. ✅ **Clear rules** - Players understand immediately
2. ✅ **Appropriate risk/reward** - Balanced payouts
3. ✅ **Fast resolution** - Results in seconds, not minutes
4. ✅ **Engaging messaging** - Fun and informative output
5. ✅ **Stat tracking** - Record plays, wins, streaks
6. ✅ **Event integration** - Support multipliers and free entry

---

### Example Game 1: Egg Hunt

**Concept:** Roll to find hidden eggs in different locations. Higher rolls find better hiding spots.

**Token:** Mystery Egg  
**Mechanics:** D10 roll, different outcomes per range  
**Expected Value:** ~20 eggs per play (cost: 20 eggs to buy token)

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        string userId = args["userId"].ToString();
        string userName = args["userName"].ToString();
        
        // Token check
        string tokenVar = $"{userId}_MysteryEgg";
        int tokens = CPH.GetGlobalVar<int>(tokenVar, true);
        bool freeEntry = CPH.GetGlobalVar<bool>("freeEntryTokensActive", true);
        
        if (tokens < 1 && !freeEntry)
        {
            CPH.SendMessage($"@{userName}, you need a Mystery Egg for the hunt!");
            return false;
        }
        
        if (!freeEntry && tokens >= 1)
        {
            CPH.SetGlobalVar(tokenVar, tokens - 1, true);
        }
        
        // Roll D10
        Random rnd = new Random();
        int roll = rnd.Next(1, 11);
        
        string location = "";
        int payout = 0;
        
        switch (roll)
        {
            case 1:
                location = "in the bushes";
                payout = 5;
                break;
            case 2:
            case 3:
                location = "under a rock";
                payout = 10;
                break;
            case 4:
            case 5:
                location = "in a tree";
                payout = 20;
                break;
            case 6:
            case 7:
                location = "behind the waterfall";
                payout = 30;
                break;
            case 8:
            case 9:
                location = "in the secret cave";
                payout = 50;
                break;
            case 10:
                location = "in the GOLDEN NEST";
                payout = 100;
                break;
        }
        
        // Apply multiplier
        double multiplier = CPH.GetGlobalVar<double>("rewardMultiplier", true);
        if (multiplier == 0) multiplier = 1.0;
        payout = (int)(payout * multiplier);
        
        string eventTag = multiplier > 1.0 ? $" [{multiplier}X]" : "";
        
        // Award
        CPH.AddPoints(userId, payout, "Egg Hunt");
        
        // Update stats
        int hunts = CPH.GetGlobalVar<int>($"{userId}_eggHunts", true);
        CPH.SetGlobalVar($"{userId}_eggHunts", hunts + 1, true);
        
        CPH.SendMessage($"🔍 @{userName} rolled {roll}! Found eggs {location}! +{payout} 🥚{eventTag}");
        
        return true;
    }
}
```

**Command:** `!egghunt` (15 second cooldown)

---

### Example Game 2: Egg Stack

**Concept:** Stack as many eggs as possible before they fall. Press your luck style.

**Token:** Dice Egg  
**Mechanics:** Multi-round, player decides when to stop  
**Expected Value:** Variable (risk vs reward)

This game requires multiple interactions, so we'll use a simplified version:

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        string userId = args["userId"].ToString();
        string userName = args["userName"].ToString();
        
        // Check for active stack
        int activeStack = CPH.GetGlobalVar<int>($"{userId}_activeStack", true);
        
        if (activeStack > 0)
        {
            // User is cashing out
            int payout = activeStack * 10; // 10 eggs per level
            
            // Apply multiplier
            double multiplier = CPH.GetGlobalVar<double>("rewardMultiplier", true);
            if (multiplier == 0) multiplier = 1.0;
            payout = (int)(payout * multiplier);
            
            CPH.AddPoints(userId, payout, "Egg Stack Win");
            
            CPH.SendMessage($"💰 @{userName} cashed out their stack of {activeStack} eggs! +{payout} 🥚");
            
            // Clear stack
            CPH.SetGlobalVar($"{userId}_activeStack", 0, true);
            
            return true;
        }
        
        // Starting new stack
        string tokenVar = $"{userId}_DiceEgg";
        int tokens = CPH.GetGlobalVar<int>(tokenVar, true);
        bool freeEntry = CPH.GetGlobalVar<bool>("freeEntryTokensActive", true);
        
        if (tokens < 1 && !freeEntry)
        {
            CPH.SendMessage($"@{userName}, you need a Dice Egg to start stacking!");
            return false;
        }
        
        if (!freeEntry && tokens >= 1)
        {
            CPH.SetGlobalVar(tokenVar, tokens - 1, true);
        }
        
        // Roll to stack
        Random rnd = new Random();
        int roll = rnd.Next(1, 7); // D6
        
        if (roll == 1)
        {
            // Failed!
            CPH.SendMessage($"💥 @{userName} rolled {roll}! The eggs tumbled! Stack failed!");
        }
        else
        {
            // Success - add to stack
            CPH.SetGlobalVar($"{userId}_activeStack", 1, true);
            CPH.SendMessage($"📦 @{userName} rolled {roll}! Egg stacked! Use !stack again to add more, or !cashout to collect 10 🥚!");
        }
        
        return true;
    }
}
```

**Commands:**
- `!stack` - Start stacking or add another egg
- `!cashout` - Collect your stacked eggs

**Note:** This simplified version starts at 1 stack. For a full press-your-luck system, you'd track stack height and increasing failure chances.

---

### Example Game 3: Boss Battle

**Concept:** Community pools Duel Eggs to defeat a boss. Winner shares loot.

**Token:** Duel Egg  
**Mechanics:** Accumulate damage until boss HP reaches 0  
**Expected Value:** Variable based on participation

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        string userId = args["userId"].ToString();
        string userName = args["userName"].ToString();
        
        // Check for active boss
        int bossHP = CPH.GetGlobalVar<int>("boss_currentHP", true);
        int bossMaxHP = CPH.GetGlobalVar<int>("boss_maxHP", true);
        
        if (bossHP <= 0)
        {
            // No active boss - spawn one
            if (args["isModerator"] == null || !(bool)args["isModerator"])
            {
                CPH.SendMessage("No active boss! Mods can spawn one with !spawnboss");
                return false;
            }
            
            // Spawn new boss (moderator only)
            bossMaxHP = 1000;
            bossHP = bossMaxHP;
            CPH.SetGlobalVar("boss_maxHP", bossMaxHP, true);
            CPH.SetGlobalVar("boss_currentHP", bossHP, true);
            CPH.SetGlobalVar("boss_lootPool", 0, true);
            CPH.SetGlobalVar("boss_participants", "", true);
            
            CPH.SendMessage($"🐉 A BOSS APPEARS! Mega Chomp has {bossMaxHP} HP! Attack with !attack!");
            
            return true;
        }
        
        // Player attacks boss
        string tokenVar = $"{userId}_DuelEgg";
        int tokens = CPH.GetGlobalVar<int>(tokenVar, true);
        bool freeEntry = CPH.GetGlobalVar<bool>("freeEntryTokensActive", true);
        
        if (tokens < 1 && !freeEntry)
        {
            CPH.SendMessage($"@{userName}, you need a Duel Egg to attack!");
            return false;
        }
        
        if (!freeEntry && tokens >= 1)
        {
            CPH.SetGlobalVar(tokenVar, tokens - 1, true);
        }
        
        // Roll damage
        Random rnd = new Random();
        int damage = rnd.Next(10, 51); // 10-50 damage
        
        bossHP -= damage;
        CPH.SetGlobalVar("boss_currentHP", bossHP, true);
        
        // Add to loot pool (5 eggs per attack)
        int lootPool = CPH.GetGlobalVar<int>("boss_lootPool", true);
        lootPool += 5;
        CPH.SetGlobalVar("boss_lootPool", lootPool, true);
        
        // Track participants
        string participants = CPH.GetGlobalVar<string>("boss_participants", true);
        if (!participants.Contains(userId))
        {
            participants += userId + ",";
            CPH.SetGlobalVar("boss_participants", participants, true);
        }
        
        if (bossHP <= 0)
        {
            // Boss defeated!
            CPH.SendMessage($"⚔️ @{userName} deals {damage} damage! 🐉 BOSS DEFEATED! Loot pool: {lootPool} 🥚 distributed to {participants.Split(',').Length - 1} heroes!");
            
            // Distribute loot (simplified - equal split)
            // In full implementation, use CPH.AddPoints for each participant
            
            // Reset boss
            CPH.SetGlobalVar("boss_currentHP", 0, true);
        }
        else
        {
            CPH.SendMessage($"⚔️ @{userName} attacks for {damage} damage! Boss HP: {bossHP}/{bossMaxHP} | Loot: {lootPool} 🥚");
        }
        
        return true;
    }
}
```

**Commands:**
- `!attack` - Attack the boss (everyone)
- `!spawnboss` - Spawn a boss (mods only)

---

### Game Design Checklist

When creating a new game, ensure:

- [ ] Token cost is appropriate for expected payout
- [ ] Code checks for free entry event
- [ ] Code applies reward multiplier
- [ ] Messages are clear and fun
- [ ] Statistics are tracked (plays, wins, etc.)
- [ ] Edge cases handled (no infinite loops, no negative values)
- [ ] Cooldown set appropriately
- [ ] Permission level correct (everyone vs mods)

---

## Advanced Payout Systems

### Progressive Jackpots

Award increasing prizes based on consecutive plays without winning.

```csharp
// In your game action, track dry streak
int dryStreak = CPH.GetGlobalVar<int>($"{userId}_gameX_dryStreak", true);

if (playerLost)
{
    dryStreak++;
    CPH.SetGlobalVar($"{userId}_gameX_dryStreak", dryStreak, true);
    
    // Give pity prize after 5 losses
    if (dryStreak >= 5)
    {
        int pityPrize = 25;
        CPH.AddPoints(userId, pityPrize, "Pity Prize");
        CPH.SendMessage($"🎁 Consolation prize for {dryStreak} tries! +{pityPrize} 🥚");
        dryStreak = 0;
        CPH.SetGlobalVar($"{userId}_gameX_dryStreak", 0, true);
    }
}
else
{
    // Reset on win
    dryStreak = 0;
    CPH.SetGlobalVar($"{userId}_gameX_dryStreak", 0, true);
}
```

---

### Dynamic Difficulty

Adjust game difficulty based on player performance.

```csharp
// Track player's win rate
int plays = CPH.GetGlobalVar<int>($"{userId}_gameX_plays", true);
int wins = CPH.GetGlobalVar<int>($"{userId}_gameX_wins", true);

double winRate = plays > 0 ? (double)wins / plays : 0.5;

// Adjust difficulty
int baseDifficulty = 50; // 50% success rate
int adjustedDifficulty = baseDifficulty;

if (winRate > 0.7)
{
    // Player too strong - increase difficulty
    adjustedDifficulty = 40; // 40% success rate
}
else if (winRate < 0.3)
{
    // Player struggling - decrease difficulty
    adjustedDifficulty = 60; // 60% success rate
}

// Use adjustedDifficulty in your roll check
Random rnd = new Random();
int roll = rnd.Next(1, 101);
bool success = roll <= adjustedDifficulty;
```

---

### Combo Systems

Reward players for chaining successes.

```csharp
// Track combo
int combo = CPH.GetGlobalVar<int>($"{userId}_gameX_combo", true);

if (playerWon)
{
    combo++;
    CPH.SetGlobalVar($"{userId}_gameX_combo", combo, true);
    
    // Bonus for high combos
    int comboBonus = 0;
    if (combo >= 3) comboBonus = 10;
    if (combo >= 5) comboBonus = 25;
    if (combo >= 10) comboBonus = 50;
    
    if (comboBonus > 0)
    {
        payout += comboBonus;
        CPH.SendMessage($"🔥 {combo}x COMBO! +{comboBonus} bonus eggs!");
    }
}
else
{
    if (combo >= 3)
    {
        CPH.SendMessage($"💔 Combo broken at {combo}x!");
    }
    combo = 0;
    CPH.SetGlobalVar($"{userId}_gameX_combo", 0, true);
}
```

---

## Team-Based Features

### Creating Teams

**Action Name:** `[TEAM] Join Team`

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        string userId = args["userId"].ToString();
        string userName = args["userName"].ToString();
        string teamName = args["rawInput0"]?.ToString()?.ToUpper();
        
        // Valid teams: RED, BLUE, GREEN
        if (teamName != "RED" && teamName != "BLUE" && teamName != "GREEN")
        {
            CPH.SendMessage($"@{userName}, valid teams are: RED, BLUE, GREEN");
            return false;
        }
        
        // Check if already on a team
        string currentTeam = CPH.GetGlobalVar<string>($"{userId}_team", true);
        if (!string.IsNullOrEmpty(currentTeam))
        {
            CPH.SendMessage($"@{userName}, you're already on Team {currentTeam}! Cost 100 🥚 to switch.");
            return false;
        }
        
        // Join team
        CPH.SetGlobalVar($"{userId}_team", teamName, true);
        
        // Update team roster
        string roster = CPH.GetGlobalVar<string>($"team_{teamName}_members", true);
        if (!roster.Contains(userId))
        {
            roster += userId + ",";
            CPH.SetGlobalVar($"team_{teamName}_members", roster, true);
        }
        
        CPH.SendMessage($"🏳️ @{userName} joined Team {teamName}!");
        
        return true;
    }
}
```

**Command:** `!jointeam <RED|BLUE|GREEN>`

---

### Team Leaderboard

**Action Name:** `[TEAM] Show Standings`

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        int redScore = CPH.GetGlobalVar<int>("team_RED_score", true);
        int blueScore = CPH.GetGlobalVar<int>("team_BLUE_score", true);
        int greenScore = CPH.GetGlobalVar<int>("team_GREEN_score", true);
        
        CPH.SendMessage($"🏆 Team Standings | 🔴 RED: {redScore} | 🔵 BLUE: {blueScore} | 🟢 GREEN: {greenScore}");
        
        return true;
    }
}
```

**Command:** `!teams`

---

### Team Games

Modify existing games to award points to teams:

```csharp
// At end of game, if player won
string playerTeam = CPH.GetGlobalVar<string>($"{userId}_team", true);

if (!string.IsNullOrEmpty(playerTeam))
{
    int teamScore = CPH.GetGlobalVar<int>($"team_{playerTeam}_score", true);
    teamScore += 10; // 10 points per win
    CPH.SetGlobalVar($"team_{playerTeam}_score", teamScore, true);
    
    CPH.SendMessage($"🏳️ +10 points for Team {playerTeam}!");
}
```

---

## Achievement System

### Define Achievements

```csharp
// Achievement definitions (add to a reference action)
Dictionary<string, string> achievements = new Dictionary<string, string>
{
    {"first_win", "🥇 First Victory - Win any game"},
    {"streak_5", "🔥 Hot Streak - Get 5 win streak in Chomp"},
    {"golden_hunter", "✨ Golden Hunter - Find 10 golden eggs"},
    {"duel_master", "⚔️ Duel Master - Win 50 duels"},
    {"high_roller", "🎲 High Roller - Roll 20 in Hatch Roll"},
    {"egg_lord", "👑 Egg Lord - Reach 10,000 total eggs"}
};
```

---

### Check and Award Achievements

**Action Name:** `[ACHIEVEMENT] Check`

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        string userId = args["userId"].ToString();
        string userName = args["userName"].ToString();
        string achievementId = args["achievementId"]?.ToString(); // Passed from game
        
        if (string.IsNullOrEmpty(achievementId))
        {
            return false;
        }
        
        // Check if already earned
        string earnedVar = $"{userId}_achievement_{achievementId}";
        bool alreadyEarned = CPH.GetGlobalVar<bool>(earnedVar, true);
        
        if (alreadyEarned)
        {
            return false; // Already has it
        }
        
        // Award achievement
        CPH.SetGlobalVar(earnedVar, true, true);
        
        // Achievement descriptions
        string title = "";
        int reward = 100; // Default reward
        
        switch (achievementId)
        {
            case "first_win":
                title = "🥇 First Victory";
                reward = 50;
                break;
            case "streak_5":
                title = "🔥 Hot Streak";
                reward = 150;
                break;
            case "golden_hunter":
                title = "✨ Golden Hunter";
                reward = 250;
                break;
            case "duel_master":
                title = "⚔️ Duel Master";
                reward = 500;
                break;
            case "high_roller":
                title = "🎲 High Roller";
                reward = 200;
                break;
            case "egg_lord":
                title = "👑 Egg Lord";
                reward = 1000;
                break;
        }
        
        // Award bonus eggs
        CPH.AddPoints(userId, reward, "Achievement Unlock");
        
        // Increment achievement count
        int totalAchievements = CPH.GetGlobalVar<int>($"{userId}_totalAchievements", true);
        CPH.SetGlobalVar($"{userId}_totalAchievements", totalAchievements + 1, true);
        
        CPH.SendMessage($"🏆 @{userName} unlocked achievement: {title}! +{reward} 🥚");
        
        return true;
    }
}
```

---

### Trigger Achievements from Games

Add to your game actions:

```csharp
// Example: Chomp Tunnel - Check for streak achievement
if (streak == 5)
{
    // Trigger achievement check
    CPH.SetArgument("achievementId", "streak_5");
    CPH.RunAction("[ACHIEVEMENT] Check", false);
}

// Example: Hatch Roll - Check for high roller
if (roll == 20)
{
    CPH.SetArgument("achievementId", "high_roller");
    CPH.RunAction("[ACHIEVEMENT] Check", false);
}

// Example: After ANY win - Check for first win
int totalWins = CPH.GetGlobalVar<int>($"{userId}_totalWins", true);
if (totalWins == 1)
{
    CPH.SetArgument("achievementId", "first_win");
    CPH.RunAction("[ACHIEVEMENT] Check", false);
}
```

---

### View Achievements Command

**Action Name:** `[USER] View Achievements`

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        string userId = args["userId"].ToString();
        string userName = args["userName"].ToString();
        
        int total = CPH.GetGlobalVar<int>($"{userId}_totalAchievements", true);
        
        // Check specific achievements
        bool firstWin = CPH.GetGlobalVar<bool>($"{userId}_achievement_first_win", true);
        bool streak5 = CPH.GetGlobalVar<bool>($"{userId}_achievement_streak_5", true);
        bool goldenHunter = CPH.GetGlobalVar<bool>($"{userId}_achievement_golden_hunter", true);
        bool duelMaster = CPH.GetGlobalVar<bool>($"{userId}_achievement_duel_master", true);
        bool highRoller = CPH.GetGlobalVar<bool>($"{userId}_achievement_high_roller", true);
        bool eggLord = CPH.GetGlobalVar<bool>($"{userId}_achievement_egg_lord", true);
        
        string earned = "";
        if (firstWin) earned += "🥇 ";
        if (streak5) earned += "🔥 ";
        if (goldenHunter) earned += "✨ ";
        if (duelMaster) earned += "⚔️ ";
        if (highRoller) earned += "🎲 ";
        if (eggLord) earned += "👑 ";
        
        if (string.IsNullOrEmpty(earned))
        {
            CPH.SendMessage($"@{userName} has no achievements yet! Play games to unlock them!");
        }
        else
        {
            CPH.SendMessage($"@{userName}'s Achievements ({total}/6): {earned}");
        }
        
        return true;
    }
}
```

**Command:** `!achievements`

---

## Season Pass System

Create limited-time progression with exclusive rewards.

### Season Structure

```csharp
// Season variables
CPH.SetGlobalVar("currentSeason", 1, true);
CPH.SetGlobalVar("seasonEndDate", DateTime.Parse("2026-03-31").Ticks, true);
CPH.SetGlobalVar("seasonTheme", "Spring Awakening", true);
```

---

### Season XP System

**Award XP for actions:**

```csharp
// After game completion
int xpEarned = 10; // Base XP
int seasonXP = CPH.GetGlobalVar<int>($"{userId}_seasonXP", true);
seasonXP += xpEarned;
CPH.SetGlobalVar($"{userId}_seasonXP", seasonXP, true);

// Check for level up (every 100 XP = 1 level)
int newLevel = seasonXP / 100;
int oldLevel = CPH.GetGlobalVar<int>($"{userId}_seasonLevel", true);

if (newLevel > oldLevel)
{
    CPH.SetGlobalVar($"{userId}_seasonLevel", newLevel, true);
    
    // Award level rewards
    int levelReward = newLevel * 50; // 50 eggs per level
    CPH.AddPoints(userId, levelReward, "Season Level Up");
    
    CPH.SendMessage($"⬆️ @{userName} reached Season Level {newLevel}! +{levelReward} 🥚");
    
    // Special rewards at milestones
    if (newLevel == 10)
    {
        CPH.SendMessage($"🎁 @{userName} unlocked: Exclusive Season Token!");
        CPH.SetGlobalVar($"{userId}_seasonToken_unlocked", true, true);
    }
}
```

---

### Season Pass Command

**Action Name:** `[SEASON] View Pass`

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        string userId = args["userId"].ToString();
        string userName = args["userName"].ToString();
        
        int seasonLevel = CPH.GetGlobalVar<int>($"{userId}_seasonLevel", true);
        int seasonXP = CPH.GetGlobalVar<int>($"{userId}_seasonXP", true);
        int xpToNext = ((seasonLevel + 1) * 100) - seasonXP;
        
        string theme = CPH.GetGlobalVar<string>("seasonTheme", true);
        long endDate = CPH.GetGlobalVar<long>("seasonEndDate", true);
        TimeSpan remaining = TimeSpan.FromTicks(endDate - DateTime.Now.Ticks);
        
        CPH.SendMessage($"🌸 {theme} | @{userName} - Level {seasonLevel} ({seasonXP} XP) | Next: {xpToNext} XP | {remaining.Days} days left");
        
        return true;
    }
}
```

**Command:** `!seasonpass`

---

## Custom Rank Tiers

Extend beyond the base 7 ranks with custom tiers.

### Define Custom Ranks

```csharp
public class CPHInline
{
    public bool Execute()
    {
        string userId = args["userId"].ToString();
        string userName = args["userName"].ToString();
        int pouchEggs = CPH.GetPoints(userId);
        
        string rank = "", icon = "", nextRank = "";
        int nextThreshold = 0;
        string perkDesc = "";
        
        if (pouchEggs < 100) 
        { 
            rank = "Hatchling"; 
            icon = "🥚"; 
            nextRank = "Egg Runner"; 
            nextThreshold = 100;
            perkDesc = "None yet!";
        }
        else if (pouchEggs < 500) 
        { 
            rank = "Egg Runner"; 
            icon = "🏃"; 
            nextRank = "Nest Builder"; 
            nextThreshold = 500;
            perkDesc = "5% bonus to all payouts";
        }
        else if (pouchEggs < 1000) 
        { 
            rank = "Nest Builder"; 
            icon = "🏠"; 
            nextRank = "Egg Guardian"; 
            nextThreshold = 1000;
            perkDesc = "10% bonus + Free reroll monthly";
        }
        else if (pouchEggs < 2500) 
        { 
            rank = "Egg Guardian"; 
            icon = "🛡️"; 
            nextRank = "Yoshi Knight"; 
            nextThreshold = 2500;
            perkDesc = "15% bonus + Special color";
        }
        else if (pouchEggs < 5000) 
        { 
            rank = "Yoshi Knight"; 
            icon = "⚔️"; 
            nextRank = "Grand Yoshi"; 
            nextThreshold = 5000;
            perkDesc = "20% bonus + VIP status";
        }
        else if (pouchEggs < 10000) 
        { 
            rank = "Grand Yoshi"; 
            icon = "👑"; 
            nextRank = "Egg Emperor"; 
            nextThreshold = 10000;
            perkDesc = "25% bonus + Custom title";
        }
        else if (pouchEggs < 25000)
        { 
            rank = "Egg Emperor"; 
            icon = "🌟"; 
            nextRank = "Egg Deity"; 
            nextThreshold = 25000;
            perkDesc = "30% bonus + Emperor perks";
        }
        else if (pouchEggs < 50000)
        {
            rank = "Egg Deity";
            icon = "💫";
            nextRank = "Egg Transcendent";
            nextThreshold = 50000;
            perkDesc = "40% bonus + Deity aura";
        }
        else 
        { 
            rank = "Egg Transcendent"; 
            icon = "✨🌈✨"; 
            nextRank = "MAX"; 
            nextThreshold = 0;
            perkDesc = "50% bonus + LEGENDARY";
        }
        
        string message = $"@{userName} | {icon} {rank} ({pouchEggs} 🥚) | Perk: {perkDesc}";
        if (nextThreshold > 0) 
        {
            message += $" | Next: {nextRank} ({nextThreshold - pouchEggs} needed)";
        } 
        else 
        {
            message += " | 🎉 MAX RANK ACHIEVED!";
        }
        
        CPH.SendMessage(message);
        return true;
    }
}
```

---

### Apply Rank Bonuses

In your game actions, apply rank-based bonuses:

```csharp
// Get player rank bonus
int pouchEggs = CPH.GetPoints(userId);
double rankBonus = 0;

if (pouchEggs >= 50000) rankBonus = 0.50; // 50%
else if (pouchEggs >= 25000) rankBonus = 0.40; // 40%
else if (pouchEggs >= 10000) rankBonus = 0.30; // 30%
else if (pouchEggs >= 5000) rankBonus = 0.25; // 25%
else if (pouchEggs >= 2500) rankBonus = 0.20; // 20%
else if (pouchEggs >= 1000) rankBonus = 0.15; // 15%
else if (pouchEggs >= 500) rankBonus = 0.10; // 10%
else if (pouchEggs >= 100) rankBonus = 0.05; // 5%

// Apply rank bonus
if (rankBonus > 0)
{
    int bonusAmount = (int)(payout * rankBonus);
    payout += bonusAmount;
    CPH.SendMessage($"🎖️ Rank bonus: +{bonusAmount} 🥚");
}
```

---

## Integration with Other Systems

### Integrate with Channel Points

Allow viewers to convert Channel Points to Pouch Eggs.

**Channel Point Reward:**
1. Create Custom Reward in Twitch: "Convert to Eggs" (10,000 points)
2. Create Action in Streamer.bot

**Action Name:** `[INTEGRATION] Channel Points to Eggs`

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        string userId = args["userId"].ToString();
        string userName = args["userName"].ToString();
        
        // Award 100 Pouch Eggs for channel point redemption
        int eggReward = 100;
        CPH.AddPoints(userId, eggReward, "Channel Points Conversion");
        
        CPH.SendMessage($"✨ @{userName} converted Channel Points to {eggReward} 🥚!");
        
        return true;
    }
}
```

**Link to Channel Point Reward:**
- In Streamer.bot, link this action to the Channel Point Reward trigger

---

### Integration with Bits

**Action Name:** `[INTEGRATION] Bits to Eggs`

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        string userId = args["userId"].ToString();
        string userName = args["userName"].ToString();
        int bits = int.Parse(args["bits"].ToString());
        
        // Convert bits to eggs (1 bit = 10 eggs)
        int eggReward = bits * 10;
        CPH.AddPoints(userId, eggReward, "Bits Bonus");
        
        CPH.SendMessage($"💎 @{userName} cheered {bits} bits and received {eggReward} 🥚! Thank you!");
        
        return true;
    }
}
```

**Trigger:** Link to Twitch Bits event in Streamer.bot

---

### Integration with Subs

**Action Name:** `[INTEGRATION] Sub Bonus`

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        string userId = args["userId"].ToString();
        string userName = args["userName"].ToString();
        
        // Sub bonus: 500 eggs
        int eggReward = 500;
        CPH.AddPoints(userId, eggReward, "Sub Bonus");
        
        // Also give some tokens
        CPH.SetGlobalVar($"{userId}_MysteryEgg", CPH.GetGlobalVar<int>($"{userId}_MysteryEgg", true) + 3, true);
        CPH.SetGlobalVar($"{userId}_DiceEgg", CPH.GetGlobalVar<int>($"{userId}_DiceEgg", true) + 3, true);
        CPH.SetGlobalVar($"{userId}_DuelEgg", CPH.GetGlobalVar<int>($"{userId}_DuelEgg", true) + 3, true);
        
        CPH.SendMessage($"🎉 @{userName} subscribed! +{eggReward} 🥚 and +3 of each token! Welcome to the nest!");
        
        return true;
    }
}
```

**Trigger:** Link to Twitch Sub event in Streamer.bot

---

## Summary

This Advanced Features Guide covered:

✅ **Custom Tokens** - Add unlimited token types with template  
✅ **New Games** - Three example games with different mechanics  
✅ **Advanced Payouts** - Progressive jackpots, difficulty scaling, combos  
✅ **Team Features** - Team creation, leaderboards, team games  
✅ **Achievements** - Unlock system with rewards  
✅ **Season Pass** - XP progression with exclusive rewards  
✅ **Custom Ranks** - Extended rank system with bonuses  
✅ **Integrations** - Connect with Channel Points, Bits, Subs  

**Next Steps:**
1. Choose which features fit your community best
2. Start with one feature and test thoroughly
3. Gather viewer feedback before adding more
4. Balance rewards to maintain economy health

**Related Documentation:**
- [Variable Reference](Variable_Reference.md) - All variables explained
- [Event System Guide](Event_System_Guide.md) - Bonus events and multipliers
- [Unified Eggonomy Guide](Unified_Yoshi_Eggonomy.md) - Core implementation
