# merge_project.ps1
# Script PowerShell para juntar todo o projeto num único arquivo de texto, sem parâmetros.

# Define o diretório raiz do projeto (diretório onde o script está localizado)
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Define o caminho do arquivo de saída com timeStamp no diretorio output se não existir criar o diretorio
$OutputDir = Join-Path $ProjectRoot "output"
If (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}
$OutputFile = Join-Path $OutputDir ("projeto_" + (Get-Date -Format "yyyyMMdd_HHmmss") + ".txt")

# Extensões de arquivo a incluir na união
$Include = @("*.ps1", "*.py", "*.md")

# Diretórios a excluir
$Exclude = @('.git', '.venv')

Function Get-SourceFiles {
    Get-ChildItem $ProjectRoot -Recurse -File `
      -Include $Include `
      -Exclude $Exclude |
    Sort-Object FullName
}

Function Write-FileHeader {
    Param($File)
    Add-Content $OutputFile ""
    Add-Content $OutputFile ("#".PadRight(60,'='))
    Add-Content $OutputFile "# File: $($File.FullName.Substring($ProjectRoot.Length + 1))"
    Add-Content $OutputFile ("#".PadRight(60,'='))
}

Function Append-FileContent {
    Param($File)
    Try {
        $text = Get-Content $File -Raw -ErrorAction Stop
        Add-Content $OutputFile $text -Encoding UTF8
    } Catch {
        Write-Warning "Falha ao ler $($File): $_"
    }
}

# Remove o arquivo de saída antigo, se existir
If (Test-Path $OutputFile) {
    Remove-Item $OutputFile
}

# Coleta e mescla os arquivos
$files = Get-SourceFiles
$total = $files.Count
for ($i = 0; $i -lt $total; $i++) {
    $f = $files[$i]
    Write-Progress -Activity "Juntando arquivos" `
      -Status "$(($i+1)) / $total" `
      -PercentComplete (((($i+1)/$total)*100))
    Write-FileHeader $f
    Append-FileContent $f
}

Write-Host "Arquivo gerado em $OutputFile"
