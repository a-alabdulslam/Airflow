Write-Host "Creating Airflow Connections" -ForegroundColor Yellow

$file = '.\connections.json'
$contents = Get-Content -Raw -Encoding UTF8 -Path $file | ConvertFrom-Json

foreach ($obj in $contents.PSObject.Properties) {
    $conn_name = $obj.Name
    $result = docker exec airflow-airflow-webserver-1 airflow connections get $conn_name

    if ([string]::IsNullOrEmpty($result)) {
        Write-Host "Adding connection $conn_name" -ForegroundColor Green

        $connJson = $obj.Value | ConvertTo-Json
        
        docker exec airflow-airflow-webserver-1 airflow connections add $conn_name --conn-json $connJson.Replace('"', '\"')
    }
    else {
        Write-Host "Variable $conn_name is already there. Skipping insertion ..." -ForegroundColor Blue
    }
}