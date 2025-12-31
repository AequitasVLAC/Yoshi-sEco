# Streamer.bot Import Testing Guide
## Yoshi's Island Eggonomy - Manual Verification Procedures

**Version:** 1.0  
**Date:** December 31, 2025  
**Target:** Streamer.bot v1.0.1

---

## Overview

This guide provides step-by-step procedures to manually test and verify that the Yoshi's Island Eggonomy export files work correctly in Streamer.bot v1.0.1.

---

## Prerequisites

Before testing, ensure you have:

- ✅ **Streamer.bot v1.0.1** (or v0.2.0+) installed
- ✅ **Windows OS** (Streamer.bot requirement)
- ✅ **Twitch account** connected to Streamer.bot
- ✅ **Loyalty system enabled** in Streamer.bot
- ✅ **Test user account** or willingness to test with main account

---

## Test Procedure Overview

1. Pre-Import Checks
2. Import Test (JSON File Method)
3. Import Test (String Method)
4. Post-Import Verification
5. Basic Functionality Tests
6. Advanced Functionality Tests
7. Edge Case Testing

---

## 1. Pre-Import Checks

### Step 1.1: Verify Streamer.bot Version
1. Open Streamer.bot
2. Go to **Help** → **About**
3. Verify version is **v1.0.1** or later
4. ✅ If correct version, proceed
5. ❌ If older version, update Streamer.bot first

### Step 1.2: Enable Loyalty System
1. Go to **Settings** → **Loyalty**
2. Check **"Enable Loyalty"** checkbox
3. Click **Save**
4. ✅ Loyalty system is now enabled

### Step 1.3: Backup Existing Configuration (Recommended)
1. Go to **Actions** tab
2. Right-click in actions list
3. Select **Export**
4. Save backup file to safe location
5. ✅ You can restore if needed

---

## 2. Import Test (JSON File Method)

### Step 2.1: Download JSON File
1. Download `Yoshi_Eggonomy_Complete_v1.0.1_FINAL.json`
2. Save to an accessible location (e.g., Desktop)
3. Verify file size: ~40 KB
4. ✅ File downloaded successfully

### Step 2.2: Import into Streamer.bot
1. Open Streamer.bot v1.0.1
2. Go to **Actions** tab
3. Right-click in the actions list
4. Select **Import**
5. Choose **"Import from file"**
6. Navigate to downloaded JSON file
7. Select the file and click **Open**

### Step 2.3: Verify Import Success
**Expected Results:**
- ✅ No error messages appear
- ✅ Import dialog shows "Import successful" or similar message
- ✅ Actions list updates with new actions

**If Import Fails:**
- ❌ Check error message in Streamer.bot logs
- ❌ Verify file is not corrupted (try re-downloading)
- ❌ Confirm you're using Streamer.bot v1.0.1+
- ❌ Try alternative import method (String Method)

### Step 2.4: Count Imported Items
After successful import, verify:
- ✅ **13 actions** imported (look for [ECON], [GAME], [PVP], [USER], [MOD] prefixes)
- ✅ **12 commands** available in Commands tab
- ✅ **1 timed action** visible (Duel Resolver Timer)

**Action Names to Look For:**
1. [ECON] Buy Token
2. [GAME] Chomp Tunnel
3. [GAME] Hatch Roll
4. [GAME] DnD Adventure
5. [PVP] Duel Challenge
6. [PVP] Duel Accept
7. [PVP] Duel Resolver
8. [USER] View Titles
9. [USER] View Inventory
10. [USER] View Character Sheet
11. [USER] Reset Character
12. [MOD] Check Economy Funds
13. [USER] Top Leaderboard

---

## 3. Import Test (String Method)

### Step 3.1: Copy Import String
1. Open `Yoshi_Eggonomy_Complete_Import_String_FINAL.txt`
2. Select **ALL** text (Ctrl+A or Cmd+A)
3. Copy to clipboard (Ctrl+C or Cmd+C)
4. Verify copied length: ~8,596 characters
5. ✅ String copied successfully

### Step 3.2: Import String into Streamer.bot
1. Open Streamer.bot v1.0.1
2. Go to **Actions** tab
3. Right-click in the actions list
4. Select **Import**
5. Choose **"Import from string"**
6. Paste the string (Ctrl+V or Cmd+V)
7. Click **Import**

### Step 3.3: Verify Import Success
Same verification as Step 2.3 and 2.4 above.

---

## 4. Post-Import Verification

### Step 4.1: Check Actions List
1. Go to **Actions** tab
2. Sort actions alphabetically
3. Verify all 13 actions are present
4. Check each action:
   - ✅ Has a name
   - ✅ Is enabled (green checkmark)
   - ✅ Has group assigned
   - ✅ No error indicators

### Step 4.2: Check Commands Tab
1. Go to **Commands** tab
2. Verify all 12 commands are present:
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

3. For each command, verify:
   - ✅ Is enabled
   - ✅ Has cooldown set
   - ✅ Links to correct action
   - ✅ No error indicators

### Step 4.3: Check Timed Actions
1. Go to **Actions** tab
2. Look for clock icon next to "Duel Resolver"
3. Right-click → Properties
4. Verify settings:
   - ✅ Enabled
   - ✅ Interval: 60 seconds
   - ✅ Repeat: Enabled
   - ✅ Action linked correctly

### Step 4.4: Configure Loyalty Currency
**REQUIRED STEP - System won't work without this!**

1. Go to **Settings** → **Loyalty** → **Points Settings**
2. Set the following:
   - **Currency Name (Singular):** `🥚 Pouch Egg`
   - **Currency Name (Plural):** `🥚 Pouch Eggs`
   - **Default Command:** `!eggs`
   - **Enable Command:** ✅ Checked
3. Set passive income rates:
   - **Online Viewers:** `5` eggs per `10` minutes
   - **Active Chatters:** `10` eggs per `10` minutes
4. Click **Save**
5. ✅ Currency configured

### Step 4.5: Initialize Global Variables
1. Go to **Variables** tab
2. Check for these global variables:
   - `bigNestFund` (should be 1000)
   - `eggCartonJackpot` (should be 500)
3. If missing, create them:
   - Right-click → **Add Variable**
   - Name: `bigNestFund`, Value: `1000`, Persisted: ✅
   - Name: `eggCartonJackpot`, Value: `500`, Persisted: ✅

---

## 5. Basic Functionality Tests

### Test 5.1: Check Currency Balance
**Command:** `!eggs`

**Test Steps:**
1. Connect to Twitch chat
2. Type `!eggs` in chat
3. Observe bot response

**Expected Result:**
```
@YourName, you have X 🥚 Pouch Eggs!
```

**✅ Pass Criteria:**
- Bot responds within 1-2 seconds
- Message shows your username
- Message shows egg count
- Egg emoji displays correctly

**❌ Fail Criteria:**
- No response
- Error message
- Missing egg count
- Incorrect username

---

### Test 5.2: Purchase Tokens
**Command:** `!buy MysteryEgg 1`

**Prerequisites:**
- Have at least 20 eggs (use Settings → Loyalty to add manually if needed)

**Test Steps:**
1. Check current egg balance with `!eggs`
2. Type `!buy MysteryEgg 1` in chat
3. Observe bot response
4. Check egg balance again with `!eggs`

**Expected Result:**
```
@YourName purchased 1 Mystery Egg for 20 🥚! You now have X 🥚 left.
```

**✅ Pass Criteria:**
- Bot responds with purchase confirmation
- Egg balance decreased by 20
- Mystery Egg token added to inventory

**❌ Fail Criteria:**
- No response
- Error message
- Eggs not deducted
- Token not added

---

### Test 5.3: View Inventory
**Command:** `!eggpack`

**Prerequisites:**
- Have at least 1 token (from Test 5.2)

**Test Steps:**
1. Type `!eggpack` in chat
2. Observe bot response

**Expected Result:**
```
@YourName's Eggpack: 🥚 X Pouch Eggs | 🎲 Mystery Eggs: Y | 🎲 Dice Eggs: Z | ⚔️ Duel Eggs: W
```

**✅ Pass Criteria:**
- Bot shows current egg count
- Bot shows token counts
- All categories displayed
- Numbers are correct

---

### Test 5.4: Play a Game (Chomp Tunnel)
**Command:** `!chomp`

**Prerequisites:**
- Have at least 1 Mystery Egg token

**Test Steps:**
1. Type `!chomp` in chat
2. Observe bot response

**Expected Result (Win):**
```
🐊 @YourName chomped through the tunnel! 🎲 Rolled: X. You earned Y 🥚!
```

**Expected Result (Loss):**
```
🐊 @YourName got chomped! 🎲 Rolled: 1. Better luck next time!
```

**✅ Pass Criteria:**
- Bot responds with game result
- Roll number is shown (1-6)
- Eggs awarded on win (10+ eggs)
- Mystery Egg token consumed
- Appropriate emoji used

---

### Test 5.5: View Rank Progression
**Command:** `!titles`

**Test Steps:**
1. Type `!titles` in chat
2. Observe bot response

**Expected Result:**
```
🥚 Rank Titles: Hatchling (0🥚) → Egg Seeker (100🥚) → Egg Keeper (500🥚) → Nest Builder (2000🥚) → Egg Master (10000🥚) → Yoshi Guardian (50000🥚) → Egg Emperor (100000🥚)
```

**✅ Pass Criteria:**
- Bot shows all 7 rank tiers
- Egg requirements shown for each
- Emojis display correctly
- Message fits within character limit

---

## 6. Advanced Functionality Tests

### Test 6.1: PvP Duel Challenge
**Command:** `!duelnest @TargetUser 50`

**Prerequisites:**
- Have at least 1 Duel Egg token
- Have at least 50 eggs for wager
- Have another user to test with (or test on yourself)

**Test Steps:**
1. Type `!duelnest @TargetUser 50` in chat
2. Observe bot response
3. Wait for response from target user

**Expected Result:**
```
@YourName has challenged @TargetUser to a Duel Nest battle! Wager: 50 🥚. @TargetUser, type !accept within 2 minutes!
```

**✅ Pass Criteria:**
- Challenge message sent
- Both users tagged correctly
- Wager amount shown
- Instructions clear

---

### Test 6.2: Accept PvP Duel
**Command:** `!accept`

**Prerequisites:**
- Active duel challenge from Test 6.1
- Target user has 1 Duel Egg token
- Target user has enough eggs for wager

**Test Steps:**
1. As target user, type `!accept` within 2 minutes
2. Observe bot response

**Expected Result:**
```
@TargetUser accepted the duel! ⚔️ Results: @YourName rolled X, @TargetUser rolled Y. @WinnerName wins Z 🥚!
```

**✅ Pass Criteria:**
- Duel executes immediately
- Both rolls shown (1-100)
- Winner determined correctly
- Eggs distributed correctly
- Both users' Duel Eggs consumed

---

### Test 6.3: DnD Adventure
**Command:** `!adventure`

**Prerequisites:**
- Have at least 500 eggs

**Test Steps:**
1. Type `!adventure` in chat
2. Observe bot response
3. Try command again immediately

**Expected Result (First Use):**
```
🎲 @YourName embarks on an adventure! [Scenario text] You rolled a X (Y saving throw)! [Outcome] +Z 🥚 earned!
```

**Expected Result (Second Use - Cooldown):**
```
@YourName, you're still recovering from your last adventure! Try again in X hours.
```

**✅ Pass Criteria:**
- Adventure executes first time
- Random scenario generated
- D20 roll shown (1-20)
- Saving throw type shown
- Outcome based on roll
- Eggs awarded/deducted appropriately
- 24-hour cooldown enforced

---

### Test 6.4: Top Leaderboard
**Command:** `!top`

**Test Steps:**
1. Type `!top` in chat
2. Observe bot response

**Expected Result:**
```
🏆 Top Egg Holders: 1. @User1 (X🥚) | 2. @User2 (Y🥚) | 3. @User3 (Z🥚)
```

**✅ Pass Criteria:**
- Shows top 3 users
- Sorted by egg count (highest first)
- Egg counts displayed
- Emojis present

---

### Test 6.5: Economy Monitoring (Moderators Only)
**Command:** `!econfunds`

**Prerequisites:**
- Test with moderator account

**Test Steps:**
1. As moderator, type `!econfunds` in chat
2. Observe bot response

**Expected Result:**
```
💰 Economy Status: Big Nest Fund: X 🥚 | Egg Carton Jackpot: Y 🥚
```

**✅ Pass Criteria:**
- Shows both fund values
- Numbers are correct
- Non-moderators cannot use command

---

## 7. Edge Case Testing

### Test 7.1: Insufficient Funds
**Test:** Try to buy token without enough eggs

**Steps:**
1. Ensure you have < 20 eggs
2. Type `!buy MysteryEgg 1`

**Expected:**
```
@YourName, you don't have enough eggs! You need 20 🥚 but only have X 🥚.
```

**✅ Pass:** Proper error message, no eggs deducted

---

### Test 7.2: Insufficient Tokens
**Test:** Try to play game without token

**Steps:**
1. Ensure you have 0 Mystery Eggs
2. Type `!chomp`

**Expected:**
```
@YourName, you need 1 Mystery Egg to play! Use !buy MysteryEgg 1 (costs 20 🥚).
```

**✅ Pass:** Proper error message, game doesn't execute

---

### Test 7.3: Duel Challenge Timeout
**Test:** Challenge expires if not accepted

**Steps:**
1. Issue duel challenge
2. Wait more than 2 minutes without accepting

**Expected:**
- Challenge expires silently
- New challenges can be issued
- Eggs/tokens not consumed

**✅ Pass:** System cleans up expired challenges

---

### Test 7.4: Cooldown Enforcement
**Test:** Commands respect cooldowns

**Steps:**
1. Use `!chomp`
2. Immediately try `!chomp` again

**Expected:**
```
@YourName, please wait X seconds before using this command again.
```

**✅ Pass:** Cooldown properly enforced

---

### Test 7.5: Character Reset
**Command:** `!reroll`

**Prerequisites:**
- Have at least 1000 eggs

**Test Steps:**
1. Note current token counts
2. Type `!reroll` in chat
3. Check inventory with `!eggpack`

**Expected:**
```
@YourName has reset their character! All tokens cleared. Fresh start!
```

**✅ Pass Criteria:**
- All tokens reset to 0
- 1000 eggs deducted
- User stats reset
- Confirmation message sent

---

## 8. Compilation Test

### Step 8.1: Check for C# Compilation Errors
1. Go to **Actions** tab
2. For each imported action:
   - Double-click to open
   - Look for any red error indicators
   - Check sub-actions for compilation errors
3. Open **Logs** tab
4. Look for any C# compilation errors

**✅ Pass Criteria:**
- No red error indicators
- No compilation errors in logs
- All actions show as "Ready"

**❌ If Errors Found:**
- Note the specific error message
- Check action code for syntax issues
- Verify Streamer.bot is up to date
- Report issue with error details

---

## Test Results Checklist

Use this checklist to track your testing:

### Import Tests
- [ ] JSON file import successful
- [ ] Import string method successful
- [ ] All 13 actions imported
- [ ] All 12 commands imported
- [ ] 1 timed action imported

### Basic Functionality
- [ ] !eggs command works
- [ ] !buy command works (tokens purchased)
- [ ] !eggpack shows inventory
- [ ] !chomp game plays correctly
- [ ] !titles shows ranks

### Advanced Functionality
- [ ] !duelnest challenge works
- [ ] !accept duel works
- [ ] !adventure game works
- [ ] !top leaderboard works
- [ ] !econfunds (mod only) works

### Edge Cases
- [ ] Insufficient funds handled
- [ ] Insufficient tokens handled
- [ ] Duel timeout handled
- [ ] Cooldowns enforced
- [ ] Character reset works

### Technical
- [ ] No C# compilation errors
- [ ] No errors in logs
- [ ] All actions enabled
- [ ] All commands enabled
- [ ] Timed action running

---

## Troubleshooting

### Problem: Import fails
**Solution:**
1. Verify Streamer.bot version is v1.0.1+
2. Try alternative import method
3. Check file integrity (re-download if needed)
4. Check Streamer.bot logs for specific error

### Problem: Commands don't respond
**Solution:**
1. Verify loyalty system is enabled
2. Check Pouch Eggs currency is configured
3. Verify commands are enabled in Commands tab
4. Check Twitch connection is active

### Problem: C# code won't compile
**Solution:**
1. Check Streamer.bot logs for error details
2. Verify .NET Framework is installed
3. Try re-importing the action
4. Update Streamer.bot to latest version

### Problem: Duel resolver not working
**Solution:**
1. Check timed action is enabled
2. Verify interval is 60 seconds
3. Check action is linked correctly
4. Restart Streamer.bot

---

## Reporting Issues

If you encounter issues during testing:

1. **Document the problem:**
   - What command/action failed?
   - What was the expected result?
   - What actually happened?
   - Any error messages?

2. **Collect information:**
   - Streamer.bot version
   - Operating system
   - Relevant log entries
   - Steps to reproduce

3. **Check existing documentation:**
   - IMPORT_GUIDE.md
   - Troubleshooting_Guide.md
   - This testing guide

4. **Report:**
   - GitHub Issues
   - Streamer.bot Discord
   - Include all collected information

---

## Success Criteria

The import and system are considered **successful** if:

✅ All import tests pass  
✅ All basic functionality tests pass  
✅ All advanced functionality tests pass  
✅ No C# compilation errors  
✅ No persistent errors in logs  
✅ Edge cases handled correctly

---

## Conclusion

If all tests pass, the Yoshi's Island Eggonomy system is **fully functional** and ready for production use!

**Testing Time:** Approximately 30-45 minutes for complete testing

**Next Steps:**
- Configure economy balance settings
- Customize messages if desired
- Go live and enjoy your new economy system!

---

**Document Version:** 1.0  
**Last Updated:** December 31, 2025  
**Tested With:** Streamer.bot v1.0.1
