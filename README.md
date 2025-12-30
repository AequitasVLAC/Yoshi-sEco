# Yoshi's Island Eggonomy

Welcome to the Yoshi's Island Eggonomy repository! This repository contains comprehensive documentation for building an interactive and engaging egg-based economy system using Streamer.bot.

## What's Inside

This repository provides a complete, production-ready guide for implementing an egg-based economy system that includes:

### Core Features
- **Main Currency System:** Pouch Eggs earned passively by viewers
- **Token System:** Mystery Eggs, Dice Eggs, and Duel Eggs for different games
- **Interactive Games:** Chomp Tunnel, Hatch Roll, and Duel Nest PvP
- **Balanced Economy:** Built-in currency sinks to prevent inflation
- **User Commands:** Comprehensive commands for inventory, stats, and gameplay
- **Event System:** Streamer-controlled events like Double Rewards and Free Entry
- **Advanced Features:** Achievements, teams, season pass, and custom tokens

### What Makes This System Special
✨ **100% Streamer.bot Native** - No external scripts, databases, or services  
✨ **175+ Variables Documented** - Complete reference for every variable  
✨ **Detailed Step-by-Step Guides** - Implementation takes 30-120 minutes  
✨ **Event System** - Create hype with Double Rewards and special bonuses  
✨ **Expandable** - Add custom tokens, games, and features easily  
✨ **Production-Tested** - Balanced economy with proven currency sinks  
✨ **Comprehensive Troubleshooting** - Solutions to every common issue

## Documentation

### 📚 Core Guides

#### **[Quick Start Guide](docs/Quick_Start_Guide.md)** ⚡
Get a working economy in 30-45 minutes! Perfect for beginners.
- Core currency setup
- Token purchase system
- One complete game
- Basic user commands

#### **[Unified Eggonomy Guide](docs/Unified_Yoshi_Eggonomy.md)** 📖
Complete implementation guide with all features (1-2 hours).
- Full setup instructions
- All three games
- All user commands
- PvP system with auto-resolution
- Economy monitoring

### 📚 Reference Documentation

#### **[Variable Reference](docs/Variable_Reference.md)** 📊
Complete documentation of all 175+ variables used in the system.
- Global economy variables
- Per-user token variables
- Game statistics variables
- Temporary state variables
- Event and bonus variables
- Variable naming conventions
- Type reference and examples

#### **[Event System Guide](docs/Event_System_Guide.md)** 🎉
Streamer-controlled events and bonus systems.
- Double Rewards Hour
- Free Entry Tokens
- Flexible multiplier system (1.5x, 3x, 5x, etc.)
- Special jackpot events
- Community milestone events
- Scheduled automation (Happy Hour, Weekend Bonus)
- Event management dashboard

#### **[Advanced Features Guide](docs/Advanced_Features_Guide.md)** 🚀
Extend the system with custom features.
- Adding custom token types (step-by-step template)
- Creating new games (3 complete examples)
- Advanced payout systems (progressive jackpots, combos)
- Team-based features
- Achievement system
- Season pass system
- Custom rank tiers
- Integration with Channel Points, Bits, and Subs

#### **[Troubleshooting Guide](docs/Troubleshooting_Guide.md)** 🔧
Solutions to common issues and best practices.
- 50+ common issues with solutions
- Code compilation error reference
- Variable troubleshooting
- Performance optimization
- Economy balance tips
- Testing procedures
- Backup & recovery
- Monitoring & maintenance schedules

## Quick Start

**Never used Streamer.bot before?** Start here:

1. **[Quick Start Guide](docs/Quick_Start_Guide.md)** (30-45 minutes)
   - Get basic economy running fast
   - Test with one game
   - Verify everything works

2. **[Unified Eggonomy Guide](docs/Unified_Yoshi_Eggonomy.md)** (add remaining features)
   - Add more games
   - Set up PvP system
   - Configure all commands

3. **[Event System Guide](docs/Event_System_Guide.md)** (optional)
   - Add Double Rewards events
   - Set up Free Entry mode
   - Create special occasions

4. **[Advanced Features Guide](docs/Advanced_Features_Guide.md)** (optional)
   - Add custom tokens
   - Create unique games
   - Implement achievements

**Already familiar with Streamer.bot?** Jump straight to the [Unified Guide](docs/Unified_Yoshi_Eggonomy.md).
**Already familiar with Streamer.bot?** Jump straight to the [Unified Guide](docs/Unified_Yoshi_Eggonomy.md).

## Implementation Paths

### Path 1: Minimal (30-45 minutes)
Perfect for testing or small streams:
- Follow [Quick Start Guide](docs/Quick_Start_Guide.md)
- Get core currency + tokens + 1 game
- Add more features later as needed

### Path 2: Complete (1-2 hours)
Full-featured economy:
- Follow [Unified Eggonomy Guide](docs/Unified_Yoshi_Eggonomy.md)
- All games, commands, and PvP
- Ready for immediate production use

### Path 3: Enhanced (2-3 hours)
Everything plus events and custom features:
- Complete path + [Event System Guide](docs/Event_System_Guide.md)
- Add [Advanced Features](docs/Advanced_Features_Guide.md) as desired
- Maximum engagement potential

## Key Features

### 💰 Economy System
- **Passive Income** - Viewers earn eggs automatically
- **Three Game Types** - Risk-based, luck-based, and PvP gameplay
- **Token Economy** - Separate tokens for different activities
- **Currency Sinks** - Multiple mechanisms to maintain economic balance
- **Fund Management** - Track economy health with monitoring commands

### 🎮 Games
- **Chomp Tunnel** - Risk/reward with streak multipliers and golden eggs
- **Hatch Roll** - D20 luck-based game with tiered rewards
- **Duel Nest** - PvP battles with auto-resolution after 10 minutes
- **DnD Adventure** - Daily D&D-style adventures with saving throws and randomized scenarios

### 🎉 Events (Optional)
- **Double Rewards** - 2x payouts for limited time
- **Free Entry** - Let players play without tokens
- **Custom Multipliers** - Any value (1.5x, 3x, 5x, etc.)
- **Jackpot Events** - Award accumulated funds
- **Scheduled Events** - Automated Happy Hour, Weekend Bonus

### 🏆 Progression
- **Seven Rank Tiers** - From Hatchling to Egg Emperor
- **Leaderboard System** - Track top egg holders
- **User Stats** - Track streaks, wins, and performance
- **Achievements** - Unlock system with rewards (optional)
- **Season Pass** - XP-based progression (optional)

### 🎨 Customization
- **Custom Tokens** - Add unlimited token types with template
- **Custom Games** - Create unique games for your community
- **Custom Ranks** - Extend to 9+ tiers with special perks
- **Teams** - Team-based competitions and leaderboards
- **Integrations** - Connect with Channel Points, Bits, Subs

## Commands Overview

| Command | Purpose | Cost |
|---------|---------|------|
| `!eggs` | Check Pouch Egg balance | Free |
| `!buy <token> <qty>` | Purchase tokens | Varies by token |
| `!chomp` | Play Chomp Tunnel | 1 Mystery Egg |
| `!eggroll` | Play Hatch Roll | 1 Dice Egg |
| `!duelnest @user <wager>` | Challenge to PvP | 1 Duel Egg + wager |
| `!accept` | Accept a duel challenge | 1 Duel Egg + wager |
| `!adventure` | Daily DnD-style adventure | 500 Pouch Eggs |
| `!top` | View leaderboard | Free |
| `!titles` | View rank progression | Free |
| `!eggpack` | View full inventory (Pouch Eggs + all tokens) | Free |
| `!sheet` | View character stats | Free |
| `!reroll` | Reset character | 1,000 Pouch Eggs |
| `!econfunds` | Check economy funds (Mod only) | Free |
| `!doublerewards` | Toggle 2x event (Mod only) | Free |
| `!freeentry` | Toggle free games (Mod only) | Free |

## Why Streamer.bot?

This economy runs 100% inside Streamer.bot with no external dependencies:

✅ **No External Scripts** - Everything in Streamer.bot actions  
✅ **No Database Setup** - Uses Streamer.bot's built-in SQLite storage  
✅ **No Web Services** - No APIs or external services needed  
✅ **Automatic Persistence** - All data survives restarts  
✅ **Built-in Integration** - Native Twitch chat and loyalty system  
✅ **Easy to Modify** - C# code is straightforward and documented  

## System Requirements

- **Streamer.bot:** v0.2.0 or later
- **Operating System:** Windows (Streamer.bot requirement)
- **Twitch Account:** Connected to Streamer.bot
- **Knowledge Level:** Beginner-friendly (no coding experience required)
- **Time Investment:**
  - Quick Start: 30-45 minutes
  - Full Implementation: 1-2 hours
  - With Advanced Features: 2-3 hours

## What's Included

### Documentation Files
1. **Quick_Start_Guide.md** - 30-minute implementation (14KB)
2. **Unified_Yoshi_Eggonomy.md** - Complete guide with all features (80KB+)
3. **Variable_Reference.md** - All 175+ variables documented (22KB)
4. **Event_System_Guide.md** - Events and bonuses (35KB)
5. **Advanced_Features_Guide.md** - Custom tokens and games (36KB)
6. **DnD_Adventure_Guide.md** - D&D-style daily adventure game (29KB)
7. **Troubleshooting_Guide.md** - Solutions and best practices (23KB)

### Total Content
- **180+ pages** of documentation
- **35+ code examples** ready to copy/paste
- **15+ complete game implementations**
- **180+ variables** fully explained
- **50+ common issues** with solutions
- **20+ customization templates**

## Community & Support

### Before Asking for Help
1. Check the [Troubleshooting Guide](docs/Troubleshooting_Guide.md)
2. Review relevant documentation section
3. Check Streamer.bot logs for errors
4. Test with a fresh backup

### Where to Get Help
- **Streamer.bot Discord** - Active community
- **Repository Issues** - Report bugs or request features
- **Streamer.bot Subreddit** - General discussion
- **Documentation** - Most answers are here!

### Contributing
This is a community-driven project. Feel free to:
- Suggest improvements
- Report issues
- Share your customizations
- Help other users

## License

This project is provided as-is for use with Streamer.bot. Customize and adapt it to fit your community's needs!

## Credits

Created for the Streamer.bot community. Special thanks to all streamers who tested and provided feedback.

---

## Recent Updates

**December 2025 - Major Expansion Release:**
- ✅ Added comprehensive Variable Reference (175+ variables documented)
- ✅ Added Event System Guide (6 event types with full implementation)
- ✅ Added Advanced Features Guide (custom tokens, games, achievements)
- ✅ Added Troubleshooting Guide (50+ issues with solutions)
- ✅ Added Quick Start Guide (30-minute minimal setup)
- ✅ Enhanced main guide with detailed variable explanations
- ✅ Added event integration to all game examples
- ✅ Expanded from 7 to 9+ rank tiers
- ✅ Added team system, achievements, and season pass
- ✅ Included integration guides for Channel Points, Bits, Subs

**What's New:**
- **Event System** - Double Rewards, Free Entry, Custom Multipliers
- **Complete Variable Documentation** - Every variable explained with examples
- **Advanced Customization** - Templates for tokens, games, and features
- **Troubleshooting** - Comprehensive solutions to common issues
- **Quick Start** - Get running in 30 minutes
- **Performance Tips** - Optimization for large communities
- **Economy Balance** - Monitoring and adjustment guidelines

---

## Getting Started Right Now

**Want to start immediately?**

1. Have Streamer.bot installed? ✅
2. Have 30 minutes free? ✅  
3. Go to: **[Quick Start Guide](docs/Quick_Start_Guide.md)** →

**Want to see everything first?**

1. Read: **[Unified Eggonomy Guide](docs/Unified_Yoshi_Eggonomy.md)**
2. Review: **[Variable Reference](docs/Variable_Reference.md)**
3. Explore: **[Event System Guide](docs/Event_System_Guide.md)**
4. Customize: **[Advanced Features Guide](docs/Advanced_Features_Guide.md)**

---

**Ready to build your egg-based economy? Start with the [Quick Start Guide](docs/Quick_Start_Guide.md)!** 🥚🎉
