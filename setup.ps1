param(
    [string]$VenvPath = ".venv"
)

$ErrorActionPreference = "Stop"

function Get-PythonCommand {
    $commands = @("python", "py")

    foreach ($command in $commands) {
        $resolved = Get-Command $command -ErrorAction SilentlyContinue
        if ($null -eq $resolved) {
            continue
        }

        try {
            & $command --version *> $null
            if ($LASTEXITCODE -eq 0) {
                return $command
            }
        }
        catch {
            continue
        }
    }

    throw "Python not installed"
}

$python = Get-PythonCommand
$venvPython = Join-Path $VenvPath "Scripts\python.exe"

Write-Host "Using Python: $python"

if (-not (Test-Path $venvPython)) {
    Write-Host "Creating virtual environment: $VenvPath..."
    & $python -m venv $VenvPath
}
else {
    Write-Host "Virtual environment already exist: $VenvPath"
}

Write-Host "Updating pip..."
& $venvPython -m pip install --upgrade pip

Write-Host "Installing dependencies..."
& $venvPython -m pip install -r requirements.txt

Write-Host ""
Write-Host "Done."
Write-Host "Activate Virtual Enviroment:"
Write-Host "  .\$VenvPath\Scripts\Activate.ps1"
Write-Host ""
Write-Host "Run with:"
Write-Host "  python overlay.py"
Write-Host ""
Write-Host "Or run without activate:"
Write-Host "  .\$VenvPath\Scripts\python.exe overlay.py"
