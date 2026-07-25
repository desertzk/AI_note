$ErrorActionPreference='Stop';$dir=Join-Path (Get-Location).ProviderPath 'lihongyi_ml\（2／2）KV Cache';$src="$dir\source";$out="$dir\slides";New-Item -ItemType Directory -Force $out|Out-Null
$title='（2／2）KV Cache';$url='https://www.youtube.com/watch?v=fDQaadKysSA';$times=@(0,28,76,254,270,292,318,458,514,596,680,720,1010,1144,1384,1528,1590,1704,1824,1868,1944,1976,2016,2056)
$titles=@('KV Cache：用空間換時間','語言模型生成：Prefill 與 Decode','KV Cache 如何避免重算','KV Cache 會撐爆 HBM','序列長度造成線性增長','Multi-Head Attention 放大 Cache','Gemma 2 的 KV Cache 容量估算','Multi-Query Attention','Grouped-Query Attention','Multi-Head Latent Attention','MLA 不需顯式解壓縮','吸收矩陣：在 latent 空間算 Attention','Sliding Window Attention','StreamingLLM 與 Attention Sink','Pruning KV Cache','剪除 80% KV 的效果與限制','跨對話的 Prefix Cache','Cached Input 的價格折扣','AI Agent 的 System Prompt 適合快取','System Prompt 的穩定內容應前置','改寫 Prompt 以提高 Cache Hit','把變數移到共同前綴之後','Prompt Cache 可節省多少成本？','本講方法總結')
$sections=@('一、KV Cache 基礎','一、KV Cache 基礎','一、KV Cache 基礎','二、容量成本','二、容量成本','二、容量成本','二、容量成本','三、減少 KV Heads','三、減少 KV Heads','三、減少 KV Heads','三、減少 KV Heads','三、減少 KV Heads','四、限制注意力範圍','四、限制注意力範圍','五、KV Cache Pruning','五、KV Cache Pruning','六、跨請求 Prompt Cache','六、跨請求 Prompt Cache','六、跨請求 Prompt Cache','六、跨請求 Prompt Cache','六、跨請求 Prompt Cache','六、跨請求 Prompt Cache','六、跨請求 Prompt Cache','七、總結')
$exp=@(
'KV Cache 保存已計算的 key 與 value，以 GPU 記憶體換取解碼速度；Cache 與 cash 同音，也確實會直接影響服務成本。',
'生成分為 Prefill 與 Decode。Prefill 一次處理完整提示；Decode 每次只產生一個 token，並把新 token 接回輸入繼續生成。',
'因 causal attention 下舊 token 的 K/V 不會改變，Decode 時只需計算新 token 的 Q/K/V，並讓新 query 查詢已快取的歷史 K/V，避免每步重算整段前綴。',
'上一講擔心 SRAM 工作台太小；KV Cache 則可能把容量很大的 HBM 倉庫也撐爆。它加速計算的代價是長期保存中間狀態。',
'每個輸入或輸出 token 都新增一組 K/V，所以 Cache 容量隨上下文長度線性增加；長對話與多使用者併發會迅速累積。',
'Multi-Head Attention 的每層、每個 KV head 都要保存 K/V。容量大致正比於層數、KV heads、head dimension、序列長度、batch size 與資料精度。',
'以 Gemma 2 27B 為例，可由層數、KV heads、head size 和精度估算每 token Cache；再乘長度與同時服務人數。投影片也引出它採用的 GQA。',
'MQA 保留多個 query heads，卻讓所有 query 共用一組 K/V。因只有 K/V 需要快取，容量大幅下降；代價是注意力表達能力可能受影響，且通常需用此架構訓練模型。',
'GQA 是 MHA 與 MQA 的折衷：多個 query heads 分組共用較少的 KV heads。它保留部分多頭差異，同時減少 Cache 和記憶體頻寬。',
'MLA 不直接快取多組 K/V，而把它們壓縮到低維 latent 向量 $c$。模型以 bottleneck transformation 生成 K/V，Cache 只保存壓縮表示。',
'若每次 Attention 都把 latent 完整解壓回多組 K/V，節省的記憶體可能換來過高運算成本。MLA 的關鍵是可以透過代數重排直接使用 latent。',
'因 $k=W_Kc$，$q^Tk=q^TW_Kc=(W_K^Tq)^Tc$，可把解壓矩陣吸收到 query 端；value/output 路徑也可類似重排。因此无需物化完整 K/V。',
'Sliding Window Attention 只保留最近固定窗口的 K/V，使 Cache 容量有上限；但它改變原始全域 Attention，長距離資訊可能被遺忘。',
'StreamingLLM 發現除最近窗口外，保留序列最前面的少數 attention-sink tokens 可显著穩定長序列表現，甚至不需額外訓練。它仍是近似並犧牲部分歷史。',
'Scissorhands 與 H2O 指出，多數歷史 token 很少再被注意，可依重要性移除 K/V。Pruning 把有限 Cache 留給高影響 token，而非固定保存全部。',
'部分任務只保留約 20% K/V，表現仍接近完整 Cache；但效果依任務與資料而異，資訊一旦錯刪便無法恢復，因此不是無條件安全。',
'KV Cache 也能跨請求重用：若不同請求具有完全相同前綴，該 prefix 的 K/V 可直接復用。匹配必須從第一個 token 開始連續成立。',
'模型服務商對 cached input 給大幅折扣，因已快取前綴省掉 Prefill 計算。折扣反映供應商實際降低的 GPU 工作量，而不是單純促銷。',
'AI Agent 每次請求前常附上很長且固定的 system prompt，包括身份、目標、工具與規則，因此特別容易形成跨請求 cache hit。',
'為最大化共同前綴，固定的工具說明與規則應放前面；日期、記憶、使用者狀態等常變內容放後面。一處前綴改動會使其後 Cache 全部失效。',
'「幫我訂從台北到波士頓」和「從舊金山到紐約」很早便分歧，只有短前綴命中；語意相似不等於 token prefix 相同。',
'可把固定模板「從 X 到 Y」放前面，再把 X/Y 的實際值放末尾，使大量指令 token 完全一致。若模板很長，節省會顯著累積。',
'實測研究在多種 Agent 與模型上比較 prompt-caching 策略；Gemini 2.5 Pro 和 GPT-4o 等案例可降低約 50% 或更多成本，但收益取決於定價與重用率。',
'FlashAttention 減少資料搬運；KV Cache 避免重算但耗 HBM；MQA/GQA/MLA 減少每 token 的 K/V；Sliding/Streaming/Pruning 限制保存歷史；Prompt Cache 則跨請求重用共同前綴。每種方法的精確性、是否需訓練及資源代價不同。')

# Exact VTT cues and timestamped transcript.
$cues=New-Object Collections.Generic.List[object];$st=$null;$buf=New-Object Collections.Generic.List[string]
function Flush{if($null-ne$script:st-and$script:buf.Count){$x=[Net.WebUtility]::HtmlDecode((($script:buf-join' ')-replace'<[^>]+>',''));$x=($x-replace'\s+',' ').Trim();if($x){$p=$script:st.Split(':');$cues.Add([pscustomobject]@{T=[double]$p[0]*3600+[double]$p[1]*60+[double]$p[2];S=$script:st.Substring(0,8);X=$x})}};$script:buf.Clear()}
foreach($l in Get-Content -Encoding UTF8 "$src\video.zh-TW.vtt"){if($l-match'^(\d\d:\d\d:\d\d\.\d+) -->'){Flush;$st=$matches[1]}elseif(-not$l.Trim()){Flush;$st=$null}elseif($null-ne$st-and$l-notmatch'^(WEBVTT|Kind:|Language:)'){$buf.Add($l.Trim())}};Flush
$u=[Text.UTF8Encoding]::new($false);[IO.File]::WriteAllLines("$src\transcript.txt",@($cues|%{"[$($_.S)] $($_.X)"}),$u)
function Stamp([int]$s,[string]$z='-'){('{0:D2}{3}{1:D2}{3}{2:D2}'-f[int]($s/3600),[int](($s/60)%60),[int]($s%60),$z)}
$csv=New-Object Collections.Generic.List[string];$csv.Add('slide,timestamp_seconds,timestamp,file')
for($i=0;$i-lt$times.Count;$i++){$fn=('{0:D3}_{1}.jpg'-f($i+1),(Stamp $times[$i]));Copy-Item -Force "$dir\slides_raw\scene_$('{0:D4}'-f($i+1)).jpg" "$out\$fn";$csv.Add(('"{0}","{1}","{2}","{3}"'-f($i+1),$times[$i],(Stamp $times[$i] ':'),$fn))};[IO.File]::WriteAllLines("$out\index.csv",$csv,$u)
$head="# $title`n`n- 講者：李宏毅`n- 影片：[YouTube]($url)`n- 長度：38:33`n- 字幕：原始繁體中文字幕`n`n本講說明 KV Cache 如何以記憶體換取語言模型解碼速度，並比較 MQA、GQA、MLA、局部注意力、Cache pruning 與跨請求 prompt caching。時間資料保存在 ``source/transcript.txt`` 與 ``slides/index.csv``。`n";$std=New-Object Text.StringBuilder;$clean=New-Object Text.StringBuilder;$detail=New-Object Text.StringBuilder;@($std,$clean,$detail)|%{[void]$_.AppendLine($head)};$last=''
for($i=0;$i-lt$times.Count;$i++){if($sections[$i]-ne$last){@($std,$clean,$detail)|%{[void]$_.AppendLine("`n## $($sections[$i])")};$last=$sections[$i]};$fn=('{0:D3}_{1}.jpg'-f($i+1),(Stamp $times[$i]));$base="`n### Slide $($i+1) — $($titles[$i]) ([Video]($url&t=$($times[$i])s))`n`n![Slide $($i+1) — $($titles[$i])](slides/$fn)`n`n$($exp[$i])`n";@($std,$clean,$detail)|%{[void]$_.AppendLine($base)};$next=if($i+1-lt$times.Count){$times[$i+1]}else{2313};$a=@($cues|?{$_.T-ge$times[$i]-and$_.T-lt$next});$n=(($a.X)-join' ')-replace'\s+',' ';[void]$std.AppendLine("`n<details>`n<summary><strong>Cleaned narration</strong></summary>`n`n> $n`n`n</details>`n");[void]$detail.AppendLine("`n<details>`n<summary><strong>All subtitles</strong></summary>`n");$ls=New-Object Collections.Generic.List[string];$line='';foreach($c in $a){$q=if($line){$line+' '+$c.X}else{$c.X};if($line-and$q.Length-gt64){$ls.Add($line);$line=$c.X}else{$line=$q}};if($line){$ls.Add($line)};if($ls.Count-gt1-and$ls[$ls.Count-1].Length-lt32){$z=$ls[$ls.Count-1];$ls.RemoveAt($ls.Count-1);$ls[$ls.Count-1]+=' '+$z};$ls|%{[void]$detail.AppendLine('> '+$_)};[void]$detail.AppendLine("`n</details>`n")}
$tail="`n## 核心結論`n`n- KV Cache 不改變 Attention 結果，但以 HBM 容量換取 Decode 速度。`n- MQA、GQA 與 MLA 減少每 token 的快取量，通常需要相應模型架構或訓練。`n- Sliding Window、StreamingLLM 與 pruning 限制歷史 K/V，可能改變結果或遺失資訊。`n- 跨請求 prompt caching 要求完全相同的 token 前綴；固定內容前置能同時降低延遲與成本。`n";@($std,$clean,$detail)|%{[void]$_.AppendLine($tail)};[IO.File]::WriteAllText("$dir\$title - Slide Notes.md",$std,$u);[IO.File]::WriteAllText("$dir\$title - Clean Slide Notes.md",$clean,$u);[IO.File]::WriteAllText("$dir\$title - Detail Slide Notes.md",$detail,$u);"Generated $($times.Count) slides, $($cues.Count) cues"
