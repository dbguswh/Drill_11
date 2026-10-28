Add-Type -AssemblyName System.Drawing

$width = 1100
$height = 650
$bitmap = [System.Drawing.Bitmap]::new($width, $height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
$graphics.Clear([System.Drawing.Color]::White)

$dark = [System.Drawing.Color]::FromArgb(31, 41, 55)
$blue = [System.Drawing.Color]::FromArgb(18, 111, 177)
$orange = [System.Drawing.Color]::FromArgb(220, 89, 0)
$green = [System.Drawing.Color]::FromArgb(35, 135, 91)
$gray = [System.Drawing.Color]::FromArgb(90, 102, 115)
$titleFont = [System.Drawing.Font]::new('Malgun Gothic', 25, [System.Drawing.FontStyle]::Bold)
$stateFont = [System.Drawing.Font]::new('Malgun Gothic', 20, [System.Drawing.FontStyle]::Bold)
$detailFont = [System.Drawing.Font]::new('Malgun Gothic', 12)
$labelFont = [System.Drawing.Font]::new('Malgun Gothic', 14, [System.Drawing.FontStyle]::Bold)
$titleBrush = [System.Drawing.SolidBrush]::new($dark)
$detailBrush = [System.Drawing.SolidBrush]::new($gray)
$labelBrush = [System.Drawing.SolidBrush]::new($dark)

function Draw-State([string]$name, [string]$detail, [float]$x, [float]$y,
                    [float]$w, [float]$h, [System.Drawing.Color]$border,
                    [System.Drawing.Color]$fill) {
    $fillBrush = [System.Drawing.SolidBrush]::new($fill)
    $outline = [System.Drawing.Pen]::new($border, 3)
    $rect = [System.Drawing.RectangleF]::new($x, $y, $w, $h)
    $graphics.FillRectangle($fillBrush, $rect)
    $graphics.DrawRectangle($outline, $x, $y, $w, $h)
    $graphics.DrawString($name, $stateFont, $titleBrush, $x + 18, $y + 12)
    $graphics.DrawString($detail, $detailFont, $detailBrush, $x + 18, $y + 53)
    $outline.Dispose()
    $fillBrush.Dispose()
}

function Draw-Arrow([System.Drawing.PointF[]]$points, [System.Drawing.Color]$color) {
    $pen = [System.Drawing.Pen]::new($color, 3)
    $graphics.DrawLines($pen, $points)
    $last = $points[$points.Length - 1]
    $previous = $points[$points.Length - 2]
    $dx = $last.X - $previous.X
    $dy = $last.Y - $previous.Y
    $length = [Math]::Sqrt($dx * $dx + $dy * $dy)
    $ux = $dx / $length
    $uy = $dy / $length
    $baseX = $last.X - 15 * $ux
    $baseY = $last.Y - 15 * $uy
    $head = [System.Drawing.PointF[]]@(
        [System.Drawing.PointF]::new($last.X, $last.Y),
        [System.Drawing.PointF]::new($baseX - 7 * $uy, $baseY + 7 * $ux),
        [System.Drawing.PointF]::new($baseX + 7 * $uy, $baseY - 7 * $ux)
    )
    $brush = [System.Drawing.SolidBrush]::new($color)
    $graphics.FillPolygon($brush, $head)
    $brush.Dispose()
    $pen.Dispose()
}

function Point([float]$x, [float]$y) {
    return [System.Drawing.PointF]::new($x, $y)
}

$graphics.DrawString('Drill #11  소년 상태 다이어그램', $titleFont, $titleBrush, 65, 30)
$graphics.DrawString('기존 상태와 AutoRun 전환', $detailFont, $detailBrush, 68, 78)

Draw-State 'IDLE' '대기' 100 250 180 100 $blue ([System.Drawing.Color]::FromArgb(232, 244, 252))
Draw-State 'AUTORUN' '빠른 이동 · 확대 · 무적' 400 250 240 100 $orange ([System.Drawing.Color]::FromArgb(255, 240, 226))
Draw-State 'RUN' '방향키 이동' 760 250 180 100 $green ([System.Drawing.Color]::FromArgb(230, 247, 236))
Draw-State 'SLEEP' '잠자기' 100 470 180 100 $gray ([System.Drawing.Color]::FromArgb(239, 241, 243))

Draw-Arrow @((Point 280 280), (Point 400 280)) $orange
$graphics.DrawString('A키', $labelFont, $labelBrush, 320, 244)

Draw-Arrow @((Point 470 250), (Point 470 120), (Point 190 120), (Point 190 250)) $orange
$graphics.DrawString('5초 경과', $labelFont, $labelBrush, 268, 82)

Draw-Arrow @((Point 640 280), (Point 760 280)) $orange
$graphics.DrawString('방향키', $labelFont, $labelBrush, 664, 244)

Draw-Arrow @((Point 850 250), (Point 850 180), (Point 65 180), (Point 65 300), (Point 100 300)) $green
$graphics.DrawString('방향키 해제', $labelFont, $labelBrush, 520, 143)

Draw-Arrow @((Point 145 350), (Point 145 470)) $gray
$graphics.DrawString('5초 대기', $detailFont, $detailBrush, 60, 400)

Draw-Arrow @((Point 235 470), (Point 235 350)) $gray
$graphics.DrawString('Space', $detailFont, $detailBrush, 240, 400)

Draw-Arrow @((Point 280 525), (Point 850 525), (Point 850 350)) $green
$graphics.DrawString('방향키', $labelFont, $labelBrush, 497, 488)

$graphics.DrawString('AutoRun: 화면 좌·우 끝에서 방향 반전, 상태 유지', $detailFont, $detailBrush, 395, 372)

$outputPath = Join-Path $PSScriptRoot 'state_diagram.png'
$bitmap.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)

$titleFont.Dispose()
$stateFont.Dispose()
$detailFont.Dispose()
$labelFont.Dispose()
$titleBrush.Dispose()
$detailBrush.Dispose()
$labelBrush.Dispose()
$graphics.Dispose()
$bitmap.Dispose()
