<#
.SYNOPSIS
    Sets up and launches the OpenBB MCP server for the Wealth Management platform.

.DESCRIPTION
    1. Creates a Python virtual environment (if not already present)
    2. Installs openbb[all] into the venv
    3. Loads API keys from the project-root .env file
    4. Starts the OpenBB MCP server on 127.0.0.1:8080
#>

$ErrorActionPreference = "Stop"

# --- Paths ---
$SkillDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Resolve-Path (Join-Path $SkillDir "..\..\..") 
$VenvDir    = Join-Path $SkillDir ".venv"
$EnvFile    = Join-Path $ProjectRoot ".env"

Write-Host "=== OpenBB MCP Server Setup ===" -ForegroundColor Cyan
Write-Host "Skill directory : $SkillDir"
Write-Host "Project root    : $ProjectRoot"
Write-Host ""

# --- Step 1: Create virtual environment ---
if (-not (Test-Path (Join-Path $VenvDir "Scripts\Activate.ps1"))) {
    Write-Host "[1/4] Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv $VenvDir
} else {
    Write-Host "[1/4] Virtual environment already exists." -ForegroundColor Green
}

# --- Step 2: Activate virtual environment ---
Write-Host "[2/4] Activating virtual environment..." -ForegroundColor Yellow
& (Join-Path $VenvDir "Scripts\Activate.ps1")

# --- Step 3: Install dependencies ---
Write-Host "[3/4] Installing openbb[all]... (this may take a few minutes)" -ForegroundColor Yellow
pip install --quiet --upgrade pip
pip install --quiet "openbb[all]"

# --- Step 4: Load API keys from .env ---
if (Test-Path $EnvFile) {
    Write-Host "[4/4] Loading API keys from .env..." -ForegroundColor Yellow
    Get-Content $EnvFile | ForEach-Object {
        $line = $_.Trim()
        # Skip empty lines and comments
        if ($line -and -not $line.StartsWith("#")) {
            $parts = $line -split "=", 2
            if ($parts.Count -eq 2) {
                $key   = $parts[0].Trim()
                $value = $parts[1].Trim().Trim('"').Trim("'")
                [System.Environment]::SetEnvironmentVariable($key, $value, "Process")
                Write-Host "  Loaded: $key" -ForegroundColor DarkGray
            }
        }
    }
} else {
    Write-Host "[4/4] WARNING: No .env file found at $EnvFile" -ForegroundColor Red
    Write-Host "       Create a .env file with your API keys (e.g., OPENBB_TOKEN, FMP_API_KEY)" -ForegroundColor Red
}

# --- Launch MCP Server ---
Write-Host ""
Write-Host "=== Launching OpenBB MCP Server ===" -ForegroundColor Cyan
Write-Host "  Host : 127.0.0.1"
Write-Host "  Port : 8080"
Write-Host "  Categories : equity, news"
Write-Host "  Endpoint : http://127.0.0.1:8080/mcp/"
Write-Host ""

openbb-mcp --allowed-categories equity,news --host 127.0.0.1 --port 8080
