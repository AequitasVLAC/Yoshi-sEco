# Yoshi's Island Eggonomy - Streamer.bot Module Files

## 📦 What Are These .sb Files?

These `.sb` (Streamer.bot) files are **modular components** for building a complete egg-based economy system in Streamer.bot. Each file represents a self-contained system that can be imported and configured independently.

## 🎯 Quick Start

### Option 1: Complete System (Recommended)
Import the all-in-one file for instant setup:
- **File**: `Yoshi_Eggonomy_Complete.sb`
- **Contains**: All modules integrated
- **Setup Time**: 15-30 minutes

### Option 2: Modular Installation
Import individual modules for customization:
- Start with `CurrencySetup.sb` (required)
- Add `TokenSystem.sb` (required)
- Choose games, PvP, adventures, shop, and leaderboard modules as needed
- **Setup Time**: 30-60 minutes

## 📂 Module Files

### Core Modules (Required)

#### `CurrencySetup.sb`
**Main currency system for Pouch Eggs**
- ✅ Initialize economy funds (bigNestFund, eggCartonJackpot)
- ✅ Check balance (!eggs)
- ✅ Award eggs for cheers, subs, raids
- ✅ Economy monitoring (!econfunds)

**Commands:**
- `!eggs` - Check balance
- `!econfunds` - View economy funds (Mod only)

---

#### `TokenSystem.sb`
**Token purchase and inventory management**
- ✅ 5 token types: Mystery, Dice, Duel, RRToken, D20Token
- ✅ Purchase tokens with Pouch Eggs
- ✅ View complete inventory
- ✅ Economic distribution (70% bigNest, 20% jackpot, 10% sink)

**Commands:**
- `!buy <token> <qty>` - Purchase tokens
- `!eggpack` - View inventory

**Token Costs:**
- Mystery Egg: 20🥚 (for Chomp Tunnel)
- Dice Egg: 10🥚 (for Hatch Roll)
- Duel Egg: 5🥚 (for PvP)
- RRToken: 50🥚 (roulette protection)
- D20Token: 100🥚 (daily adventure)

---

### Game Modules

#### `Games.sb`
**Four interactive games with varied mechanics**

**Roll20 Game** (`!roll20`)
- Entry: 10 Pouch Eggs
- Rewards: Up to 2,000 eggs on Nat 20
- Mechanics: D20 roll with tiered payouts

**Roulette Game** (`!roulette`)
- Entry: 10 Pouch Eggs
- Protection: Use RRToken to prevent losses
- Mechanics: 6-sided spin with risk/reward

**Chomp Tunnel** (`!chomp`)
- Entry: 1 Mystery Egg
- Rewards: Streak multipliers + Golden Egg bonus
- Mechanics: Risk vs reward with Chain Chomp

**Hatch Roll** (`!eggroll`)
- Entry: 1 Dice Egg
- Rewards: D20-based tiered payouts
- Mechanics: Luck-based hatching game

---

#### `PvPMechanics.sb`
**Player vs Player combat systems**

**Auto-Battle PvP** (`!pvp`)
- Instant automatic combat (no acceptance)
- 10-minute cooldown for challenger
- D&D-style narrative summaries
- Token stealing (20% chance)
- Winner gets wager + 50% of opponent's

**Duel Nest** (`!duelnest` + `!accept`)
- Traditional challenge/accept system
- 2-minute acceptance window
- Auto-resolves after 10 minutes
- Winner gets 85% of pot, 15% to economy

**Requirements:**
- Setup Duel Resolver Timer (60 sec interval, repeat enabled)

---

#### `Adventures.sb`
**Daily D&D-style adventure system**

**Daily Adventure** (`!adventure`)
- Requires: 1 D20Token
- Cooldown: 24 hours per user
- Saving Throws: STR, DEX, CON, INT, WIS, CHA, DEATH
- Randomized scenarios
- Rewards: 200-1,500 eggs + tokens on success
- Penalties: Up to 250 egg loss on critical failure

**Commands:**
- `!adventure` - Start adventure
- `!adventuretime` - Check cooldown
- `!adventurestats` - View stats

---

#### `Shop.sb`
**Virtual shop for items and rewards**

**Shop Catalog:**
1. Mega Token Pack (150🥚) - 5 of each token type
2. Lucky Charm (500🥚) - Luck buff for next game
3. Egg Doubler (750🥚) - Doubles next game reward
4. Golden Egg (1000🥚) - Collectible item
5. Shoutout (2000🥚) - Stream shoutout
6. Custom Emote (5000🥚) - Emote request

**Commands:**
- `!shop` - Browse catalog
- `!shopbuy <item>` - Purchase item
- `!myitems` - View purchased items
- `!shopadd <id> <cost> <name>` - (Mod) Add custom item

**Economic Impact:**
- 50% of purchases go to bigNestFund

---

#### `Leaderboard.sb`
**Rankings and progression system**

**Rank Tiers:**
- 🥚 Hatchling (0-99)
- 🏃 Egg Runner (100-499)
- 🏠 Nest Builder (500-999)
- 🛡️ Egg Guardian (1k-2.5k)
- ⚔️ Yoshi Knight (2.5k-5k)
- 👑 Grand Yoshi (5k-10k)
- 🌟 Egg Emperor (10k+)

**Commands:**
- `!top` - Top 5 earners
- `!titles` - Your rank and progress
- `!sheet` - All statistics
- `!ranks` - View all tiers
- `!pvptop` - Top PvP champions
- `!adventuretop` - Top adventurers
- `!reroll` - Reset character (1000🥚)

---

## 🚀 Installation Guide

### Step 1: Prepare Streamer.bot
1. Open Streamer.bot v0.2.0+
2. Connect to your Twitch account
3. Enable Loyalty Points (Settings → Loyalty)

### Step 2: Configure Loyalty System
1. Go to Settings → Loyalty → Points Settings
2. Set currency name: **Pouch Egg** / **Pouch Eggs**
3. Set icon: **🥚**
4. Set default command: **!eggs**
5. Configure passive income:
   - Online Viewers: 5 eggs per 10 minutes
   - Active Chatters: 10 eggs per 10 minutes
   - Subscribers: +5 eggs bonus
6. Save changes

### Step 3: Import Modules

**Option A: Complete System**
1. In Streamer.bot: Actions → Import
2. Select `Yoshi_Eggonomy_Complete.sb`
3. Import all actions
4. Skip to Step 4

**Option B: Individual Modules**
1. Import `CurrencySetup.sb`
2. Import `TokenSystem.sb`
3. Import desired game/feature modules
4. Each import adds actions to your Actions list

### Step 4: Initialize Economy
1. Go to Actions tab
2. Find "Initialize Currency System" action
3. Right-click → Test Trigger (runs once)
4. Verify global variables created:
   - bigNestFund = 1000
   - eggCartonJackpot = 500

### Step 5: Create Commands
For each action, create a corresponding command:

**In Commands tab:**
1. Click Add
2. Enter command (e.g., `!eggs`)
3. Link to corresponding action
4. Set permissions (Everyone/Mod/VIP)
5. Set cooldowns:
   - Info commands: 10-15 seconds
   - Games: 10-30 seconds
   - PvP: 30-60 seconds
   - Mod commands: 5 seconds

### Step 6: Setup Timers (Critical for PvP)
1. Go to Actions tab
2. Find "Duel Resolver Timer" action
3. Right-click → Add Timed Action
4. Set interval: 60 seconds
5. Enable "Repeat"
6. Save and enable timer

### Step 7: Test Everything
Run test commands in order:
1. `!eggs` - Check balance works
2. `!buy MysteryEgg 1` - Purchase token
3. `!eggpack` - View inventory
4. `!chomp` - Test game
5. `!titles` - Check rank system
6. `!shop` - View shop
7. Create test duel with alt account

### Step 8: Announce and Go Live
1. Post announcement in Discord/social
2. Explain basic commands
3. Monitor first hour for issues
4. Use `!econfunds` to track economy

---

## 🔧 Customization

### Adjust Costs
Edit token costs in `TokenSystem.sb`:
```csharp
{"MysteryEgg", 20},  // Change 20 to desired cost
{"DiceEgg", 10},
{"DuelEgg", 5}
```

### Adjust Game Rewards
Edit payout values in `Games.sb`:
```csharp
if (roll == 20)
{
    payout = 2000;  // Change to desired jackpot
}
```

### Add Shop Items
Use moderator command:
```
!shopadd customItem 500 My Custom Item
```

Or edit `Shop.sb` catalog directly.

### Modify Rank Tiers
Edit rank thresholds in `Leaderboard.sb`:
```csharp
if (pouchEggs < 100) { rank = "Hatchling"; }
// Add more tiers or change values
```

---

## 📊 Economic Balance

### Currency Flow
**Income Sources:**
- Passive viewing: 5-10🥚 per 10 min
- Cheers: 1🥚 per bit
- Subs: 100-500🥚
- Raids: 50🥚
- Game winnings: 5-2000🥚

**Currency Sinks:**
- Token purchases: 10% removed
- Shop purchases: 50% to fund
- Game entries: Removed or risked
- Character reroll: 1000🥚 removed

### Monitoring
Check economy health with:
- `!econfunds` - View fund balances
- If bigNestFund grows too large: Run giveaways
- If inflation occurs: Increase sink percentages

---

## 🆘 Troubleshooting

### Commands Don't Work
- ✅ Verify command is enabled in Commands tab
- ✅ Check action is linked correctly
- ✅ Test action directly in Actions tab
- ✅ Check Streamer.bot is connected to Twitch

### Duels Don't Resolve
- ✅ Verify Duel Resolver Timer is created
- ✅ Check timer is enabled and repeating
- ✅ Test timer manually (right-click → Test)

### Tokens Not Showing
- ✅ Check global variables exist (Settings → Variables)
- ✅ Verify user ID format (not username)
- ✅ Ensure `persisted: true` in all SetGlobalVar calls

### Balance Issues
- ✅ Check loyalty points are enabled
- ✅ Verify CPH.GetPoints() returns correct values
- ✅ Test with streamer account first

### Code Won't Compile
- ✅ Ensure `using System;` is at top
- ✅ Check all braces {} are balanced
- ✅ Verify no smart quotes (" ") used
- ✅ Class name must be `CPHInline`

---

## 📚 Additional Resources

### Documentation
- **Quick Start Guide**: docs/Quick_Start_Guide.md
- **Unified Guide**: docs/Unified_Yoshi_Eggonomy.md
- **Variable Reference**: docs/Variable_Reference.md
- **Event System**: docs/Event_System_Guide.md
- **Advanced Features**: docs/Advanced_Features_Guide.md
- **Troubleshooting**: docs/Troubleshooting_Guide.md

### Community
- Streamer.bot Discord
- Repository Issues
- Documentation Index: docs/Documentation_Index.md

---

## ✨ Features Summary

✅ **Currency System**: Passive income + Twitch event rewards  
✅ **5 Token Types**: Mystery, Dice, Duel, RR, D20  
✅ **4 Games**: Roll20, Roulette, Chomp, Hatch Roll  
✅ **PvP System**: Auto-battle + traditional duels  
✅ **Daily Adventures**: D&D-style with 7 save types  
✅ **Shop System**: 6+ items with mod customization  
✅ **7 Rank Tiers**: Hatchling → Egg Emperor  
✅ **Economic Balance**: Built-in sinks and funds  
✅ **100% Streamer.bot**: No external dependencies  

---

## 🎉 Ready to Launch!

Your Yoshi's Island Eggonomy system is ready. Follow the installation steps, test thoroughly, and enjoy watching your community engage with the egg-based economy!

**Need help?** Check the Troubleshooting Guide or join the Streamer.bot Discord.

**Happy streaming!** 🥚🎮✨
