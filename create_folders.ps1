# create_folders.ps1
# Script PowerShell para criar as pastas necessárias no disco D:

# Defina o usuário conforme seu perfil
$UserName = "Vinicius"

# Lista de caminhos a serem criados
$paths = @(
    "D:\Users\$UserName\AppData\Local\Programs",
    "D:\Users\$UserName\AppData\Local\JetBrains\Toolbox\scripts"
)

foreach ($p in $paths) {
    if (-not (Test-Path -Path $p)) {
        New-Item -ItemType Directory -Path $p -Force | Out-Null
        Write-Host "Criado: $p"
    } else {
        Write-Host "Já existe: $p"
    }
}
