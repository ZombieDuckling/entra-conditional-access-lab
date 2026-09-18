<#
.SYNOPSIS
Exports Conditional Access policies with read-only Microsoft Graph scopes.
#>
param(
    [Parameter(Mandatory = $false)]
    [string]$OutputPath = "./exports/current-ca-policies.json"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Module -ListAvailable -Name Microsoft.Graph.Identity.SignIns)) {
    throw "Microsoft.Graph.Identity.SignIns module is required. Install it outside this script after approval."
}

$context = Get-MgContext
if (-not $context) {
    throw "Connect to Graph first with: Connect-MgGraph -Scopes 'Policy.Read.All','Directory.Read.All'"
}

$directory = Split-Path -Parent $OutputPath
if ($directory -and -not (Test-Path $directory)) {
    New-Item -ItemType Directory -Path $directory | Out-Null
}

$policies = Get-MgIdentityConditionalAccessPolicy -All
$policies | ConvertTo-Json -Depth 20 | Set-Content -Path $OutputPath -Encoding UTF8
Write-Host "Exported $($policies.Count) policies to $OutputPath"
