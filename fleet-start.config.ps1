# Per-repo fleet start config for sdr-mcp
# Three ports: Vite 10890, MCP HTTP 10891, REST web_api 10892 (/api/health).
# Edit ports/backend target here - start.ps1 is fleet-standard.
@{
    Name         = 'sdr-mcp'
    BackendPort  = 10892
    FrontendPort = 10890
    HealthPath   = '/api/health'
    WebRoot      = 'D:\Dev\repos\sdr-mcp\web_sota'
    Backend = @{
        Kind       = 'custom'
        WorkDir    = 'D:\Dev\repos\sdr-mcp'
        SyncExtras = @('dev')
        Command    = "foreach (`$p in 10891, 10892) { Get-NetTCPConnection -LocalPort `$p -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id `$_.OwningProcess -Force -ErrorAction SilentlyContinue } }; uv run sdr-mcp serve --http --port 10891 --host 127.0.0.1 --web-api-port 10892"
    }
    Frontend = @{
        Kind           = 'vite-npm'
        PackageManager = 'npm'
        PortEnvVar     = 'VITE_PORT'
        ApiTargetEnv   = 'VITE_API_TARGET'
    }
}
