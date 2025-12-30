# Quick Start Guide - 30 Minutes to Working Economy

**Platform:** Streamer.bot (v0.2.0+)  
**Time Required:** 30-45 minutes  
**Difficulty:** Beginner-friendly

This guide gets you from zero to a working egg economy in under an hour. Follow these steps exactly for fastest setup.

---

## What You'll Have After This Guide

✅ Main currency (Pouch Eggs) with passive income  
✅ Three token types players can buy  
✅ One working game (Chomp Tunnel)  
✅ Basic user commands (!eggs, !eggpack, !titles)  
✅ Economy monitoring command for you  

**After this works, you can add:**
- More games (Hatch Roll, Duel Nest)
- Event system (Double Rewards, Free Entry)
- Advanced features (Achievements, Teams, Season Pass)

---

## Prerequisites Checklist

Before starting, ensure:
- [ ] Streamer.bot v0.2.0+ installed
- [ ] Connected to your Twitch account
- [ ] You can access Actions and Commands tabs
- [ ] You have 30 minutes of uninterrupted time

---

## Phase 1: Currency Setup (5 minutes)

### Step 1.1: Enable Loyalty Points

1. Open Streamer.bot
2. Go to: **Settings** → **Loyalty** → **Points Settings**
3. Configure these fields:

| Setting | Value |
|---------|-------|
| **Enable Loyalty Points** | ✅ Checked |
| **Currency Name (Singular)** | `🥚 Pouch Egg` |
| **Currency Name (Plural)** | `🥚 Pouch Eggs` |
| **Default Command** | `!eggs` |
| **Online Viewers** | `5` eggs per `10` minutes |
| **Active Chatters** | `10` eggs per `10` minutes |

4. Click **Save**

**Test:** Type `!eggs` in your chat → Should show your balance

---

### Step 1.2: Create Economy Variables

1. Go to: **Settings** → **Variables**
2. Click **Add** button twice to create these:

**Variable 1:**
- Name: `bigNestFund`
- Type: Number
- Value: `1000`
- Persisted: ✅ Yes

**Variable 2:**
- Name: `eggCartonJackpot`
- Type: Number
- Value: `500`
- Persisted: ✅ Yes

3. Click **Save**

---

## Phase 2: Token Purchase System (10 minutes)

### Step 2.1: Create Buy Token Action

1. Go to: **Actions** tab
2. Click **Add**
3. Name: `[ECON] Buy Token`
4. Click **OK**

---

### Step 2.2: Add Code

1. With action selected, click **Add Sub-Action**
2. Choose: **Core** → **C#** → **Execute Code**
3. **Delete ALL default code**
4. Paste this code:

```csharp
using System;
using System.Collections.Generic;

public class CPHInline
{
    public bool Execute()
    {
        string userId = args["userId"].ToString();
        string userName = args["userName"].ToString();
        string tokenType = args["rawInput0"]?.ToString();
        
        if (args["rawInput1"] == null || !int.TryParse(args["rawInput1"].ToString(), out int quantity) || quantity < 1)
        {
            CPH.SendMessage($"@{userName}, please specify a valid quantity! Example: !buy MysteryEgg 1");
            return false;
        }
        
        Dictionary<string, int> tokenCosts = new Dictionary<string, int>
        {
            {"MysteryEgg", 20},
            {"DiceEgg", 10},
            {"DuelEgg", 5}
        };
        
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
        
        int totalCost = tokenCosts[tokenKey] * quantity;
        int userBalance = CPH.GetPoints(userId);
        
        if (userBalance < totalCost)
        {
            CPH.SendMessage($"@{userName}, you need {totalCost} 🥚 but only have {userBalance} 🥚");
            return false;
        }
        
        CPH.RemovePoints(userId, totalCost, "Token Purchase");
        
        string tokenVar = $"{userId}_{tokenKey}";
        int currentTokens = CPH.GetGlobalVar<int>(tokenVar, true);
        CPH.SetGlobalVar(tokenVar, currentTokens + quantity, true);
        
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

5. Click **Compile** (bottom right)
6. Should say "Compiled Successfully"
7. Click **Save and Compile**

---

### Step 2.3: Create Command

1. Go to: **Commands** tab
2. Click **Add**
3. Configure:

| Setting | Value |
|---------|-------|
| **Command** | `!buy` |
| **Enabled** | ✅ Yes |
| **Permissions** | Everyone |
| **Action** | `[ECON] Buy Token` |
| **User Cooldown** | `5` seconds |

4. Click **OK**

**Test:** Type `!buy MysteryEgg 1` in chat → Should cost 20 eggs

---

## Phase 3: First Game - Chomp Tunnel (10 minutes)

### Step 3.1: Create Game Action

1. **Actions** tab → **Add**
2. Name: `[GAME] Chomp Tunnel`
3. **OK**

---

### Step 3.2: Add Game Code

1. **Add Sub-Action** → **Core** → **C#** → **Execute Code**
2. **Delete all default code**
3. Paste this:

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        string userId = args["userId"].ToString();
        string userName = args["userName"].ToString();
        
        string tokenVar = $"{userId}_MysteryEgg";
        int mysteryEggs = CPH.GetGlobalVar<int>(tokenVar, true);
        
        if (mysteryEggs < 1)
        {
            CPH.SendMessage($"@{userName}, you need 1 Mystery Egg! Use: !buy MysteryEgg 1");
            return false;
        }
        
        CPH.SetGlobalVar(tokenVar, mysteryEggs - 1, true);
        
        Random rnd = new Random();
        int roll = rnd.Next(1, 7);
        
        bool goldenEgg = rnd.Next(1, 101) <= 5;
        
        if (roll == 1)
        {
            CPH.SetGlobalVar($"{userId}_chompStreak", 0, true);
            CPH.SendMessage($"💀 @{userName} rolled {roll}! Chain Chomp ate your egg! Streak reset.");
        }
        else
        {
            int streak = CPH.GetGlobalVar<int>($"{userId}_chompStreak", true);
            streak++;
            CPH.SetGlobalVar($"{userId}_chompStreak", streak, true);
            
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

4. **Compile** → Should succeed
5. **Save and Compile**

---

### Step 3.3: Create Game Command

1. **Commands** tab → **Add**
2. Configure:

| Setting | Value |
|---------|-------|
| **Command** | `!chomp` |
| **Enabled** | ✅ Yes |
| **Permissions** | Everyone |
| **Action** | `[GAME] Chomp Tunnel` |
| **User Cooldown** | `10` seconds |

3. **OK**

**Test:**
```
!buy MysteryEgg 1  → Buy token
!chomp             → Play game
```

---

## Phase 4: User Commands (5 minutes)

### Command 1: View Inventory (!eggpack)

**Create Action:**
1. **Actions** → **Add** → Name: `[USER] View Inventory`
2. **Add Sub-Action** → **Execute Code**
3. Paste:

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

4. **Compile & Save**

**Create Command:**
- Command: `!eggpack`
- Enabled: ✅
- Action: `[USER] View Inventory`
- Cooldown: 10 seconds

---

### Command 2: View Rank (!titles)

**Create Action:**
1. **Actions** → **Add** → Name: `[USER] View Titles`
2. **Execute Code**:

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

3. **Compile & Save**

**Create Command:**
- Command: `!titles`
- Enabled: ✅
- Action: `[USER] View Titles`
- Cooldown: 15 seconds

---

## Phase 5: Moderator Monitoring (5 minutes)

**Create Action:**
1. **Actions** → **Add** → Name: `[MOD] Check Economy Funds`
2. **Execute Code**:

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        int bigNestFund = CPH.GetGlobalVar<int>("bigNestFund", true);
        int eggCartonJackpot = CPH.GetGlobalVar<int>("eggCartonJackpot", true);
        
        CPH.SendMessage($"💰 Economy Funds | Big Nest: {bigNestFund} 🥚 | Jackpot: {eggCartonJackpot} 🥚");
        
        return true;
    }
}
```

3. **Compile & Save**

**Create Command:**
- Command: `!econfunds`
- Enabled: ✅
- Permissions: **Moderators only**
- Action: `[MOD] Check Economy Funds`
- Cooldown: 30 seconds

---

## Testing Phase (5 minutes)

### Complete Test Checklist

Run these tests in order:

1. **Currency Test**
   ```
   !eggs  → Shows your balance
   ```

2. **Buy Token Test**
   ```
   !buy MysteryEgg 2  → Costs 40 eggs
   ```

3. **Inventory Test**
   ```
   !eggpack  → Shows 2 Mystery Eggs
   ```

4. **Game Test**
   ```
   !chomp  → Rolls dice, awards/loses eggs
   !chomp  → Try again (should work if you have tokens)
   ```

5. **Rank Test**
   ```
   !titles  → Shows your current rank
   ```

6. **Economy Test** (if moderator)
   ```
   !econfunds  → Shows fund balances
   ```

**All Tests Pass?** ✅ You're done! Economy is live!

---

## What's Next?

Now that core system works, you can:

### Immediate Next Steps:
1. **Add More Games**
   - Hatch Roll (dice game)
   - Duel Nest (PvP)
   - See: [Unified Guide](Unified_Yoshi_Eggonomy.md)

2. **Add Event System**
   - Double Rewards Hour
   - Free Entry events
   - See: [Event System Guide](Event_System_Guide.md)

3. **Customize**
   - Change token costs
   - Adjust game payouts
   - Create custom ranks

### Advanced Features:
- **Custom Tokens** - Add your own token types
- **New Games** - Create unique games for your community
- **Achievements** - Unlock system with rewards
- **Teams** - Team-based competitions
- **Season Pass** - XP progression system

**See:** [Advanced Features Guide](Advanced_Features_Guide.md)

---

## Troubleshooting

**Command not working?**
- Check command is **Enabled** (✅ checkbox)
- Verify Streamer.bot is **Connected** to Twitch
- Check **Logs** (View → Logs) for errors

**Code won't compile?**
- Make sure you **deleted ALL default code** before pasting
- Check you have `using System;` at the top
- Class name must be exactly `CPHInline`

**Variables not saving?**
- Ensure `persisted: true` in all GetGlobalVar/SetGlobalVar calls
- Check Settings → Variables to see if they exist

**For detailed troubleshooting:** See [Troubleshooting Guide](Troubleshooting_Guide.md)

---

## Command Reference

| Command | Description | Who Can Use |
|---------|-------------|-------------|
| `!eggs` | Check balance | Everyone |
| `!buy <token> <qty>` | Buy tokens | Everyone |
| `!chomp` | Play Chomp Tunnel | Everyone (needs Mystery Egg) |
| `!eggpack` | View inventory | Everyone |
| `!titles` | View rank | Everyone |
| `!econfunds` | Check economy funds | Moderators only |

---

## Success Checklist

You have a working economy if:
- ✅ Users can check balance with `!eggs`
- ✅ Users earn eggs passively while watching
- ✅ Users can buy tokens with `!buy`
- ✅ Users can play games with tokens
- ✅ Users can check inventory with `!eggpack`
- ✅ Users can view ranks with `!titles`
- ✅ You can monitor economy with `!econfunds`

**Congratulations!** 🎉 Your egg-based economy is live!

---

## Full Documentation

For complete implementation and all features:

📚 **[Unified Eggonomy Guide](Unified_Yoshi_Eggonomy.md)** - Complete step-by-step guide  
📚 **[Variable Reference](Variable_Reference.md)** - All variables explained  
📚 **[Event System Guide](Event_System_Guide.md)** - Bonus events and multipliers  
📚 **[Advanced Features Guide](Advanced_Features_Guide.md)** - Custom features and extensions  
📚 **[Troubleshooting Guide](Troubleshooting_Guide.md)** - Solutions to common issues  

---

**Questions or Issues?**  
Check the troubleshooting guide or create an issue in the repository.

**Share Your Success!**  
Let us know how your economy is working in your community!
