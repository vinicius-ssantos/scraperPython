# juntar_projeto_em_txt.ps1

# Criar pasta output/ se não existir
$outputFolder = "output"
if (!(Test-Path -Path $outputFolder)) {
    New-Item -ItemType Directory -Path $outputFolder | Out-Null
}

# Gerar timestamp
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"

# Nome do arquivo final
$outputFile = "$outputFolder/projeto_amazon_scraper_$timestamp.txt"

# Padrões de arquivos para juntar
$patterns = @("*.py", "*.yml", "*.txt")

Write-Host "🔧 Juntando arquivos..."

foreach ($pattern in $patterns) {
    Get-ChildItem -Path . -Recurse -Filter $pattern | Where-Object {
        # Ignorar pastas output, logs, .venv, .idea
        $_.FullName -notmatch "\\(output|logs|\\.venv|\\.idea)\\"
    } | ForEach-Object {
        Add-Content -Path $outputFile -Value ("`n# ===== Arquivo: " + $_.FullName + " =====`n")
        Get-Content $_.FullName | Add-Content -Path $outputFile
        Add-Content -Path $outputFile -Value ("`n# ===== Fim do arquivo: " + $_.FullName + " =====`n")
        Add-Content -Path $outputFile -Value ("`n`n---`n")
    }
}

Write-Host "Arquivo $outputFile gerado com sucesso!"
