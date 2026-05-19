param(
    [ValidateSet("Debug", "Release")]
    [string]$Variant = "Debug"
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$AndroidDir = (Resolve-Path (Join-Path $ScriptDir "..")).Path
$ProjectRoot = (Resolve-Path (Join-Path $AndroidDir "..")).Path
$DistDir = Join-Path $ProjectRoot "dist"
$VariantLower = $Variant.ToLowerInvariant()

New-Item -ItemType Directory -Force -Path $DistDir | Out-Null

$GradleWrapper = Join-Path $AndroidDir "gradlew.bat"
if (Test-Path $GradleWrapper) {
    $Command = $GradleWrapper
    $Arguments = @(":app:assemble$Variant")
} else {
    $GradleCommand = Get-Command "gradle" -ErrorAction SilentlyContinue
    if (-not $GradleCommand) {
        throw "未找到 Gradle。建议优先使用 GitHub Actions 云端打包，或安装 Android Studio/Gradle 后再运行本脚本。"
    }

    $Command = $GradleCommand.Source
    $Arguments = @("-p", $AndroidDir, ":app:assemble$Variant")
}

Write-Host "=== Build MyGames Android $Variant APK ==="
& $Command @Arguments

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

$ApkDir = Join-Path $AndroidDir "app/build/outputs/apk/$VariantLower"
$Apk = Get-ChildItem -Path $ApkDir -Filter "*.apk" | Select-Object -First 1
if (-not $Apk) {
    throw "构建完成但未找到 APK：$ApkDir"
}

$Output = Join-Path $DistDir "MyGames-android-$VariantLower.apk"
Copy-Item -LiteralPath $Apk.FullName -Destination $Output -Force

Write-Host "=== Done: $Output ==="
