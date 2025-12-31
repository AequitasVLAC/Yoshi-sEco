# Manual Testing Guide for Fixed Import Files

This guide provides step-by-step instructions for manually testing the fixed Streamer.bot export files.

## Prerequisites

- Windows PC
- Streamer.bot v1.0.1 installed (or v0.2.0+)
- Twitch account connected to Streamer.bot
- Loyalty system enabled in Streamer.bot

---

## Test 1: Import Validation

### Step 1.1: Import JSON File

1. Download `Yoshi_Eggonomy_Complete_v1.0.1_FINAL.json`
2. Open Streamer.bot
3. Go to **Actions** tab
4. Right-click in actions area → **Import**
5. Select the downloaded JSON file
6. Click **Import**

**Expected Result:**
- ✅ Import dialog shows list of actions, commands, and timed actions
- ✅ No error messages appear
- ✅ All 13 actions are listed
- ✅ All 12 commands are listed
- ✅ 1 timed action is listed

### Step 1.2: Verify Actions Imported

After import:

1. Check **Actions** tab
2. Verify these 13 actions exist:
   - [ECON] Buy Token
   - [GAME] Chomp Tunnel
   - [GAME] Hatch Roll
   - [GAME] DnD Adventure
   - [PVP] Duel Challenge
   - [PVP] Duel Accept
   - [PVP] Duel Resolver
   - [USER] View Titles
   - [USER] View Inventory
   - [USER] View Character Sheet
   - [USER] Reset Character
   - [USER] Top Leaderboard
   - [MOD] Check Economy Funds

**Expected Result:**
- ✅ All 13 actions present
- ✅ All actions enabled by default
- ✅ Actions show in appropriate groups

### Step 1.3: Verify Commands Imported

1. Go to **Commands** tab
2. Verify these 12 commands exist:
   - !buy
   - !chomp
   - !eggroll
   - !adventure
   - !duelnest
   - !accept
   - !top
   - !titles
   - !eggpack
   - !sheet
   - !reroll
   - !econfunds

**Expected Result:**
- ✅ All 12 commands present
- ✅ All commands enabled by default
- ✅ Commands show correct action references

### Step 1.4: Verify C# Code

1. Double-click on **[ECON] Buy Token** action
2. Check the subaction (should be "Execute Code (C#)")
3. Click on the subaction to view code

**Expected Result:**
- ✅ C# code editor opens
- ✅ Code is present and properly formatted
- ✅ Code includes `using System;` statements
- ✅ Code includes `public class CPHInline` with `public bool Execute()` method
- ✅ No syntax errors highlighted

---

## Test 2: Post-Import Configuration

### Step 2.1: Configure Loyalty Currency

1. Go to **Settings** → **Loyalty** → **Points Settings**
2. Enable Loyalty Points
3. Set Currency Name:
   - Singular: `🥚 Pouch Egg`
   - Plural: `🥚 Pouch Eggs`
   - Default Command: `!eggs`
4. Set Passive Income:
   - Online Viewers: 5 per 10 minutes
   - Active Chatters: 10 per 10 minutes
5. Click **Save**

**Expected Result:**
- ✅ Settings save without errors
- ✅ Loyalty system shows as enabled
- ✅ Currency name displays correctly

### Step 2.2: Verify Timed Action

1. Go to **Actions** tab
2. Look for **Duel Resolver** action with clock icon
3. Right-click → **Edit**

**Expected Result:**
- ✅ Timed action exists
- ✅ Enabled checkbox is checked
- ✅ Interval is 60 seconds
- ✅ Repeat is enabled

---

## Test 3: Functional Testing

### Test 3.1: Basic Currency Check

In Twitch chat (or Streamer.bot test):

```
!eggs
```

**Expected Result:**
- ✅ Bot responds with your current Pouch Egg balance
- ✅ Message format: "You have X 🥚 Pouch Eggs"

### Test 3.2: Token Purchase

```
!buy MysteryEgg 1
```

**Expected Result:**
- ✅ Bot responds confirming purchase
- ✅ Your balance decreases by 20 eggs
- ✅ Bot shows you now have 1 Mystery Egg

### Test 3.3: Check Inventory

```
!eggpack
```

**Expected Result:**
- ✅ Bot shows your Pouch Eggs balance
- ✅ Bot shows your token counts (Mystery Eggs, Dice Eggs, Duel Eggs)
- ✅ Message is under 500 characters

### Test 3.4: Play Chomp Tunnel Game

```
!chomp
```

**Expected Result:**
- ✅ Bot responds with game result
- ✅ If you don't have Mystery Eggs, bot tells you to buy one
- ✅ If you have Mystery Eggs, game plays and shows result
- ✅ Result shows roll, outcome, and egg reward

### Test 3.5: View Rank Titles

```
!titles
```

**Expected Result:**
- ✅ Bot shows all 7 rank tiers
- ✅ Shows egg requirements for each rank
- ✅ Shows your current rank highlighted

### Test 3.6: Moderator Command

As a moderator:

```
!econfunds
```

**Expected Result:**
- ✅ Bot shows bigNestFund balance
- ✅ Bot shows eggCartonJackpot balance
- ✅ Message is formatted correctly

### Test 3.7: Play Hatch Roll Game

First buy a Dice Egg:
```
!buy DiceEgg 1
```

Then play:
```
!eggroll
```

**Expected Result:**
- ✅ Bot rolls D20 (1-20)
- ✅ Bot shows tiered reward based on roll
- ✅ Eggs are awarded correctly

### Test 3.8: View Leaderboard

```
!top
```

**Expected Result:**
- ✅ Bot shows top egg holders
- ✅ Shows rankings with egg counts
- ✅ Message is properly formatted

### Test 3.9: DnD Adventure (Once Per 24 Hours)

```
!adventure
```

**Expected Result:**
- ✅ If first time or after 24h: Game plays
- ✅ Shows saving throw type (STR, DEX, CON, INT, WIS, CHA, or DEATH)
- ✅ Shows D20 roll result
- ✅ Shows scenario and outcome
- ✅ Awards eggs and possibly tokens
- ✅ If within 24h: Bot tells you cooldown remaining

---

## Test 4: Edge Cases

### Test 4.1: Insufficient Funds

Try to buy without enough eggs:
```
!buy MysteryEgg 10
```

(If you don't have 200 eggs)

**Expected Result:**
- ✅ Bot tells you insufficient funds
- ✅ No transaction occurs

### Test 4.2: Invalid Command Arguments

```
!buy InvalidToken 1
```

**Expected Result:**
- ✅ Bot tells you invalid token type
- ✅ Shows valid token types

### Test 4.3: PvP Challenge Flow

User1:
```
!duelnest @User2 50
```

**Expected Result:**
- ✅ Challenge is created
- ✅ User2 is notified
- ✅ 2-minute acceptance window starts

User2:
```
!accept
```

**Expected Result:**
- ✅ Duel is accepted
- ✅ Both players roll
- ✅ Winner is determined
- ✅ Eggs are distributed correctly

---

## Test 5: Persistence Testing

1. Play a few games to accumulate stats
2. Close Streamer.bot completely
3. Reopen Streamer.bot
4. Check your stats with `!sheet`

**Expected Result:**
- ✅ All balances preserved
- ✅ All stats preserved
- ✅ Global variables (funds) preserved
- ✅ No data loss

---

## Test 6: Performance Testing

1. Run commands rapidly (within cooldowns):
   ```
   !eggs
   !eggpack
   !titles
   !sheet
   ```

2. Have multiple users run commands simultaneously

**Expected Result:**
- ✅ All commands respond correctly
- ✅ No lag or crashes
- ✅ Variables update correctly
- ✅ No race conditions or data corruption

---

## Test 7: Error Handling

### Test 7.1: C# Code Compilation

1. Open any action with C# code
2. Check Streamer.bot logs (View → Logs)

**Expected Result:**
- ✅ No compilation errors in logs
- ✅ Actions compile successfully on load
- ✅ No red error messages

### Test 7.2: Command Errors

Try various invalid inputs:
```
!buy
!buy MysteryEgg
!buy MysteryEgg abc
!duelnest
!duelnest @User1
```

**Expected Result:**
- ✅ All errors handled gracefully
- ✅ Helpful error messages shown
- ✅ No crashes or exceptions

---

## Test Checklist Summary

Mark each test as completed:

### Import Tests
- [ ] JSON file imports successfully
- [ ] All 13 actions imported
- [ ] All 12 commands imported
- [ ] 1 timed action imported
- [ ] C# code intact and valid

### Configuration Tests
- [ ] Loyalty currency configured
- [ ] Timed action enabled and configured
- [ ] All commands enabled

### Functional Tests
- [ ] !eggs works
- [ ] !buy works
- [ ] !eggpack works
- [ ] !chomp works
- [ ] !eggroll works
- [ ] !adventure works
- [ ] !duelnest works
- [ ] !accept works
- [ ] !top works
- [ ] !titles works
- [ ] !sheet works
- [ ] !reroll works
- [ ] !econfunds works (moderators)

### Edge Case Tests
- [ ] Insufficient funds handled
- [ ] Invalid inputs handled
- [ ] PvP flow works end-to-end

### Persistence Tests
- [ ] Data survives restart
- [ ] Variables persist correctly

### Performance Tests
- [ ] Multiple commands work
- [ ] Concurrent usage works

### Error Handling Tests
- [ ] C# compiles without errors
- [ ] Command errors handled gracefully

---

## If All Tests Pass

**✅ IMPORT SUCCESSFUL!** The Yoshi's Island Eggonomy system is working correctly.

You can now:
1. Customize settings as desired
2. Announce to your community
3. Go live with the economy system!

---

## If Tests Fail

1. Check Streamer.bot logs for errors
2. Verify Streamer.bot version (needs v0.2.0+)
3. Ensure loyalty system is enabled
4. Review IMPORT_GUIDE.md for troubleshooting
5. Check docs/Troubleshooting_Guide.md for common issues

---

**Testing Version:** 1.0 (Fixed)  
**Last Updated:** December 31, 2025  
**Compatible With:** Streamer.bot v1.0.1 (and v0.2.0+)
