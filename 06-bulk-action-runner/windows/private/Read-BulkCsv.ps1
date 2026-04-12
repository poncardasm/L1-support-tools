<#
.SYNOPSIS
    Parses a CSV file and validates required columns.

.DESCRIPTION
    Reads a CSV file and ensures it contains the 'email' column.
    Supports both comma and semicolon delimiters.

.PARAMETER CsvPath
    Path to the CSV file.

.PARAMETER RequiredColumns
    Array of column names that must exist in the CSV.

.EXAMPLE
    $users = Read-BulkCsv -CsvPath "users.csv"
#>
function Read-BulkCsv {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$CsvPath,
        
        [string[]]$RequiredColumns = @('email')
    )
    
    # Verify file exists
    if (-not (Test-Path -Path $CsvPath)) {
        throw "CSV file not found: $CsvPath"
    }
    
    # Try comma delimiter first, then semicolon
    $users = $null
    $delimiters = @(',', ';')
    
    foreach ($delimiter in $delimiters) {
        try {
            $users = Import-Csv -Path $CsvPath -Delimiter $delimiter -ErrorAction Stop
            if ($users -and $users.Count -gt 0) {
                break
            }
        }
        catch {
            continue
        }
    }
    
    if (-not $users) {
        throw "Failed to parse CSV file: $CsvPath"
    }
    
    # Validate required columns
    if ($users.Count -gt 0) {
        $firstRow = $users | Select-Object -First 1
        $actualColumns = $firstRow.PSObject.Properties.Name
        
        foreach ($column in $RequiredColumns) {
            if ($actualColumns -notcontains $column) {
                throw "Required column '$column' not found in CSV. Available columns: $($actualColumns -join ', ')"
            }
        }
    }
    
    # Validate email format for each row
    $emailRegex = '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    $invalidRows = @()
    
    foreach ($user in $users) {
        if ($user.email -notmatch $emailRegex) {
            $invalidRows += "Row with email '$($user.email)' has invalid format"
        }
    }
    
    if ($invalidRows.Count -gt 0) {
        throw "Invalid email format found:`n$($invalidRows -join "`n")"
    }
    
    return $users
}
