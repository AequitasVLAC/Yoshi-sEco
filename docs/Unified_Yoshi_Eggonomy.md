# Unified Guide: Egg-Based Economy for Streamer.bot

This document provides a comprehensive setup for creating an interactive egg-based economy using Streamer.bot. It integrates the token system, PvP mechanics, and games into a single, functional system where users can earn, spend, and lose eggs effectively. The design includes cohesive interactions, balanced game mechanics, and sinks to maintain a sustainable economy.

## Key Features
- **Main Currency:** Pouch Eggs (earned passively by viewers).
- **Token System:** Playable-game tokens (Mystery Eggs, Dice Eggs, Duel Eggs).
- **Games:** Fun and rewarding games like Chomp Tunnel, Hatch Roll, and PvP battles.
- **Balanced Economy:** Currency sinks to manage inflation and ensure long-term viability.
- **PvP with Timer-Based Resolution:** The Duel Nest PvP system is resolved automatically within 10 minutes.
- **Interactive Commands:** Clear and consistent commands for users to interact with the system.

---

## Stage 1: Initial Setup

### 1.1 Configure Pouch Eggs as the Main Currency
1. **Navigate to Points Settings:** Go to `Settings > Loyalty Points`.
2. **Rename Currency:**
    - **Name (Singular):** 🥚 Pouch Egg.
    - **Name (Plural):** 🥚 Pouch Eggs.
    - **Default Command:** `!eggs` (to check balance).
3. **Set Passive Income:**
    - **Base Reward:** 5 eggs per 10 minutes.
    - **Active Reward:** 10 eggs per 10 minutes for users who recently chat.
4. **Save:** Apply your changes.

### 1.2 Initialize Global Variables
Create the following global variables in Streamer.bot to track economy funds:
- **`bigNestFund`**: Accumulates 70% of all token purchases.
- **`eggCartonJackpot`**: Accumulates 20% of all token purchases.

These can be initialized via Streamer.bot's Variables section or through an initialization action.

---

## Stage 2: Token System

### 2.1 Token Definitions
The token system includes three token types, purchased using Pouch Eggs:
- **Mystery Eggs:** Cost 20 eggs, used in the *Chomp Tunnel* game.
- **Dice Eggs:** Cost 10 eggs, used in the *Hatch Roll* game.
- **Duel Eggs:** Cost 5 eggs, used in the PvP Duel Nest.

### 2.2 Buy Token Command
**Command:** `!buy <TokenType> <Quantity>`

**Example Usage:**
- `!buy MysteryEgg 1` - Purchase 1 Mystery Egg for 20 Pouch Eggs.
- `!buy DiceEgg 5` - Purchase 5 Dice Eggs for 50 Pouch Eggs.
- `!buy DuelEgg 2` - Purchase 2 Duel Eggs for 10 Pouch Eggs.

#### Implementation Steps:
1. **Create the Action:** `[ECON] Buy Token`
2. **Add the Token-Purchase Logic:**
    ```csharp
    // Parse user input
    string tokenType = args["rawInput0"]?.ToString(); // e.g., "MysteryEgg"
    
    // Validate quantity input
    if (args["rawInput1"] == null || !int.TryParse(args["rawInput1"].ToString(), out int quantity) || quantity < 1)
    {
        CPH.SendMessage($"@{args["userName"]}, please specify a valid quantity! Example: !buy MysteryEgg 1");
        return false;
    }
    
    // Define token costs
    Dictionary<string, int> tokenCosts = new Dictionary<string, int>
    {
        {"MysteryEgg", 20},
        {"DiceEgg", 10},
        {"DuelEgg", 5}
    };
    
    // Validate token type
    if (!tokenCosts.ContainsKey(tokenType))
    {
        CPH.SendMessage($"@{args["userName"]}, invalid token type! Use MysteryEgg, DiceEgg, or DuelEgg.");
        return false;
    }
    
    // Calculate total cost
    int totalCost = tokenCosts[tokenType] * quantity;
    int userBalance = CPH.GetPoints(args["userId"].ToString());
    
    // Check if user has enough Pouch Eggs
    if (userBalance < totalCost)
    {
        CPH.SendMessage($"@{args["userName"]}, you need {totalCost} Pouch Eggs but only have {userBalance}.");
        return false;
    }
    
    // Deduct Pouch Eggs
    CPH.RemovePoints(args["userId"].ToString(), totalCost);
    
    // Increment token balance
    string tokenVar = $"{args["userId"]}_{tokenType}";
    int currentTokens = CPH.GetGlobalVar<int>(tokenVar, true);
    CPH.SetGlobalVar(tokenVar, currentTokens + quantity, true);
    
    // Distribute funds
    int bigNestContribution = (int)(totalCost * 0.7);
    int jackpotContribution = (int)(totalCost * 0.2);
    // 10% is removed as a sink (not redistributed)
    
    int bigNestFund = CPH.GetGlobalVar<int>("bigNestFund", true);
    int eggCartonJackpot = CPH.GetGlobalVar<int>("eggCartonJackpot", true);
    
    CPH.SetGlobalVar("bigNestFund", bigNestFund + bigNestContribution, true);
    CPH.SetGlobalVar("eggCartonJackpot", eggCartonJackpot + jackpotContribution, true);
    
    CPH.SendMessage($"@{args["userName"]} purchased {quantity} {tokenType}(s) for {totalCost} Pouch Eggs!");
    
    return true;
    ```

3. **Configure Command Trigger:**
    - **Command:** `!buy`
    - **Permissions:** Everyone
    - **Cooldown:** 5 seconds per user

---

## Stage 3: Games

### 3.1 Game: Chomp Tunnel
**Command:** `!chomp`

**Mechanics:**
- **Cost:** 1 Mystery Egg.
- **Gameplay:**
  - Roll a 6-sided die (1-6).
  - A roll of `1` results in a loss (Chain Chomp eats the egg and your streak resets).
  - Any other roll increases your streak multiplier.
  - Payouts increase with streak (e.g., streak 1 = 10 eggs, streak 2 = 15 eggs, etc.).
  - **Rare Reward:** 5% chance to receive a Golden Egg bonus (100 eggs).

#### Implementation Steps:
1. **Create the Action:** `[GAME] Chomp Tunnel`
2. **Add Game Logic:**
    ```csharp
    string userId = args["userId"].ToString();
    string userName = args["userName"].ToString();
    
    // Check if user has Mystery Eggs
    string tokenVar = $"{userId}_MysteryEgg";
    int mysteryEggs = CPH.GetGlobalVar<int>(tokenVar, true);
    
    if (mysteryEggs < 1)
    {
        CPH.SendMessage($"@{userName}, you need at least 1 Mystery Egg to play Chomp Tunnel! Use !buy MysteryEgg 1");
        return false;
    }
    
    // Deduct 1 Mystery Egg
    CPH.SetGlobalVar(tokenVar, mysteryEggs - 1, true);
    
    // Roll the dice
    Random rnd = new Random();
    int roll = rnd.Next(1, 7); // 1-6
    
    // Check for rare Golden Egg (5% chance)
    bool goldenEgg = rnd.Next(1, 101) <= 5;
    
    if (roll == 1)
    {
        // Loss - Reset streak
        CPH.SetGlobalVar($"{userId}_chompStreak", 0, true);
        CPH.SendMessage($"@{userName} rolled a {roll}! 💀 Chain Chomp ate your egg! Streak reset.");
    }
    else
    {
        // Win - Increase streak
        int streak = CPH.GetGlobalVar<int>($"{userId}_chompStreak", true);
        streak++;
        CPH.SetGlobalVar($"{userId}_chompStreak", streak, true);
        
        // Calculate payout
        int basePayout = 10;
        int payout = basePayout + (streak * 5);
        
        if (goldenEgg)
        {
            payout += 100;
            CPH.AddPoints(userId, payout);
            CPH.SendMessage($"@{userName} rolled a {roll}! 🌟 GOLDEN EGG BONUS! +{payout} Pouch Eggs! Streak: {streak}");
        }
        else
        {
            CPH.AddPoints(userId, payout);
            CPH.SendMessage($"@{userName} rolled a {roll}! Safe! +{payout} Pouch Eggs! Streak: {streak}");
        }
    }
    
    return true;
    ```

3. **Configure Command Trigger:**
    - **Command:** `!chomp`
    - **Permissions:** Everyone
    - **Cooldown:** 10 seconds per user

---

### 3.2 Game: Hatch Roll
**Command:** `!eggroll`

**Mechanics:**
- **Cost:** 1 Dice Egg.
- **Gameplay:**
  - Roll a 20-sided die (D20).
  - Reward tiers based on roll:
    - **1:** No reward (egg hatches into nothing).
    - **2-5:** Small reward (5 eggs).
    - **6-10:** Medium reward (15 eggs).
    - **11-15:** Good reward (30 eggs).
    - **16-18:** Great reward (50 eggs).
    - **19-20:** Jackpot reward (100 eggs).

#### Implementation Steps:
1. **Create the Action:** `[GAME] Hatch Roll`
2. **Add Game Logic:**
    ```csharp
    string userId = args["userId"].ToString();
    string userName = args["userName"].ToString();
    
    // Check if user has Dice Eggs
    string tokenVar = $"{userId}_DiceEgg";
    int diceEggs = CPH.GetGlobalVar<int>(tokenVar, true);
    
    if (diceEggs < 1)
    {
        CPH.SendMessage($"@{userName}, you need at least 1 Dice Egg to play Hatch Roll! Use !buy DiceEgg 1");
        return false;
    }
    
    // Deduct 1 Dice Egg
    CPH.SetGlobalVar(tokenVar, diceEggs - 1, true);
    
    // Roll D20
    Random rnd = new Random();
    int roll = rnd.Next(1, 21); // 1-20
    
    int payout = 0;
    string message = "";
    
    if (roll == 1)
    {
        message = $"@{userName} rolled a {roll}! 💔 Your egg hatched into nothing!";
    }
    else if (roll <= 5)
    {
        payout = 5;
        message = $"@{userName} rolled a {roll}! 🥚 Small hatch! +{payout} Pouch Eggs!";
    }
    else if (roll <= 10)
    {
        payout = 15;
        message = $"@{userName} rolled a {roll}! 🐣 Medium hatch! +{payout} Pouch Eggs!";
    }
    else if (roll <= 15)
    {
        payout = 30;
        message = $"@{userName} rolled a {roll}! 🐥 Good hatch! +{payout} Pouch Eggs!";
    }
    else if (roll <= 18)
    {
        payout = 50;
        message = $"@{userName} rolled a {roll}! 🌟 Great hatch! +{payout} Pouch Eggs!";
    }
    else
    {
        payout = 100;
        message = $"@{userName} rolled a {roll}! 🎉 JACKPOT HATCH! +{payout} Pouch Eggs!";
    }
    
    if (payout > 0)
    {
        CPH.AddPoints(userId, payout);
    }
    
    CPH.SendMessage(message);
    
    return true;
    ```

3. **Configure Command Trigger:**
    - **Command:** `!eggroll`
    - **Permissions:** Everyone
    - **Cooldown:** 10 seconds per user

---

### 3.3 Game: Duel Nest PvP
**Command:** `!duelnest <@opponent> <wager>`

**Mechanics:**
- **Cost:** 1 Duel Egg per participant.
- **Gameplay:**
  - Challenger initiates a duel with an opponent and a wager amount.
  - Both players must have at least 1 Duel Egg and sufficient Pouch Eggs for the wager.
  - Opponent has 2 minutes to accept with `!accept`.
  - Once accepted, the duel auto-resolves after 10 minutes with randomized rolls.
  - **Winner:** Receives 85% of the loser's wager + their original bet back.
  - **Sink:** 15% goes to `bigNestFund`.

#### Implementation Steps:
1. **Create the Action:** `[PVP] Duel Nest Challenge`
2. **Add Challenge Logic:**
    ```csharp
    string challengerId = args["userId"].ToString();
    string challengerName = args["userName"].ToString();
    string opponentName = args["rawInput0"]?.ToString().TrimStart('@');
    
    // Validate wager input
    if (args["rawInput1"] == null || !int.TryParse(args["rawInput1"].ToString(), out int wager) || wager < 1)
    {
        CPH.SendMessage($"@{challengerName}, please specify a valid wager amount! Example: !duelnest @user 50");
        return false;
    }
    
    // Validate opponent name
    if (string.IsNullOrEmpty(opponentName))
    {
        CPH.SendMessage($"@{challengerName}, please specify an opponent! Example: !duelnest @user 50");
        return false;
    }
    
    // Validate wager
    if (wager < 1)
    {
        CPH.SendMessage($"@{challengerName}, wager must be at least 1 Pouch Egg!");
        return false;
    }
    
    // Check if challenger has Duel Eggs
    string challengerTokenVar = $"{challengerId}_DuelEgg";
    int challengerDuelEggs = CPH.GetGlobalVar<int>(challengerTokenVar, true);
    
    if (challengerDuelEggs < 1)
    {
        CPH.SendMessage($"@{challengerName}, you need at least 1 Duel Egg! Use !buy DuelEgg 1");
        return false;
    }
    
    // Check if challenger has enough Pouch Eggs
    int challengerBalance = CPH.GetPoints(challengerId);
    if (challengerBalance < wager)
    {
        CPH.SendMessage($"@{challengerName}, you only have {challengerBalance} Pouch Eggs but are wagering {wager}!");
        return false;
    }
    
    // Get opponent user ID
    // Note: In Streamer.bot, you can use CPH.GetUserIdForName(opponentName) to validate the user exists
    // Alternatively, the accept command will validate the opponent when they try to accept
    
    // Store challenge details
    CPH.SetGlobalVar($"duel_challenger", challengerId, true);
    CPH.SetGlobalVar($"duel_challengerName", challengerName, true);
    CPH.SetGlobalVar($"duel_opponentName", opponentName, true);
    CPH.SetGlobalVar($"duel_wager", wager, true);
    CPH.SetGlobalVar($"duel_timestamp", DateTime.Now.Ticks, true);
    
    CPH.SendMessage($"@{opponentName}, {challengerName} challenges you to a Duel Nest for {wager} Pouch Eggs! Type !accept within 2 minutes!");
    
    return true;
    ```

3. **Create the Action:** `[PVP] Duel Nest Accept`
4. **Add Accept Logic:**
    ```csharp
    string accepterId = args["userId"].ToString();
    string accepterName = args["userName"].ToString();
    
    // Check if there's an active challenge for this user
    string opponentName = CPH.GetGlobalVar<string>("duel_opponentName", true);
    
    if (opponentName != accepterName)
    {
        CPH.SendMessage($"@{accepterName}, there's no active duel challenge for you!");
        return false;
    }
    
    // Check timestamp (2 minute window)
    long challengeTime = CPH.GetGlobalVar<long>("duel_timestamp", true);
    TimeSpan elapsed = TimeSpan.FromTicks(DateTime.Now.Ticks - challengeTime);
    
    if (elapsed.TotalMinutes > 2)
    {
        CPH.SendMessage($"@{accepterName}, the duel challenge has expired!");
        CPH.UnsetGlobalVar("duel_challenger", true);
        return false;
    }
    
    // Get challenge details
    string challengerId = CPH.GetGlobalVar<string>("duel_challenger", true);
    string challengerName = CPH.GetGlobalVar<string>("duel_challengerName", true);
    int wager = CPH.GetGlobalVar<int>("duel_wager", true);
    
    // Check if accepter has Duel Eggs
    string accepterTokenVar = $"{accepterId}_DuelEgg";
    int accepterDuelEggs = CPH.GetGlobalVar<int>(accepterTokenVar, true);
    
    if (accepterDuelEggs < 1)
    {
        CPH.SendMessage($"@{accepterName}, you need at least 1 Duel Egg to accept! Use !buy DuelEgg 1");
        return false;
    }
    
    // Check if accepter has enough Pouch Eggs
    int accepterBalance = CPH.GetPoints(accepterId);
    if (accepterBalance < wager)
    {
        CPH.SendMessage($"@{accepterName}, you need {wager} Pouch Eggs but only have {accepterBalance}!");
        return false;
    }
    
    // Deduct Duel Eggs from both players
    string challengerTokenVar = $"{challengerId}_DuelEgg";
    int challengerDuelEggs = CPH.GetGlobalVar<int>(challengerTokenVar, true);
    CPH.SetGlobalVar(challengerTokenVar, challengerDuelEggs - 1, true);
    CPH.SetGlobalVar(accepterTokenVar, accepterDuelEggs - 1, true);
    
    // Store duel details for resolution
    CPH.SetGlobalVar($"activeDuel_challenger", challengerId, true);
    CPH.SetGlobalVar($"activeDuel_challengerName", challengerName, true);
    CPH.SetGlobalVar($"activeDuel_accepter", accepterId, true);
    CPH.SetGlobalVar($"activeDuel_accepterName", accepterName, true);
    CPH.SetGlobalVar($"activeDuel_wager", wager, true);
    CPH.SetGlobalVar($"activeDuel_startTime", DateTime.Now.Ticks, true);
    
    CPH.SendMessage($"⚔️ Duel accepted! {challengerName} vs {accepterName} for {wager} Pouch Eggs! The duel will auto-resolve in 10 minutes!");
    
    // Schedule resolution after 10 minutes (would need a timer/delayed action in Streamer.bot)
    // For implementation: Create a separate action that runs every minute to check for duels to resolve
    
    // Clear challenge variables
    CPH.UnsetGlobalVar("duel_challenger", true);
    CPH.UnsetGlobalVar("duel_challengerName", true);
    CPH.UnsetGlobalVar("duel_opponentName", true);
    CPH.UnsetGlobalVar("duel_wager", true);
    CPH.UnsetGlobalVar("duel_timestamp", true);
    
    return true;
    ```

5. **Create the Action:** `[PVP] Duel Nest Resolver` (runs periodically)
6. **Add Resolution Logic:**
    ```csharp
    // Check if there's an active duel
    string challengerId = CPH.GetGlobalVar<string>("activeDuel_challenger", true);
    if (string.IsNullOrEmpty(challengerId))
    {
        return false; // No active duel
    }
    
    // Check if 10 minutes have passed
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
    
    // Randomized roll to determine winner
    Random rnd = new Random();
    int challengerRoll = rnd.Next(1, 101);
    int accepterRoll = rnd.Next(1, 101);
    
    string winner, loser, winnerId, loserId;
    
    if (challengerRoll > accepterRoll)
    {
        winner = challengerName;
        winnerId = challengerId;
        loser = accepterName;
        loserId = accepterId;
    }
    else
    {
        winner = accepterName;
        winnerId = accepterId;
        loser = challengerName;
        loserId = challengerId;
    }
    
    // Calculate payouts
    int totalPot = wager * 2;
    int winnerPayout = (int)(wager * 1.85); // Winner gets their wager back + 85% of opponent's
    int sinkAmount = totalPot - winnerPayout;
    
    // Deduct wagers
    CPH.RemovePoints(challengerId, wager);
    CPH.RemovePoints(accepterId, wager);
    
    // Award winner
    CPH.AddPoints(winnerId, winnerPayout);
    
    // Add to bigNestFund
    int bigNestFund = CPH.GetGlobalVar<int>("bigNestFund", true);
    CPH.SetGlobalVar("bigNestFund", bigNestFund + sinkAmount, true);
    
    CPH.SendMessage($"⚔️ Duel Result: {winner} (roll: {(winner == challengerName ? challengerRoll : accepterRoll)}) defeats {loser} (roll: {(loser == challengerName ? challengerRoll : accepterRoll)})! {winner} wins {winnerPayout} Pouch Eggs!");
    
    // Clear active duel
    CPH.UnsetGlobalVar("activeDuel_challenger", true);
    CPH.UnsetGlobalVar("activeDuel_challengerName", true);
    CPH.UnsetGlobalVar("activeDuel_accepter", true);
    CPH.UnsetGlobalVar("activeDuel_accepterName", true);
    CPH.UnsetGlobalVar("activeDuel_wager", true);
    CPH.UnsetGlobalVar("activeDuel_startTime", true);
    
    return true;
    ```

7. **Configure Command Triggers:**
    - **Command for Challenge:** `!duelnest`
    - **Command for Accept:** `!accept`
    - **Permissions:** Everyone
    - **Cooldown:** 30 seconds per user
    
8. **Set up Timer for Auto-Resolution:**
    - In Streamer.bot, go to `Actions > Timed Actions`
    - Create a new timed action
    - Set it to run every **1 minute** (or 60 seconds)
    - Link it to the `[PVP] Duel Nest Resolver` action
    - Enable the timer
    - This will check for duels that need to be resolved every minute

---

## Stage 4: Commands and User Interaction

### 4.1 View Inventory
**Command:** `!eggpack`

Displays the user's current token balances.

#### Implementation Steps:
1. **Create the Action:** `[USER] View Inventory`
2. **Add Display Logic:**
    ```csharp
    string userId = args["userId"].ToString();
    string userName = args["userName"].ToString();
    
    // Get token balances
    int mysteryEggs = CPH.GetGlobalVar<int>($"{userId}_MysteryEgg", true);
    int diceEggs = CPH.GetGlobalVar<int>($"{userId}_DiceEgg", true);
    int duelEggs = CPH.GetGlobalVar<int>($"{userId}_DuelEgg", true);
    int pouchEggs = CPH.GetPoints(userId);
    
    CPH.SendMessage($"@{userName}'s Egg Pack 🎒: {pouchEggs} Pouch Eggs 🥚 | {mysteryEggs} Mystery Eggs 🔮 | {diceEggs} Dice Eggs 🎲 | {duelEggs} Duel Eggs ⚔️");
    
    return true;
    ```

3. **Configure Command Trigger:**
    - **Command:** `!eggpack`
    - **Permissions:** Everyone
    - **Cooldown:** 10 seconds per user

---

### 4.2 Check Character Sheet
**Command:** `!sheet`

Shows the user's current game stats (streaks, total wins, etc.).

#### Implementation Steps:
1. **Create the Action:** `[USER] View Character Sheet`
2. **Add Display Logic:**
    ```csharp
    string userId = args["userId"].ToString();
    string userName = args["userName"].ToString();
    
    // Get stats
    int chompStreak = CPH.GetGlobalVar<int>($"{userId}_chompStreak", true);
    int chompWins = CPH.GetGlobalVar<int>($"{userId}_chompWins", true);
    int eggrollPlays = CPH.GetGlobalVar<int>($"{userId}_eggrollPlays", true);
    int duelWins = CPH.GetGlobalVar<int>($"{userId}_duelWins", true);
    int duelLosses = CPH.GetGlobalVar<int>($"{userId}_duelLosses", true);
    
    CPH.SendMessage($"@{userName}'s Sheet 📋: Chomp Streak: {chompStreak} | Chomp Wins: {chompWins} | Egg Rolls: {eggrollPlays} | Duel W/L: {duelWins}/{duelLosses}");
    
    return true;
    ```

3. **Configure Command Trigger:**
    - **Command:** `!sheet`
    - **Permissions:** Everyone
    - **Cooldown:** 10 seconds per user

---

### 4.3 Reset Character
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
| `!eggpack` | View your inventory | Free |
| `!sheet` | View your character stats | Free |
| `!reroll` | Reset your character | 1,000 Pouch Eggs |

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