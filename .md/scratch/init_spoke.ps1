# Init Spoke Script
$kbDirs = @(
    ".md\seminars", 
    ".md\legal_docs", 
    ".md\extracted_docs", 
    ".md\scratch", 
    ".md\data", 
    ".md\knowledge\configs", 
    ".md\knowledge\guidelines", 
    ".md\knowledge\related_papers", 
    ".md\knowledge\reports", 
    ".md\knowledge\specs_and_roadmaps"
)
foreach ($dir in $kbDirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

$hub = "D:\GitHubProjects\ccba-agent-platform"
New-Item -ItemType Directory -Force -Path ".agents\skills", ".agents\workflows" | Out-Null

$bundles = @("_core", "_qc", "_consulting")
foreach ($b in $bundles) {
    $sSrc = Join-Path $hub (".agents\skills\" + $b)
    if (Test-Path $sSrc) {
        Copy-Item -Path ($sSrc + "\*") -Destination ".agents\skills\" -Recurse -Force
    }
    $wSrc = Join-Path $hub (".agents\workflows\" + $b)
    if (Test-Path $wSrc) {
        Copy-Item -Path ($wSrc + "\*") -Destination ".agents\workflows\" -Recurse -Force
    }
}

$hubTemplates = Join-Path $hub ".agents\workflows\resources\templates"
if (Test-Path $hubTemplates) {
    if (-not (Test-Path ".md\data\contracts")) { New-Item -ItemType Directory -Path ".md\data\contracts" -Force | Out-Null }
    Copy-Item -Path (Join-Path $hubTemplates "ccba_rd_seminar_template.md") -Destination ".md\seminars\CCBA_RD_SEMINAR_001_Rev00-Template.md" -Force -ErrorAction SilentlyContinue
    Copy-Item -Path (Join-Path $hubTemplates "contract_template.md") -Destination ".md\data\contracts\contract_template.md" -Force -ErrorAction SilentlyContinue
    Copy-Item -Path (Join-Path $hubTemplates "weekly_report_template.md") -Destination ".md\knowledge\reports\weekly_report_template.md" -Force -ErrorAction SilentlyContinue
}
