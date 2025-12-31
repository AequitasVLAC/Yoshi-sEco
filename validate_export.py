#!/usr/bin/env python3
"""
Streamer.bot v1.0.1 Export Validator
=====================================
This script validates that JSON export files and import strings are correctly
formatted for Streamer.bot v1.0.1 import functionality.

Usage:
    python validate_export.py <json_file> [import_string_file]
"""

import json
import base64
import gzip
import sys
from pathlib import Path

# Streamer.bot type constants
TYPE_EXPORT = 'Streamer.bot.Data.Export, Streamer.bot'
TYPE_ACTION = 'Streamer.bot.Data.Action, Streamer.bot'
TYPE_COMMAND = 'Streamer.bot.Data.Command, Streamer.bot'
TYPE_TIMED_ACTION = 'Streamer.bot.Data.TimedAction, Streamer.bot'


def validate_streamerbot_export(json_data):
    """Validate that the JSON matches Streamer.bot v1.0.1 export format"""
    issues = []
    warnings = []
    
    # Root level validation
    if '$type' not in json_data:
        issues.append("Missing root $type field")
    elif json_data['$type'] != TYPE_EXPORT:
        issues.append(f"Incorrect root $type: {json_data['$type']}")
    
    # Required root fields
    required_fields = ['actions', 'commands']
    for field in required_fields:
        if field not in json_data:
            issues.append(f"Missing required root field: {field}")
    
    # Actions validation
    if 'actions' in json_data:
        for i, action in enumerate(json_data['actions']):
            action_name = action.get('name', f'Action {i}')
            
            if '$type' not in action:
                issues.append(f"{action_name}: Missing $type")
            elif action['$type'] != TYPE_ACTION:
                issues.append(f"{action_name}: Incorrect $type: {action['$type']}")
            
            required_action_fields = ['id', 'name', 'enabled', 'group']
            for field in required_action_fields:
                if field not in action:
                    issues.append(f"{action_name}: Missing {field} field")
            
            if 'subActions' not in action:
                warnings.append(f"{action_name}: Has no subActions")
            else:
                # Validate subActions
                for j, subaction in enumerate(action['subActions']):
                    if '$type' not in subaction:
                        issues.append(f"{action_name} subAction {j}: Missing $type")
                    
                    # Check for C# code compilation flag
                    if 'ExecuteCode' in subaction.get('$type', ''):
                        if 'code' not in subaction:
                            issues.append(f"{action_name} subAction {j}: ExecuteCode missing code field")
    
    # Commands validation
    if 'commands' in json_data:
        action_ids = {a['id'] for a in json_data.get('actions', []) if 'id' in a}
        
        for i, command in enumerate(json_data['commands']):
            cmd_name = command.get('name', f'Command {i}')
            
            if '$type' not in command:
                issues.append(f"{cmd_name}: Missing $type")
            elif command['$type'] != TYPE_COMMAND:
                issues.append(f"{cmd_name}: Incorrect $type: {command['$type']}")
            
            required_cmd_fields = ['id', 'name', 'enabled', 'actionId']
            for field in required_cmd_fields:
                if field not in command:
                    issues.append(f"{cmd_name}: Missing {field} field")
            
            if 'actionId' in command and command['actionId'] not in action_ids:
                issues.append(f"{cmd_name}: References non-existent action ID")
    
    # Timed actions validation
    if 'timedActions' in json_data:
        action_ids = {a['id'] for a in json_data.get('actions', []) if 'id' in a}
        
        for i, timed in enumerate(json_data['timedActions']):
            timed_name = timed.get('name', f'Timed Action {i}')
            
            if '$type' not in timed:
                issues.append(f"{timed_name}: Missing $type")
            elif timed['$type'] != TYPE_TIMED_ACTION:
                issues.append(f"{timed_name}: Incorrect $type")
            
            if 'actionId' not in timed:
                issues.append(f"{timed_name}: Missing actionId")
            elif timed['actionId'] not in action_ids:
                issues.append(f"{timed_name}: References non-existent action")
    
    return issues, warnings


def validate_import_string(import_string, expected_json=None):
    """Validate that an import string is correctly encoded"""
    errors = []
    
    try:
        # Remove any whitespace
        import_string = import_string.strip()
        
        # Base64 decode
        try:
            compressed = base64.b64decode(import_string)
        except Exception as e:
            errors.append(f"Base64 decode failed: {e}")
            return errors, None
        
        # Gzip decompress
        try:
            decompressed = gzip.decompress(compressed)
        except Exception as e:
            errors.append(f"Gzip decompress failed: {e}")
            return errors, None
        
        # Parse JSON
        try:
            json_data = json.loads(decompressed.decode('utf-8'))
        except Exception as e:
            errors.append(f"JSON parse failed: {e}")
            return errors, None
        
        # If expected JSON provided, compare
        if expected_json is not None:
            expected_str = json.dumps(expected_json, sort_keys=True)
            actual_str = json.dumps(json_data, sort_keys=True)
            if expected_str != actual_str:
                errors.append("Import string does not match expected JSON file")
        
        return errors, json_data
        
    except Exception as e:
        errors.append(f"Unexpected error: {e}")
        return errors, None


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_export.py <json_file> [import_string_file]")
        sys.exit(1)
    
    json_file = Path(sys.argv[1])
    import_string_file = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    
    print("=" * 70)
    print("STREAMER.BOT v1.0.1 EXPORT VALIDATOR")
    print("=" * 70)
    
    # Validate JSON file
    print(f"\n📄 Validating JSON file: {json_file.name}")
    
    if not json_file.exists():
        print(f"❌ File not found: {json_file}")
        sys.exit(1)
    
    with open(json_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    issues, warnings = validate_streamerbot_export(json_data)
    
    print(f"\n📋 Export Summary:")
    print(f"  • Actions: {len(json_data.get('actions', []))}")
    print(f"  • Commands: {len(json_data.get('commands', []))}")
    print(f"  • Timed Actions: {len(json_data.get('timedActions', []))}")
    print(f"  • Global Variables: {len(json_data.get('globalVariables', []))}")
    
    if issues:
        print(f"\n❌ CRITICAL ISSUES FOUND ({len(issues)}):")
        for issue in issues:
            print(f"  • {issue}")
    else:
        print("\n✅ No critical issues found!")
    
    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for warning in warnings[:10]:  # Show first 10
            print(f"  • {warning}")
        if len(warnings) > 10:
            print(f"  ... and {len(warnings) - 10} more")
    
    # Validate import string if provided
    if import_string_file:
        print(f"\n📝 Validating import string: {import_string_file.name}")
        
        if not import_string_file.exists():
            print(f"❌ File not found: {import_string_file}")
            sys.exit(1)
        
        with open(import_string_file, 'r', encoding='utf-8') as f:
            import_string = f.read()
        
        errors, string_json = validate_import_string(import_string, json_data)
        
        if errors:
            print(f"\n❌ IMPORT STRING ISSUES FOUND ({len(errors)}):")
            for error in errors:
                print(f"  • {error}")
        else:
            print(f"\n✅ Import string is valid!")
            original_size = len(json.dumps(json_data))
            compressed_size = len(base64.b64decode(import_string.strip()))
            encoded_size = len(import_string.strip())
            
            print(f"  • Original size: {original_size:,} bytes")
            print(f"  • Compressed size: {compressed_size:,} bytes")
            print(f"  • Base64 encoded: {encoded_size:,} characters")
            print(f"  • Compression ratio: {compressed_size/original_size*100:.1f}%")
            print(f"\n✅ Import string matches JSON file exactly!")
    
    # Final verdict
    print("\n" + "=" * 70)
    print("FINAL VERDICT")
    print("=" * 70)
    
    if not issues and (not import_string_file or not errors):
        print("\n🎉 EXPORT IS VALID FOR STREAMER.BOT v1.0.1!")
        print("\nThe export file and import string are properly formatted and ready")
        print("for import into Streamer.bot v1.0.1.")
        sys.exit(0)
    else:
        print("\n❌ EXPORT HAS ISSUES THAT MUST BE FIXED")
        print("\nThe export will NOT work correctly in Streamer.bot v1.0.1 until")
        print("the issues listed above are resolved.")
        sys.exit(1)


if __name__ == '__main__':
    main()
