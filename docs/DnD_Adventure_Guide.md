# DnD-Style Adventure Game for Streamer.bot

**Platform:** Streamer.bot (v0.2.0+)  
**Last Updated:** December 2025  
**Integration:** Yoshi's Island Eggonomy System

> **💬 Twitch Chat Compliant:** All messages respect Twitch's 500 character limit and deliver compact, engaging adventure scenarios.

This guide teaches you how to add an interactive DnD-style "Choose Your Own Adventure" game to your Streamer.bot economy system. Players spend eggs for daily adventures with saving throws, randomized outcomes, and rewards.

---

## Table of Contents

1. [Game Overview](#game-overview)
2. [Game Mechanics](#game-mechanics)
3. [Implementation Guide](#implementation-guide)
4. [Variable Reference](#variable-reference)
5. [Customization Options](#customization-options)
6. [Testing & Troubleshooting](#testing--troubleshooting)

---

## Game Overview

### What is the DnD Adventure Game?

The DnD Adventure is a daily interactive text-based adventure that brings tabletop RPG mechanics to your Twitch stream. Each viewer can embark on one adventure per day, facing randomized challenges that require saving throws using classic DnD attributes.

### Key Features

- **Daily Adventure:** Players can participate once every 24 hours
- **Entry Cost:** 500 Pouch Eggs per adventure
- **Saving Throws:** Seven types (STR, DEX, CON, INT, WIS, CHA, Death)
- **D20 Rolls:** Classic 1-20 rolls determine success or failure
- **Randomized Scenarios:** Unique challenges each time
- **Rewards:** Earn eggs, Mystery/Dice/Duel tokens, or bonuses
- **Compact Messages:** All scenarios fit in Twitch's 500-character limit
- **Economy Integration:** Works seamlessly with existing egg economy

### Game Flow

1. Player types `!adventure` (once per 24 hours)
2. System deducts 500 eggs
3. Random scenario selected
4. Saving throw required (random attribute)
5. D20 roll determines outcome
6. Reward or penalty applied based on roll
7. Adventure completes, 24-hour cooldown starts

---

## Game Mechanics

### Saving Throw System

Each adventure requires a saving throw using one of seven attributes:

| Attribute | Abbreviation | Used For |
|-----------|--------------|----------|
| **Strength** | STR | Physical challenges, breaking barriers |
| **Dexterity** | DEX | Avoiding traps, quick reflexes |
| **Constitution** | CON | Resisting poison, environmental damage |
| **Intelligence** | INT | Solving puzzles, resisting enchantments |
| **Wisdom** | WIS | Resisting mind control, perceiving danger |
| **Charisma** | CHA | Negotiating, charming NPCs |
| **Death Saves** | DEATH | Life-or-death situations |

### Roll Outcomes (D20)

The outcome of each saving throw depends on the D20 roll:

- **1 (Critical Failure):** Severe negative outcome
- **2-5 (Failure):** Moderate failure, minor penalty
- **6-10 (Partial Success):** Success with complications
- **11-15 (Success):** Good outcome with rewards
- **16-19 (Great Success):** Excellent outcome with bonus rewards
- **20 (Critical Success):** Extraordinary outcome, maximum rewards

### Reward Structure

Based on roll results, players can earn:

- **Critical Failure (1):** Lose 200-300 eggs
- **Failure (2-5):** Lose 50-100 eggs or break even
- **Partial Success (6-10):** Gain 100-300 eggs
- **Success (11-15):** Gain 400-600 eggs + chance for 1 token
- **Great Success (16-19):** Gain 700-900 eggs + 1 guaranteed token
- **Critical Success (20):** Gain 1000-1500 eggs + 2 tokens

### Daily Cooldown

- Each player can play once every 24 hours
- Cooldown tracked using global variable with timestamp
- Attempting to play before cooldown expires shows remaining time

---

## Implementation Guide

### Prerequisites

Before implementing the DnD Adventure game, ensure you have:

- ✅ Core Yoshi's Eggonomy system implemented (Pouch Eggs currency)
- ✅ Token system configured (Mystery, Dice, Duel tokens)
- ✅ Basic understanding of Streamer.bot actions and commands
- ✅ Familiarity with global variable management

If you haven't set up the base economy, see the [Unified Eggonomy Guide](Unified_Yoshi_Eggonomy.md) first.

---

### Step 1: Create the Main Adventure Action

**Action Name:** `[GAME] DnD Adventure`

**Setup Instructions:**

1. Open Streamer.bot
2. Go to `Actions` tab → Click **Add**
3. **Action Name:** `[GAME] DnD Adventure`
4. Click **OK**

**Add Execute Code Sub-Action:**

1. Click **Add Sub-Action** → `Core` → `C#` → `Execute Code`
2. **DELETE ALL** default code and paste the complete code below:

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        string userId = args["userId"].ToString();
        string userName = args["userName"].ToString();
        
        // Check daily cooldown (24 hours)
        string cooldownVar = $"{userId}_adventureLastPlayed";
        long lastPlayed = CPH.GetGlobalVar<long>(cooldownVar, true);
        long currentTime = DateTimeOffset.UtcNow.ToUnixTimeSeconds();
        long cooldownSeconds = 86400; // 24 hours
        
        if (lastPlayed > 0 && (currentTime - lastPlayed) < cooldownSeconds)
        {
            long remainingSeconds = cooldownSeconds - (currentTime - lastPlayed);
            long hours = remainingSeconds / 3600;
            long minutes = (remainingSeconds % 3600) / 60;
            
            CPH.SendMessage($"@{userName}, you've already had your daily adventure! Return in {hours}h {minutes}m. 🗡️");
            return false;
        }
        
        // Check if user has enough eggs (500 cost)
        int currentEggs = CPH.GetPoints(userId);
        int adventureCost = 500;
        
        if (currentEggs < adventureCost)
        {
            CPH.SendMessage($"@{userName}, you need {adventureCost} 🥚 for an adventure! You have {currentEggs} 🥚.");
            return false;
        }
        
        // Deduct entry cost
        CPH.RemovePoints(userId, adventureCost, "DnD Adventure Entry");
        
        // Update cooldown
        CPH.SetGlobalVar(cooldownVar, currentTime, true);
        
        // Select random saving throw type
        Random rnd = new Random();
        string[] savingThrows = { "STR", "DEX", "CON", "INT", "WIS", "CHA", "DEATH" };
        string saveType = savingThrows[rnd.Next(savingThrows.Length)];
        
        // Roll D20
        int roll = rnd.Next(1, 21);
        
        // Select random scenario based on saving throw type
        string scenario = GetScenario(saveType, roll);
        
        // Determine outcome and rewards
        int eggReward = 0;
        int tokenReward = 0;
        string tokenType = "";
        
        if (roll == 1)
        {
            // Critical Failure
            eggReward = -rnd.Next(200, 301);
            scenario += $" You lose {Math.Abs(eggReward)} 🥚!";
        }
        else if (roll <= 5)
        {
            // Failure
            eggReward = -rnd.Next(50, 101);
            scenario += $" You lose {Math.Abs(eggReward)} 🥚.";
        }
        else if (roll <= 10)
        {
            // Partial Success
            eggReward = rnd.Next(100, 301);
            scenario += $" You gain {eggReward} 🥚!";
        }
        else if (roll <= 15)
        {
            // Success
            eggReward = rnd.Next(400, 601);
            // 50% chance for token
            if (rnd.Next(1, 3) == 1)
            {
                tokenReward = 1;
                tokenType = GetRandomToken(rnd);
            }
            string tokenMsg = tokenReward > 0 ? $" + 1 {tokenType} token!" : "!";
            scenario += $" You gain {eggReward} 🥚{tokenMsg}";
        }
        else if (roll <= 19)
        {
            // Great Success
            eggReward = rnd.Next(700, 901);
            tokenReward = 1;
            tokenType = GetRandomToken(rnd);
            scenario += $" You gain {eggReward} 🥚 + 1 {tokenType} token!";
        }
        else
        {
            // Critical Success (20)
            eggReward = rnd.Next(1000, 1501);
            tokenReward = 2;
            tokenType = GetRandomToken(rnd);
            scenario += $" CRITICAL! You gain {eggReward} 🥚 + 2 {tokenType} tokens!";
        }
        
        // Apply egg rewards/penalties
        if (eggReward > 0)
        {
            CPH.AddPoints(userId, eggReward, "DnD Adventure Win");
        }
        else if (eggReward < 0)
        {
            CPH.RemovePoints(userId, Math.Abs(eggReward), "DnD Adventure Loss");
        }
        
        // Apply token rewards
        if (tokenReward > 0)
        {
            string tokenVar = $"{userId}_{tokenType}";
            int currentTokens = CPH.GetGlobalVar<int>(tokenVar, true);
            CPH.SetGlobalVar(tokenVar, currentTokens + tokenReward, true);
        }
        
        // Update statistics
        int totalAdventures = CPH.GetGlobalVar<int>($"{userId}_totalAdventures", true);
        CPH.SetGlobalVar($"{userId}_totalAdventures", totalAdventures + 1, true);
        
        // Send the adventure message
        CPH.SendMessage($"🎲 @{userName} | {saveType} Save (Roll: {roll}) | {scenario}");
        
        return true;
    }
    
    private string GetScenario(string saveType, int roll)
    {
        Random rnd = new Random();
        
        switch (saveType)
        {
            case "STR":
                return GetStrengthScenario(roll, rnd);
            case "DEX":
                return GetDexterityScenario(roll, rnd);
            case "CON":
                return GetConstitutionScenario(roll, rnd);
            case "INT":
                return GetIntelligenceScenario(roll, rnd);
            case "WIS":
                return GetWisdomScenario(roll, rnd);
            case "CHA":
                return GetCharismaScenario(roll, rnd);
            case "DEATH":
                return GetDeathSaveScenario(roll, rnd);
            default:
                return "A mysterious event occurs.";
        }
    }
    
    private string GetStrengthScenario(int roll, Random rnd)
    {
        string[] scenarios = {
            "A massive boulder blocks your path!",
            "You must lift a portcullis to escape!",
            "An iron door stands between you and treasure!",
            "You wrestle a cave troll!",
            "A rope bridge starts to collapse!"
        };
        
        string scenario = scenarios[rnd.Next(scenarios.Length)];
        
        if (roll == 1) return scenario + " You fail catastrophically and get crushed.";
        if (roll <= 5) return scenario + " You strain but can't overcome it.";
        if (roll <= 10) return scenario + " You barely manage with great effort.";
        if (roll <= 15) return scenario + " You succeed with impressive strength!";
        if (roll <= 19) return scenario + " You dominate the challenge!";
        return scenario + " You obliterate it with godly might!";
    }
    
    private string GetDexterityScenario(int roll, Random rnd)
    {
        string[] scenarios = {
            "Poison darts shoot from the walls!",
            "The floor gives way to a pit trap!",
            "A swinging axe pendulum appears!",
            "You must leap across crumbling stones!",
            "Arrows fly from hidden mechanisms!"
        };
        
        string scenario = scenarios[rnd.Next(scenarios.Length)];
        
        if (roll == 1) return scenario + " You stumble and take the full hit.";
        if (roll <= 5) return scenario + " You dodge too slowly and get grazed.";
        if (roll <= 10) return scenario + " You narrowly avoid the worst.";
        if (roll <= 15) return scenario + " You gracefully evade!";
        if (roll <= 19) return scenario + " You perform an acrobatic feat!";
        return scenario + " You backflip through impossibly!";
    }
    
    private string GetConstitutionScenario(int roll, Random rnd)
    {
        string[] scenarios = {
            "Toxic gas fills the chamber!",
            "A venomous snake bites you!",
            "You drink from a cursed fountain!",
            "Freezing water threatens hypothermia!",
            "Diseased rats swarm you!"
        };
        
        string scenario = scenarios[rnd.Next(scenarios.Length)];
        
        if (roll == 1) return scenario + " Your body fails you completely.";
        if (roll <= 5) return scenario + " You suffer badly from the effects.";
        if (roll <= 10) return scenario + " You endure but feel weakened.";
        if (roll <= 15) return scenario + " You resist most of the harm!";
        if (roll <= 19) return scenario + " Your fortitude is impressive!";
        return scenario + " You're completely immune!";
    }
    
    private string GetIntelligenceScenario(int roll, Random rnd)
    {
        string[] scenarios = {
            "An ancient rune puzzle bars the way!",
            "You must decode a cryptic riddle!",
            "A magical trap activates!",
            "You find a mysterious tome!",
            "An illusion threatens to deceive you!"
        };
        
        string scenario = scenarios[rnd.Next(scenarios.Length)];
        
        if (roll == 1) return scenario + " Your wrong answer triggers disaster.";
        if (roll <= 5) return scenario + " You can't solve it and face consequences.";
        if (roll <= 10) return scenario + " You figure it out after some struggle.";
        if (roll <= 15) return scenario + " You solve it cleverly!";
        if (roll <= 19) return scenario + " Your genius shines through!";
        return scenario + " You comprehend it instantly with brilliant insight!";
    }
    
    private string GetWisdomScenario(int roll, Random rnd)
    {
        string[] scenarios = {
            "A siren's song tries to charm you!",
            "Mind-altering spores cloud your judgment!",
            "A spectral voice whispers madness!",
            "You sense danger but can't locate it!",
            "An evil presence attempts to dominate you!"
        };
        
        string scenario = scenarios[rnd.Next(scenarios.Length)];
        
        if (roll == 1) return scenario + " You succumb completely to the effect.";
        if (roll <= 5) return scenario + " You're heavily influenced and suffer.";
        if (roll <= 10) return scenario + " You resist but feel the strain.";
        if (roll <= 15) return scenario + " You see through it clearly!";
        if (roll <= 19) return scenario + " Your mental fortitude prevails!";
        return scenario + " You turn the effect back on itself!";
    }
    
    private string GetCharismaScenario(int roll, Random rnd)
    {
        string[] scenarios = {
            "You encounter hostile bandits!",
            "A dragon demands tribute!",
            "Suspicious guards question you!",
            "A merchant has rare items to trade!",
            "A rival adventurer challenges your claim!"
        };
        
        string scenario = scenarios[rnd.Next(scenarios.Length)];
        
        if (roll == 1) return scenario + " You offend them gravely.";
        if (roll <= 5) return scenario + " Your words make things worse.";
        if (roll <= 10) return scenario + " You barely convince them.";
        if (roll <= 15) return scenario + " You charm them successfully!";
        if (roll <= 19) return scenario + " They become your allies!";
        return scenario + " You win them over completely, gaining legendary favor!";
    }
    
    private string GetDeathSaveScenario(int roll, Random rnd)
    {
        string[] scenarios = {
            "You're on the brink of death!",
            "Your life force fades rapidly!",
            "You feel yourself slipping away!",
            "Darkness closes in around you!",
            "Your heartbeat slows dangerously!"
        };
        
        string scenario = scenarios[rnd.Next(scenarios.Length)];
        
        if (roll == 1) return scenario + " You fail to stabilize.";
        if (roll <= 5) return scenario + " You barely cling to consciousness.";
        if (roll <= 10) return scenario + " You stabilize but are weak.";
        if (roll <= 15) return scenario + " You recover with determination!";
        if (roll <= 19) return scenario + " You spring back with vigor!";
        return scenario + " You defy death itself with miraculous recovery!";
    }
    
    private string GetRandomToken(Random rnd)
    {
        string[] tokens = { "MysteryEgg", "DiceEgg", "DuelEgg" };
        return tokens[rnd.Next(tokens.Length)];
    }
}
```

3. Click **Compile** → Should say "Compiled Successfully"
4. Click **Save and Compile**

---

### Step 2: Create the Command

**Setup Instructions:**

1. Go to `Commands` tab → Click **Add**
2. **Command:** `!adventure`
3. **Enabled:** ✅ Yes
4. **Action:** Select `[GAME] DnD Adventure`
5. **User Cooldown:** 5 seconds (prevents spam, game has internal 24h cooldown)
6. **Allow Command to Execute While Already Running:** ❌ No
7. Click **OK**

---

### Step 3: Add Adventure Stats Command (Optional)

Create a command to let players check their adventure statistics.

**Action Name:** `[USER] Adventure Stats`

**Setup Instructions:**

1. Go to `Actions` tab → Click **Add**
2. **Action Name:** `[USER] Adventure Stats`
3. Add Execute Code Sub-Action with this code:

```csharp
using System;

public class CPHInline
{
    public bool Execute()
    {
        string userId = args["userId"].ToString();
        string userName = args["userName"].ToString();
        
        // Get adventure statistics
        int totalAdventures = CPH.GetGlobalVar<int>($"{userId}_totalAdventures", true);
        
        // Check cooldown status
        string cooldownVar = $"{userId}_adventureLastPlayed";
        long lastPlayed = CPH.GetGlobalVar<long>(cooldownVar, true);
        long currentTime = DateTimeOffset.UtcNow.ToUnixTimeSeconds();
        long cooldownSeconds = 86400; // 24 hours
        
        string status = "";
        if (lastPlayed > 0 && (currentTime - lastPlayed) < cooldownSeconds)
        {
            long remainingSeconds = cooldownSeconds - (currentTime - lastPlayed);
            long hours = remainingSeconds / 3600;
            long minutes = (remainingSeconds % 3600) / 60;
            status = $"Next adventure in: {hours}h {minutes}m";
        }
        else
        {
            status = "Adventure ready!";
        }
        
        CPH.SendMessage($"@{userName}'s Adventures 🗡️ | Total: {totalAdventures} | {status}");
        
        return true;
    }
}
```

4. Create command `!adventurestats` that triggers this action

---

### Step 4: Update Inventory Command (Optional)

If you want to include adventure status in the `!eggpack` command, add this to your existing inventory action:

```csharp
// Add after token display code
long lastPlayed = CPH.GetGlobalVar<long>($"{userId}_adventureLastPlayed", true);
long currentTime = DateTimeOffset.UtcNow.ToUnixTimeSeconds();
string adventureStatus = (lastPlayed > 0 && (currentTime - lastPlayed) < 86400) ? "Used" : "Ready";
```

Then modify the message to include:
```csharp
CPH.SendMessage($"@{userName}'s Egg Pack 🎒 | {pouchEggs} 🥚 | {mysteryEggs} Mystery 🔮 | {diceEggs} Dice 🎲 | {duelEggs} Duel ⚔️ | Adventure: {adventureStatus} 🗡️");
```

---

## Variable Reference

### DnD Adventure Variables

| Variable Name | Type | Description | Persistence |
|--------------|------|-------------|-------------|
| `{userId}_adventureLastPlayed` | long | Unix timestamp of last adventure | Persistent |
| `{userId}_totalAdventures` | int | Total adventures completed | Persistent |

### Usage Examples

**Check if user can play:**
```csharp
long lastPlayed = CPH.GetGlobalVar<long>($"{userId}_adventureLastPlayed", true);
long currentTime = DateTimeOffset.UtcNow.ToUnixTimeSeconds();
bool canPlay = (currentTime - lastPlayed) >= 86400;
```

**Get total adventures:**
```csharp
int total = CPH.GetGlobalVar<int>($"{userId}_totalAdventures", true);
```

---

## Customization Options

### Adjust Entry Cost

To change the 500 egg entry cost, modify this line:
```csharp
int adventureCost = 500; // Change to any value
```

### Adjust Cooldown Duration

To change from 24 hours to another duration:
```csharp
long cooldownSeconds = 86400; // 24 hours
// Examples:
// 12 hours = 43200
// 6 hours = 21600
// 1 hour = 3600
```

### Adjust Reward Values

Modify the reward ranges in the main code:

```csharp
// Critical Failure
eggReward = -rnd.Next(200, 301); // Change range

// Failure
eggReward = -rnd.Next(50, 101); // Change range

// Partial Success
eggReward = rnd.Next(100, 301); // Change range

// Success
eggReward = rnd.Next(400, 601); // Change range

// Great Success
eggReward = rnd.Next(700, 901); // Change range

// Critical Success
eggReward = rnd.Next(1000, 1501); // Change range
```

### Add Custom Scenarios

To add more scenarios to any saving throw type, modify the scenario arrays:

```csharp
private string GetStrengthScenario(int roll, Random rnd)
{
    string[] scenarios = {
        "A massive boulder blocks your path!",
        "You must lift a portcullis to escape!",
        "Your custom scenario here!", // Add more
        "Another custom scenario!" // Add more
    };
    // ... rest of code
}
```

### Token Reward Probabilities

Adjust token reward chances:

```csharp
// Success tier (11-15) - currently 50% chance
if (rnd.Next(1, 3) == 1) // Change to rnd.Next(1, 4) for 33%, etc.
{
    tokenReward = 1;
}

// Great Success tier (16-19) - currently 100%
tokenReward = 1; // Always 1 token

// Critical Success tier (20) - currently 100%
tokenReward = 2; // Change to 3 for 3 tokens, etc.
```

### Add More Saving Throw Types

You can add custom saving throw types:

```csharp
string[] savingThrows = { "STR", "DEX", "CON", "INT", "WIS", "CHA", "DEATH", "LUCK", "SPEED" };
```

Then add corresponding scenario methods:
```csharp
case "LUCK":
    return GetLuckScenario(roll, rnd);
```

---

## Testing & Troubleshooting

### Testing Checklist

Before going live, test these scenarios:

- [ ] **First Time Play:** New user can start adventure
- [ ] **Insufficient Eggs:** User with <500 eggs gets proper error
- [ ] **Cooldown Active:** User trying to play twice gets cooldown message
- [ ] **Cooldown Expired:** User can play again after 24 hours
- [ ] **All Roll Values:** Test rolls 1, 5, 10, 15, 19, 20
- [ ] **Egg Deduction:** Entry cost properly deducted
- [ ] **Egg Rewards:** Positive rewards properly added
- [ ] **Egg Penalties:** Negative outcomes properly deducted
- [ ] **Token Rewards:** Tokens properly added to inventory
- [ ] **Stats Tracking:** Total adventures increments correctly
- [ ] **Message Length:** All messages under 500 characters

### Common Issues

**Issue: "Adventure ready!" but cooldown not expired**

Solution: Check that timestamps are in seconds, not milliseconds:
```csharp
long currentTime = DateTimeOffset.UtcNow.ToUnixTimeSeconds(); // Correct
// NOT: DateTimeOffset.UtcNow.ToUnixTimeMilliseconds();
```

**Issue: Same scenario every time**

Solution: Ensure Random is properly seeded. The code uses `new Random()` which should be sufficient, but for better randomization:
```csharp
Random rnd = new Random(Guid.NewGuid().GetHashCode());
```

**Issue: Negative egg balances**

Solution: Add a check before removing eggs:
```csharp
if (eggReward < 0)
{
    int currentEggs = CPH.GetPoints(userId);
    int toRemove = Math.Min(Math.Abs(eggReward), currentEggs);
    CPH.RemovePoints(userId, toRemove, "DnD Adventure Loss");
}
```

**Issue: Code won't compile**

Solution: Check for these common issues:
- Missing `using System;` at the top
- Curly braces `{}` not matched properly
- Semicolons `;` missing at end of statements
- Copy/paste didn't capture all code

**Issue: Message too long for Twitch**

Solution: All scenarios are designed under 500 chars, but if customized:
```csharp
string message = $"🎲 @{userName} | {saveType} Save (Roll: {roll}) | {scenario}";
if (message.Length > 500)
{
    message = message.Substring(0, 497) + "...";
}
CPH.SendMessage(message);
```

### Testing Commands

**Force reset cooldown for testing:**

Create a mod-only command `!resetadventure` with this code:
```csharp
string targetUser = args["rawInput"].ToString().Trim();
if (string.IsNullOrEmpty(targetUser))
{
    CPH.SendMessage("Usage: !resetadventure <username>");
    return false;
}

// Note: You'd need to get the userId from username
// For testing, use your own: !resetadventure
string userId = args["userId"].ToString();
CPH.SetGlobalVar($"{userId}_adventureLastPlayed", 0L, true);
CPH.SendMessage($"Adventure cooldown reset for @{userName}");
```

---

## Integration with Events

### Double Rewards Event

To make adventures respect the Double Rewards multiplier:

```csharp
// After calculating eggReward, add:
double multiplier = CPH.GetGlobalVar<double>("rewardMultiplier", true);
if (multiplier == 0) multiplier = 1.0;

if (eggReward > 0) // Only apply to positive rewards
{
    eggReward = (int)(eggReward * multiplier);
}
```

### Free Entry Event

To make adventures free during Free Entry events:

```csharp
// Replace the cost check with:
bool freeEntry = CPH.GetGlobalVar<bool>("freeEntryTokensActive", true);
int adventureCost = freeEntry ? 0 : 500;

if (currentEggs < adventureCost)
{
    CPH.SendMessage($"@{userName}, you need {adventureCost} 🥚 for an adventure! You have {currentEggs} 🥚.");
    return false;
}

if (adventureCost > 0)
{
    CPH.RemovePoints(userId, adventureCost, "DnD Adventure Entry");
}
```

---

## Advanced Features

### Difficulty Levels

Add difficulty tiers that affect rewards:

```csharp
// After getting userName, add:
string difficulty = "Normal"; // Could be from user choice
int difficultyMultiplier = 1;

switch (difficulty)
{
    case "Easy":
        difficultyMultiplier = 1;
        adventureCost = 300;
        break;
    case "Normal":
        difficultyMultiplier = 1;
        adventureCost = 500;
        break;
    case "Hard":
        difficultyMultiplier = 2;
        adventureCost = 750;
        break;
}

// Later, multiply rewards:
eggReward = eggReward * difficultyMultiplier;
```

### Adventure Streaks

Track consecutive successful adventures:

```csharp
// After determining outcome, add:
if (eggReward > 0)
{
    int streak = CPH.GetGlobalVar<int>($"{userId}_adventureStreak", true);
    streak++;
    CPH.SetGlobalVar($"{userId}_adventureStreak", streak, true);
    
    if (streak >= 5)
    {
        int bonus = 100 * streak;
        eggReward += bonus;
        scenario += $" +{bonus} streak bonus!";
    }
}
else
{
    CPH.SetGlobalVar($"{userId}_adventureStreak", 0, true);
}
```

### Character Classes

Let users choose classes that affect saving throw bonuses:

```csharp
// Get user's class (stored separately)
string userClass = CPH.GetGlobalVar<string>($"{userId}_adventureClass", true);

// Apply bonus to relevant saves
if ((userClass == "Fighter" && saveType == "STR") ||
    (userClass == "Rogue" && saveType == "DEX") ||
    (userClass == "Wizard" && saveType == "INT"))
{
    roll += 2; // Class bonus
    if (roll > 20) roll = 20; // Cap at 20
}
```

---

## Economy Balance

### Expected Value Analysis

With default settings:

- **Entry Cost:** 500 eggs
- **Expected Return:** ~450 eggs average (slightly negative for balance)
- **Token Value:** Mystery (20), Dice (10), Duel (5) = ~12 eggs average
- **Total Expected Value:** ~462 eggs
- **House Edge:** ~38 eggs (7.6%)

This creates a small currency sink while providing exciting gameplay.

### Adjusting Balance

**Make more profitable:**
```csharp
// Increase success rewards
eggReward = rnd.Next(500, 701); // Was 400-600

// Increase token rates
tokenReward = 1; // Always give tokens on success
```

**Make less profitable (stronger sink):**
```csharp
// Decrease all rewards by 20%
eggReward = (int)(eggReward * 0.8);

// Reduce token rewards
if (roll <= 15) tokenReward = 0; // No tokens until great success
```

---

## Command Summary

| Command | Purpose | Cost | Cooldown |
|---------|---------|------|----------|
| `!adventure` | Start daily adventure | 500 🥚 | 24 hours |
| `!adventurestats` | View adventure statistics | Free | None |

---

## Additional Resources

- **[Unified Eggonomy Guide](Unified_Yoshi_Eggonomy.md)** - Core economy system
- **[Event System Guide](Event_System_Guide.md)** - Double Rewards integration
- **[Advanced Features Guide](Advanced_Features_Guide.md)** - More game ideas
- **[Variable Reference](Variable_Reference.md)** - All system variables
- **[Troubleshooting Guide](Troubleshooting_Guide.md)** - Common issues

---

## Conclusion

The DnD Adventure game adds an engaging daily ritual to your stream that combines luck, storytelling, and risk/reward decisions. The once-per-day limit creates anticipation, while the randomized scenarios keep the experience fresh.

**Key Benefits:**
- ✅ Daily viewer engagement
- ✅ Small currency sink for economy health
- ✅ Exciting storytelling moments
- ✅ Token distribution system
- ✅ Easy to customize and expand

**Next Steps:**
1. Implement the core adventure system
2. Test thoroughly with multiple users
3. Customize scenarios to match your stream theme
4. Monitor economy impact over first week
5. Adjust rewards based on community feedback

Enjoy bringing D&D-style adventures to your stream! 🎲🗡️🥚
