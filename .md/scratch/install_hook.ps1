# Install Git Pre-commit Hook Script
if (Test-Path ".git") {
    $hookDir = ".git\hooks"
    if (-not (Test-Path $hookDir)) {
        New-Item -ItemType Directory -Path $hookDir -Force | Out-Null
    }
    $hookPath = Join-Path $hookDir "pre-commit"
    $hookContent = @'
#!/bin/sh
# CCBA Maskara Pre-commit Security Hook
echo 'Running Maskara staged files scan...'

staged_files=$(git diff --cached --name-only --diff-filter=d)

if [ -z "$staged_files" ]; then
    echo "No files staged for commit. Skipping scan."
    exit 0
fi

has_leak=0
for file in $staged_files; do
    if echo "$file" | grep -qE '\.(png|jpg|jpeg|gif|ico|pdf|zip|tar|gz|exe|dll|so|dylib|woff|woff2|eot|ttf|mp3|mp4|wav|avi)$'; then
        continue
    fi
    if echo "$file" | grep -qE '^(\.md/scratch/|\.venv/|node_modules/)'; then
        continue
    fi
    if [ -f "$file" ]; then
        python "D:/GitHubProjects/ccba-agent-platform/scripts/maskara.py" scan --root "$file" > /dev/null 2>&1
        status_code=$?
        if [ $status_code -ne 0 ]; then
            echo "❌ Leak detected in staged file: $file"
            python "D:/GitHubProjects/ccba-agent-platform/scripts/maskara.py" scan --root "$file"
            has_leak=1
        fi
    fi
done

if [ $has_leak -ne 0 ]; then
    echo 'Error: Raw API keys or credentials detected. Commit blocked!'
    exit 1
fi

echo "✅ Security check passed."
exit 0
'@
    [System.IO.File]::WriteAllText($hookPath, $hookContent)
    Write-Host "Git pre-commit hook installed successfully."
}
