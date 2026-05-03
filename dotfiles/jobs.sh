#!/bin/bash
PATH_TO_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

JOBS_SCRIPT="$(cd "$PATH_TO_SCRIPT_DIR/../scripts" && pwd)/run-jobs.py"
PYTHON_SCRIPT="$(command -v python3)"
JOBS_PLIST="$HOME/Library/LaunchAgents/local.dotfiles.run-jobs.plist"

if [ ! -f "$JOBS_PLIST" ]; then
    cat > "$JOBS_PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>local.dotfiles.run-jobs</string>
    <key>ProgramArguments</key>
    <array>
        <string>$PYTHON_SCRIPT</string>
        <string>$JOBS_SCRIPT</string>
    </array>
    <key>StartInterval</key>
    <integer>3600</integer>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
EOF
    launchctl load "$JOBS_PLIST"
fi

# Run all due jobs right now (useful for testing)
function run-jobs {
    "$PYTHON_SCRIPT" "$JOBS_SCRIPT"
}
