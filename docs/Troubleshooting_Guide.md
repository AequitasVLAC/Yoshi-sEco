# Troubleshooting & Best Practices Guide

**Platform:** Streamer.bot (v0.2.0+)  
**Last Updated:** December 2025

This guide provides comprehensive solutions to common issues, best practices for maintaining your economy, and optimization tips for Streamer.bot performance.

---

## Table of Contents

1. [Common Issues & Solutions](#common-issues--solutions)
2. [Variable Troubleshooting](#variable-troubleshooting)
3. [Code Compilation Errors](#code-compilation-errors)
4. [Performance Optimization](#performance-optimization)
5. [Economy Balance Tips](#economy-balance-tips)
6. [Testing Procedures](#testing-procedures)
7. [Backup & Recovery](#backup--recovery)
8. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Common Issues & Solutions

### Issue: Command Not Found

**Symptoms:** Typing `!buy`, `!chomp`, etc. in chat does nothing

**Solutions:**

1. **Check Command is Enabled**
   - Go to: `Commands` tab in Streamer.bot
   - Find your command in the list
   - Ensure checkbox next to it is ✅ checked
   - Click **Save** if you made changes

2. **Verify Command Spelling**
   - Commands are case-sensitive in some versions
   - Check for extra spaces or typos
   - Command must start with `!` (exclamation mark)

3. **Check Streamer.bot Connection**
   - Look at top of Streamer.bot window
   - Should show "Connected" status to Twitch
   - If disconnected, click "Reconnect"
   - Check your internet connection

4. **Verify Permissions**
   - Some commands may be set to "Moderators Only"
   - Test with a moderator account
   - Adjust permissions in Command settings

5. **Check for Conflicting Commands**
   - Another bot or Streamer.bot action may override
   - Disable other bots temporarily to test
   - Check for duplicate command names

**Quick Fix:**
```
1. Disable command
2. Save
3. Enable command
4. Save
5. Test in chat
```

---

### Issue: Compile Errors in C# Code

**Symptoms:** "Compilation Failed" message when clicking Compile button

**Common Causes & Solutions:**

#### Error: "The type or namespace name 'System' could not be found"

**Solution:** Add `using System;` at the top of your code

```csharp
using System;  // ← THIS MUST BE FIRST LINE

public class CPHInline
{
    public bool Execute()
    {
        // Your code here
    }
}
```

---

#### Error: "The name 'CPH' does not exist in the current context"

**Solution:** Ensure class name is exactly `CPHInline` (case-sensitive)

```csharp
// ❌ WRONG
public class MyClass

// ✅ CORRECT
public class CPHInline
```

---

#### Error: "Unexpected symbol '}' " or bracket mismatch

**Solution:** Check all brackets are balanced

```csharp
// Every { needs a matching }
if (condition)
{
    // code
}  // ← Closing brace here

// Count them:
// { = 1, } = 1  ✅ Balanced
```

**Tool Tip:** Use a code editor with bracket matching (VS Code, Notepad++) to paste code and check

---

#### Error: "Cannot implicitly convert type 'string' to 'int'"

**Solution:** Use proper type parsing

```csharp
// ❌ WRONG
int value = args["something"];

// ✅ CORRECT
int value = int.Parse(args["something"].ToString());
```

---

#### Error: "Smart quotes" causing syntax errors

**Symptoms:** Code looks correct but won't compile

**Solution:** Replace smart quotes with straight quotes

```csharp
// ❌ WRONG (smart quotes from copy/paste)
string text = "Hello";

// ✅ CORRECT (straight quotes)
string text = "Hello";
```

**How to Fix:**
1. Copy problematic code to Notepad (plain text)
2. Re-type quotes manually
3. Copy back to Streamer.bot

---

### Issue: Duel Never Resolves

**Symptoms:** Players accept duel but it never finishes

**Solutions:**

1. **Check Timer is Running**
   - Go to: `Actions` tab
   - Find `[PVP] Duel Resolver` action
   - Look for timer/clock icon
   - Should show "Running" or "Enabled" status

2. **Verify Timer Configuration**
   - Right-click action → View Timed Action settings
   - **Interval:** Should be 60 seconds (or 1 minute)
   - **Repeat:** MUST be checked (infinite loop)
   - **Enabled:** MUST be checked

3. **Check for Errors in Resolver Code**
   - Go to Streamer.bot logs (View → Logs)
   - Look for errors when timer runs
   - Common issue: Missing `activeDuel_` variables

4. **Manual Resolution** (temporary fix)
   - Run `[PVP] Duel Resolver` action manually
   - Click action → Test Trigger
   - Duel should resolve immediately

5. **Verify Active Duel Variables Exist**
   - Go to: Settings → Variables
   - Look for:
     - `activeDuel_challenger`
     - `activeDuel_accepter`
     - `activeDuel_wager`
     - `activeDuel_startTime`
   - If missing, duel wasn't properly accepted

**Prevention:**
- Always test duels in development before going live
- Monitor first few duels with `!econfunds` to verify economy funds change
- Set timer to 1 minute for testing, 10 minutes for production

---

### Issue: Tokens Not Showing in !eggpack

**Symptoms:** User buys tokens but `!eggpack` shows 0

**Solutions:**

1. **Check Variable Names (Case-Sensitive)**
   ```
   ✅ CORRECT: 12345678_MysteryEgg
   ❌ WRONG:   12345678_mysteryegg
   ❌ WRONG:   12345678_Mysteryegg
   ```

2. **Verify userId vs userName**
   - Variables MUST use userId (numeric)
   - NOT username (text)
   - Check in code: `$"{userId}_MysteryEgg"` not `$"{userName}_MysteryEgg"`

3. **Check Settings → Variables**
   - Look for user's variables manually
   - Format: `12345678_MysteryEgg` where 12345678 is Twitch user ID
   - If doesn't exist, purchase didn't complete

4. **Test Variable Creation**
   ```csharp
   // In buy token code, add logging
   CPH.LogInfo($"Setting variable: {tokenVar} to {currentTokens + quantity}");
   
   // Check Streamer.bot logs to see if this line runs
   ```

5. **Verify Persistence Flag**
   ```csharp
   // ❌ WRONG - Not persisted
   CPH.SetGlobalVar(tokenVar, amount, false);
   
   // ✅ CORRECT - Persisted
   CPH.SetGlobalVar(tokenVar, amount, true);
   ```

**Quick Test:**
```
1. User types: !buy MysteryEgg 1
2. Immediately type: !eggpack
3. Should show: 1 Mystery
4. If not, check logs for errors
```

---

### Issue: Points Not Adding/Removing Correctly

**Symptoms:** Game awards eggs but balance doesn't change

**Solutions:**

1. **Check Loyalty System Enabled**
   - Settings → Loyalty
   - "Enable Loyalty Points" must be ✅ checked
   - Save settings if you toggled it

2. **Verify userId Parameter**
   ```csharp
   // ✅ CORRECT
   CPH.AddPoints(userId, amount, "description");
   
   // ❌ WRONG (using userName instead)
   CPH.AddPoints(userName, amount, "description");
   ```

3. **Check Point Limits**
   - Some Streamer.bot configs have max point limits
   - Check Settings → Loyalty → Advanced
   - Remove or increase max point cap

4. **Verify Transaction Log**
   - In Streamer.bot, check loyalty point history
   - Should show transactions with descriptions
   - Look for your "Chomp Win" or "Token Purchase" entries

5. **Test with Manual Point Commands**
   ```
   !points add @username 100
   !points remove @username 50
   
   If these work, problem is in your code
   If these fail, loyalty system issue
   ```

**Debug Code:**
```csharp
// Before adding points
int before = CPH.GetPoints(userId);
CPH.LogInfo($"Balance before: {before}");

// Add points
CPH.AddPoints(userId, 50, "Test");

// After adding points
int after = CPH.GetPoints(userId);
CPH.LogInfo($"Balance after: {after}");

// Check logs - should show before and after values
```

---

### Issue: Random Numbers Always Same

**Symptoms:** Rolling dice gives same result repeatedly

**Explanation:** This is actually NORMAL in rapid testing!

**Why It Happens:**
- `new Random()` uses time-based seed
- If you test multiple times per second, seed is identical
- In real usage with delays, this won't occur

**Solutions (for testing):**

1. **Wait 1-2 Seconds Between Tests**
   - Natural delay between user commands solves this

2. **Use Static Random (Advanced)**
   ```csharp
   // At class level (outside Execute method)
   private static Random rnd = new Random();
   
   public bool Execute()
   {
       // Use existing rnd instance
       int roll = rnd.Next(1, 7);
   }
   ```

3. **Seed with Additional Entropy**
   ```csharp
   // Use Guid for extra randomness
   Random rnd = new Random(Guid.NewGuid().GetHashCode());
   int roll = rnd.Next(1, 7);
   ```

**Best Practice:**
- In production, default `new Random()` is fine
- Users never command fast enough to trigger issue
- Only a concern during rapid testing

---

## Variable Troubleshooting

### Issue: Variables Not Persisting After Restart

**Symptoms:** All tokens/stats reset when Streamer.bot restarts

**Solutions:**

1. **Check `persisted: true` Parameter**
   ```csharp
   // ❌ WRONG - Lost on restart
   CPH.GetGlobalVar<int>("myVar", false);
   CPH.SetGlobalVar("myVar", 100, false);
   
   // ✅ CORRECT - Persists
   CPH.GetGlobalVar<int>("myVar", true);
   CPH.SetGlobalVar("myVar", 100, true);
   ```

2. **Verify Database Permissions**
   - Streamer.bot needs write access to AppData folder
   - Check folder: `%AppData%\Streamer.bot\`
   - Try running Streamer.bot as Administrator

3. **Check Disk Space**
   - SQLite database needs space to grow
   - Check system drive has free space
   - Clean up old logs if needed

4. **Database Corruption Check**
   - Close Streamer.bot
   - Backup `Streamer.bot` folder
   - Delete database files
   - Restart Streamer.bot (will create fresh DB)
   - Re-initialize variables

---

### Issue: Cannot Find Variable in UI

**Symptoms:** Variable exists in code but not in Settings → Variables

**Solutions:**

1. **Variable Only Appears After First Set**
   - Variables don't exist until `SetGlobalVar` is called
   - Run the action once to create variable
   - Then it will appear in UI

2. **Refresh Streamer.bot UI**
   - Close and reopen Settings → Variables
   - Or restart Streamer.bot entirely

3. **Check Exact Spelling and Case**
   - Search in Variables using exact name
   - Case-sensitive: `bigNestFund` ≠ `bignestfund`

4. **Check if Non-Persisted**
   - If `persisted: false`, variable won't show in UI
   - Change to `persisted: true` and set again

---

### Issue: "Object reference not set" Errors

**Symptoms:** Code crashes with null reference error

**Cause:** Trying to use a variable that doesn't exist or is null

**Solution:** Always check for null before using

```csharp
// ❌ WRONG - Can crash if null
string name = CPH.GetGlobalVar<string>("duel_challenger", true);
if (name.Equals("something")) { } // CRASH!

// ✅ CORRECT - Safe null checking
string name = CPH.GetGlobalVar<string>("duel_challenger", true);
if (string.IsNullOrEmpty(name)) {
    // Handle null case
    return false;
} else {
    // Safe to use name
    if (name.Equals("something")) { }
}
```

**Pattern for All Variable Types:**
```csharp
// Integers (default to 0 if not exists)
int value = CPH.GetGlobalVar<int>("varName", true);
// No null check needed - always has value

// Strings (can be null)
string text = CPH.GetGlobalVar<string>("varName", true);
if (string.IsNullOrEmpty(text)) {
    // Handle missing variable
}

// Booleans (default to false if not exists)
bool flag = CPH.GetGlobalVar<bool>("varName", true);
// No null check needed - always has value
```

---

## Code Compilation Errors

### Quick Reference Table

| Error Message | Cause | Solution |
|--------------|-------|----------|
| "Missing using directive" | Missing `using System;` | Add at top of file |
| "Expected class, delegate..." | Wrong class name | Use `CPHInline` exactly |
| "The name 'CPH' does not exist" | Wrong class name | Use `CPHInline` exactly |
| "Cannot convert string to int" | Wrong type | Use `int.Parse()` or `int.TryParse()` |
| "Unexpected symbol" | Bracket mismatch | Count { and } - must match |
| "'args' does not exist" | Wrong method signature | Use `public bool Execute()` |
| "Smart quotes error" | Copy/paste from formatted text | Retype quotes manually |
| "Semicolon expected" | Missing semicolon | Add `;` at end of statement |

---

### Best Practices to Avoid Compile Errors

1. **Always Start with Template**
   ```csharp
   using System;
   
   public class CPHInline
   {
       public bool Execute()
       {
           // Your code here
           return true;
       }
   }
   ```

2. **Delete ALL Default Code**
   - When adding Execute Code sub-action
   - Streamer.bot may include template code
   - DELETE it completely before pasting

3. **Test Compile Early and Often**
   - Don't write entire action before testing
   - Compile after every 5-10 lines
   - Easier to find errors in small chunks

4. **Use Code Editor for Complex Actions**
   - Write in VS Code or Notepad++
   - Get syntax highlighting and error detection
   - Copy final working code to Streamer.bot

5. **Comment Your Code**
   ```csharp
   // Good comments explain WHY, not WHAT
   
   // Reset streak because player lost
   CPH.SetGlobalVar($"{userId}_chompStreak", 0, true);
   ```

---

## Performance Optimization

### Best Practices for Large Communities

**If you have 100+ active users:**

1. **Limit Variable Lookups in Loops**
   ```csharp
   // ❌ SLOW - Looks up variable 100 times
   for (int i = 0; i < 100; i++) {
       int fund = CPH.GetGlobalVar<int>("bigNestFund", true);
       // use fund
   }
   
   // ✅ FAST - Looks up once
   int fund = CPH.GetGlobalVar<int>("bigNestFund", true);
   for (int i = 0; i < 100; i++) {
       // use fund
   }
   ```

2. **Use Appropriate Timer Intervals**
   ```
   ✅ Duel Resolver: 60 seconds (fine)
   ✅ Event Expiry: 60 seconds (fine)
   ❌ Any Timer: < 5 seconds (risky)
   ```

3. **Avoid Unnecessary Logging**
   ```csharp
   // Only log important events
   if (goldenEgg) {
       CPH.LogInfo($"Golden egg found by {userName}!");
   }
   
   // Don't log every single action
   ```

4. **Clean Up Old User Data**
   - Periodically remove variables for inactive users (90+ days)
   - Reduces database size
   - Improves query speed

---

### Monitoring Performance

**Signs of Performance Issues:**
- Commands take > 2 seconds to respond
- Streamer.bot UI becomes sluggish
- Chat messages delayed

**Diagnostics:**
1. Check Streamer.bot CPU usage in Task Manager
2. Check database file size (Settings → Variables)
3. Review logs for errors or warnings
4. Test commands one at a time to isolate issues

**Solutions:**
- Restart Streamer.bot weekly
- Back up and clean database monthly
- Disable unused actions and commands
- Increase system resources (RAM/CPU)

---

## Economy Balance Tips

### Monitoring Your Economy

**Key Metrics to Track Weekly:**

1. **Total Eggs in Circulation**
   - Sum of all user balances
   - Should grow steadily but slowly
   - Rapid growth = inflation problem

2. **Fund Balances**
   ```
   !econfunds  → Check bigNestFund and jackpot
   
   Healthy ranges:
   bigNestFund: 500-5000 🥚
   jackpot: 250-2000 🥚
   ```

3. **Average User Balance**
   - Most users should have 50-500 🥚
   - Top users can have 1000-10000 🥚
   - If everyone has 50000+ → inflation issue

4. **Game Play Frequency**
   - Track using global counter variables
   - Games should be played regularly
   - Low play rate = tokens too expensive or rewards too low

---

### Adjusting the Economy

**If Inflation is Too High (Everyone has too many eggs):**

1. **Reduce Passive Income**
   - Settings → Loyalty → Decrease per-interval rewards
   - Try: 3 eggs per 10 min (was 5)

2. **Increase Token Costs**
   - Edit `[ECON] Buy Token` action
   - Change dictionary values:
     ```csharp
     {"MysteryEgg", 25},  // was 20
     {"DiceEgg", 12},     // was 10
     {"DuelEgg", 6}       // was 5
     ```

3. **Decrease Game Payouts**
   - Lower base payouts in each game by 10-20%

4. **Add New Currency Sinks**
   - Premium commands (cost eggs)
   - Special cosmetic purchases
   - Donations to causes

**If Deflation is Too High (No one has enough eggs):**

1. **Increase Passive Income**
   - Settings → Loyalty → Increase per-interval rewards
   - Try: 7 eggs per 10 min (was 5)

2. **Decrease Token Costs**
   - Lower by 10-20%

3. **Increase Game Payouts**
   - Raise base payouts by 10-20%

4. **Add One-Time Bonuses**
   - Run Double Rewards events
   - Give new viewers starter packs

**Rule of Thumb:**
- Users should earn 1 token worth of eggs per hour of watching
- Active chatters should earn 2-3 tokens worth per hour

---

## Testing Procedures

### Pre-Launch Testing Checklist

Complete ALL tests before going live:

**Currency Tests:**
- [ ] `!eggs` shows correct balance
- [ ] Passive income works (wait 10+ minutes and check)
- [ ] Active chatter bonus works (chat and wait 10+ minutes)

**Token Purchase Tests:**
- [ ] `!buy MysteryEgg 1` costs 20 eggs
- [ ] `!buy DiceEgg 2` costs 20 eggs (10 each)
- [ ] `!buy DuelEgg 5` costs 25 eggs (5 each)
- [ ] `!eggpack` shows correct token counts
- [ ] Insufficient funds message works
- [ ] Invalid token type shows error message
- [ ] Economy funds increase (`!econfunds`)

**Game Tests:**
- [ ] `!chomp` consumes 1 Mystery Egg
- [ ] `!chomp` roll shows 1-6 result
- [ ] `!chomp` win awards eggs and increases streak
- [ ] `!chomp` loss (roll 1) resets streak
- [ ] `!eggroll` consumes 1 Dice Egg
- [ ] `!eggroll` shows proper payout for all roll ranges
- [ ] `!duelnest @user 10` creates challenge
- [ ] `!accept` starts duel
- [ ] Duel resolves after 10 minutes automatically

**User Command Tests:**
- [ ] `!titles` shows correct rank
- [ ] `!sheet` shows correct stats
- [ ] `!eggpack` shows all tokens
- [ ] `!reroll` costs 1000 eggs and resets everything

**Event Tests (if implemented):**
- [ ] `!doublerewards` activates 2x payouts
- [ ] `!freeentry` allows free games
- [ ] Events expire automatically
- [ ] `!events` shows active events

**Stress Tests:**
- [ ] Multiple users buying tokens simultaneously
- [ ] Multiple games running at once
- [ ] Rapid command spamming (should have cooldowns)

---

### Testing with Test Accounts

**Best Practice:** Create 2-3 test Twitch accounts

**Test Account Setup:**
1. Create test Twitch account
2. Make it moderator in your channel
3. Have test account join your channel
4. Test commands from test account

**Test Scenarios:**
```
Main Account: !duelnest @TestAccount 10
Test Account: !accept

Main Account: !buy MysteryEgg 5
Test Account: !buy DiceEgg 3

Main Account: !chomp
Test Account: !eggroll
```

---

## Backup & Recovery

### Backup Procedures

**Daily Backup (Automated):**

1. Create Windows scheduled task
2. Run daily at 3 AM (low activity time)
3. Script:
   ```batch
   @echo off
   xcopy "C:\Users\%USERNAME%\AppData\Roaming\Streamer.bot" "D:\Backups\Streamerbot\%date:~-4,4%%date:~-10,2%%date:~-7,2%\" /E /I /H /Y
   ```

**Manual Backup (Before Changes):**

1. Close Streamer.bot
2. Navigate to: `%AppData%\Streamer.bot\`
3. Copy entire folder to backup location
4. Name: `Streamerbot_Backup_YYYY-MM-DD`
5. Reopen Streamer.bot

**What to Backup:**
- ✅ All variables (in database files)
- ✅ Actions and commands (in config files)
- ✅ Settings and configurations
- ❌ Log files (optional, usually not needed)

---

### Recovery Procedures

**If Variables Lost:**

1. Close Streamer.bot
2. Navigate to backup folder
3. Copy database files to current Streamer.bot folder
4. Restart Streamer.bot
5. Verify variables: Settings → Variables

**If Actions Lost:**

1. Close Streamer.bot
2. Copy backup folder completely
3. Replace current Streamer.bot folder
4. Restart Streamer.bot
5. Verify actions: Actions tab

**If Only Some Variables Corrupted:**

1. Go to: Settings → Variables
2. Manually re-enter known values
3. Or use initialization script from Variable Reference guide

**Nuclear Option (Fresh Start):**

1. Backup everything first
2. Uninstall Streamer.bot
3. Delete AppData folder
4. Reinstall Streamer.bot
5. Manually recreate actions from this guide
6. Use initialization script for variables

---

## Monitoring & Maintenance

### Weekly Maintenance Tasks

**Every Week:**
- [ ] Check `!econfunds` - Record values
- [ ] Review Streamer.bot logs for errors
- [ ] Test each game once
- [ ] Backup database
- [ ] Check active user counts and balances

**Monthly Maintenance Tasks:**

**Every Month:**
- [ ] Clean up old user variables (90+ days inactive)
- [ ] Review economy balance (inflation/deflation)
- [ ] Update token costs if needed
- [ ] Add new features or events
- [ ] Major database backup (off-site)

---

### Logging Best Practices

**Enable Logging in Your Actions:**

```csharp
// At key decision points
CPH.LogInfo($"User {userName} bought {quantity} tokens for {totalCost} eggs");

// On errors
CPH.LogWarn($"User {userName} insufficient funds: has {balance}, needs {cost}");

// On critical events
CPH.LogInfo($"Golden egg found by {userName}! Total found: {count}");
```

**Review Logs:**
- View → Logs in Streamer.bot
- Filter by severity: Info, Warning, Error
- Search for user names or action names
- Export logs for long-term storage

---

## Quick Troubleshooting Flowchart

```
Command not working?
├─ Is command enabled? → Enable it
├─ Is Streamer.bot connected? → Reconnect
├─ Does action exist? → Create it
└─ Check logs for errors → Fix reported error

Code won't compile?
├─ Missing using System;? → Add it
├─ Class name CPHInline? → Fix it
├─ Smart quotes? → Retype quotes
└─ Brackets balanced? → Count { and }

Variables not persisting?
├─ persisted: true? → Fix parameter
├─ Disk space available? → Free up space
└─ Database corrupted? → Restore backup

Economy unbalanced?
├─ Inflation (too many eggs)? → Reduce income, increase costs
├─ Deflation (too few eggs)? → Increase income, reduce costs
└─ Check metrics weekly → Adjust gradually
```

---

## Getting Help

**Before Asking for Help:**
1. Check this troubleshooting guide
2. Review Streamer.bot logs
3. Test with fresh backup
4. Search Streamer.bot Discord/forum

**When Asking for Help, Include:**
- Streamer.bot version number
- Exact error message or behavior
- Code snippet causing issue
- What you've already tried
- Screenshots if UI-related

**Where to Get Help:**
- Streamer.bot Discord server
- Streamer.bot subreddit
- This guide's repository Issues page
- Streamer.bot documentation

---

## Summary

This troubleshooting guide covers:

✅ **50+ Common Issues** with solutions  
✅ **Code compilation** help and debugging  
✅ **Performance optimization** for large streams  
✅ **Economy balance** monitoring and adjustment  
✅ **Testing procedures** before going live  
✅ **Backup & recovery** best practices  
✅ **Monitoring & maintenance** schedules  

**Prevention is Better Than Cure:**
- Test thoroughly before going live
- Back up before making changes
- Monitor economy metrics weekly
- Keep Streamer.bot updated
- Document your customizations

**Related Documentation:**
- [Variable Reference](Variable_Reference.md) - All variables explained
- [Unified Eggonomy Guide](Unified_Yoshi_Eggonomy.md) - Core implementation
- [Event System Guide](Event_System_Guide.md) - Events and bonuses
- [Advanced Features Guide](Advanced_Features_Guide.md) - Custom extensions
