# Documentation Index - Yoshi's Island Eggonomy

**Platform:** Streamer.bot (v0.2.0+)  
**Version:** 2.0 Enhanced Edition  
**Last Updated:** December 2025

This index helps you navigate the complete documentation for the Yoshi's Island Eggonomy system. Choose your path based on your experience level and time available.

---

## 📋 Quick Navigation

### For New Users
1. Start Here → [Quick Start Guide](#quick-start-guide)
2. Then Read → [Unified Eggonomy Guide](#unified-eggonomy-guide)
3. Reference → [Variable Reference](#variable-reference)

### For Experienced Users
1. Jump To → [Unified Eggonomy Guide](#unified-eggonomy-guide)
2. Enhance With → [Event System Guide](#event-system-guide)
3. Customize → [Advanced Features Guide](#advanced-features-guide)

### For Troubleshooting
1. Check → [Troubleshooting Guide](#troubleshooting-guide)
2. Search → [Variable Reference](#variable-reference)
3. Review → Relevant Implementation Guide

---

## 📚 Documentation Files

### Quick Start Guide
**File:** `Quick_Start_Guide.md` (14.5 KB)  
**Time Required:** 30-45 minutes  
**Difficulty:** ⭐ Beginner

**What You'll Build:**
- Main currency (Pouch Eggs) with passive income
- Token purchase system (3 token types)
- One complete game (Chomp Tunnel)
- Basic user commands (!eggs, !eggpack, !titles)
- Economy monitoring command for moderators

**Start Here If:**
- You're new to Streamer.bot
- You want to test the system quickly
- You have limited time right now
- You want to validate the concept first

**Contains:**
- 5 implementation phases
- Complete code for each feature
- Step-by-step instructions
- Testing checklist
- Troubleshooting quick reference

---

### Unified Eggonomy Guide
**File:** `Unified_Yoshi_Eggonomy.md` (80+ KB)  
**Time Required:** 1-2 hours  
**Difficulty:** ⭐⭐ Intermediate

**What You'll Build:**
- Everything from Quick Start, plus:
- Hatch Roll game (D20 luck-based)
- Duel Nest PvP (auto-resolving battles)
- All user commands (stats, leaderboard, reroll)
- Complete economy monitoring
- Progression rank system (7 tiers)

**Use This If:**
- You want the complete system
- You're implementing for production
- You followed Quick Start and want more
- You need all features documented

**Contains:**
- 6 implementation stages
- Complete C# code for all features
- Detailed variable explanations
- Data persistence documentation
- Currency sink mechanics
- Economy balance formulas

**Key Sections:**
1. Initial Setup (10 min)
2. Token System (15 min)
3. Games Implementation (30-45 min)
4. User Commands (15 min)
5. Economy Monitoring (5 min)
6. Testing & Go-Live (15 min)

---

### Variable Reference
**File:** `Variable_Reference.md` (22 KB)  
**Time Required:** Reference (as needed)  
**Difficulty:** ⭐⭐⭐ Reference

**What's Documented:**
- 175+ variables used in the system
- Global economy variables
- Per-user token variables
- Game statistics variables
- Temporary state variables
- Event and bonus variables

**Use This When:**
- Debugging variable issues
- Creating custom features
- Understanding data flow
- Troubleshooting persistence issues
- Extending the system

**Contains:**
- Complete variable catalog
- Type reference (int, string, bool, long)
- Naming conventions
- Storage details (persistence, defaults)
- Code examples for each variable
- Troubleshooting tips

**Key Sections:**
1. Variable Storage in Streamer.bot
2. Global Economy Variables
3. Per-User Token Variables
4. Per-User Game Statistics
5. Temporary Game State Variables
6. Event and Bonus Variables
7. Variable Management
8. Backup & Recovery

---

### Event System Guide
**File:** `Event_System_Guide.md` (35 KB)  
**Time Required:** 30-60 minutes per feature  
**Difficulty:** ⭐⭐ Intermediate

**What You'll Build:**
- Double Rewards Hour (2x payouts)
- Free Entry Tokens (play without tokens)
- Flexible multiplier system (any value)
- Special jackpot events
- Community milestone tracking
- Scheduled event automation
- Event management dashboard

**Use This If:**
- You want special events for streams
- You need engagement boosts
- You want scheduled bonuses
- You're running special occasions

**Contains:**
- 6 event types fully implemented
- Complete C# code for each
- Auto-expiry timers
- Warning systems
- Streamer control commands
- Event preset system

**Event Types:**
1. Double Rewards Hour
2. Free Entry Tokens
3. Bonus Multiplier System (1.5x to 10x)
4. Special Jackpot Events
5. Community Milestone Events
6. Scheduled Event Automation

---

### Advanced Features Guide
**File:** `Advanced_Features_Guide.md` (36 KB)  
**Time Required:** Variable (30 min to 2 hours per feature)  
**Difficulty:** ⭐⭐⭐ Advanced

**What You'll Build:**
- Custom token types (unlimited)
- New games (3 examples included)
- Advanced payout systems
- Team-based features
- Achievement system
- Season pass progression
- Custom rank tiers
- External integrations

**Use This If:**
- You want unique features
- You're comfortable with C#
- You want to differentiate your stream
- You need advanced customization

**Contains:**
- Token creation template
- 3 complete example games
- Achievement unlock system
- Team competition mechanics
- Season XP progression
- Integration code for Channel Points, Bits, Subs

**Example Games Included:**
1. Lucky Draw (card-based lottery)
2. Egg Hunt (location-based rewards)
3. Boss Battle (community pooling)

**Advanced Systems:**
1. Progressive Jackpots
2. Dynamic Difficulty
3. Combo Systems
4. Pity Prizes
5. Team Leaderboards
6. Achievement Unlocks
7. Season Pass Progression
8. Custom Rank Bonuses

---

### DnD Adventure Guide
**File:** `DnD_Adventure_Guide.md` (29 KB)  
**Time Required:** 30-45 minutes  
**Difficulty:** ⭐⭐ Intermediate

**What You'll Build:**
- Daily DnD-style adventure game
- Seven saving throw types (STR, DEX, CON, INT, WIS, CHA, Death)
- D20 roll system with tiered outcomes
- Randomized scenario generation
- 24-hour cooldown system
- Egg and token reward system
- Adventure statistics tracking

**Use This If:**
- You want daily engagement mechanics
- Your community enjoys RPG elements
- You want storytelling in your economy
- You need once-per-day content

**Contains:**
- Complete implementation guide
- Full C# code for adventure system
- 35+ unique scenarios
- Reward balance formulas
- Event system integration
- Customization options
- Testing procedures

**Key Features:**
1. D20 saving throw mechanics
2. Critical success/failure outcomes
3. Randomized scenario selection
4. Daily cooldown enforcement
5. Token reward distribution
6. Adventure streak tracking
7. Difficulty customization options

---

### Troubleshooting Guide
**File:** `Troubleshooting_Guide.md` (23 KB)  
**Time Required:** Reference (as needed)  
**Difficulty:** ⭐⭐ Reference

**What's Covered:**
- 50+ common issues with solutions
- Code compilation errors
- Variable troubleshooting
- Performance optimization
- Economy balance tips
- Testing procedures
- Backup & recovery
- Monitoring & maintenance

**Use This When:**
- Commands not working
- Code won't compile
- Variables not persisting
- Economy unbalanced
- Performance issues
- Before asking for help

**Contains:**
- Issue symptom descriptions
- Step-by-step solutions
- Quick fix commands
- Diagnostic procedures
- Prevention tips
- Best practices

**Key Sections:**
1. Common Issues & Solutions
2. Variable Troubleshooting
3. Code Compilation Errors
4. Performance Optimization
5. Economy Balance Tips
6. Testing Procedures
7. Backup & Recovery
8. Monitoring & Maintenance

---

## 🎯 Implementation Paths

### Path 1: Minimal Setup (30-45 minutes)
**Goal:** Get basic economy running for testing

1. Follow [Quick Start Guide](Quick_Start_Guide.md) completely
2. Test all features
3. Decide if you want to expand

**You'll Have:**
- Currency system
- Token purchases
- 1 game (Chomp Tunnel)
- Basic commands
- Economy monitoring

**Next Steps:**
- Add more games from Unified Guide
- Or go live with just this!

---

### Path 2: Complete Implementation (1-2 hours)
**Goal:** Full-featured production economy

1. Skip Quick Start, go to [Unified Eggonomy Guide](Unified_Yoshi_Eggonomy.md)
2. Follow all 6 stages sequentially
3. Complete testing checklist
4. Go live!

**You'll Have:**
- Complete currency system
- All 3 token types
- All 3 games
- All user commands
- Full economy monitoring
- PvP system
- Rank progression

**Next Steps:**
- Monitor economy weekly
- Add events as desired
- Customize as needed

---

### Path 3: Enhanced Experience (2-3 hours)
**Goal:** Maximum engagement with events and custom features

1. Complete Path 2 (Unified Guide)
2. Add events from [Event System Guide](Event_System_Guide.md)
3. Pick features from [Advanced Features Guide](Advanced_Features_Guide.md)

**You'll Have:**
- Everything from Path 2
- Double Rewards events
- Free Entry mode
- Custom multipliers
- Special events
- Optional: Achievements, Teams, Season Pass, Custom Tokens

**Next Steps:**
- Run weekly events
- Track community milestones
- Create unique features
- Integrate with other systems

---

### Path 4: Custom Development (Variable time)
**Goal:** Create unique features for your community

1. Understand core system (Unified Guide)
2. Study [Variable Reference](Variable_Reference.md)
3. Use templates from [Advanced Features Guide](Advanced_Features_Guide.md)
4. Create your own tokens, games, and features

**Prerequisites:**
- Comfortable with C#
- Understanding of variable system
- Working core economy

**Resources:**
- Variable Reference for all variables
- Advanced Features for templates
- Troubleshooting for debugging
- Event System for event integration

---

## 📊 Feature Comparison Matrix

| Feature | Quick Start | Unified | Events | Advanced | DnD Adventure |
|---------|------------|---------|--------|----------|---------------|
| **Currency System** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Token Purchases** | ✅ (3 types) | ✅ (3 types) | ✅ (3 types) | ✅ (Unlimited) | ✅ (3 types) |
| **Chomp Tunnel** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Hatch Roll** | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Duel Nest PvP** | ❌ | ✅ | ✅ | ✅ | ✅ |
| **DnD Adventure** | ❌ | ❌ | ❌ | ❌ | ✅ |
| **User Commands** | Basic | Complete | Complete | Complete | Complete |
| **Economy Monitoring** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Rank System** | ✅ (7 tiers) | ✅ (7 tiers) | ✅ (7 tiers) | ✅ (9+ tiers) | ✅ (7 tiers) |
| **Double Rewards** | ❌ | ❌ | ✅ | ✅ | ✅ |
| **Free Entry** | ❌ | ❌ | ✅ | ✅ | ✅ |
| **Custom Multipliers** | ❌ | ❌ | ✅ | ✅ | ✅ |
| **Jackpot Events** | ❌ | ❌ | ✅ | ✅ | ❌ |
| **Scheduled Events** | ❌ | ❌ | ✅ | ✅ | ❌ |
| **Custom Tokens** | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Custom Games** | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Achievements** | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Teams** | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Season Pass** | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Integrations** | ❌ | ❌ | ❌ | ✅ | ❌ |

---

## 🔍 Finding Information

### By Topic

**Currency & Economy:**
- Initial setup → Unified Guide, Stage 1
- Economy balance → Troubleshooting Guide, Economy Balance Tips
- Currency sinks → Unified Guide, Economy Balance
- Fund management → Variable Reference, Global Economy Variables

**Tokens:**
- Base 3 tokens → Unified Guide, Stage 2
- Token variables → Variable Reference, Per-User Token Variables
- Custom tokens → Advanced Features Guide, Adding Custom Token Types
- Token economics → Unified Guide, Token Definitions

**Games:**
- Chomp Tunnel → Quick Start or Unified Guide, Stage 3.1
- Hatch Roll → Unified Guide, Stage 3.2
- Duel Nest → Unified Guide, Stage 3.3
- DnD Adventure → DnD Adventure Guide
- Custom games → Advanced Features Guide, Creating New Games

**Events:**
- Double Rewards → Event System Guide, Double Rewards Hour
- Free Entry → Event System Guide, Free Entry Tokens Event
- Multipliers → Event System Guide, Bonus Multiplier System
- Jackpots → Event System Guide, Special Jackpot Events

**Commands:**
- Basic commands → Quick Start Guide or Unified Guide, Stage 4
- Moderator commands → Unified Guide, Stage 5
- Custom commands → Advanced Features Guide

**Variables:**
- All variables → Variable Reference
- Global variables → Variable Reference, Global Economy Variables
- User variables → Variable Reference, Per-User Variables
- Event variables → Variable Reference, Event and Bonus Variables

**Troubleshooting:**
- Commands not working → Troubleshooting Guide, Common Issues
- Compilation errors → Troubleshooting Guide, Code Compilation Errors
- Variable issues → Troubleshooting Guide, Variable Troubleshooting
- Performance → Troubleshooting Guide, Performance Optimization

---

## 📖 Reading Order by Goal

### Goal: Learn the System
1. README.md (overview)
2. Quick Start Guide (hands-on basics)
3. Unified Eggonomy Guide (complete understanding)
4. Variable Reference (deep dive)
5. Event System Guide (optional features)
6. Advanced Features Guide (customization)

### Goal: Implement Quickly
1. Quick Start Guide (30-45 min)
2. Test everything
3. Expand with Unified Guide as needed

### Goal: Complete Implementation
1. Unified Eggonomy Guide (all stages)
2. Variable Reference (as needed for customization)
3. Troubleshooting Guide (for any issues)

### Goal: Add Events
1. Complete Unified Guide first
2. Event System Guide (pick desired events)
3. Test each event thoroughly

### Goal: Create Custom Features
1. Understand Unified Guide completely
2. Study Variable Reference thoroughly
3. Use Advanced Features Guide templates
4. Reference Troubleshooting for debugging

---

## 💡 Best Practices

### Before Implementation
1. ✅ Read relevant documentation completely
2. ✅ Have Streamer.bot ready and connected
3. ✅ Backup current Streamer.bot configuration
4. ✅ Set aside uninterrupted time
5. ✅ Have test Twitch account ready

### During Implementation
1. ✅ Follow steps in exact order
2. ✅ Test each feature before moving on
3. ✅ Read code comments for understanding
4. ✅ Keep Variable Reference open for lookup
5. ✅ Save and backup after each completed feature

### After Implementation
1. ✅ Complete full testing checklist
2. ✅ Monitor economy for first week
3. ✅ Adjust values as needed
4. ✅ Back up working configuration
5. ✅ Document your customizations

---

## 🆘 Getting Help

### Self-Help Resources (Try These First)
1. [Troubleshooting Guide](Troubleshooting_Guide.md) - 50+ common issues
2. [Variable Reference](Variable_Reference.md) - All variables explained
3. Streamer.bot logs (View → Logs)
4. This documentation (search for keywords)

### Community Help
1. Streamer.bot Discord server
2. Streamer.bot subreddit
3. Repository Issues page
4. Streamer.bot documentation

### When Asking for Help, Include:
- Streamer.bot version number
- Which guide you're following
- What step you're on
- Exact error message
- What you've already tried
- Relevant code snippet
- Screenshots (if UI issue)

---

## 📈 Documentation Statistics

### Total Content
- **6 documentation files**
- **150+ pages** of content
- **30+ complete code examples**
- **10+ game implementations**
- **175+ variables documented**
- **50+ troubleshooting solutions**
- **20+ customization templates**

### File Sizes
- Quick Start: 14.5 KB
- Unified Guide: 80+ KB
- Variable Reference: 22 KB
- Event System: 35 KB
- Advanced Features: 36 KB
- Troubleshooting: 23 KB
- **Total: 210+ KB of documentation**

### Time Estimates
- Quick Start: 30-45 minutes
- Unified Implementation: 1-2 hours
- With Events: 2-3 hours
- With Advanced Features: 3-4 hours
- Custom Development: Variable

---

## 🎯 Success Criteria

### You Have a Working Economy If:
- ✅ Users earn eggs passively
- ✅ Users can buy tokens with !buy
- ✅ Users can play at least one game
- ✅ Users can check inventory
- ✅ You can monitor economy funds
- ✅ All commands respond in chat
- ✅ Variables persist after restart

### You're Ready for Production If:
- ✅ All above criteria met
- ✅ Completed full testing checklist
- ✅ All games working correctly
- ✅ Economy balanced (not inflating)
- ✅ Backup created and tested
- ✅ You understand variable system
- ✅ You can troubleshoot basic issues

---

## 🚀 Quick Links

- **[README](../README.md)** - Project overview and getting started
- **[Quick Start](Quick_Start_Guide.md)** - 30-minute implementation
- **[Unified Guide](Unified_Yoshi_Eggonomy.md)** - Complete implementation
- **[Variables](Variable_Reference.md)** - All variables documented
- **[Events](Event_System_Guide.md)** - Event system implementation
- **[Advanced](Advanced_Features_Guide.md)** - Custom features
- **[Troubleshooting](Troubleshooting_Guide.md)** - Solutions and tips

---

## 📝 Version History

**Version 2.0 - Enhanced Edition (December 2025)**
- Added 5 new documentation files
- Expanded from 1 to 6 comprehensive guides
- Documented 175+ variables completely
- Added event system (6 event types)
- Added advanced features (achievements, teams, season pass)
- Added troubleshooting guide (50+ issues)
- Added quick start guide (30-minute path)
- Enhanced main guide with detailed variable explanations
- Total content increased from ~30 pages to 150+ pages

**Version 1.0 - Initial Release**
- Single unified guide
- Core economy system
- 3 games (Chomp, Hatch Roll, Duel Nest)
- Basic commands
- ~30 pages of documentation

---

**Ready to start? Choose your path:**
- **New User?** → [Quick Start Guide](Quick_Start_Guide.md)
- **Want Everything?** → [Unified Eggonomy Guide](Unified_Yoshi_Eggonomy.md)
- **Need Help?** → [Troubleshooting Guide](Troubleshooting_Guide.md)

**Happy building!** 🥚🎉
