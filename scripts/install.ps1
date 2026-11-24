[CmdletBinding()]
param(
    [switch]$All,
    [switch]$WithWorkflow,
    [switch]$WithRule,
    [switch]$WithPack,
    [switch]$OpenCode,
    [switch]$Uninstall,
    [string]$TargetRoot = (Join-Path $HOME ".gemini"),
    [string]$OpenCodeRoot = $(if ($env:XDG_CONFIG_HOME) { Join-Path $env:XDG_CONFIG_HOME "opencode" } else { Join-Path (Join-Path $HOME ".config") "opencode" })
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$SkillName = "00-lock360-zero-gaps"
$SkillDst = Join-Path (Join-Path (Join-Path $TargetRoot "config") "skills") $SkillName
$WfDstDir = Join-Path (Join-Path $TargetRoot "config") "workflows"
$WfDst = Join-Path $WfDstDir "00-lock360-zero-gaps.md"
$GeminiFile = Join-Path $TargetRoot "GEMINI.md"
$OcSkillDst = Join-Path (Join-Path $OpenCodeRoot "skills") $SkillName
$OcAgentsFile = Join-Path $OpenCodeRoot "AGENTS.md"
$StartMarker = "<!-- LOCK360_START -->"
$EndMarker = "<!-- LOCK360_END -->"
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

Write-Host "[lock360] TargetRoot: $TargetRoot"
if ($OpenCode) { Write-Host "[lock360] OpenCodeRoot: $OpenCodeRoot" }

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

# Skill payload = SKILL.md, README.md, gist/, references/, prompts/, scripts/lock360.py only
# (never verify_repo.py nor the installers). Existing install is backed up under $BackupRoot first.
function Copy-SkillPayload([string]$Src, [string]$Dst, [string]$BackupRoot, [string]$BackupPrefix) {
    if (Test-Path -LiteralPath $Dst) {
        $bak = Join-Path $BackupRoot ($BackupPrefix + (Get-Date -Format "yyyyMMdd_HHmmss"))
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
    foreach ($d in @("gist", "references", "prompts")) {
        $sd = Join-Path $Src $d
        $dd = Join-Path $Dst $d
        if (Test-Path -LiteralPath $dd) { Remove-Item -LiteralPath $dd -Recurse -Force }
        if (Test-Path -LiteralPath $sd) {
            Copy-Item -LiteralPath $sd -Destination $dd -Recurse -Force
        }
    }
    $engineSrc = Join-Path (Join-Path $Src "scripts") "lock360.py"
    $engineDir = Join-Path $Dst "scripts"
    if (Test-Path -LiteralPath $engineDir) { Remove-Item -LiteralPath $engineDir -Recurse -Force }
    if (Test-Path -LiteralPath $engineSrc) {
        New-Item -ItemType Directory -Path $engineDir -Force | Out-Null
        Copy-Item -LiteralPath $engineSrc -Destination (Join-Path $engineDir "lock360.py") -Force
    }
    Write-Host "[lock360] Installed skill to: $Dst"
}

function Get-SnippetSkillPath([string]$Root, [string]$DefaultRoot, [string]$PortablePrefix, [string]$AbsoluteSkillDir) {
    $a = ([string]$Root).TrimEnd('\', '/')
    $b = ([string]$DefaultRoot).TrimEnd('\', '/')
    if ([string]::Equals($a, $b, [System.StringComparison]::OrdinalIgnoreCase)) {
        return ($PortablePrefix + $SkillName + "/SKILL.md")
    }
    return (Join-Path $AbsoluteSkillDir "SKILL.md")
}

function Build-Snippet([string]$SkillPath) {
    # Literal lines are Unescape'd FIRST; the runtime skill path is concatenated AFTER (never passed through Unescape).
    $head = [regex]::Unescape("## \uD83D\uDD12 \u0628\u0631\u0648\u062A\u0648\u0643\u0648\u0644 \u0627\u0644\u062A\u0642\u0641\u064A\u0644 \u0627\u0644\u0634\u0627\u0645\u0644 360\u00B0 (Lock360 v2.8)")
    $srcA = [regex]::Unescape("- **\u0627\u0644\u0645\u0635\u062F\u0631 \u0627\u0644\u0645\u0648\u062D\u062F:** ``00-lock360-zero-gaps`` (``")
    $srcB = [regex]::Unescape("`` \u00B7 ``gist/01-CORE-PROMPT-360-v2.md`` \u00B7 ``workflows/00-lock360-zero-gaps.md``).")
    $tail = @(
        "- **``L1 Auto-Guard`` (``P`` \u062A\u0644\u0642\u0627\u0626\u064A\u0627\u064B \u0628\u0639\u062F \u0627\u0644\u0623\u0639\u0645\u0627\u0644 \u063A\u064A\u0631 \u0627\u0644\u062A\u0627\u0641\u0647\u0629):** \u0631\u0627\u062C\u0639 \u0627\u0644\u0645\u062A\u0628\u0642\u064A/\u0627\u0644\u062D\u062F\u0648\u062F\u060C \u0623\u0645\u0627\u0646 \u0627\u0644\u062A\u0633\u0644\u064A\u0645 \u0648\u0627\u0644\u062A\u0632\u0627\u0645\u0646\u060C \u0627\u0644\u062F\u0644\u064A\u0644 \u0627\u0644\u0642\u0627\u0637\u0639 \u0628\u0639\u062F \u0622\u062E\u0631 \u062A\u0639\u062F\u064A\u0644\u060C \u0648\u0627\u0633\u0623\u0644 \u0627\u0644\u0645\u0633\u062A\u062E\u062F\u0645 \u0639\u0646 \u0623\u064A \u063A\u0645\u0648\u0636 \u0628\u062F\u0644 \u0627\u0644\u062A\u062E\u0645\u064A\u0646."
        "- **``L2 / L3``:** \u0639\u0646\u062F \u0637\u0644\u0628 \u0642\u0641\u0651\u0644 360 / \u0628\u0627\u0644\u0636\u0628\u0629 \u0648\u0627\u0644\u0645\u0641\u062A\u0627\u062D / 1600\u00B0-10000\u00B0 / ``/lock360`` \u062D\u0645\u0651\u0644 \u0627\u0644\u0645\u0647\u0627\u0631\u0629 \u0648\u0646\u0641\u0651\u0630 \u0627\u0644\u062A\u0631\u0633 \u0627\u0644\u0645\u0646\u0627\u0633\u0628 (``S / M / L``)\u060C \u0648\u0645\u0631\u0651\u0631 \u0627\u0644\u0645\u062E\u0631\u062C \u0639\u0644\u0649 ``scripts/lock360.py audit`` \u0642\u0628\u0644 \u0627\u0644\u0625\u063A\u0644\u0627\u0642\u060C \u0645\u0639 \u0627\u0644\u0627\u0644\u062A\u0632\u0627\u0645 \u0628\u0642\u0627\u0639\u062F\u0629 ``RTL-Safe`` (\u0628\u0644\u0627 \u062C\u062F\u0627\u0648\u0644 ``| col |`` \u0641\u064A \u0627\u0644\u0634\u0627\u062A)."
    ) -join "`n"
    $tailText = [regex]::Unescape($tail)
    $lines = @(
        $StartMarker
        $head
        ""
        ($srcA + $SkillPath + $srcB)
        $tailText
        $EndMarker
    )
    return ($lines -join "`n")
}

# Shared for GEMINI.md and OpenCode AGENTS.md: only the LOCK360 marker block is touched; every other line is preserved.
function Update-MarkerBlock([string]$File, [bool]$RemoveOnly, [string]$SkillPath) {
    $existing = ""
    if (Test-Path -LiteralPath $File) {
        $existing = [System.IO.File]::ReadAllText($File, $Utf8NoBom) -replace "`r`n", "`n"
    } elseif ($RemoveOnly) {
        return
    }
    $sCount = ([regex]::Matches($existing, [regex]::Escape($StartMarker))).Count
    $eCount = ([regex]::Matches($existing, [regex]::Escape($EndMarker))).Count
    if (($sCount -ne $eCount) -or ($sCount -gt 1)) {
        throw "Refusing to modify ${File}: expected 0 or 1 matched LOCK360 marker pair (found start=$sCount end=$eCount)."
    }
    if (Test-Path -LiteralPath $File) {
        Copy-Item -LiteralPath $File -Destination "$File.bak" -Force
    }
    if ($sCount -eq 1) {
        $pattern = "(?s)\n*" + [regex]::Escape($StartMarker) + ".*?" + [regex]::Escape($EndMarker) + "\n*"
        if ($RemoveOnly) {
            $updated = ([regex]::Replace($existing, $pattern, "`n")).TrimEnd() + "`n"
            Write-Utf8Atomic -Path $File -Text $updated
            Write-Host "[lock360] Removed LOCK360 block from: $File (preserved all other lines)"
        } else {
            $snippet = Build-Snippet -SkillPath $SkillPath
            $safeRep = ("`n`n" + $snippet + "`n").Replace('$', '$$')
            $updated = [regex]::Replace($existing, $pattern, $safeRep)
            Write-Utf8Atomic -Path $File -Text $updated
            Write-Host "[lock360] Updated LOCK360 block in: $File"
        }
    } elseif (-not $RemoveOnly) {
        $snippet = Build-Snippet -SkillPath $SkillPath
        $prefix = if ($existing.Trim()) { $existing.TrimEnd() + "`n`n" } else { "" }
        Write-Utf8Atomic -Path $File -Text ($prefix + $snippet + "`n")
        Write-Host "[lock360] Added LOCK360 block to: $File"
    }
}

function Assert-MarkersValid([string]$File) {
    if (-not (Test-Path -LiteralPath $File)) { return }
    $txt = [System.IO.File]::ReadAllText($File, $Utf8NoBom) -replace "`r`n", "`n"
    $sc = ([regex]::Matches($txt, [regex]::Escape($StartMarker))).Count
    $ec = ([regex]::Matches($txt, [regex]::Escape($EndMarker))).Count
    if (($sc -ne $ec) -or ($sc -gt 1)) {
        throw "Refusing to modify ${File}: expected 0 or 1 matched LOCK360 marker pair (found start=$sc end=$ec)."
    }
}

$GeminiSnippetPath = Get-SnippetSkillPath -Root $TargetRoot -DefaultRoot (Join-Path $HOME ".gemini") -PortablePrefix "~/.gemini/config/skills/" -AbsoluteSkillDir $SkillDst
$OcSnippetPath = Get-SnippetSkillPath -Root $OpenCodeRoot -DefaultRoot (Join-Path (Join-Path $HOME ".config") "opencode") -PortablePrefix "~/.config/opencode/skills/" -AbsoluteSkillDir $OcSkillDst

$PackRoot = Join-Path $RepoRoot "skills-pack"

function Copy-PackPayload {
    if (-not (Test-Path -LiteralPath $PackRoot)) {
        throw "skills-pack directory not found at: $PackRoot"
    }
    $skillsDstRoot = Join-Path (Join-Path $TargetRoot "config") "skills"
    $rulesDstRoot = Join-Path (Join-Path $TargetRoot "config") "rules"
    $bakRoot = Join-Path $TargetRoot (".backup_lock360_pack_" + (Get-Date -Format "yyyyMMdd_HHmmss"))
    $bakCreated = $false
    $ensureBak = {
        param([string]$Sub)
        $p = Join-Path $bakRoot $Sub
        if (-not (Test-Path -LiteralPath $p)) {
            New-Item -ItemType Directory -Path $p -Force | Out-Null
        }
        return $p
    }

    $packSkillsDir = Join-Path $PackRoot "skills"
    $skillCount = 0
    if (Test-Path -LiteralPath $packSkillsDir) {
        if (-not (Test-Path -LiteralPath $skillsDstRoot)) {
            New-Item -ItemType Directory -Path $skillsDstRoot -Force | Out-Null
        }
        foreach ($dir in Get-ChildItem -LiteralPath $packSkillsDir -Directory) {
            $dst = Join-Path $skillsDstRoot $dir.Name
            if (Test-Path -LiteralPath $dst) {
                $bdir = & $ensureBak "skills"
                $bakCreated = $true
                Copy-Item -LiteralPath $dst -Destination (Join-Path $bdir $dir.Name) -Recurse -Force
                Remove-Item -LiteralPath $dst -Recurse -Force
            }
            Copy-Item -LiteralPath $dir.FullName -Destination $dst -Recurse -Force
            $skillCount++
        }
    }

    $packWfDir = Join-Path $PackRoot "workflows"
    $wfCount = 0
    if (Test-Path -LiteralPath $packWfDir) {
        if (-not (Test-Path -LiteralPath $WfDstDir)) {
            New-Item -ItemType Directory -Path $WfDstDir -Force | Out-Null
        }
        foreach ($f in Get-ChildItem -LiteralPath $packWfDir -File) {
            $dst = Join-Path $WfDstDir $f.Name
            if (Test-Path -LiteralPath $dst) {
                $bdir = & $ensureBak "workflows"
                $bakCreated = $true
                Copy-Item -LiteralPath $dst -Destination (Join-Path $bdir $f.Name) -Force
            }
            Copy-Item -LiteralPath $f.FullName -Destination $dst -Force
            $wfCount++
        }
    }

    $packRulesDir = Join-Path $PackRoot "rules"
    $ruleCount = 0
    if (Test-Path -LiteralPath $packRulesDir) {
        if (-not (Test-Path -LiteralPath $rulesDstRoot)) {
            New-Item -ItemType Directory -Path $rulesDstRoot -Force | Out-Null
        }
        foreach ($f in Get-ChildItem -LiteralPath $packRulesDir -File) {
            $dst = Join-Path $rulesDstRoot $f.Name
            if (Test-Path -LiteralPath $dst) {
                $bdir = & $ensureBak "rules"
                $bakCreated = $true
                Copy-Item -LiteralPath $dst -Destination (Join-Path $bdir $f.Name) -Force
            }
            Copy-Item -LiteralPath $f.FullName -Destination $dst -Force
            $ruleCount++
        }
    }

    if ($bakCreated) {
        Write-Host "[lock360] Backed up existing pack targets to: $bakRoot"
    }
    Write-Host "[lock360] Installed skills-pack: skills=$skillCount workflows=$wfCount rules=$ruleCount"

    if ($All -or $WithRule) {
        $tpl = Join-Path $PackRoot "GEMINI.template.md"
        if (Test-Path -LiteralPath $tpl) {
            if (-not (Test-Path -LiteralPath $GeminiFile)) {
                $tplTxt = [System.IO.File]::ReadAllText($tpl, $Utf8NoBom)
                Write-Utf8Atomic -Path $GeminiFile -Text $tplTxt
                Write-Host "[lock360] Seeded new GEMINI.md from sanitized skills-pack/GEMINI.template.md"
            } else {
                Write-Host "[lock360] Existing GEMINI.md preserved (sanitized template available at skills-pack/GEMINI.template.md)"
            }
        }
    }
}

function Remove-PackPayload {
    if (-not (Test-Path -LiteralPath $PackRoot)) {
        Write-Host "[lock360] Warning: skills-pack not found in repo; skipping pack uninstall."
        return
    }
    $skillsDstRoot = Join-Path (Join-Path $TargetRoot "config") "skills"
    $rulesDstRoot = Join-Path (Join-Path $TargetRoot "config") "rules"
    $bakRoot = Join-Path $TargetRoot (".backup_lock360_pack_uninstall_" + (Get-Date -Format "yyyyMMdd_HHmmss"))
    $bakCreated = $false
    $ensureBak = {
        param([string]$Sub)
        $p = Join-Path $bakRoot $Sub
        if (-not (Test-Path -LiteralPath $p)) {
            New-Item -ItemType Directory -Path $p -Force | Out-Null
        }
        return $p
    }

    $packSkillsDir = Join-Path $PackRoot "skills"
    if (Test-Path -LiteralPath $packSkillsDir) {
        foreach ($dir in Get-ChildItem -LiteralPath $packSkillsDir -Directory) {
            $dst = Join-Path $skillsDstRoot $dir.Name
            if (Test-Path -LiteralPath $dst) {
                $bdir = & $ensureBak "skills"
                $bakCreated = $true
                Copy-Item -LiteralPath $dst -Destination (Join-Path $bdir $dir.Name) -Recurse -Force
                Remove-Item -LiteralPath $dst -Recurse -Force
            }
        }
    }

    $packWfDir = Join-Path $PackRoot "workflows"
    if (Test-Path -LiteralPath $packWfDir) {
        foreach ($f in Get-ChildItem -LiteralPath $packWfDir -File) {
            $dst = Join-Path $WfDstDir $f.Name
            if (Test-Path -LiteralPath $dst) {
                $bdir = & $ensureBak "workflows"
                $bakCreated = $true
                Copy-Item -LiteralPath $dst -Destination (Join-Path $bdir $f.Name) -Force
                Remove-Item -LiteralPath $dst -Force
            }
        }
    }

    $packRulesDir = Join-Path $PackRoot "rules"
    if (Test-Path -LiteralPath $packRulesDir) {
        foreach ($f in Get-ChildItem -LiteralPath $packRulesDir -File) {
            $dst = Join-Path $rulesDstRoot $f.Name
            if (Test-Path -LiteralPath $dst) {
                $bdir = & $ensureBak "rules"
                $bakCreated = $true
                Copy-Item -LiteralPath $dst -Destination (Join-Path $bdir $f.Name) -Force
                Remove-Item -LiteralPath $dst -Force
            }
        }
    }

    if ($bakCreated) {
        Write-Host "[lock360] Backed up and removed skills-pack targets (backup: $bakRoot)"
    }
}

# OpenCode: skill under <root>\skills\<name>, marker block in <root>\AGENTS.md. opencode.json / cli.json are never read or written.
function Install-OpenCode {
    Assert-MarkersValid -File $OcAgentsFile
    Copy-SkillPayload -Src $RepoRoot -Dst $OcSkillDst -BackupRoot $OpenCodeRoot -BackupPrefix ".backup_lock360_opencode_"
    Update-MarkerBlock -File $OcAgentsFile -RemoveOnly $false -SkillPath $OcSnippetPath
    Write-Host "[lock360] OpenCode install complete (opencode.json / cli.json untouched)."
}

function Remove-OpenCode {
    Assert-MarkersValid -File $OcAgentsFile
    if (Test-Path -LiteralPath $OcSkillDst) {
        $bak = Join-Path $OpenCodeRoot (".backup_lock360_opencode_uninstall_" + (Get-Date -Format "yyyyMMdd_HHmmss"))
        New-Item -ItemType Directory -Path $bak -Force | Out-Null
        Copy-Item -LiteralPath $OcSkillDst -Destination (Join-Path $bak $SkillName) -Recurse -Force
        Write-Host "[lock360] Backed up OpenCode skill before uninstall: $bak\$SkillName"
        Remove-Item -LiteralPath $OcSkillDst -Recurse -Force
        Write-Host "[lock360] Removed OpenCode skill: $OcSkillDst"
    }
    Update-MarkerBlock -File $OcAgentsFile -RemoveOnly $true -SkillPath $OcSnippetPath
}

if ($Uninstall) {
    Assert-MarkersValid -File $GeminiFile
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
    if ($WithPack) {
        Remove-PackPayload
    }
    if ($OpenCode) {
        Remove-OpenCode
    }
    Update-MarkerBlock -File $GeminiFile -RemoveOnly $true -SkillPath $GeminiSnippetPath
    Write-Host "[lock360] Uninstall complete."
    exit 0
}

if ($All -or $WithRule) {
    Assert-MarkersValid -File $GeminiFile
}
if ($OpenCode) {
    Assert-MarkersValid -File $OcAgentsFile
}

Copy-SkillPayload -Src $RepoRoot -Dst $SkillDst -BackupRoot $TargetRoot -BackupPrefix ".backup_lock360_"

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

if ($WithPack) {
    Copy-PackPayload
}

if ($OpenCode) {
    Install-OpenCode
}

if ($All -or $WithRule) {
    Update-MarkerBlock -File $GeminiFile -RemoveOnly $false -SkillPath $GeminiSnippetPath
}

Write-Host "[lock360] Done."
