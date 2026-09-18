<#
.SYNOPSIS
Compares a reviewed Conditional Access policy pack with a current export.
#>
param(
    [Parameter(Mandatory = $true)]
    [string]$BaselinePath,

    [Parameter(Mandatory = $true)]
    [string]$CurrentPath
)

$ErrorActionPreference = "Stop"

$baseline = Get-Content -Raw -Path $BaselinePath | ConvertFrom-Json
$current = Get-Content -Raw -Path $CurrentPath | ConvertFrom-Json

$baselineNames = @($baseline.policies | ForEach-Object { $_.displayName })
$currentNames = @($current | ForEach-Object { $_.displayName })

$missingFromCurrent = $baselineNames | Where-Object { $_ -notin $currentNames }
$unexpectedCurrent = $currentNames | Where-Object { $_ -notin $baselineNames }

[PSCustomObject]@{
    BaselineCount = $baselineNames.Count
    CurrentCount = $currentNames.Count
    MissingFromCurrent = $missingFromCurrent
    UnexpectedCurrent = $unexpectedCurrent
} | ConvertTo-Json -Depth 5
