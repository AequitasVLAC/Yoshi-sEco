# Event-Based Bonus System for Yoshi's Eggonomy

**Platform:** Streamer.bot (v0.2.0+)  
**Last Updated:** December 2025

> **💬 Twitch Chat Compliant:** All messages optimized for Twitch's 500 character limit. Event Dashboard updated to use single-line format (no newlines).

This guide provides complete implementation details for streamer-controlled events and bonus systems that enhance viewer engagement and create special moments during streams.

---

## Table of Contents

1. [Overview](#overview)
2. [Double Rewards Hour](#double-rewards-hour)
3. [Free Entry Tokens Event](#free-entry-tokens-event)
4. [Bonus Multiplier System](#bonus-multiplier-system)
5. [Special Jackpot Events](#special-jackpot-events)
6. [Community Milestone Events](#community-milestone-events)
7. [Scheduled Event Automation](#scheduled-event-automation)
8. [Event Management Commands](#event-management-commands)

---

## Overview

### What Are Event-Based Bonuses?

Events are special, time-limited bonuses that streamers can activate to:
- **Increase engagement** during slow periods
- **Reward loyal viewers** with special benefits
- **Create hype** around stream milestones
- **Test economy balance** with temporary boosts
- **Celebrate occasions** (birthdays, anniversaries, holidays)

### Event Types

| Event Type | Duration | Effect | Streamer Control |
|-----------|----------|--------|------------------|
| Double Rewards | 15-60 min | 2x egg payouts from games | Manual toggle |
| Free Entry Tokens | 30-120 min | Games don't consume tokens | Manual toggle |
| Bonus Multiplier | Variable | 1.5x to 5x rewards | Set multiplier value |
| Special Jackpot | One-time | Award big nest fund to player(s) | Manual trigger |
| Community Goals | Until goal | Unlock rewards at milestones | Track progress |
| Happy Hour | Scheduled | Auto-activates at set times | Timer-based |

### Variables Used By Events

All event variables are documented in the [Variable Reference](Variable_Reference.md). Key ones:

- `doubleRewardsActive` - Boolean flag for 2x rewards
- `doubleRewardsEndTime` - Timestamp when event ends
- `freeEntryTokensActive` - Boolean flag for free games
- `freeEntryEndTime` - Timestamp when free entry ends
- `rewardMultiplier` - Current multiplier (1.0 = normal, 2.0 = double)
- `eventMessage` - Custom message to display during event

---

## Double Rewards Hour

### What It Does

When activated, all game payouts are multiplied by 2 for a specified duration.

**Affected Games:**
- ✅ Chomp Tunnel - 2x eggs from wins
- ✅ Hatch Roll - 2x eggs from all outcomes
- ✅ Duel Nest - 2x pot distribution (winner gets more)
- ✅ Golden Eggs - 2x bonus from rare finds

**Not Affected:**
- ❌ Passive income (viewers still earn normal rate)
- ❌ Token purchases (cost stays the same)
- ❌ Economy funds (distribution percentages unchanged)

### Implementation

#### Step 1: Create Toggle Action

**Action Name:** `[EVENT] Toggle Double Rewards`

**Action Configuration:**
1. Go to: `Actions` tab → Click **Add**
2. **Action Name:** `[EVENT] Toggle Double Rewards`
3. Click **OK**

**Execute Code Sub-Action:**

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        // Check if currently active
        bool isActive = CPH.GetGlobalVar<bool>("doubleRewardsActive", true);
        
        if (isActive)
        {
            // Deactivate event
            CPH.SetGlobalVar("doubleRewardsActive", false, true);
            CPH.SetGlobalVar("doubleRewardsEndTime", 0L, true);
            CPH.SendMessage("⏸️ Double Rewards Hour has ended! Payouts return to normal.");
            CPH.LogInfo("Double Rewards deactivated manually");
        }
        else
        {
            // Activate event for 1 hour (default)
            // Parse duration from command argument if provided
            int durationMinutes = 60; // Default 1 hour
            
            if (args.ContainsKey("rawInput0") && !string.IsNullOrEmpty(args["rawInput0"].ToString()))
            {
                if (int.TryParse(args["rawInput0"].ToString(), out int parsedDuration))
                {
                    durationMinutes = parsedDuration;
                }
            }
            
            CPH.SetGlobalVar("doubleRewardsActive", true, true);
            
            long endTime = DateTime.Now.AddMinutes(durationMinutes).Ticks;
            CPH.SetGlobalVar("doubleRewardsEndTime", endTime, true);
            
            CPH.SendMessage($"🎉 DOUBLE REWARDS HOUR ACTIVATED! All game payouts are 2X for the next {durationMinutes} minutes! 🥚🥚");
            CPH.LogInfo($"Double Rewards activated for {durationMinutes} minutes");
        }
        
        return true;
    }
}
```

**Command Configuration:**
1. Go to: `Commands` tab → Click **Add**
2. **Command:** `!doublerewards`
3. **Enabled:** ✅ Yes
4. **Action:** Select `[EVENT] Toggle Double Rewards`
5. **Permissions:** Moderators only
6. **Usage:** `!doublerewards` (toggle) or `!doublerewards 30` (30 minutes)

---

#### Step 2: Create Auto-Expire Timer

**Action Name:** `[EVENT] Check Double Rewards Expiry`

**Execute Code:**

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        // Check if double rewards is active
        bool isActive = CPH.GetGlobalVar<bool>("doubleRewardsActive", true);
        
        if (!isActive)
        {
            return false; // Nothing to check
        }
        
        // Get end time
        long endTime = CPH.GetGlobalVar<long>("doubleRewardsEndTime", true);
        
        if (endTime == 0)
        {
            return false; // No end time set
        }
        
        // Check if time has passed
        if (DateTime.Now.Ticks >= endTime)
        {
            // Deactivate
            CPH.SetGlobalVar("doubleRewardsActive", false, true);
            CPH.SetGlobalVar("doubleRewardsEndTime", 0L, true);
            CPH.SendMessage("⏱️ Double Rewards Hour has automatically ended! Thanks for playing!");
            CPH.LogInfo("Double Rewards expired automatically");
        }
        else
        {
            // Calculate remaining time for optional notification
            TimeSpan remaining = TimeSpan.FromTicks(endTime - DateTime.Now.Ticks);
            
            // Optional: Warn when 5 minutes remaining
            if (remaining.TotalMinutes <= 5 && remaining.TotalMinutes > 4)
            {
                CPH.SendMessage("⏰ Only 5 minutes left of Double Rewards Hour! Get your games in!");
            }
        }
        
        return true;
    }
}
```

**Timer Configuration:**
1. Right-click the action → **Add Timed Action**
2. **Interval:** 60 seconds (checks every minute)
3. **Repeat:** ✅ Yes (infinite)
4. **Enabled:** ✅ Yes

---

#### Step 3: Modify Game Actions to Check Event

**For Chomp Tunnel:** Add this code BEFORE the final SendMessage:

```csharp
// Check for double rewards event
bool doubleRewards = CPH.GetGlobalVar<bool>("doubleRewardsActive", true);
if (doubleRewards)
{
    payout = payout * 2;
}
```

**Complete Modified Chomp Tunnel Code with Double Rewards:**

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
        
        // Increment play counter
        int plays = CPH.GetGlobalVar<int>($"{userId}_chompPlays", true);
        CPH.SetGlobalVar($"{userId}_chompPlays", plays + 1, true);
        
        // Roll the dice (1-6)
        Random rnd = new Random();
        int roll = rnd.Next(1, 7);
        
        // Check for rare Golden Egg (5% chance)
        bool goldenEgg = rnd.Next(1, 101) <= 5;
        
        if (roll == 1)
        {
            // Loss - Reset streak
            CPH.SetGlobalVar($"{userId}_chompStreak", 0, true);
            CPH.SendMessage($"💀 @{userName} rolled {roll}! Chain Chomp ate your egg! Streak reset. [Play #{plays}]");
        }
        else
        {
            // Win - Increase streak
            int streak = CPH.GetGlobalVar<int>($"{userId}_chompStreak", true);
            streak++;
            CPH.SetGlobalVar($"{userId}_chompStreak", streak, true);
            
            // Update win counter
            int wins = CPH.GetGlobalVar<int>($"{userId}_chompWins", true);
            CPH.SetGlobalVar($"{userId}_chompWins", wins + 1, true);
            
            // Calculate base payout (10 + 5 per streak level)
            int payout = 10 + (streak * 5);
            
            // Add golden egg bonus
            if (goldenEgg)
            {
                payout += 100;
                int goldenCount = CPH.GetGlobalVar<int>($"{userId}_goldenEggsFound", true);
                CPH.SetGlobalVar($"{userId}_goldenEggsFound", goldenCount + 1, true);
            }
            
            // *** CHECK FOR DOUBLE REWARDS EVENT ***
            bool doubleRewards = CPH.GetGlobalVar<bool>("doubleRewardsActive", true);
            string eventTag = "";
            if (doubleRewards)
            {
                payout = payout * 2;
                eventTag = " [2X EVENT]";
            }
            
            // Award eggs
            CPH.AddPoints(userId, payout, "Chomp Win");
            
            // Update total eggs won stat
            int totalWon = CPH.GetGlobalVar<int>($"{userId}_totalEggsWon", true);
            CPH.SetGlobalVar($"{userId}_totalEggsWon", totalWon + payout, true);
            
            // Send message
            if (goldenEgg)
            {
                CPH.SendMessage($"🌟✨ @{userName} rolled {roll}! GOLDEN EGG! +{payout} 🥚 | Streak: {streak}{eventTag}");
            }
            else
            {
                CPH.SendMessage($"✅ @{userName} rolled {roll}! Safe! +{payout} 🥚 | Streak: {streak}{eventTag}");
            }
        }
        
        return true;
    }
}
```

**Apply Similar Changes to:**
- ✅ Hatch Roll (`[GAME] Hatch Roll`)
- ✅ Duel Resolver (`[PVP] Duel Resolver`)

---

### Usage Examples

**Streamer Commands:**
```
!doublerewards           → Toggle ON for 60 minutes (default)
!doublerewards 30        → Activate for 30 minutes
!doublerewards 120       → Activate for 2 hours
!doublerewards           → Toggle OFF immediately
```

**Player Experience:**
```
Normal Chomp win:    ✅ @Player rolled 4! Safe! +15 🥚 | Streak: 2
During 2X event:     ✅ @Player rolled 4! Safe! +30 🥚 | Streak: 2 [2X EVENT]

Normal Hatch Roll:   🐥 @Player rolled 13! Good hatch! +30 🥚
During 2X event:     🐥 @Player rolled 13! Good hatch! +60 🥚 [2X EVENT]
```

---

### Advanced Configuration

#### Variable Duration Messages

Modify the activation code to provide context-aware messages:

```csharp
string durationText = "";
if (durationMinutes < 60)
{
    durationText = $"{durationMinutes} minutes";
}
else if (durationMinutes == 60)
{
    durationText = "1 hour";
}
else
{
    int hours = durationMinutes / 60;
    int mins = durationMinutes % 60;
    durationText = mins > 0 ? $"{hours} hours {mins} minutes" : $"{hours} hours";
}

CPH.SendMessage($"🎉 DOUBLE REWARDS ACTIVATED! All game payouts are 2X for the next {durationText}! 🥚🥚");
```

#### Countdown Warnings

Add multiple warning thresholds to the expiry checker:

```csharp
TimeSpan remaining = TimeSpan.FromTicks(endTime - DateTime.Now.Ticks);

// Check if we should send warnings
int minutesRemaining = (int)remaining.TotalMinutes;

// Track last warning sent to avoid spam
int lastWarning = CPH.GetGlobalVar<int>("doubleRewards_lastWarning", true);

if (minutesRemaining == 10 && lastWarning != 10)
{
    CPH.SendMessage("⏰ 10 minutes remaining in Double Rewards Hour!");
    CPH.SetGlobalVar("doubleRewards_lastWarning", 10, true);
}
else if (minutesRemaining == 5 && lastWarning != 5)
{
    CPH.SendMessage("⏰ Only 5 minutes left of Double Rewards Hour!");
    CPH.SetGlobalVar("doubleRewards_lastWarning", 5, true);
}
else if (minutesRemaining == 1 && lastWarning != 1)
{
    CPH.SendMessage("⏰ FINAL MINUTE of Double Rewards! Get your games in NOW!");
    CPH.SetGlobalVar("doubleRewards_lastWarning", 1, true);
}
```

#### Time Remaining Command

Create a viewer command to check event status:

**Action Name:** `[EVENT] Check Event Status`

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        bool doubleActive = CPH.GetGlobalVar<bool>("doubleRewardsActive", true);
        bool freeActive = CPH.GetGlobalVar<bool>("freeEntryTokensActive", true);
        
        string message = "📊 Current Events: ";
        
        if (!doubleActive && !freeActive)
        {
            message += "No active events. Check back later!";
        }
        else
        {
            if (doubleActive)
            {
                long endTime = CPH.GetGlobalVar<long>("doubleRewardsEndTime", true);
                TimeSpan remaining = TimeSpan.FromTicks(endTime - DateTime.Now.Ticks);
                int minsLeft = (int)remaining.TotalMinutes;
                message += $"🎉 Double Rewards ({minsLeft} min left) ";
            }
            
            if (freeActive)
            {
                long endTime = CPH.GetGlobalVar<long>("freeEntryEndTime", true);
                TimeSpan remaining = TimeSpan.FromTicks(endTime - DateTime.Now.Ticks);
                int minsLeft = (int)remaining.TotalMinutes;
                message += $"🎁 Free Entry ({minsLeft} min left)";
            }
        }
        
        CPH.SendMessage(message);
        return true;
    }
}
```

**Command:** `!events` (available to everyone, 30s cooldown)

---

## Free Entry Tokens Event

### What It Does

When activated, players can play games WITHOUT consuming tokens for a limited time. This is perfect for:
- Letting new viewers try the system
- High-energy celebration moments
- Encouraging participation during slow chat
- Special occasions or milestones

**How It Works:**
- Games check for `freeEntryTokensActive` flag
- If true, skip token deduction
- Players still need at least 1 token initially (proves they engaged with the system)
- Payouts remain normal (unless combined with Double Rewards!)

### Implementation

#### Step 1: Create Toggle Action

**Action Name:** `[EVENT] Toggle Free Entry`

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        bool isActive = CPH.GetGlobalVar<bool>("freeEntryTokensActive", true);
        
        if (isActive)
        {
            // Deactivate
            CPH.SetGlobalVar("freeEntryTokensActive", false, true);
            CPH.SetGlobalVar("freeEntryEndTime", 0L, true);
            CPH.SendMessage("⏸️ Free Entry Event has ended! Token costs are back to normal.");
            CPH.LogInfo("Free Entry deactivated");
        }
        else
        {
            // Activate - default 30 minutes
            int durationMinutes = 30;
            
            if (args.ContainsKey("rawInput0") && !string.IsNullOrEmpty(args["rawInput0"].ToString()))
            {
                if (int.TryParse(args["rawInput0"].ToString(), out int parsed))
                {
                    durationMinutes = parsed;
                }
            }
            
            CPH.SetGlobalVar("freeEntryTokensActive", true, true);
            
            long endTime = DateTime.Now.AddMinutes(durationMinutes).Ticks;
            CPH.SetGlobalVar("freeEntryEndTime", endTime, true);
            
            CPH.SendMessage($"🎁 FREE ENTRY EVENT! Play all games WITHOUT using tokens for {durationMinutes} minutes! Go wild! 🥚");
            CPH.LogInfo($"Free Entry activated for {durationMinutes} minutes");
        }
        
        return true;
    }
}
```

**Command:** `!freeentry` (Moderator only)

---

#### Step 2: Modify Game Actions

**For Chomp Tunnel:** Modify token check section:

```csharp
// Check if user has Mystery Eggs
string tokenVar = $"{userId}_MysteryEgg";
int mysteryEggs = CPH.GetGlobalVar<int>(tokenVar, true);

// Check for free entry event
bool freeEntry = CPH.GetGlobalVar<bool>("freeEntryTokensActive", true);

if (mysteryEggs < 1 && !freeEntry)
{
    CPH.SendMessage($"@{userName}, you need 1 Mystery Egg! Use: !buy MysteryEgg 1");
    return false;
}

// Deduct token only if NOT free entry
if (!freeEntry && mysteryEggs >= 1)
{
    CPH.SetGlobalVar(tokenVar, mysteryEggs - 1, true);
}
```

**Apply to all games:**
- Chomp Tunnel (Mystery Egg check)
- Hatch Roll (Dice Egg check)
- Duel Nest Challenge (Duel Egg check)
- Duel Accept (Duel Egg check)

---

#### Step 3: Create Auto-Expire Timer

**Action Name:** `[EVENT] Check Free Entry Expiry`

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        bool isActive = CPH.GetGlobalVar<bool>("freeEntryTokensActive", true);
        
        if (!isActive)
        {
            return false;
        }
        
        long endTime = CPH.GetGlobalVar<long>("freeEntryEndTime", true);
        
        if (endTime == 0)
        {
            return false;
        }
        
        if (DateTime.Now.Ticks >= endTime)
        {
            CPH.SetGlobalVar("freeEntryTokensActive", false, true);
            CPH.SetGlobalVar("freeEntryEndTime", 0L, true);
            CPH.SendMessage("⏱️ Free Entry Event has ended! Hope you had fun!");
            CPH.LogInfo("Free Entry expired");
        }
        else
        {
            TimeSpan remaining = TimeSpan.FromTicks(endTime - DateTime.Now.Ticks);
            
            int lastWarning = CPH.GetGlobalVar<int>("freeEntry_lastWarning", true);
            int minutesRemaining = (int)remaining.TotalMinutes;
            
            if (minutesRemaining == 5 && lastWarning != 5)
            {
                CPH.SendMessage("⏰ 5 minutes left of Free Entry! Get your games in!");
                CPH.SetGlobalVar("freeEntry_lastWarning", 5, true);
            }
            else if (minutesRemaining == 1 && lastWarning != 1)
            {
                CPH.SendMessage("⏰ FINAL MINUTE of Free Entry! Last chance!");
                CPH.SetGlobalVar("freeEntry_lastWarning", 1, true);
            }
        }
        
        return true;
    }
}
```

**Timer:** 60 seconds, repeat indefinitely

---

### Combined Events

You can run Double Rewards + Free Entry simultaneously for maximum hype!

**Streamer Activates Both:**
```
!doublerewards 60
!freeentry 60
```

**Player Experience:**
```
Normal:           ✅ @Player rolled 4! Safe! +15 🥚 | Streak: 2 [Token used]
Free Entry:       ✅ @Player rolled 4! Safe! +15 🥚 | Streak: 2 [FREE PLAY]
2X + Free Entry:  ✅ @Player rolled 4! Safe! +30 🥚 | Streak: 2 [FREE 2X EVENT]
```

**Update Message to Show Combined Events:**

```csharp
// Build event tags
string eventTags = "";
bool doubleRewards = CPH.GetGlobalVar<bool>("doubleRewardsActive", true);
bool freeEntry = CPH.GetGlobalVar<bool>("freeEntryTokensActive", true);

if (freeEntry && doubleRewards)
{
    eventTags = " [FREE 2X EVENT]";
}
else if (freeEntry)
{
    eventTags = " [FREE PLAY]";
}
else if (doubleRewards)
{
    eventTags = " [2X EVENT]";
}

// Apply multiplier
if (doubleRewards)
{
    payout = payout * 2;
}

// Add tag to message
CPH.SendMessage($"✅ @{userName} rolled {roll}! Safe! +{payout} 🥚 | Streak: {streak}{eventTags}");
```

---

## Bonus Multiplier System

### What It Does

A flexible multiplier system that allows ANY multiplier value (1.5x, 3x, 5x, etc.), not just 2x.

**Use Cases:**
- Subscriber celebration: 1.5x for an hour
- Birthday stream: 3x all day
- Charity stream: 5x during donation goals
- Weekend bonus: 1.25x on Saturdays

### Implementation

**Action Name:** `[EVENT] Set Reward Multiplier`

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        // Parse multiplier from command
        if (args["rawInput0"] == null || !double.TryParse(args["rawInput0"].ToString(), out double multiplier))
        {
            CPH.SendMessage("Usage: !multiplier <value> <duration_minutes>");
            CPH.SendMessage("Examples: !multiplier 1.5 60  or  !multiplier 3 120");
            return false;
        }
        
        // Special case: 1.0 = disable
        if (multiplier == 1.0)
        {
            CPH.SetGlobalVar("rewardMultiplier", 1.0, true);
            CPH.SetGlobalVar("multiplierEndTime", 0L, true);
            CPH.SendMessage("💫 Reward multiplier reset to normal (1.0x)");
            return true;
        }
        
        // Parse duration (default 60 minutes)
        int durationMinutes = 60;
        if (args.ContainsKey("rawInput1") && !string.IsNullOrEmpty(args["rawInput1"].ToString()))
        {
            if (int.TryParse(args["rawInput1"].ToString(), out int parsed))
            {
                durationMinutes = parsed;
            }
        }
        
        // Validate multiplier range
        if (multiplier < 0.1 || multiplier > 10.0)
        {
            CPH.SendMessage("Multiplier must be between 0.1 and 10.0");
            return false;
        }
        
        // Set multiplier
        CPH.SetGlobalVar("rewardMultiplier", multiplier, true);
        
        long endTime = DateTime.Now.AddMinutes(durationMinutes).Ticks;
        CPH.SetGlobalVar("multiplierEndTime", endTime, true);
        
        CPH.SendMessage($"🌟 REWARD MULTIPLIER SET! All payouts are now {multiplier}X for {durationMinutes} minutes! 🥚✨");
        CPH.LogInfo($"Multiplier set to {multiplier}x for {durationMinutes} minutes");
        
        return true;
    }
}
```

**Command:** `!multiplier` (Moderator only)

---

### Modify Games to Use Multiplier

**Replace the 2x check with flexible multiplier:**

```csharp
// Get current multiplier (default 1.0 = normal)
double multiplier = CPH.GetGlobalVar<double>("rewardMultiplier", true);
if (multiplier == 0) multiplier = 1.0; // Default if not set

// Apply multiplier
payout = (int)(payout * multiplier);

// Build event tag
string eventTag = "";
if (multiplier > 1.0)
{
    eventTag = $" [{multiplier}X EVENT]";
}
```

**Auto-Expire Timer:**

```csharp
double multiplier = CPH.GetGlobalVar<double>("rewardMultiplier", true);

if (multiplier <= 1.0)
{
    return false; // No active multiplier
}

long endTime = CPH.GetGlobalVar<long>("multiplierEndTime", true);

if (endTime > 0 && DateTime.Now.Ticks >= endTime)
{
    CPH.SetGlobalVar("rewardMultiplier", 1.0, true);
    CPH.SetGlobalVar("multiplierEndTime", 0L, true);
    CPH.SendMessage("⏱️ Reward multiplier has ended! Payouts return to normal.");
}
```

---

## Special Jackpot Events

### Instant Jackpot Award

Award the entire `eggCartonJackpot` fund to a specific player or split among online viewers.

**Action Name:** `[EVENT] Award Jackpot`

```csharp
using System;
using System.Linq;

public class CPHInline
{
    public bool Execute()
    {
        int jackpot = CPH.GetGlobalVar<int>("eggCartonJackpot", true);
        
        if (jackpot < 100)
        {
            CPH.SendMessage($"Jackpot is too small ({jackpot} 🥚). Wait for it to grow!");
            return false;
        }
        
        // Check if specific user mentioned
        string targetUser = args["rawInput0"]?.ToString()?.TrimStart('@');
        
        if (!string.IsNullOrEmpty(targetUser))
        {
            // Award to specific user
            // Note: This requires getting userId from username
            // Streamer.bot API varies by version
            
            CPH.SendMessage($"🎉🎊 JACKPOT! {targetUser} wins {jackpot} 🥚 from the Egg Carton Jackpot! 🎊🎉");
            
            // Reset jackpot to base value
            CPH.SetGlobalVar("eggCartonJackpot", 500, true);
            
            // Award eggs (requires userId - implementation depends on Streamer.bot version)
            // CPH.AddPoints(userId, jackpot, "Jackpot Win");
        }
        else
        {
            // Split among all online viewers
            CPH.SendMessage($"🎉 COMMUNITY JACKPOT! {jackpot} 🥚 will be split among active chatters!");
            
            // Reset jackpot
            CPH.SetGlobalVar("eggCartonJackpot", 500, true);
            
            // Distribution logic depends on Streamer.bot version
            // Option: Use "Add points to all viewers" if available
        }
        
        return true;
    }
}
```

**Command:** `!awardjackpot` or `!awardjackpot @username` (Broadcaster only)

---

### Random Jackpot Trigger

Automatically award jackpot when it reaches a certain size.

**Action Name:** `[EVENT] Check Auto Jackpot`

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        int jackpot = CPH.GetGlobalVar<int>("eggCartonJackpot", true);
        
        // Trigger when jackpot reaches 5000
        if (jackpot >= 5000)
        {
            // Random chance to trigger (10% per check)
            Random rnd = new Random();
            if (rnd.Next(1, 101) <= 10)
            {
                CPH.SendMessage($"🎰 AUTO JACKPOT TRIGGERED! {jackpot} 🥚 up for grabs! Type !jackpot to enter!");
                
                // Set jackpot drawing state
                CPH.SetGlobalVar("jackpotDrawingActive", true, true);
                CPH.SetGlobalVar("jackpotDrawingAmount", jackpot, true);
                CPH.SetGlobalVar("jackpotDrawingEndTime", DateTime.Now.AddMinutes(2).Ticks, true);
                
                // Reset main jackpot
                CPH.SetGlobalVar("eggCartonJackpot", 500, true);
            }
        }
        
        return true;
    }
}
```

**Timer:** Every 5 minutes

---

## Community Milestone Events

### What It Does

Track community progress toward goals and unlock rewards when milestones are reached.

**Examples:**
- Reach 10,000 total eggs in circulation → Everyone gets 100 eggs
- Reach 1000 games played → Free Entry event for 24 hours
- Reach 100 duels completed → Unlock new token type

### Implementation

**Action Name:** `[EVENT] Check Milestones`

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        // Get milestone tracking variables
        int milestone_10k = CPH.GetGlobalVar<int>("milestone_10kEggs_complete", true);
        int milestone_1kGames = CPH.GetGlobalVar<int>("milestone_1kGames_complete", true);
        int milestone_100Duels = CPH.GetGlobalVar<int>("milestone_100Duels_complete", true);
        
        // Check each milestone
        
        // Milestone 1: 10,000 total eggs awarded
        if (milestone_10k == 0)
        {
            // Calculate total eggs awarded (approximate)
            int bigNest = CPH.GetGlobalVar<int>("bigNestFund", true);
            
            // Simplified check - in real implementation, track total separately
            if (bigNest >= 3000) // Indicates ~10k eggs circulated
            {
                CPH.SendMessage("🎊 MILESTONE REACHED! Community has circulated over 10,000 eggs! Everyone gets 100 bonus eggs!");
                
                CPH.SetGlobalVar("milestone_10kEggs_complete", 1, true);
                
                // Award bonus to all (requires Streamer.bot API)
                // CPH.AddPointsToAll(100, "Milestone Bonus");
            }
        }
        
        // Milestone 2: 1,000 total games played
        if (milestone_1kGames == 0)
        {
            // Track total games played globally
            int totalGames = CPH.GetGlobalVar<int>("globalGamesPlayed", true);
            
            if (totalGames >= 1000)
            {
                CPH.SendMessage("🎮 MILESTONE! 1,000 games played! Free Entry activated for 24 hours!");
                
                CPH.SetGlobalVar("milestone_1kGames_complete", 1, true);
                
                // Auto-activate free entry
                CPH.SetGlobalVar("freeEntryTokensActive", true, true);
                long endTime = DateTime.Now.AddHours(24).Ticks;
                CPH.SetGlobalVar("freeEntryEndTime", endTime, true);
            }
        }
        
        return true;
    }
}
```

**Add to Each Game:** Increment global counter

```csharp
// At end of game action
int globalGames = CPH.GetGlobalVar<int>("globalGamesPlayed", true);
CPH.SetGlobalVar("globalGamesPlayed", globalGames + 1, true);
```

---

## Scheduled Event Automation

### Happy Hour Auto-Activation

Automatically activate events at specific times each day.

**Action Name:** `[EVENT] Check Scheduled Events`

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        DateTime now = DateTime.Now;
        
        // Happy Hour: Every day 8-9 PM (20:00-21:00)
        if (now.Hour == 20 && now.Minute < 5)
        {
            // Check if already activated today
            string lastActivation = CPH.GetGlobalVar<string>("happyHour_lastDate", true);
            string today = now.ToString("yyyy-MM-dd");
            
            if (lastActivation != today)
            {
                // Activate double rewards
                CPH.SetGlobalVar("doubleRewardsActive", true, true);
                long endTime = DateTime.Now.AddHours(1).Ticks;
                CPH.SetGlobalVar("doubleRewardsEndTime", endTime, true);
                
                CPH.SendMessage("🍹 HAPPY HOUR! Double rewards for the next hour! 🥚🥚");
                
                CPH.SetGlobalVar("happyHour_lastDate", today, true);
            }
        }
        
        // Weekend Bonus: Saturday/Sunday gets 1.5x
        if ((now.DayOfWeek == DayOfWeek.Saturday || now.DayOfWeek == DayOfWeek.Sunday) 
            && now.Hour == 12 && now.Minute < 5)
        {
            string lastActivation = CPH.GetGlobalVar<string>("weekendBonus_lastDate", true);
            string today = now.ToString("yyyy-MM-dd");
            
            if (lastActivation != today)
            {
                CPH.SetGlobalVar("rewardMultiplier", 1.5, true);
                long endTime = DateTime.Now.AddHours(12).Ticks;
                CPH.SetGlobalVar("multiplierEndTime", endTime, true);
                
                CPH.SendMessage("🎉 WEEKEND BONUS! 1.5x rewards for 12 hours! Enjoy! 🥚");
                
                CPH.SetGlobalVar("weekendBonus_lastDate", today, true);
            }
        }
        
        return true;
    }
}
```

**Timer:** Every 5 minutes during stream

---

## Event Management Commands

### Master Event Dashboard

**Action Name:** `[EVENT] Show Dashboard`

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        // Check each event status
        bool doubleActive = CPH.GetGlobalVar<bool>("doubleRewardsActive", true);
        bool freeActive = CPH.GetGlobalVar<bool>("freeEntryTokensActive", true);
        double multiplier = CPH.GetGlobalVar<double>("rewardMultiplier", true);
        int jackpot = CPH.GetGlobalVar<int>("eggCartonJackpot", true);
        int bigNest = CPH.GetGlobalVar<int>("bigNestFund", true);
        
        // Build single-line message (Twitch chat limit: 500 chars, no newlines supported)
        string message = "📊 Events: ";
        message += $"2X {(doubleActive ? "🟢" : "🔴")} | ";
        message += $"Free {(freeActive ? "🟢" : "🔴")} | ";
        message += $"Multi: {(multiplier > 1.0 ? $"{multiplier}x🟢" : "1.0x🔴")} | ";
        message += $"Jackpot: {jackpot}🥚 | BigNest: {bigNest}🥚";
        
        CPH.SendMessage(message);
        
        return true;
    }
}
```

**Command:** `!eventdash` (Moderator only)

---

### Quick Event Presets

**Action Name:** `[EVENT] Activate Preset`

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        string preset = args["rawInput0"]?.ToString()?.ToLower();
        
        switch (preset)
        {
            case "hype":
                // Double rewards + free entry for 30 min
                CPH.SetGlobalVar("doubleRewardsActive", true, true);
                CPH.SetGlobalVar("doubleRewardsEndTime", DateTime.Now.AddMinutes(30).Ticks, true);
                CPH.SetGlobalVar("freeEntryTokensActive", true, true);
                CPH.SetGlobalVar("freeEntryEndTime", DateTime.Now.AddMinutes(30).Ticks, true);
                CPH.SendMessage("🔥 HYPE MODE! 2X + FREE ENTRY for 30 minutes! GO GO GO! 🔥");
                break;
                
            case "celebration":
                // 3x rewards for 1 hour
                CPH.SetGlobalVar("rewardMultiplier", 3.0, true);
                CPH.SetGlobalVar("multiplierEndTime", DateTime.Now.AddHours(1).Ticks, true);
                CPH.SendMessage("🎊 CELEBRATION MODE! 3X rewards for 1 hour! 🎉");
                break;
                
            case "chill":
                // 1.25x rewards, no time limit
                CPH.SetGlobalVar("rewardMultiplier", 1.25, true);
                CPH.SetGlobalVar("multiplierEndTime", 0L, true);
                CPH.SendMessage("😎 CHILL MODE! 1.25x rewards active!");
                break;
                
            case "off":
                // Disable everything
                CPH.SetGlobalVar("doubleRewardsActive", false, true);
                CPH.SetGlobalVar("freeEntryTokensActive", false, true);
                CPH.SetGlobalVar("rewardMultiplier", 1.0, true);
                CPH.SendMessage("⏸️ All events disabled. Back to normal!");
                break;
                
            default:
                CPH.SendMessage("Available presets: hype, celebration, chill, off");
                break;
        }
        
        return true;
    }
}
```

**Command:** `!preset <name>` (Moderator only)

**Usage:**
```
!preset hype         → 2X + Free Entry for 30 min
!preset celebration  → 3X rewards for 1 hour
!preset chill        → 1.25X rewards indefinitely
!preset off          → Disable all events
```

---

## Summary

The Event-Based Bonus System provides:

✅ **5+ Event Types** - Double rewards, free entry, multipliers, jackpots, milestones  
✅ **Flexible Duration** - From minutes to hours to indefinite  
✅ **Auto-Expiry** - Events end automatically with warnings  
✅ **Stackable Events** - Combine multiple events for mega-hype  
✅ **Scheduled Automation** - Happy hour and weekend bonuses  
✅ **Quick Presets** - One-command event activation  
✅ **Full Control** - Streamer can enable/disable anytime

**Next Steps:**
1. Implement Double Rewards Hour first (most popular)
2. Add Free Entry for special occasions
3. Create your own custom events based on community needs
4. Monitor economy balance and adjust multipliers as needed

**Related Documentation:**
- [Variable Reference](Variable_Reference.md) - All event variables explained
- [Unified Eggonomy Guide](Unified_Yoshi_Eggonomy.md) - Core system implementation
- [Advanced Features Guide](Advanced_Features_Guide.md) - More customization options
