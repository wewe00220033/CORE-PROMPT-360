[CmdletBinding()]
param(
    [switch]$All,
    [switch]$WithWorkflow,
    [switch]$WithRule,
    [switch]$Uninstall,
    [string]$TargetRoot = (Join-Path $HOME ".gemini")
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$SkillName = "00-lock360-zero-gaps"
$SkillDst = Join-Path (Join-Path (Join-Path $TargetRoot "config") "skills") $SkillName
$WfDstDir = Join-Path (Join-Path $TargetRoot "config") "workflows"
$WfDst = Join-Path $WfDstDir "00-lock360-zero-gaps.md"
$GeminiFile = Join-Path $TargetRoot "GEMINI.md"
$StartMarker = "<!-- LOCK360_START -->"
$EndMarker = "<!-- LOCK360_END -->"
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Write-Utf8Atomic([string]$Path, [string]$Text) {
    $parent = Split-Path -Parent $Path
    if (-not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    $tmp = "$Path.tmp-$PID-$(Get-Random)"
    try {
        $normalized = ($Text -replace "`r`n", "`n")
        [System.IO.File]::WriteAllText($tmp, $normalized, $Utf8NoBom)
        Move-Item -LiteralPath $tmp -Destination $Path -Force
    } finally {
        if (Test-Path -LiteralPath $tmp) {
            Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue
        }
    }
}

function Copy-SkillPayload([string]$Src, [string]$Dst) {
    if (Test-Path -LiteralPath $Dst) {
        $bak = Join-Path $TargetRoot (".backup_lock360_" + (Get-Date -Format "yyyyMMdd_HHmmss"))
        New-Item -ItemType Directory -Path $bak -Force | Out-Null
        Copy-Item -LiteralPath $Dst -Destination (Join-Path $bak $SkillName) -Recurse -Force
        Write-Host "[lock360] Backed up existing skill to: $bak\$SkillName"
    } else {
        New-Item -ItemType Directory -Path $Dst -Force | Out-Null
    }
    foreach ($f in @("SKILL.md", "README.md")) {
        $sp = Join-Path $Src $f
        if (Test-Path -LiteralPath $sp) {
            Copy-Item -LiteralPath $sp -Destination (Join-Path $Dst $f) -Force
        }
    }
    foreach ($d in @("gist", "references")) {
        $sd = Join-Path $Src $d
        if (Test-Path -LiteralPath $sd) {
            $dd = Join-Path $Dst $d
            if (Test-Path -LiteralPath $dd) { Remove-Item -LiteralPath $dd -Recurse -Force }
            Copy-Item -LiteralPath $sd -Destination $dd -Recurse -Force
        }
    }
    Write-Host "[lock360] Installed skill to: $Dst"
}

function Build-GeminiSnippet {
    $raw = @(
        $StartMarker
        "## \uD83D\uDD12 \u0628\u0631\u0648\u062A\u0648\u0643\u0648\u0644 \u0627\u0644\u062A\u0642\u0641\u064A\u0644 \u0627\u0644\u0634\u0627\u0645\u0644 360\u00B0 (Lock360 v2.3)"
        ""
        "- **\u0627\u0644\u0645\u0635\u062F\u0631 \u0627\u0644\u0645\u0648\u062D\u062F:** ``00-lock360-zero-gaps`` (``~/.gemini/config/skills/00-lock360-zero-gaps/SKILL.md`` \u00B7 ``gist/01-CORE-PROMPT-360-v2.md`` \u00B7 ``workflows/00-lock360-zero-gaps.md``)."
        "- **``L1 Auto-Guard`` (``P`` \u062A\u0644\u0642\u0627\u0626\u064A\u0627\u064B \u0628\u0639\u062F \u0627\u0644\u0623\u0639\u0645\u0627\u0644 \u063A\u064A\u0631 \u0627\u0644\u062A\u0627\u0641\u0647\u0629):** \u0631\u0627\u062C\u0639 \u0627\u0644\u0645\u062A\u0628\u0642\u064A/\u0627\u0644\u062D\u062F\u0648\u062F\u060C \u0623\u0645\u0627\u0646 \u0627\u0644\u062A\u0633\u0644\u064A\u0645 \u0648\u0627\u0644\u062A\u0632\u0627\u0645\u0646\u060C \u0627\u0644\u062F\u0644\u064A\u0644 \u0627\u0644\u0642\u0627\u0637\u0639 \u0628\u0639\u062F \u0622\u062E\u0631 \u062A\u0639\u062F\u064A\u0644\u060C \u0648\u0627\u0633\u0623\u0644 \u0627\u0644\u0645\u0633\u062A\u062E\u062F\u0645 \u0639\u0646 \u0623\u064A \u063A\u0645\u0648\u0636 \u0628\u062F\u0644 \u0627\u0644\u062A\u062E\u0645\u064A\u0646."
        "- **``L2 / L3``:** \u0639\u0646\u062F \u0637\u0644\u0628 \u0642\u0641\u0651\u0644 360 / \u0628\u0627\u0644\u0636\u0628\u0629 \u0648\u0627\u0644\u0645\u0641\u062A\u0627\u062D / 1600\u00B0-10000\u00B0 / ``/lock360`` \u062D\u0645\u0651\u0644 \u0627\u0644\u0645\u0647\u0627\u0631\u0629 \u0648\u0646\u0641\u0651\u0630 \u0627\u0644\u062A\u0631\u0633 \u0627\u0644\u0645\u0646\u0627\u0633\u0628 (``S / M / L``)\u060C \u0645\u0639 \u0627\u0644\u0627\u0644\u062A\u0632\u0627\u0645 \u0628\u0642\u0627\u0639\u062F\u0629 ``RTL-Safe`` (\u0628\u0644\u0627 \u062C\u062F\u0627\u0648\u0644 ``| col |`` \u0641\u064A \u0627\u0644\u0634\u0627\u062A)."
        $EndMarker
    ) -join "`n"
    return [regex]::Unescape($raw)
}

function Update-GeminiMarkerBlock([bool]$RemoveOnly) {
    $existing = ""
    if (Test-Path -LiteralPath $GeminiFile) {
        $existing = [System.IO.File]::ReadAllText($GeminiFile, $Utf8NoBom) -replace "`r`n", "`n"
    } elseif ($RemoveOnly) {
        return
    }
    $sCount = ([regex]::Matches($existing, [regex]::Escape($StartMarker))).Count
    $eCount = ([regex]::Matches($existing, [regex]::Escape($EndMarker))).Count
    if (($sCount -ne $eCount) -or ($sCount -gt 1)) {
        throw "Refusing to modify GEMINI.md: expected 0 or 1 matched LOCK360 marker pair (found start=$sCount end=$eCount)."
    }
    if (Test-Path -LiteralPath $GeminiFile) {
        Copy-Item -LiteralPath $GeminiFile -Destination "$GeminiFile.bak" -Force
    }
    if ($sCount -eq 1) {
        $pattern = "(?s)\n*" + [regex]::Escape($StartMarker) + ".*?" + [regex]::Escape($EndMarker) + "\n*"
        if ($RemoveOnly) {
            $updated = ([regex]::Replace($existing, $pattern, "`n")).TrimEnd() + "`n"
            Write-Utf8Atomic -Path $GeminiFile -Text $updated
            Write-Host "[lock360] Removed LOCK360 block from: $GeminiFile (preserved all other rules)"
        } else {
            $snippet = Build-GeminiSnippet
            $safeRep = ("`n`n" + $snippet + "`n").Replace('$', '$$')
            $updated = [regex]::Replace($existing, $pattern, $safeRep)
            Write-Utf8Atomic -Path $GeminiFile -Text $updated
            Write-Host "[lock360] Updated LOCK360 block in: $GeminiFile"
        }
    } elseif (-not $RemoveOnly) {
        $snippet = Build-GeminiSnippet
        $prefix = if ($existing.Trim()) { $existing.TrimEnd() + "`n`n" } else { "" }
        Write-Utf8Atomic -Path $GeminiFile -Text ($prefix + $snippet + "`n")
        Write-Host "[lock360] Added LOCK360 block to: $GeminiFile"
    }
}

function Assert-GeminiMarkersValid {
    if (-not (Test-Path -LiteralPath $GeminiFile)) { return }
    $txt = [System.IO.File]::ReadAllText($GeminiFile, $Utf8NoBom) -replace "`r`n", "`n"
    $sc = ([regex]::Matches($txt, [regex]::Escape($StartMarker))).Count
    $ec = ([regex]::Matches($txt, [regex]::Escape($EndMarker))).Count
    if (($sc -ne $ec) -or ($sc -gt 1)) {
        throw "Refusing to modify GEMINI.md: expected 0 or 1 matched LOCK360 marker pair (found start=$sc end=$ec)."
    }
}

if ($Uninstall) {
    Assert-GeminiMarkersValid
    if (Test-Path -LiteralPath $SkillDst) {
        $bak = Join-Path $TargetRoot (".backup_lock360_uninstall_" + (Get-Date -Format "yyyyMMdd_HHmmss"))
        New-Item -ItemType Directory -Path $bak -Force | Out-Null
        Copy-Item -LiteralPath $SkillDst -Destination (Join-Path $bak $SkillName) -Recurse -Force
        Write-Host "[lock360] Backed up skill before uninstall (preserves Extension Slots): $bak\$SkillName"
        Remove-Item -LiteralPath $SkillDst -Recurse -Force
        Write-Host "[lock360] Removed skill: $SkillDst"
    }
    if (Test-Path -LiteralPath $WfDst) {
        Remove-Item -LiteralPath $WfDst -Force
        Write-Host "[lock360] Removed workflow: $WfDst"
    }
    Update-GeminiMarkerBlock -RemoveOnly $true
    Write-Host "[lock360] Uninstall complete."
    exit 0
}

if ($All -or $WithRule) {
    Assert-GeminiMarkersValid
}

Copy-SkillPayload -Src $RepoRoot -Dst $SkillDst

if ($All -or $WithWorkflow) {
    $wfSrc = Join-Path (Join-Path $RepoRoot "workflows") "00-lock360-zero-gaps.md"
    if (Test-Path -LiteralPath $wfSrc) {
        if (-not (Test-Path -LiteralPath $WfDstDir)) {
            New-Item -ItemType Directory -Path $WfDstDir -Force | Out-Null
        }
        Copy-Item -LiteralPath $wfSrc -Destination $WfDst -Force
        Write-Host "[lock360] Installed workflow to: $WfDst"
    }
}

if ($All -or $WithRule) {
    Update-GeminiMarkerBlock -RemoveOnly $false
}

Write-Host "[lock360] Done."
