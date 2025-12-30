# Complete Egg-Based Economy System for Streamer.bot

**Platform:** Streamer.bot (v0.2.0+)  
**Setup Location:** All actions, commands, and configurations are created within Streamer.bot  
**No External Scripts Required:** Everything runs natively in Streamer.bot using C# Execute Code actions

This document provides a comprehensive, step-by-step setup for creating an interactive egg-based economy using Streamer.bot. It integrates the token system, PvP mechanics, and games into a single, functional system where users can earn, spend, and lose eggs effectively. The design includes cohesive interactions, balanced game mechanics, and sinks to maintain a sustainable economy.

## Prerequisites

Before starting, ensure you have:
- **Streamer.bot v0.2.0 or later** installed and connected to your Twitch account
- **Loyalty Points system enabled** in Streamer.bot
- **Basic understanding of** creating Actions and Commands in Streamer.bot
- **C# code execution enabled** (default in Streamer.bot)

## Implementation Time Estimate
- **Quick Setup (Core Features):** 30-45 minutes
- **Full Implementation (All Games & Commands):** 1-2 hours

---

## Quick Start Checklist

Follow these steps in order for a working implementation:

1. ✅ **Stage 1:** Configure currency and initialize global variables (10 min)
2. ✅ **Stage 2:** Set up token purchase system (15 min)
3. ✅ **Stage 3:** Implement games (30-45 min)
4. ✅ **Stage 4:** Add user commands (15 min)
5. ✅ **Stage 5:** Configure economy monitoring (5 min)
6. ✅ **Test:** Verify all features work before going live (15 min)

---

## Key Features
- **Main Currency:** Pouch Eggs (earned passively by viewers).
- **Token System:** Playable-game tokens (Mystery Eggs, Dice Eggs, Duel Eggs).
- **Games:** Fun and rewarding games like Chomp Tunnel, Hatch Roll, and PvP battles.
- **Leaderboard & Ranks:** Track top players and progression through 7 rank tiers.
- **Balanced Economy:** Currency sinks to manage inflation and ensure long-term viability.
- **PvP with Timer-Based Resolution:** The Duel Nest PvP system is resolved automatically within 10 minutes.
- **Interactive Commands:** Clear and consistent commands for users to interact with the system.

---

## Stage 1: Initial Setup (REQUIRED - 10 minutes)

### 1.1 Configure Pouch Eggs as the Main Currency

**Step-by-Step Instructions:**

1. Open Streamer.bot
2. Navigate to: `Settings` (top menu) → `Loyalty` → `Points Settings`
3. Configure the following:
   - **Enable Loyalty Points:** ✅ Check this box
   - **Currency Name (Singular):** `🥚 Pouch Egg`
   - **Currency Name (Plural):** `🥚 Pouch Eggs`
   - **Default Command:** `!eggs`
4. **Set Passive Income Rates:**
   - **Offline Viewers:** 0 eggs per interval (optional)
   - **Online Viewers:** 5 eggs per 10 minutes
   - **Active Chatters:** 10 eggs per 10 minutes
   - **Subscribers Bonus:** +5 eggs (optional)
5. Click **Save Changes**

**Verify:** Type `!eggs` in your chat - it should show your current balance.

---

### 1.2 Initialize Global Variables

**Step-by-Step Instructions:**

1. In Streamer.bot, go to: `Settings` → `Variables` → `Global Variables`
2. Click **Add Variable** and create these two variables:

   **Variable 1:**
   - **Name:** `bigNestFund`
   - **Type:** Number
   - **Initial Value:** `1000`
   - **Persisted:** ✅ Yes
   
   **Variable 2:**
   - **Name:** `eggCartonJackpot`
   - **Type:** Number
   - **Initial Value:** `500`
   - **Persisted:** ✅ Yes

3. Click **Save**

**Note:** These funds collect token purchase fees and can be used for special events or giveaways.

---

## Stage 2: Token System (15 minutes)

### 2.1 Token Definitions
The token system includes three token types, purchased using Pouch Eggs:
- **Mystery Eggs:** Cost 20 eggs, used in the *Chomp Tunnel* game.
- **Dice Eggs:** Cost 10 eggs, used in the *Hatch Roll* game.
- **Duel Eggs:** Cost 5 eggs, used in the PvP Duel Nest.

### 2.2 Buy Token Command - `!buy`

**Command:** `!buy <TokenType> <Quantity>`

**Example Usage:**
- `!buy MysteryEgg 1` - Purchase 1 Mystery Egg for 20 Pouch Eggs.
- `!buy DiceEgg 5` - Purchase 5 Dice Eggs for 50 Pouch Eggs.
- `!buy DuelEgg 2` - Purchase 2 Duel Eggs for 10 Pouch Eggs.

#### Step-by-Step Setup:

**1. Create the Action:**
   - In Streamer.bot, go to: `Actions` tab
   - Click **Add** button
   - **Action Name:** `[ECON] Buy Token`
   - Click **OK**

**2. Add Execute Code Sub-Action:**
   - With the `[ECON] Buy Token` action selected, click **Add Sub-Action**
   - Choose: `Core` → `C#` → `Execute Code`
   - In the code window, **DELETE ALL DEFAULT CODE** and paste this:

```csharp
using System;
using System.Collections.Generic;

public class CPHInline
{
    public bool Execute()
    {
        // Parse user input
        string userId = args["userId"].ToString();
        string userName = args["userName"].ToString();
        string tokenType = args["rawInput0"]?.ToString(); // e.g., "MysteryEgg"
        
        // Validate quantity input
        if (args["rawInput1"] == null || !int.TryParse(args["rawInput1"].ToString(), out int quantity) || quantity < 1)
        {
            CPH.SendMessage($"@{userName}, please specify a valid quantity! Example: !buy MysteryEgg 1");
            return false;
        }
        
        // Define token costs
        Dictionary<string, int> tokenCosts = new Dictionary<string, int>
        {
            {"MysteryEgg", 20},
            {"DiceEgg", 10},
            {"DuelEgg", 5}
        };
        
        // Validate token type (case-insensitive)
        string tokenKey = null;
        foreach (var key in tokenCosts.Keys)
        {
            if (key.Equals(tokenType, StringComparison.OrdinalIgnoreCase))
            {
                tokenKey = key;
                break;
            }
        }
        
        if (tokenKey == null)
        {
            CPH.SendMessage($"@{userName}, invalid token type! Use: MysteryEgg, DiceEgg, or DuelEgg");
            return false;
        }
        
        // Calculate total cost
        int totalCost = tokenCosts[tokenKey] * quantity;
        int userBalance = CPH.GetPoints(userId);
        
        // Check if user has enough Pouch Eggs
        if (userBalance < totalCost)
        {
            CPH.SendMessage($"@{userName}, you need {totalCost} 🥚 but only have {userBalance} 🥚");
            return false;
        }
        
        // Deduct Pouch Eggs
        CPH.RemovePoints(userId, totalCost, "Token Purchase");
        
        // Increment token balance
        string tokenVar = $"{userId}_{tokenKey}";
        int currentTokens = CPH.GetGlobalVar<int>(tokenVar, true);
        CPH.SetGlobalVar(tokenVar, currentTokens + quantity, true);
        
        // Distribute funds (70% to bigNestFund, 20% to jackpot, 10% sink)
        int bigNestContribution = (int)(totalCost * 0.7);
        int jackpotContribution = (int)(totalCost * 0.2);
        
        int bigNestFund = CPH.GetGlobalVar<int>("bigNestFund", true);
        int eggCartonJackpot = CPH.GetGlobalVar<int>("eggCartonJackpot", true);
        
        CPH.SetGlobalVar("bigNestFund", bigNestFund + bigNestContribution, true);
        CPH.SetGlobalVar("eggCartonJackpot", eggCartonJackpot + jackpotContribution, true);
        
        CPH.SendMessage($"✅ @{userName} purchased {quantity} {tokenKey}(s) for {totalCost} 🥚!");
        
        return true;
    }
}
```

   - Click **Compile** (bottom right) - you should see "Compiled Successfully"
   - Click **Save and Compile**

**3. Create the Command Trigger:**
   - Go to: `Commands` tab
   - Click **Add** button
   - **Command:** `!buy`
   - **Enabled:** ✅ Yes
   - **Permissions:** Everyone
   - Under **Action** section, select `[ECON] Buy Token`
   - **Cooldown Settings:**
     - User Cooldown: 5 seconds
     - Global Cooldown: 0 seconds
   - Click **OK**

**4. Test the Command:**
   - In your Twitch chat, type: `!buy MysteryEgg 1`
   - You should see a success message
   - Type: `!eggs` to verify your balance decreased

---
    

## Stage 3: Games (30-45 minutes)

### 3.1 Game: Chomp Tunnel - `!chomp`

**Game Mechanics:**
- **Cost:** 1 Mystery Egg per play
- **Roll:** 6-sided die (1-6)
- **Risk:** Rolling `1` = LOSS (Chain Chomp eats egg, streak resets)
- **Reward:** Rolls 2-6 = WIN (earn eggs + streak bonus)
- **Payouts:** Base 10 eggs + (5 × streak multiplier)
- **Rare Bonus:** 5% chance for Golden Egg (+100 extra eggs)

#### Step-by-Step Setup:

**1. Create the Action:**
   - Go to: `Actions` tab → Click **Add**
   - **Action Name:** `[GAME] Chomp Tunnel`
   - Click **OK**

**2. Add Execute Code Sub-Action:**
   - Click **Add Sub-Action** → `Core` → `C#` → `Execute Code`
   - **DELETE ALL** default code and paste this complete code:

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        string userId = args["userId"].ToString();
        string userName = args["userName"].ToString();
        
        // Check if user has Mystery Eggs
        string tokenVar = $"{userId}_MysteryEgg";
        int mysteryEggs = CPH.GetGlobalVar<int>(tokenVar, true);
        
        if (mysteryEggs < 1)
        {
            CPH.SendMessage($"@{userName}, you need 1 Mystery Egg! Use: !buy MysteryEgg 1");
            return false;
        }
        
        // Deduct 1 Mystery Egg
        CPH.SetGlobalVar(tokenVar, mysteryEggs - 1, true);
        
        // Roll the dice (1-6)
        Random rnd = new Random();
        int roll = rnd.Next(1, 7);
        
        // Check for rare Golden Egg (5% chance)
        bool goldenEgg = rnd.Next(1, 101) <= 5;
        
        if (roll == 1)
        {
            // Loss - Reset streak
            CPH.SetGlobalVar($"{userId}_chompStreak", 0, true);
            CPH.SendMessage($"💀 @{userName} rolled {roll}! Chain Chomp ate your egg! Streak reset.");
        }
        else
        {
            // Win - Increase streak
            int streak = CPH.GetGlobalVar<int>($"{userId}_chompStreak", true);
            streak++;
            CPH.SetGlobalVar($"{userId}_chompStreak", streak, true);
            
            // Calculate payout (base 10 + 5 per streak level)
            int payout = 10 + (streak * 5);
            
            if (goldenEgg)
            {
                payout += 100;
                CPH.AddPoints(userId, payout, "Chomp Win + Golden Egg");
                CPH.SendMessage($"🌟 @{userName} rolled {roll}! GOLDEN EGG! +{payout} 🥚 | Streak: {streak}");
            }
            else
            {
                CPH.AddPoints(userId, payout, "Chomp Win");
                CPH.SendMessage($"✅ @{userName} rolled {roll}! Safe! +{payout} 🥚 | Streak: {streak}");
            }
        }
        
        return true;
    }
}
```

   - Click **Compile** → Should say "Compiled Successfully"
   - Click **Save and Compile**

**3. Create Command Trigger:**
   - Go to: `Commands` tab → Click **Add**
   - **Command:** `!chomp`
   - **Enabled:** ✅ Yes
   - **Action:** Select `[GAME] Chomp Tunnel`
   - **User Cooldown:** 10 seconds
   - Click **OK**

**4. Test:** Buy a Mystery Egg and type `!chomp` in chat

---

### 3.2 Game: Hatch Roll - `!eggroll`

**Game Mechanics:**
- **Cost:** 1 Dice Egg per roll
- **Roll:** 20-sided die (D20)
- **Rewards by Roll:**
  - **1:** Nothing hatches (0 eggs)
  - **2-5:** Small hatch (5 eggs)
  - **6-10:** Medium hatch (15 eggs)
  - **11-15:** Good hatch (30 eggs)
  - **16-18:** Great hatch (50 eggs)
  - **19-20:** JACKPOT hatch (100 eggs)

#### Step-by-Step Setup:

**1. Create the Action:**
   - Go to: `Actions` tab → Click **Add**
   - **Action Name:** `[GAME] Hatch Roll`
   - Click **OK**

**2. Add Execute Code Sub-Action:**
   - Click **Add Sub-Action** → `Core` → `C#` → `Execute Code`
   - **DELETE ALL** default code and paste:

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        string userId = args["userId"].ToString();
        string userName = args["userName"].ToString();
        
        // Check if user has Dice Eggs
        string tokenVar = $"{userId}_DiceEgg";
        int diceEggs = CPH.GetGlobalVar<int>(tokenVar, true);
        
        if (diceEggs < 1)
        {
            CPH.SendMessage($"@{userName}, you need 1 Dice Egg! Use: !buy DiceEgg 1");
            return false;
        }
        
        // Deduct 1 Dice Egg
        CPH.SetGlobalVar(tokenVar, diceEggs - 1, true);
        
        // Roll D20
        Random rnd = new Random();
        int roll = rnd.Next(1, 21);
        
        int payout = 0;
        string message = "";
        
        if (roll == 1)
        {
            message = $"💔 @{userName} rolled {roll}! Your egg hatched into nothing!";
        }
        else if (roll <= 5)
        {
            payout = 5;
            message = $"🥚 @{userName} rolled {roll}! Small hatch! +{payout} 🥚";
        }
        else if (roll <= 10)
        {
            payout = 15;
            message = $"🐣 @{userName} rolled {roll}! Medium hatch! +{payout} 🥚";
        }
        else if (roll <= 15)
        {
            payout = 30;
            message = $"🐥 @{userName} rolled {roll}! Good hatch! +{payout} 🥚";
        }
        else if (roll <= 18)
        {
            payout = 50;
            message = $"🌟 @{userName} rolled {roll}! Great hatch! +{payout} 🥚";
        }
        else // 19-20
        {
            payout = 100;
            message = $"🎉 @{userName} rolled {roll}! JACKPOT HATCH! +{payout} 🥚";
        }
        
        if (payout > 0)
        {
            CPH.AddPoints(userId, payout, "Hatch Roll Win");
        }
        
        CPH.SendMessage(message);
        
        return true;
    }
}
```

   - Click **Compile** → **Save and Compile**

**3. Create Command Trigger:**
   - Go to: `Commands` tab → Click **Add**
   - **Command:** `!eggroll`
   - **Enabled:** ✅ Yes
   - **Action:** Select `[GAME] Hatch Roll`
   - **User Cooldown:** 10 seconds
   - Click **OK**

**4. Test:** Buy a Dice Egg and type `!eggroll` in chat

---

### 3.3 Game: Duel Nest PvP - `!duelnest` & `!accept`

**Game Mechanics:**
- **Cost:** 1 Duel Egg per player + wager amount
- **Process:**
  1. Challenger uses `!duelnest @opponent <wager>`
  2. Opponent has 2 minutes to `!accept`
  3. Duel auto-resolves after 10 minutes
  4. Winner gets their wager back + 85% of loser's wager
  5. 15% goes to economy sink (bigNestFund)

#### Part A: Challenge Command

**1. Create the Action:**
   - Go to: `Actions` tab → Click **Add**
   - **Action Name:** `[PVP] Duel Challenge`
   - Click **OK**

**2. Add Execute Code Sub-Action:**
   - Click **Add Sub-Action** → `Core` → `C#` → `Execute Code`
   - **DELETE ALL** default code and paste:

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        string challengerId = args["userId"].ToString();
        string challengerName = args["userName"].ToString();
        string opponentName = args["rawInput0"]?.ToString()?.TrimStart('@');
        
        // Validate wager
        if (args["rawInput1"] == null || !int.TryParse(args["rawInput1"].ToString(), out int wager) || wager < 1)
        {
            CPH.SendMessage($"@{challengerName}, usage: !duelnest @username <wager>");
            return false;
        }
        
        // Validate opponent
        if (string.IsNullOrEmpty(opponentName))
        {
            CPH.SendMessage($"@{challengerName}, please specify an opponent!");
            return false;
        }
        
        // Check for Duel Egg
        string challengerTokenVar = $"{challengerId}_DuelEgg";
        int challengerDuelEggs = CPH.GetGlobalVar<int>(challengerTokenVar, true);
        
        if (challengerDuelEggs < 1)
        {
            CPH.SendMessage($"@{challengerName}, you need 1 Duel Egg! Use: !buy DuelEgg 1");
            return false;
        }
        
        // Check balance
        int challengerBalance = CPH.GetPoints(challengerId);
        if (challengerBalance < wager)
        {
            CPH.SendMessage($"@{challengerName}, you need {wager} 🥚 but have {challengerBalance} 🥚");
            return false;
        }
        
        // Store challenge
        CPH.SetGlobalVar("duel_challenger", challengerId, true);
        CPH.SetGlobalVar("duel_challengerName", challengerName, true);
        CPH.SetGlobalVar("duel_opponentName", opponentName, true);
        CPH.SetGlobalVar("duel_wager", wager, true);
        CPH.SetGlobalVar("duel_timestamp", DateTime.Now.Ticks, true);
        
        CPH.SendMessage($"⚔️ @{opponentName}, {challengerName} challenges you to Duel Nest for {wager} 🥚! Type !accept within 2 minutes!");
        
        return true;
    }
}
```

   - Click **Compile** → **Save and Compile**

**3. Create Command Trigger:**
   - Go to: `Commands` tab → Click **Add**
   - **Command:** `!duelnest`
   - **Enabled:** ✅ Yes
   - **Action:** Select `[PVP] Duel Challenge`
   - **User Cooldown:** 30 seconds
   - Click **OK**

#### Part B: Accept Command

**1. Create the Action:**
   - Go to: `Actions` tab → Click **Add**
   - **Action Name:** `[PVP] Duel Accept`
   - Click **OK**

**2. Add Execute Code Sub-Action:**
   - Click **Add Sub-Action** → `Core` → `C#` → `Execute Code`
   - **DELETE ALL** default code and paste:

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        string accepterId = args["userId"].ToString();
        string accepterName = args["userName"].ToString();
        
        // Check for active challenge
        string opponentName = CPH.GetGlobalVar<string>("duel_opponentName", true);
        
        if (opponentName == null || !opponentName.Equals(accepterName, StringComparison.OrdinalIgnoreCase))
        {
            CPH.SendMessage($"@{accepterName}, no active duel challenge for you!");
            return false;
        }
        
        // Check timestamp (2 minute window)
        long challengeTime = CPH.GetGlobalVar<long>("duel_timestamp", true);
        TimeSpan elapsed = TimeSpan.FromTicks(DateTime.Now.Ticks - challengeTime);
        
        if (elapsed.TotalMinutes > 2)
        {
            CPH.SendMessage($"@{accepterName}, the challenge expired!");
            CPH.UnsetGlobalVar("duel_challenger", true);
            CPH.UnsetGlobalVar("duel_challengerName", true);
            CPH.UnsetGlobalVar("duel_opponentName", true);
            CPH.UnsetGlobalVar("duel_wager", true);
            CPH.UnsetGlobalVar("duel_timestamp", true);
            return false;
        }
        
        // Get challenge details
        string challengerId = CPH.GetGlobalVar<string>("duel_challenger", true);
        string challengerName = CPH.GetGlobalVar<string>("duel_challengerName", true);
        int wager = CPH.GetGlobalVar<int>("duel_wager", true);
        
        // Check accepter's Duel Egg
        string accepterTokenVar = $"{accepterId}_DuelEgg";
        int accepterDuelEggs = CPH.GetGlobalVar<int>(accepterTokenVar, true);
        
        if (accepterDuelEggs < 1)
        {
            CPH.SendMessage($"@{accepterName}, you need 1 Duel Egg! Use: !buy DuelEgg 1");
            return false;
        }
        
        // Check accepter's balance
        int accepterBalance = CPH.GetPoints(accepterId);
        if (accepterBalance < wager)
        {
            CPH.SendMessage($"@{accepterName}, you need {wager} 🥚 but have {accepterBalance} 🥚");
            return false;
        }
        
        // Deduct Duel Eggs from both
        string challengerTokenVar = $"{challengerId}_DuelEgg";
        int challengerDuelEggs = CPH.GetGlobalVar<int>(challengerTokenVar, true);
        CPH.SetGlobalVar(challengerTokenVar, challengerDuelEggs - 1, true);
        CPH.SetGlobalVar(accepterTokenVar, accepterDuelEggs - 1, true);
        
        // Store active duel for resolution
        CPH.SetGlobalVar("activeDuel_challenger", challengerId, true);
        CPH.SetGlobalVar("activeDuel_challengerName", challengerName, true);
        CPH.SetGlobalVar("activeDuel_accepter", accepterId, true);
        CPH.SetGlobalVar("activeDuel_accepterName", accepterName, true);
        CPH.SetGlobalVar("activeDuel_wager", wager, true);
        CPH.SetGlobalVar("activeDuel_startTime", DateTime.Now.Ticks, true);
        
        CPH.SendMessage($"⚔️ DUEL ACCEPTED! {challengerName} vs {accepterName} for {wager} 🥚! Auto-resolves in 10 minutes!");
        
        // Clear challenge
        CPH.UnsetGlobalVar("duel_challenger", true);
        CPH.UnsetGlobalVar("duel_challengerName", true);
        CPH.UnsetGlobalVar("duel_opponentName", true);
        CPH.UnsetGlobalVar("duel_wager", true);
        CPH.UnsetGlobalVar("duel_timestamp", true);
        
        return true;
    }
}
```

   - Click **Compile** → **Save and Compile**

**3. Create Command Trigger:**
   - Go to: `Commands` tab → Click **Add**
   - **Command:** `!accept`
   - **Enabled:** ✅ Yes
   - **Action:** Select `[PVP] Duel Accept`
   - **User Cooldown:** 5 seconds
   - Click **OK**

#### Part C: Auto-Resolver (REQUIRED for duels to complete)

**1. Create the Action:**
   - Go to: `Actions` tab → Click **Add**
   - **Action Name:** `[PVP] Duel Resolver`
   - Click **OK**

**2. Add Execute Code Sub-Action:**
   - Click **Add Sub-Action** → `Core` → `C#` → `Execute Code`
   - **DELETE ALL** default code and paste:

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        // Check for active duel
        string challengerId = CPH.GetGlobalVar<string>("activeDuel_challenger", true);
        if (string.IsNullOrEmpty(challengerId))
        {
            return false; // No active duel
        }
        
        // Check if 10 minutes passed
        long startTime = CPH.GetGlobalVar<long>("activeDuel_startTime", true);
        TimeSpan elapsed = TimeSpan.FromTicks(DateTime.Now.Ticks - startTime);
        
        if (elapsed.TotalMinutes < 10)
        {
            return false; // Not time yet
        }
        
        // Get duel details
        string challengerName = CPH.GetGlobalVar<string>("activeDuel_challengerName", true);
        string accepterId = CPH.GetGlobalVar<string>("activeDuel_accepter", true);
        string accepterName = CPH.GetGlobalVar<string>("activeDuel_accepterName", true);
        int wager = CPH.GetGlobalVar<int>("activeDuel_wager", true);
        
        // Random rolls to determine winner
        Random rnd = new Random();
        int challengerRoll = rnd.Next(1, 101);
        int accepterRoll = rnd.Next(1, 101);
        
        string winner, loser, winnerId, loserId;
        int winnerRoll, loserRoll;
        
        if (challengerRoll > accepterRoll)
        {
            winner = challengerName;
            winnerId = challengerId;
            loser = accepterName;
            loserId = accepterId;
            winnerRoll = challengerRoll;
            loserRoll = accepterRoll;
        }
        else
        {
            winner = accepterName;
            winnerId = accepterId;
            loser = challengerName;
            loserId = challengerId;
            winnerRoll = accepterRoll;
            loserRoll = challengerRoll;
        }
        
        // Calculate payouts
        int totalPot = wager * 2;
        int winnerPayout = (int)(wager + (wager * 0.85)); // Own wager + 85% of opponent's
        int sinkAmount = totalPot - winnerPayout;
        
        // Deduct wagers
        CPH.RemovePoints(challengerId, wager, "Duel Wager");
        CPH.RemovePoints(accepterId, wager, "Duel Wager");
        
        // Award winner
        CPH.AddPoints(winnerId, winnerPayout, "Duel Win");
        
        // Add to bigNestFund
        int bigNestFund = CPH.GetGlobalVar<int>("bigNestFund", true);
        CPH.SetGlobalVar("bigNestFund", bigNestFund + sinkAmount, true);
        
        // Update stats
        int winnerDuelWins = CPH.GetGlobalVar<int>($"{winnerId}_duelWins", true);
        int loserDuelLosses = CPH.GetGlobalVar<int>($"{loserId}_duelLosses", true);
        CPH.SetGlobalVar($"{winnerId}_duelWins", winnerDuelWins + 1, true);
        CPH.SetGlobalVar($"{loserId}_duelLosses", loserDuelLosses + 1, true);
        
        CPH.SendMessage($"⚔️ DUEL RESULT: {winner} ({winnerRoll}) defeats {loser} ({loserRoll})! {winner} wins {winnerPayout} 🥚!");
        
        // Clear active duel
        CPH.UnsetGlobalVar("activeDuel_challenger", true);
        CPH.UnsetGlobalVar("activeDuel_challengerName", true);
        CPH.UnsetGlobalVar("activeDuel_accepter", true);
        CPH.UnsetGlobalVar("activeDuel_accepterName", true);
        CPH.UnsetGlobalVar("activeDuel_wager", true);
        CPH.UnsetGlobalVar("activeDuel_startTime", true);
        
        return true;
    }
}
```

   - Click **Compile** → **Save and Compile**

**4. Create Timed Action (CRITICAL):**
   - Go to: `Actions` tab
   - Look for **Timed Actions** section (usually at bottom)
   - Click **Add Timed Action**
   - **Name:** `Duel Resolver Timer`
   - **Enabled:** ✅ Yes
   - **Interval:** **60 seconds** (checks every minute)
   - **Action:** Select `[PVP] Duel Resolver`
   - **Repeat:** ✅ Yes (infinite loop)
   - Click **OK**

**5. Test:** Challenge someone, accept, wait 10 minutes (or temporarily change code to 1 minute for testing)

---

## Stage 4: User Commands (15 minutes)

All commands are set up within Streamer.bot using the same pattern as the games above.

### 4.1 Leaderboard Command - `!top`

**OPTION A: Use Streamer.bot's Built-in Leaderboard (RECOMMENDED - 2 minutes)**

1. In Streamer.bot, go to: `Settings` → `Loyalty` → `Commands`
2. Find the built-in `!top` or `!leaderboard` command
3. Enable it with ✅ checkbox
4. Customize the message format to mention "🥚 Pouch Eggs"
5. Save settings

**OPTION B: Custom Leaderboard Action (If built-in not available)**

*Note: Streamer.bot's API for querying top users may vary by version. This shows a simple implementation:*

1. Go to: `Actions` tab → Click **Add**
2. **Action Name:** `[USER] Leaderboard`
3. Click **Add Sub-Action** → `Core` → `Twitch` → `Send Message`
4. **Message:** `🏆 Top Egg Holders! Use Streamer.bot's loyalty panel to see the leaderboard, or check !eggs to see your balance!`
5. Go to: `Commands` tab → Click **Add**
6. **Command:** `!top`
7. **Action:** Select `[USER] Leaderboard`
8. **User Cooldown:** 30 seconds
9. Click **OK**

---

### 4.2 Progression Ranks - `!titles`

**Rank Tiers:**
- **Hatchling:** 0-99 🥚
- **Egg Runner:** 100-499 🏃
- **Nest Builder:** 500-999 🏠
- **Egg Guardian:** 1,000-2,499 🛡️
- **Yoshi Knight:** 2,500-4,999 ⚔️
- **Grand Yoshi:** 5,000-9,999 👑
- **Egg Emperor:** 10,000+ 🌟

#### Step-by-Step Setup:

**1. Create the Action:**
   - Go to: `Actions` tab → Click **Add**
   - **Action Name:** `[USER] View Titles`
   - Click **OK**

**2. Add Execute Code Sub-Action:**
   - Click **Add Sub-Action** → `Core` → `C#` → `Execute Code`
   - **DELETE ALL** default code and paste:

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        string userId = args["userId"].ToString();
        string userName = args["userName"].ToString();
        int pouchEggs = CPH.GetPoints(userId);
        
        string rank = "", icon = "", nextRank = "";
        int nextThreshold = 0;
        
        if (pouchEggs < 100) { rank = "Hatchling"; icon = "🥚"; nextRank = "Egg Runner"; nextThreshold = 100; }
        else if (pouchEggs < 500) { rank = "Egg Runner"; icon = "🏃"; nextRank = "Nest Builder"; nextThreshold = 500; }
        else if (pouchEggs < 1000) { rank = "Nest Builder"; icon = "🏠"; nextRank = "Egg Guardian"; nextThreshold = 1000; }
        else if (pouchEggs < 2500) { rank = "Egg Guardian"; icon = "🛡️"; nextRank = "Yoshi Knight"; nextThreshold = 2500; }
        else if (pouchEggs < 5000) { rank = "Yoshi Knight"; icon = "⚔️"; nextRank = "Grand Yoshi"; nextThreshold = 5000; }
        else if (pouchEggs < 10000) { rank = "Grand Yoshi"; icon = "👑"; nextRank = "Egg Emperor"; nextThreshold = 10000; }
        else { rank = "Egg Emperor"; icon = "🌟"; nextRank = "MAX"; nextThreshold = 0; }
        
        string message = $"@{userName} | {icon} {rank} ({pouchEggs} 🥚)";
        if (nextThreshold > 0) {
            message += $" | Next: {nextRank} ({nextThreshold - pouchEggs} needed)";
        } else {
            message += " | 🎉 MAX RANK!";
        }
        
        CPH.SendMessage(message);
        return true;
    }
}
```

   - Click **Compile** → **Save and Compile**

**3. Create Command Trigger:**
   - Go to: `Commands` tab → Click **Add**
   - **Command:** `!titles`
   - **Enabled:** ✅ Yes
   - **Action:** Select `[USER] View Titles`
   - **User Cooldown:** 15 seconds
   - Click **OK**

---

### 4.3 View Inventory - `!eggpack`

Displays user's current token and egg balances.

#### Step-by-Step Setup:

**1. Create the Action:**
   - Go to: `Actions` tab → Click **Add**
   - **Action Name:** `[USER] View Inventory`
   - Click **OK**

**2. Add Execute Code Sub-Action:**
   - Click **Add Sub-Action** → `Core` → `C#` → `Execute Code`
   - **DELETE ALL** default code and paste:

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        string userId = args["userId"].ToString();
        string userName = args["userName"].ToString();
        
        int mysteryEggs = CPH.GetGlobalVar<int>($"{userId}_MysteryEgg", true);
        int diceEggs = CPH.GetGlobalVar<int>($"{userId}_DiceEgg", true);
        int duelEggs = CPH.GetGlobalVar<int>($"{userId}_DuelEgg", true);
        int pouchEggs = CPH.GetPoints(userId);
        
        CPH.SendMessage($"@{userName}'s Egg Pack 🎒 | {pouchEggs} 🥚 | {mysteryEggs} Mystery 🔮 | {diceEggs} Dice 🎲 | {duelEggs} Duel ⚔️");
        
        return true;
    }
}
```

   - Click **Compile** → **Save and Compile**

**3. Create Command Trigger:**
   - Go to: `Commands` tab → Click **Add**
   - **Command:** `!eggpack`
   - **Enabled:** ✅ Yes
   - **Action:** Select `[USER] View Inventory`
   - **User Cooldown:** 10 seconds
   - Click **OK**

---

### 4.4 Character Stats - `!sheet`

Shows user's game statistics (streaks, wins, losses).

#### Step-by-Step Setup:

**1. Create the Action:**
   - Go to: `Actions` tab → Click **Add**
   - **Action Name:** `[USER] View Character Sheet`
   - Click **OK**

**2. Add Execute Code Sub-Action:**
   - Click **Add Sub-Action** → `Core` → `C#` → `Execute Code`
   - **DELETE ALL** default code and paste:

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        string userId = args["userId"].ToString();
        string userName = args["userName"].ToString();
        
        int chompStreak = CPH.GetGlobalVar<int>($"{userId}_chompStreak", true);
        int chompWins = CPH.GetGlobalVar<int>($"{userId}_chompWins", true);
        int eggrollPlays = CPH.GetGlobalVar<int>($"{userId}_eggrollPlays", true);
        int duelWins = CPH.GetGlobalVar<int>($"{userId}_duelWins", true);
        int duelLosses = CPH.GetGlobalVar<int>($"{userId}_duelLosses", true);
        
        CPH.SendMessage($"@{userName}'s Stats 📋 | Chomp Streak: {chompStreak} | Egg Rolls: {eggrollPlays} | Duels: {duelWins}W/{duelLosses}L");
        
        return true;
    }
}
```

   - Click **Compile** → **Save and Compile**

**3. Create Command Trigger:**
   - Go to: `Commands` tab → Click **Add**
   - **Command:** `!sheet`
   - **Enabled:** ✅ Yes
   - **Action:** Select `[USER] View Character Sheet`
   - **User Cooldown:** 10 seconds
   - Click **OK**

---

### 4.5 Reset Character - `!reroll`

Allows users to reset all stats and tokens for 1,000 Pouch Eggs.

#### Step-by-Step Setup:

**1. Create the Action:**
   - Go to: `Actions` tab → Click **Add**
   - **Action Name:** `[USER] Reset Character`
   - Click **OK**

**2. Add Execute Code Sub-Action:**
   - Click **Add Sub-Action** → `Core` → `C#` → `Execute Code`
   - **DELETE ALL** default code and paste:

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        string userId = args["userId"].ToString();
        string userName = args["userName"].ToString();
        
        int resetCost = 1000;
        int userBalance = CPH.GetPoints(userId);
        
        if (userBalance < resetCost)
        {
            CPH.SendMessage($"@{userName}, character reroll costs {resetCost} 🥚. You have {userBalance} 🥚");
            return false;
        }
        
        // Deduct cost
        CPH.RemovePoints(userId, resetCost, "Character Reroll");
        
        // Reset all stats and tokens
        CPH.SetGlobalVar($"{userId}_chompStreak", 0, true);
        CPH.SetGlobalVar($"{userId}_chompWins", 0, true);
        CPH.SetGlobalVar($"{userId}_eggrollPlays", 0, true);
        CPH.SetGlobalVar($"{userId}_duelWins", 0, true);
        CPH.SetGlobalVar($"{userId}_duelLosses", 0, true);
        CPH.SetGlobalVar($"{userId}_MysteryEgg", 0, true);
        CPH.SetGlobalVar($"{userId}_DiceEgg", 0, true);
        CPH.SetGlobalVar($"{userId}_DuelEgg", 0, true);
        
        CPH.SendMessage($"🔄 @{userName} rerolled for {resetCost} 🥚! All stats and tokens reset.");
        
        return true;
    }
}
```

   - Click **Compile** → **Save and Compile**

**3. Create Command Trigger:**
   - Go to: `Commands` tab → Click **Add**
   - **Command:** `!reroll`
   - **Enabled:** ✅ Yes
   - **Action:** Select `[USER] Reset Character`
   - **User Cooldown:** 60 seconds
   - Click **OK**

---

---

### 4.5 Reset Character
**Command:** `!reroll`

Allows the user to reset their character stats for a fee of 1,000 Pouch Eggs.

#### Implementation Steps:
1. **Create the Action:** `[USER] Reset Character`
2. **Add Reset Logic:**
    ```csharp
    string userId = args["userId"].ToString();
    string userName = args["userName"].ToString();
    
    int resetCost = 1000;
    int userBalance = CPH.GetPoints(userId);
    
    // Check if user has enough eggs
    if (userBalance < resetCost)
    {
        CPH.SendMessage($"@{userName}, character reroll costs {resetCost} Pouch Eggs. You only have {userBalance}.");
        return false;
    }
    
    // Deduct cost
    CPH.RemovePoints(userId, resetCost);
    
    // Reset all stats and tokens
    CPH.SetGlobalVar($"{userId}_chompStreak", 0, true);
    CPH.SetGlobalVar($"{userId}_chompWins", 0, true);
    CPH.SetGlobalVar($"{userId}_eggrollPlays", 0, true);
    CPH.SetGlobalVar($"{userId}_duelWins", 0, true);
    CPH.SetGlobalVar($"{userId}_duelLosses", 0, true);
    CPH.SetGlobalVar($"{userId}_MysteryEgg", 0, true);
    CPH.SetGlobalVar($"{userId}_DiceEgg", 0, true);
    CPH.SetGlobalVar($"{userId}_DuelEgg", 0, true);
    
    CPH.SendMessage($"@{userName} has rerolled their character for {resetCost} Pouch Eggs! All stats and tokens reset. 🔄");
    
    return true;
    ```

3. **Configure Command Trigger:**
    - **Command:** `!reroll`
    - **Permissions:** Everyone
    - **Cooldown:** 60 seconds per user

---

## Stage 5: Economy Balance and Maintenance

### 5.1 Currency Sinks
The economy includes several sinks to prevent inflation:
- **Token Purchases:** 10% of every purchase is removed from circulation.
- **Duel Nest:** 15% of the total pot goes to `bigNestFund`.
- **Character Reroll:** 1,000 eggs are removed from circulation.

### 5.2 Global Funds
Two global funds are maintained:
- **`bigNestFund`**: Can be used for special events, giveaways, or jackpots.
- **`eggCartonJackpot`**: Can be used for periodic lottery drawings or milestone rewards.

### 5.3 Monitoring Commands (Moderator Only)
Create moderator-only commands to check the health of the economy:

**Command:** `!econfunds`
```csharp
int bigNestFund = CPH.GetGlobalVar<int>("bigNestFund", true);
int eggCartonJackpot = CPH.GetGlobalVar<int>("eggCartonJackpot", true);

CPH.SendMessage($"Economy Funds 💰: Big Nest Fund: {bigNestFund} | Egg Carton Jackpot: {eggCartonJackpot}");
```

---

## Stage 6: Quick Reference

### Command Summary
| Command | Description | Cost |
|---------|-------------|------|
| `!eggs` | Check Pouch Egg balance | Free |
| `!buy <token> <qty>` | Purchase tokens | Varies by token |
| `!chomp` | Play Chomp Tunnel | 1 Mystery Egg |
| `!eggroll` | Play Hatch Roll | 1 Dice Egg |
| `!duelnest @user <wager>` | Challenge to PvP | 1 Duel Egg + wager |
| `!accept` | Accept a duel challenge | 1 Duel Egg + wager |
| `!top` | View leaderboard of top egg holders | Free |
| `!titles` | View rank progression and your current rank | Free |
| `!eggpack` | View your inventory | Free |
| `!sheet` | View your character stats | Free |
| `!reroll` | Reset your character | 1,000 Pouch Eggs |
| `!econfunds` | Check economy fund balances (Mod only) | Free |

### Token Costs
- **Mystery Egg:** 20 Pouch Eggs
- **Dice Egg:** 10 Pouch Eggs
- **Duel Egg:** 5 Pouch Eggs

---

## Implementation Notes

### Streamer.bot Setup Requirements
1. **C# Scripting:** All actions use C# code for Streamer.bot.
2. **Global Variables:** Initialize `bigNestFund` and `eggCartonJackpot` to 0.
3. **Timer Actions:** Set up a timer to run the `[PVP] Duel Nest Resolver` action every 1 minute.
4. **User Variables:** The system uses per-user global variables with the format `{userId}_{variableName}`.

### Testing Recommendations
1. Test each command individually before enabling for all users.
2. Start with small wager amounts in Duel Nest to ensure payouts work correctly.
3. Monitor the economy funds regularly to ensure balance.
4. Adjust passive income rates if inflation becomes an issue.

### Future Enhancements
- Add leaderboards for top players.
- Implement seasonal events with special eggs.
- Create team-based egg battles.
- Add achievement system with egg rewards.

---

This unified guide provides everything needed to implement a complete, balanced egg-based economy in Streamer.bot. All components work together to create an engaging and sustainable system for your community!