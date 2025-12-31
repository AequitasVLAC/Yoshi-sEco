# Yoshi's Island Eggonomy - Export Files

This folder contains the complete, debugged, and production-ready export of the Yoshi's Island Eggonomy system for Streamer.bot v1.0.1.

## 🚀 Quick Start - Which File Do I Use?

### Recommended: Use the FINAL Version

- **File to Import:** `Yoshi_Eggonomy_Complete_v1.0.1_FINAL.json` (36KB)
- **Or Import String:** `Yoshi_Eggonomy_Complete_Import_String_FINAL.txt` (8.5KB)
- **Guide:** Read `IMPORT_GUIDE.md` for complete setup instructions

**Why FINAL?** It includes ALL 13 actions and 12 commands, including:
- DnD Adventure game (daily D20 adventures)
- Top leaderboard command
- All other economy features

---

## 📦 What's in Each File?

### FINAL Version (Complete System - **USE THIS**)

**JSON File:** `Yoshi_Eggonomy_Complete_v1.0.1_FINAL.json`
- **Size:** 36 KB
- **Actions:** 13
- **Commands:** 12
- **Includes:**
  - ✅ Buy Token system
  - ✅ Chomp Tunnel game
  - ✅ Hatch Roll game
  - ✅ **DnD Adventure game** (daily adventures with 7 saving throw types)
  - ✅ Duel Nest PvP (challenge, accept, auto-resolver)
  - ✅ User commands (titles, eggpack, sheet, reroll)
  - ✅ **Top leaderboard**
  - ✅ Economy monitoring (moderator)

**Import String:** `Yoshi_Eggonomy_Complete_Import_String_FINAL.txt`
- **Size:** 8.5 KB (8500 characters)
- **Format:** Base64-encoded gzip compressed JSON
- **Same content as JSON file above**
- **Use if:** You prefer to import via copy/paste

### Original Version (Subset of Features)

**JSON File:** `Yoshi_Eggonomy_Complete_v1.0.1.json`
- **Size:** 26 KB
- **Actions:** 11
- **Commands:** 10
- **Missing:** DnD Adventure, Top command
- **Use if:** You only want the core economy without adventures

**Import String:** `Yoshi_Eggonomy_Complete_Import_String.txt`
- **Size:** 6 KB
- **Same as JSON above, but encoded**

---

## 📖 Documentation

### IMPORT_GUIDE.md
Complete installation guide including:
- Import instructions (file or string method)
- Post-installation setup steps
- Testing checklist
- Command reference
- Troubleshooting guide
- Economy balance tips

### Additional Documentation
See the `docs/` folder for:
- **Unified_Yoshi_Eggonomy.md** - Detailed guide for manual setup
- **DnD_Adventure_Guide.md** - DnD Adventure game deep-dive
- **Variable_Reference.md** - All 175+ variables documented
- **Event_System_Guide.md** - Double Rewards, Free Entry events
- **Advanced_Features_Guide.md** - Custom tokens, achievements
- **Troubleshooting_Guide.md** - 50+ common issues solved

---

## 🎮 What's Included in the System?

### 13 Actions
1. [ECON] Buy Token
2. [GAME] Chomp Tunnel
3. [GAME] Hatch Roll
4. [GAME] DnD Adventure
5. [PVP] Duel Challenge
6. [PVP] Duel Accept
7. [PVP] Duel Resolver (timed)
8. [USER] View Titles
9. [USER] View Inventory
10. [USER] View Character Sheet
11. [USER] Reset Character
12. [USER] Top Leaderboard
13. [MOD] Check Economy Funds

### 12 Commands
1. `!buy <token> <qty>` - Purchase tokens
2. `!chomp` - Play Chomp Tunnel
3. `!eggroll` - Play Hatch Roll
4. `!adventure` - Play DnD Adventure (once per 24 hours)
5. `!duelnest @user <wager>` - Challenge to PvP
6. `!accept` - Accept PvP challenge
7. `!top` - View leaderboard
8. `!titles` - View rank progression
9. `!eggpack` - View inventory
10. `!sheet` - View stats
11. `!reroll` - Reset character
12. `!econfunds` - Check economy funds (mod only)

### Built-in Features
- **Token Economy:** Mystery Eggs (20🥚), Dice Eggs (10🥚), Duel Eggs (5🥚)
- **7 Rank Tiers:** Hatchling → Egg Emperor
- **Currency Sinks:** 10% of purchases, 15% of duels removed
- **Auto-Resolution:** Duels resolve after 10 minutes
- **Daily Cooldown:** DnD Adventure once per 24 hours
- **Stats Tracking:** Streaks, wins, losses, adventures
- **Economy Monitoring:** Moderator tools to track fund health

---

## ⚙️ System Requirements

- **Streamer.bot:** v1.0.1 (also compatible with v0.2.0+)
- **Operating System:** Windows
- **Twitch Account:** Connected to Streamer.bot
- **Loyalty System:** Must be enabled in Streamer.bot

---

## 🔧 Installation Steps (Quick)

1. **Import** the FINAL JSON file into Streamer.bot
2. **Configure** Pouch Eggs currency (Settings → Loyalty)
3. **Set** passive income rates (5/10 eggs per 10 minutes)
4. **Enable** the built-in `!eggs` command
5. **Verify** Duel Resolver Timer is running
6. **Test** with `!buy MysteryEgg 1` then `!chomp`
7. **Go live!**

For detailed steps, see `IMPORT_GUIDE.md`.

---

## 🆘 Need Help?

1. **Read:** `IMPORT_GUIDE.md` - Comprehensive setup and troubleshooting
2. **Check:** `docs/Troubleshooting_Guide.md` - 50+ solutions
3. **Verify:** Streamer.bot logs for error messages
4. **Ask:** Streamer.bot Discord community

---

## 📝 Version Information

- **Export Version:** 1.0.1
- **Created:** December 2025
- **Format:** Streamer.bot v0.2.0+ compatible JSON
- **Encoding:** Base64-encoded gzip compressed JSON (import strings)
- **Platform:** Windows / Streamer.bot

---

## ✨ What's Different from Documentation?

The documentation in `docs/` folder provides **manual setup instructions** where you create each action and command by hand.

These export files provide **one-click installation** - everything is pre-built, debugged, and ready to import.

**Use exports for:** Fast setup, guaranteed working code, easy installation  
**Use documentation for:** Understanding the system, customization, learning

---

## 🎉 Ready to Import!

Choose your method:
1. **File Import:** Use `Yoshi_Eggonomy_Complete_v1.0.1_FINAL.json`
2. **String Import:** Use `Yoshi_Eggonomy_Complete_Import_String_FINAL.txt`

Then follow `IMPORT_GUIDE.md` for setup!

**Happy streaming with your new egg economy!** 🥚🎊
