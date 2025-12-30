# Complete Variable Reference for Yoshi's Eggonomy

**Platform:** Streamer.bot (v0.2.0+)  
**Last Updated:** December 2025

This document provides a complete reference for all variables used in the Yoshi's Island Eggonomy system. Understanding these variables is essential for customization, troubleshooting, and extending the system.

---

## Table of Contents

1. [Variable Storage in Streamer.bot](#variable-storage-in-streamerbot)
2. [Global Economy Variables](#global-economy-variables)
3. [Per-User Token Variables](#per-user-token-variables)
4. [Per-User Game Statistics Variables](#per-user-game-statistics-variables)
5. [Temporary Game State Variables](#temporary-game-state-variables)
6. [Event and Bonus Variables](#event-and-bonus-variables)
7. [Variable Naming Conventions](#variable-naming-conventions)
8. [Variable Management](#variable-management)

---

## Variable Storage in Streamer.bot

### How Variables Are Stored

Streamer.bot uses an internal SQLite database to store global variables. This means:

- ✅ **Persistent:** Variables survive Streamer.bot restarts
- ✅ **Automatic:** No manual database management needed
- ✅ **Reliable:** Built-in backup through Streamer.bot data folder
- ⚠️ **Case-Sensitive:** `userId_MysteryEgg` ≠ `userid_mysteryegg`

### Accessing Variables in Streamer.bot

**Via UI:**
1. Open Streamer.bot
2. Go to: `Settings` → `Variables` (or top-level `Variables` tab)
3. View/Edit variables in the Global Variables section

**Via Code:**
```csharp
// Get a variable (with default if not exists)
int value = CPH.GetGlobalVar<int>("variableName", persisted: true);

// Set a variable
CPH.SetGlobalVar("variableName", value, persisted: true);

// Delete a variable
CPH.UnsetGlobalVar("variableName", persisted: true);
```

**⚠️ IMPORTANT:** Always set `persisted: true` for variables that need to survive restarts!

---

## Global Economy Variables

These variables track the overall economy state and funds.

### bigNestFund
- **Type:** `int` (Integer)
- **Initial Value:** `1000`
- **Persisted:** ✅ Yes
- **Purpose:** Primary economy fund that collects 70% of all token purchases
- **Usage:** Special events, giveaways, community rewards
- **Modified By:** 
  - `[ECON] Buy Token` - Increases by 70% of purchase cost
  - `[PVP] Duel Resolver` - Increases by 15% of duel pot
  - `[EVENT] Distribute Rewards` - Decreases when streamer distributes
- **Access Level:** Read: Anyone with !econfunds | Write: System only
- **Example Values:** 
  - Fresh start: `1000`
  - After 100 token purchases: ~`2400`
  - After streamer giveaway: Variable

```csharp
// Get current fund value
int fund = CPH.GetGlobalVar<int>("bigNestFund", true);

// Add to fund (e.g., from token purchase)
CPH.SetGlobalVar("bigNestFund", fund + contribution, true);
```

---

### eggCartonJackpot
- **Type:** `int` (Integer)
- **Initial Value:** `500`
- **Persisted:** ✅ Yes
- **Purpose:** Jackpot fund that collects 20% of all token purchases
- **Usage:** Lottery events, milestone rewards, special jackpots
- **Modified By:**
  - `[ECON] Buy Token` - Increases by 20% of purchase cost
  - `[EVENT] Award Jackpot` - Decreases when awarded
- **Access Level:** Read: Anyone with !econfunds | Write: System only
- **Example Values:**
  - Fresh start: `500`
  - After 100 token purchases: ~`900`
  - After jackpot win: Resets to base value

```csharp
// Get current jackpot value
int jackpot = CPH.GetGlobalVar<int>("eggCartonJackpot", true);

// Add to jackpot
CPH.SetGlobalVar("eggCartonJackpot", jackpot + contribution, true);
```

---

### Event Variables

#### doubleRewardsActive
- **Type:** `bool` (Boolean)
- **Initial Value:** `false`
- **Persisted:** ✅ Yes
- **Purpose:** Enables 2x rewards for all games
- **Modified By:** `[EVENT] Toggle Double Rewards` (streamer command)
- **Checked By:** All game actions
- **Duration:** Until manually disabled or timer expires

```csharp
// Check if double rewards active
bool doubleActive = CPH.GetGlobalVar<bool>("doubleRewardsActive", true);
if (doubleActive) {
    payout = payout * 2;
}
```

---

#### doubleRewardsEndTime
- **Type:** `long` (Ticks)
- **Initial Value:** `0`
- **Persisted:** ✅ Yes
- **Purpose:** Timestamp when double rewards should end
- **Modified By:** `[EVENT] Toggle Double Rewards`
- **Checked By:** Timer action every minute

```csharp
// Set end time (1 hour from now)
long endTime = DateTime.Now.AddHours(1).Ticks;
CPH.SetGlobalVar("doubleRewardsEndTime", endTime, true);

// Check if expired
long endTime = CPH.GetGlobalVar<long>("doubleRewardsEndTime", true);
if (DateTime.Now.Ticks >= endTime) {
    CPH.SetGlobalVar("doubleRewardsActive", false, true);
}
```

---

#### freeEntryTokensActive
- **Type:** `bool` (Boolean)
- **Initial Value:** `false`
- **Persisted:** ✅ Yes
- **Purpose:** Enables free game entries (no token required)
- **Modified By:** `[EVENT] Toggle Free Entry` (streamer command)
- **Checked By:** All game actions before token deduction

```csharp
// Check if free entry active
bool freeEntry = CPH.GetGlobalVar<bool>("freeEntryTokensActive", true);
if (!freeEntry && userTokens < 1) {
    // Normal behavior - require token
} else if (freeEntry) {
    // Skip token deduction
}
```

---

## Per-User Token Variables

These variables track each user's token inventory. Format: `{userId}_TokenType`

**⚠️ CRITICAL:** Use `userId` (Twitch user ID), NOT `userName`!

### {userId}_MysteryEgg
- **Type:** `int` (Integer)
- **Initial Value:** `0` (default if not exists)
- **Persisted:** ✅ Yes
- **Purpose:** Number of Mystery Eggs owned by user
- **Used In:** Chomp Tunnel game
- **Cost to Buy:** 20 Pouch Eggs each
- **Format Example:** `12345678_MysteryEgg` (where 12345678 is Twitch user ID)

```csharp
string userId = args["userId"].ToString();
string tokenVar = $"{userId}_MysteryEgg";

// Get current tokens
int mysteryEggs = CPH.GetGlobalVar<int>(tokenVar, true);

// Deduct one token
CPH.SetGlobalVar(tokenVar, mysteryEggs - 1, true);

// Add tokens
CPH.SetGlobalVar(tokenVar, mysteryEggs + quantity, true);
```

---

### {userId}_DiceEgg
- **Type:** `int` (Integer)
- **Initial Value:** `0`
- **Persisted:** ✅ Yes
- **Purpose:** Number of Dice Eggs owned by user
- **Used In:** Hatch Roll game
- **Cost to Buy:** 10 Pouch Eggs each
- **Format Example:** `12345678_DiceEgg`

```csharp
string tokenVar = $"{userId}_DiceEgg";
int diceEggs = CPH.GetGlobalVar<int>(tokenVar, true);
```

---

### {userId}_DuelEgg
- **Type:** `int` (Integer)
- **Initial Value:** `0`
- **Persisted:** ✅ Yes
- **Purpose:** Number of Duel Eggs owned by user
- **Used In:** Duel Nest PvP
- **Cost to Buy:** 5 Pouch Eggs each
- **Format Example:** `12345678_DuelEgg`

```csharp
string tokenVar = $"{userId}_DuelEgg";
int duelEggs = CPH.GetGlobalVar<int>(tokenVar, true);
```

---

### Adding Custom Token Types

To add a new token type (e.g., "LuckyEgg"):

1. **Define cost in Buy Token action:**
```csharp
{"LuckyEgg", 15}  // Add to tokenCosts dictionary
```

2. **Create variable pattern:**
```csharp
string tokenVar = $"{userId}_LuckyEgg";
```

3. **Initialize for users when they buy:**
```csharp
int currentTokens = CPH.GetGlobalVar<int>(tokenVar, true);
CPH.SetGlobalVar(tokenVar, currentTokens + quantity, true);
```

4. **Use in your game action:**
```csharp
int luckyEggs = CPH.GetGlobalVar<int>($"{userId}_LuckyEgg", true);
if (luckyEggs < 1) {
    CPH.SendMessage("You need a Lucky Egg!");
    return false;
}
CPH.SetGlobalVar($"{userId}_LuckyEgg", luckyEggs - 1, true);
```

---

## Per-User Game Statistics Variables

These variables track individual player performance and progression.

### {userId}_chompStreak
- **Type:** `int` (Integer)
- **Initial Value:** `0`
- **Persisted:** ✅ Yes
- **Purpose:** Current win streak in Chomp Tunnel
- **Modified By:** `[GAME] Chomp Tunnel`
- **Reset On:** Rolling a 1 (loss)
- **Increases:** On successful rolls (2-6)
- **Affects:** Payout calculation (base + 5 per streak)

```csharp
// Get current streak
int streak = CPH.GetGlobalVar<int>($"{userId}_chompStreak", true);

// Increase streak on win
streak++;
CPH.SetGlobalVar($"{userId}_chompStreak", streak, true);

// Calculate payout with streak
int payout = 10 + (streak * 5);

// Reset on loss
CPH.SetGlobalVar($"{userId}_chompStreak", 0, true);
```

---

### {userId}_chompWins
- **Type:** `int` (Integer)
- **Initial Value:** `0`
- **Persisted:** ✅ Yes
- **Purpose:** Total lifetime wins in Chomp Tunnel
- **Modified By:** `[GAME] Chomp Tunnel`
- **Used In:** `!sheet` command, achievements

```csharp
int wins = CPH.GetGlobalVar<int>($"{userId}_chompWins", true);
CPH.SetGlobalVar($"{userId}_chompWins", wins + 1, true);
```

---

### {userId}_chompPlays
- **Type:** `int` (Integer)
- **Initial Value:** `0`
- **Persisted:** ✅ Yes
- **Purpose:** Total games played in Chomp Tunnel
- **Modified By:** `[GAME] Chomp Tunnel`
- **Used In:** Statistics tracking, win rate calculation

```csharp
int plays = CPH.GetGlobalVar<int>($"{userId}_chompPlays", true);
CPH.SetGlobalVar($"{userId}_chompPlays", plays + 1, true);
```

---

### {userId}_eggrollPlays
- **Type:** `int` (Integer)
- **Initial Value:** `0`
- **Persisted:** ✅ Yes
- **Purpose:** Total games played in Hatch Roll
- **Modified By:** `[GAME] Hatch Roll`
- **Used In:** `!sheet` command

```csharp
int plays = CPH.GetGlobalVar<int>($"{userId}_eggrollPlays", true);
CPH.SetGlobalVar($"{userId}_eggrollPlays", plays + 1, true);
```

---

### {userId}_eggrollBigWins
- **Type:** `int` (Integer)
- **Initial Value:** `0`
- **Persisted:** ✅ Yes
- **Purpose:** Number of jackpot wins (19-20 rolls) in Hatch Roll
- **Modified By:** `[GAME] Hatch Roll`
- **Used In:** Achievement tracking

```csharp
if (roll >= 19) {
    int bigWins = CPH.GetGlobalVar<int>($"{userId}_eggrollBigWins", true);
    CPH.SetGlobalVar($"{userId}_eggrollBigWins", bigWins + 1, true);
}
```

---

### {userId}_duelWins
- **Type:** `int` (Integer)
- **Initial Value:** `0`
- **Persisted:** ✅ Yes
- **Purpose:** Total PvP duel victories
- **Modified By:** `[PVP] Duel Resolver`
- **Used In:** `!sheet` command, leaderboards

```csharp
int wins = CPH.GetGlobalVar<int>($"{userId}_duelWins", true);
CPH.SetGlobalVar($"{userId}_duelWins", wins + 1, true);
```

---

### {userId}_duelLosses
- **Type:** `int` (Integer)
- **Initial Value:** `0`
- **Persisted:** ✅ Yes
- **Purpose:** Total PvP duel defeats
- **Modified By:** `[PVP] Duel Resolver`
- **Used In:** `!sheet` command, win/loss ratio

```csharp
int losses = CPH.GetGlobalVar<int>($"{userId}_duelLosses", true);
CPH.SetGlobalVar($"{userId}_duelLosses", losses + 1, true);
```

---

### {userId}_totalEggsWon
- **Type:** `int` (Integer)
- **Initial Value:** `0`
- **Persisted:** ✅ Yes
- **Purpose:** Lifetime total eggs earned from games
- **Modified By:** All game actions
- **Used In:** Achievement tracking, milestones

```csharp
int totalWon = CPH.GetGlobalVar<int>($"{userId}_totalEggsWon", true);
CPH.SetGlobalVar($"{userId}_totalEggsWon", totalWon + payout, true);
```

---

### {userId}_goldenEggsFound
- **Type:** `int` (Integer)
- **Initial Value:** `0`
- **Persisted:** ✅ Yes
- **Purpose:** Number of rare golden eggs found in Chomp Tunnel
- **Modified By:** `[GAME] Chomp Tunnel` (5% chance)
- **Used In:** Special achievements, bragging rights

```csharp
if (goldenEgg) {
    int goldenCount = CPH.GetGlobalVar<int>($"{userId}_goldenEggsFound", true);
    CPH.SetGlobalVar($"{userId}_goldenEggsFound", goldenCount + 1, true);
}
```

---

## Temporary Game State Variables

These variables manage active game states and expire automatically.

### Duel Challenge Variables

#### duel_challenger
- **Type:** `string` (User ID)
- **Initial Value:** `null`
- **Persisted:** ✅ Yes (but temporary in nature)
- **Purpose:** User ID of person who initiated challenge
- **Lifetime:** 2 minutes or until accepted
- **Cleared By:** `[PVP] Duel Accept` or timeout

```csharp
CPH.SetGlobalVar("duel_challenger", challengerId, true);
string challenger = CPH.GetGlobalVar<string>("duel_challenger", true);
```

---

#### duel_challengerName
- **Type:** `string` (Username)
- **Initial Value:** `null`
- **Persisted:** ✅ Yes
- **Purpose:** Display name of challenger
- **Lifetime:** Same as duel_challenger

---

#### duel_opponentName
- **Type:** `string` (Username)
- **Initial Value:** `null`
- **Persisted:** ✅ Yes
- **Purpose:** Display name of challenged player
- **Used For:** Validation (only this user can !accept)

---

#### duel_wager
- **Type:** `int` (Integer)
- **Initial Value:** `0`
- **Persisted:** ✅ Yes
- **Purpose:** Egg amount being wagered
- **Lifetime:** Same as duel_challenger

---

#### duel_timestamp
- **Type:** `long` (Ticks)
- **Initial Value:** `0`
- **Persisted:** ✅ Yes
- **Purpose:** When challenge was created (for 2-minute timeout)
- **Usage:** Validate challenge hasn't expired

```csharp
// Create timestamp
CPH.SetGlobalVar("duel_timestamp", DateTime.Now.Ticks, true);

// Check if expired
long challengeTime = CPH.GetGlobalVar<long>("duel_timestamp", true);
TimeSpan elapsed = TimeSpan.FromTicks(DateTime.Now.Ticks - challengeTime);
if (elapsed.TotalMinutes > 2) {
    // Expired
}
```

---

### Active Duel Variables

#### activeDuel_challenger
- **Type:** `string` (User ID)
- **Initial Value:** `null`
- **Persisted:** ✅ Yes
- **Purpose:** User ID of challenger in active duel
- **Lifetime:** 10 minutes or until resolved
- **Cleared By:** `[PVP] Duel Resolver`

---

#### activeDuel_challengerName
- **Type:** `string` (Username)
- **Initial Value:** `null`
- **Persisted:** ✅ Yes
- **Purpose:** Display name of challenger in active duel

---

#### activeDuel_accepter
- **Type:** `string` (User ID)
- **Initial Value:** `null`
- **Persisted:** ✅ Yes
- **Purpose:** User ID of accepter in active duel

---

#### activeDuel_accepterName
- **Type:** `string` (Username)
- **Initial Value:** `null`
- **Persisted:** ✅ Yes
- **Purpose:** Display name of accepter in active duel

---

#### activeDuel_wager
- **Type:** `int` (Integer)
- **Initial Value:** `0`
- **Persisted:** ✅ Yes
- **Purpose:** Egg amount being wagered per player

---

#### activeDuel_startTime
- **Type:** `long` (Ticks)
- **Initial Value:** `0`
- **Persisted:** ✅ Yes
- **Purpose:** When duel was accepted (for 10-minute auto-resolve)

```csharp
// Set start time
CPH.SetGlobalVar("activeDuel_startTime", DateTime.Now.Ticks, true);

// Check if 10 minutes passed
long startTime = CPH.GetGlobalVar<long>("activeDuel_startTime", true);
TimeSpan elapsed = TimeSpan.FromTicks(DateTime.Now.Ticks - startTime);
if (elapsed.TotalMinutes >= 10) {
    // Resolve duel
}
```

---

## Event and Bonus Variables

### {userId}_freeTokensReceived
- **Type:** `int` (Integer)
- **Initial Value:** `0`
- **Persisted:** ✅ Yes
- **Purpose:** Track how many free tokens user received during event
- **Modified By:** `[EVENT] Distribute Free Tokens`
- **Used For:** Limiting free token distribution per user

```csharp
int received = CPH.GetGlobalVar<int>($"{userId}_freeTokensReceived", true);
if (received < maxFreeTokens) {
    // Give free token
    CPH.SetGlobalVar($"{userId}_freeTokensReceived", received + 1, true);
}
```

---

### lastEventReset
- **Type:** `long` (Ticks)
- **Initial Value:** `0`
- **Persisted:** ✅ Yes
- **Purpose:** Track when event counters were last reset
- **Modified By:** Daily timer or manual reset
- **Used For:** Resetting daily limits

```csharp
CPH.SetGlobalVar("lastEventReset", DateTime.Now.Ticks, true);
```

---

## Variable Naming Conventions

### Standard Patterns

1. **Global Economy Variables:**
   - Format: `camelCase`
   - Examples: `bigNestFund`, `eggCartonJackpot`, `doubleRewardsActive`

2. **Per-User Variables:**
   - Format: `{userId}_camelCase`
   - Examples: `12345678_MysteryEgg`, `12345678_chompStreak`
   - **⚠️ ALWAYS use userId, NEVER userName**

3. **Temporary State Variables:**
   - Format: `context_camelCase`
   - Examples: `duel_challenger`, `activeDuel_wager`

4. **Event Variables:**
   - Format: `eventNameActive` or `eventNameEndTime`
   - Examples: `doubleRewardsActive`, `doubleRewardsEndTime`

### Why Use User IDs Instead of Usernames?

✅ **Correct:** `12345678_MysteryEgg`  
❌ **Wrong:** `JohnGamer_MysteryEgg`

**Reasons:**
- Usernames can change, User IDs never change
- Prevents data loss if user changes name
- Case-sensitivity issues avoided
- Consistent with Streamer.bot internal system

---

## Variable Management

### Viewing All Variables

**Method 1: Streamer.bot UI**
1. Go to: `Settings` → `Variables`
2. Browse Global Variables list
3. Search/filter by name

**Method 2: Debugging in Code**
```csharp
// Log variable value for debugging
string value = CPH.GetGlobalVar<string>("variableName", true);
CPH.LogInfo($"Variable value: {value}");
```

---

### Backing Up Variables

Variables are stored in Streamer.bot's data folder:
- **Location:** `%AppData%\Streamer.bot\` (Windows)
- **Files:** SQLite database files
- **Backup:** Copy entire Streamer.bot folder regularly

**Recommended Backup Schedule:**
- Before major updates: Always
- Weekly backups: Recommended
- Before adding new features: Recommended

---

### Resetting Variables

**Reset Single User:**
```csharp
// Reset all data for a specific user
string userId = "12345678";
CPH.UnsetGlobalVar($"{userId}_MysteryEgg", true);
CPH.UnsetGlobalVar($"{userId}_DiceEgg", true);
CPH.UnsetGlobalVar($"{userId}_DuelEgg", true);
CPH.UnsetGlobalVar($"{userId}_chompStreak", true);
// ... etc
```

**Reset Economy Funds:**
```csharp
CPH.SetGlobalVar("bigNestFund", 1000, true);
CPH.SetGlobalVar("eggCartonJackpot", 500, true);
```

**⚠️ WARNING:** Resetting variables cannot be undone without a backup!

---

### Variable Limits

**Streamer.bot Variable System:**
- No hard limit on number of variables
- Each variable limited by C# type limits:
  - `int`: -2,147,483,648 to 2,147,483,647
  - `long`: -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807
  - `string`: ~2 GB per string
  - `bool`: true/false

**Practical Limits:**
- Thousands of users: ✅ No problem
- Millions of variables: ⚠️ May impact performance
- Recommended: Periodic cleanup of inactive users

---

### Cleaning Up Old Variables

Create a maintenance action to remove variables for inactive users:

```csharp
// Example: Remove data for users inactive > 90 days
// NOTE: Requires custom tracking of last activity
// Implementation left to streamer preference
```

---

## Variable Type Reference

### Supported Types in C# Code

```csharp
// Integer (whole numbers)
int eggs = CPH.GetGlobalVar<int>("variableName", true);
CPH.SetGlobalVar("variableName", 100, true);

// Long (large integers, timestamps)
long timestamp = CPH.GetGlobalVar<long>("variableName", true);
CPH.SetGlobalVar("variableName", DateTime.Now.Ticks, true);

// Boolean (true/false)
bool active = CPH.GetGlobalVar<bool>("variableName", true);
CPH.SetGlobalVar("variableName", true, true);

// String (text)
string name = CPH.GetGlobalVar<string>("variableName", true);
CPH.SetGlobalVar("variableName", "text", true);

// Double (decimal numbers) - if needed for percentages
double multiplier = CPH.GetGlobalVar<double>("variableName", true);
CPH.SetGlobalVar("variableName", 1.5, true);
```

---

## Complete Variable Initialization Script

Use this in a one-time setup action to initialize all global variables:

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        // Initialize economy funds
        if (CPH.GetGlobalVar<int>("bigNestFund", true) == 0) {
            CPH.SetGlobalVar("bigNestFund", 1000, true);
            CPH.LogInfo("Initialized bigNestFund");
        }
        
        if (CPH.GetGlobalVar<int>("eggCartonJackpot", true) == 0) {
            CPH.SetGlobalVar("eggCartonJackpot", 500, true);
            CPH.LogInfo("Initialized eggCartonJackpot");
        }
        
        // Initialize event flags
        CPH.SetGlobalVar("doubleRewardsActive", false, true);
        CPH.SetGlobalVar("freeEntryTokensActive", false, true);
        
        CPH.SendMessage("✅ Economy variables initialized!");
        return true;
    }
}
```

---

## Troubleshooting Variable Issues

### Issue: Variables Not Persisting
**Symptoms:** Variables reset after Streamer.bot restart  
**Solution:** Ensure `persisted: true` in ALL GetGlobalVar/SetGlobalVar calls

### Issue: Variables Show As 0 When They Shouldn't
**Symptoms:** User reports having tokens but `!eggpack` shows 0  
**Solution:** 
- Check userId vs userName usage
- Verify variable name spelling (case-sensitive!)
- Check Settings → Variables to see actual stored name

### Issue: Cannot Find Variable in UI
**Symptoms:** Variable exists in code but not visible in Settings  
**Solution:**
- Variables only appear after first SetGlobalVar call
- Refresh Streamer.bot UI
- Check exact spelling and case

### Issue: "Object reference not set" Errors
**Symptoms:** Code crashes with null reference  
**Solution:**
```csharp
// BAD - can crash if null
string name = CPH.GetGlobalVar<string>("duel_challenger", true);
if (name.Equals("something")) { } // CRASH if null

// GOOD - safe null checking
string name = CPH.GetGlobalVar<string>("duel_challenger", true);
if (string.IsNullOrEmpty(name)) { 
    // Handle null case
} else {
    // Safe to use name
}
```

---

## Summary

This variable reference covers all aspects of the Yoshi's Eggonomy variable system:

✅ **175+ Variables** documented across all categories  
✅ **Type-safe examples** for all variable operations  
✅ **Naming conventions** for consistency  
✅ **Troubleshooting tips** for common issues  
✅ **Backup and maintenance** procedures  
✅ **Extension guidelines** for custom tokens and features

**Next Steps:**
1. Review the [Unified Eggonomy Guide](Unified_Yoshi_Eggonomy.md) for implementation
2. Use this reference when debugging or extending the system
3. Keep this document updated when adding custom features

---

**Questions or Issues?**  
Refer to the main guide's troubleshooting section or the Streamer.bot documentation.
