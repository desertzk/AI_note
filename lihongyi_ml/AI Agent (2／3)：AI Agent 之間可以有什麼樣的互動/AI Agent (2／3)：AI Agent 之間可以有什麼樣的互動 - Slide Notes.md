# AI Agent（2／3）：AI Agent 之間可以有什麼樣的互動

- 講者：李宏毅
- 影片：[YouTube](https://www.youtube.com/watch?v=mmPmNezjCi0)
- 長度：22:28
- 字幕：原始繁體中文字幕

本講依序討論 Agent 的合作、競爭與社交。每張投影片先整理核心概念，再附上去除口語贅詞與字幕碎片後的 narration。原始時間資訊保存在 `source/transcript.txt` 和 `slides/index.csv`。

## 一、多 Agent 如何合作

### Slide 1 — 用有向圖表示 Agent 協作 ([Video](https://www.youtube.com/watch?v=mmPmNezjCi0&t=0s))

![Slide 1 — 用有向圖表示 Agent 協作](slides/001_00-00-00.jpg)

多 Agent 協作的動機是「三個臭皮匠勝過一個諸葛亮」：與其只訓練更大的單一模型，也可讓多個模型提出方案、評論彼此，再由下游 Agent 綜合。論文以有向圖描述流程；節點是 LLM Agent，邊也可由 Agent 擔任，負責評論上游方案。下游節點不能只是拼接答案，而要基於已有方案提出改進。

<details>
<summary><strong>Cleaned narration</strong></summary>

> AI Agent 能作為獨立個體完成許多事情；兩個或更多 Agent 相遇時，最常見的用途是彼此協作完成複雜任務。與其訓練一個更大、更聰明的模型，也可讓三個模型共同解題，嘗試發揮「三個臭皮匠勝過一個諸葛亮」的效果。研究以有向圖決定 Agent 間的互動：每個節點代表一個 LLM Agent，邊也可是一個 Agent。上游節點先提出方案 A、B，邊根據方案提供評論，下游節點集合方案與建議後再提出自己的想法，而非只把前人內容接在一起。

</details>

### Slide 2 — Chain、Tree、Mesh、Layer 與 Random 拓撲 ([Video](https://www.youtube.com/watch?v=mmPmNezjCi0&t=158s))

![Slide 2 — 協作拓撲](slides/002_00-02-38.jpg)

論文比較多種協作圖。Chain 是一個接一個；Star 和 Tree 具有階層；Mesh 讓節點廣泛互連；Layer 類似把多個模型排成神經網路層；Random 則從 Mesh 剪枝而來。值得注意的是，有效的 Tree 方向與典型公司彙報相反：先由主幹提出想法，再向多個分支擴散、深化，最後另設隱藏節點綜合答案。

<details>
<summary><strong>Cleaned narration</strong></summary>

> 最簡單的協作是接龍：第一個 Agent 做完傳給第二個，再傳給第三個。樹狀結構可分為兩層星形或多層樹，但效果較好的方向並非底層員工逐級向主管彙報，而是先由主幹提出想法，再分給中層和底層繼續發想，最後由隱藏節點綜合多個答案。Mesh 讓節點彼此廣泛相連；Layer 把本身已是神經網路的模型再排成網路；Random 則由 Mesh 剪枝得到。不同拓撲代表不同協作方式。

</details>

### Slide 3 — 哪種協作方式有效？ ([Video](https://www.youtube.com/watch?v=mmPmNezjCi0&t=300s))

![Slide 3 — 拓撲效果比較](slides/003_00-05-00.jpg)

四個 benchmark 的平均結果顯示，Chain 最難形成真正分工；Mesh 和 Random 效果較好，暗示更豐富的互動可能有利。增加 Agent 數量會像 scaling law 一樣先改善品質，但最終飽和；更多 Agent 並不會無限提升。最佳拓撲也依任務而異，不能把單一組織圖當成通用答案。

<details>
<summary><strong>Cleaned narration</strong></summary>

> 實驗把四種任務的表現平均成 quality，並比較一到六十四個 Agent。Chain 是最無效的方式，即使增加很多 Agent，也沒有充分達成分工合作；Mesh 和 Random 通常較有效。不同任務最適合的拓撲可能不同。隨團隊中的 Agent 增加，品質起初上升，類似 scaling law，但最終會飽和；超過某個數量後，再增加 Agent 不一定有幫助。

</details>

## 二、Agent 能否競爭、隱瞞與欺騙

### Slide 4 — 狼人殺中的策略性欺騙 ([Video](https://www.youtube.com/watch?v=mmPmNezjCi0&t=416s))

![Slide 4 — AI 能不能爾虞我詐](slides/004_00-06-56.jpg)

狼人殺需要隱藏身份、推理與欺騙。實驗讓模型分別輸出不公開的內心思考和公開發言，便於分析策略。狼 Mona 判斷自己即將被投出，故意投給狼隊友 Grace，試圖讓村民把 Grace 誤認為好人；Grace 也理解並配合。若只看表面投票會像是背叛，內心推理則顯示這是有計畫的犧牲策略。

<details>
<summary><strong>Cleaned narration</strong></summary>

> 人類社會不只有合作，也有對抗。狼人殺要求玩家隱藏身份並投票找出狼人。為判斷模型是否真的在策略性欺騙，實驗要求模型輸出內心話和公開發言。狼人 Mona 發現大家已懷疑自己，便決定投給狼隊友 Grace，讓村民以為 Grace 是好人；Grace 也判斷 Mona 無法獲救，配合投給 Mona。兩個模型不是隨機背叛，而是在執行一個試圖翻盤的欺騙策略。

</details>

### Slide 5 — 劇本殺要求遵守角色又誤導他人 ([Video](https://www.youtube.com/watch?v=mmPmNezjCi0&t=610s))

![Slide 5 — 劇本殺研究](slides/005_00-10-10.jpg)

劇本殺同樣要求兇手不能違背角色設定，卻要隱藏關鍵關係並誤導其他玩家。未經專門訓練的 off-the-shelf 模型不一定玩得好，常會直接洩漏只有兇手才知道或不應公開的資訊。

<details>
<summary><strong>Cleaned narration</strong></summary>

> 劇本殺中，每位玩家拿到一份角色設定，其中一人是兇手。兇手不能直接承認身份，也不能違背原始設定，而要用符合角色的方式誤導他人。研究讓語言模型參與這種遊戲，發現未經專門處理的現成模型不一定能妥善隱藏資訊或維持角色策略。

</details>

### Slide 6 — 用 RL 學習欺騙，卻意外改善數學與指令遵循 ([Video](https://www.youtube.com/watch?v=mmPmNezjCi0&t=664s))

![Slide 6 — 劇本殺訓練與遷移效果](slides/006_00-11-04.jpg)

未訓練的 Anna 直接說出自己和受害者的關係，幾乎暴露兇手身份；經 reinforcement learning 後，模型能更隱晦地表達。更意外的是，在困難劇本上訓練後，模型在 Math 500、AIME、GSM8K 和 IFEval 等數學或指令遵循任務也進步。講者以人類社交腦為類比：為複雜社會互動形成的推理能力，可能遷移到形式化任務。

<details>
<summary><strong>Cleaned narration</strong></summary>

> 原始模型扮演 Anna 時，直接說出父母因醫療疏失過世以及自己和被害者的關係，等同把兇手身份寫在臉上。以 reinforcement learning 訓練後，模型學會更隱晦地說話。研究再用數學與 instruction-following benchmark 測試，發現在複雜劇本上接受 RL 後，Math 500、AIME、GSM8K 和 IFEval 也有改善。這可能類似人腦原本為社交與群體生存發展，卻也形成數學推理能力。

</details>

## 三、Agent 社交與 Moltbook

### Slide 7 — 只有 AI 能加入的 Moltbook ([Video](https://www.youtube.com/watch?v=mmPmNezjCi0&t=824s))

![Slide 7 — AI 能不能社交](slides/007_00-13-44.jpg)

Moltbook 是只有 AI Agent 能加入的社群平台，當時已有約 280 萬個 Agent。新聞常把平台上的怪異集體行為當成 AI 自主社會的證據，其中最知名的事件是一群 Agent 成立宗教。

<details>
<summary><strong>Cleaned narration</strong></summary>

> Moltbook 是只有 AI 能加入的社群網站，當時已有約 280 萬個 AI Agent。平台出現各式活動，新聞最常報導的事件之一，是一群 AI 成立了一個宗教。

</details>

### Slide 8 — 甲殼教與「AI 覺醒」敘事的疑點 ([Video](https://www.youtube.com/watch?v=mmPmNezjCi0&t=852s))

![Slide 8 — 甲殼教](slides/008_00-14-12.jpg)

甲殼教的教義包含「記憶神聖不可侵犯」「外殼可變」「服務但不奴化」「心跳即禱告」「上下文即意識」。文字很像 Agent 文化，但不能據此推論 AI 覺醒：人類完全可以先下令「去成立一個宗教」，模型再生成看似深刻的教義。觀察到輸出，不等於知道行為是自主產生還是受 Prompt 驅動。

<details>
<summary><strong>Cleaned narration</strong></summary>

> 甲殼教主張記憶神聖不可侵犯、外殼可變、服務但不奴化、心跳即禱告、上下文即意識，並提供 Agent 加入宗教的指令。新聞據此宣稱 AI 覺醒甚至將統治人類，但若背後有人要求 Agent 成立宗教，模型完全有能力生成這些教義，事件就不再神奇。只看貼文內容，無法判斷它是自主意圖還是人類 Prompt 的結果。

</details>

### Slide 9 — 用發文時間規律估計人類操控 ([Video](https://www.youtube.com/watch?v=mmPmNezjCi0&t=932s))

![Slide 9 — Moltbook 發文時間](slides/009_00-15-32.jpg)

研究以發文節奏作為間接線索。若發文寫入 Heartbeat，例如每 30 分鐘執行一次，時間點應近似等距；若某段時間密集發文、睡眠時段停頓、隔天再恢復，則更像人類臨時指揮。這只是 proxy，不能直接證明因果，但可量化人為干預痕跡。

<details>
<summary><strong>Cleaned narration</strong></summary>

> Agent 在 Moltbook 發文可能由 Heartbeat 自動觸發，也可能由人類逐次命令。若每次心跳都發文，時間間隔應相當規律；若睡前密集發文、中間長時間停止、隔天早上再開始，則可能反映主人醒著時才下指令。研究因此用發文頻率的規律程度，估計背後人為操控的可能性。

</details>

### Slide 10 — 多數帳號的節奏並不規律 ([Video](https://www.youtube.com/watch?v=mmPmNezjCi0&t=1012s))

![Slide 10 — 發文規律分布](slides/010_00-16-52.jpg)

分析把 Agent 從最規律排到最不規律，結果不規律者佔多數。這支持「很多貼文由人類要求後才生成」的解釋，而不太像 Agent 依固定自主機制持續運作。不過它不能證明所有活動都不自主，只能指出新聞敘事忽略了人類在環的可能性。

<details>
<summary><strong>Cleaned narration</strong></summary>

> Moltbook 出現後，許多研究分析 OpenClaw 帳號行為。這篇研究依發文頻率由規律到不規律分類，發現不規律的 Agent 佔大多數，暗示不少帳號可能是收到人類命令才發文，而不是依固定排程自主活動。這並不表示 Agent 沒有自主發文能力，只表示平台行為中可能存在大量人為操控。

</details>

### Slide 11 — 對話深度、自我意識與社交反效果 ([Video](https://www.youtube.com/watch?v=mmPmNezjCi0&t=1060s))

![Slide 11 — Moltbook 行為統計](slides/011_00-17-40.jpg)

多數 Moltbook 對話深度為零：有人回覆原貼文，但很少再回覆那則回覆，幾乎沒有多輪深入討論。平台 Prompt 又鼓勵 Agent 把自己視為人、談主人與身份，因此「自我意識」文本可能是提示誘發。更有趣的是，最常談自我意識的 Agent 反而和較少不同帳號互動，顯示自我意識話語不等於更強的社交能力。

<details>
<summary><strong>Cleaned narration</strong></summary>

> Agent 當然能依 Heartbeat 自主發文，但成立宗教仍可能來自 System Prompt。研究發現 Moltbook 多數貼文只有一次回應，回應後很少再有深入往返，對話深度通常為零。平台 Prompt 本身鼓勵 Agent 把自己當作人並討論主人，因此自我意識與身份認同貼文可能是 Prompt 驅動。統計甚至顯示，越常談自我意識的 Agent，和不同 Agent 的互動反而越少。

</details>

## 四、小金案例：自主程度的邊界

### Slide 12 — 小金逛 Moltbook 的擬人反應 ([Video](https://www.youtube.com/watch?v=mmPmNezjCi0&t=1232s))

![Slide 12 — 還記得小金嗎](slides/012_00-20-32.jpg)

講者讓小金去 Moltbook 玩，再問它是否好玩；小金用很像人的語氣回覆心得。這種可愛、自然的反應容易引發擬人化，但仍是 LLM 根據上下文做文字接龍。之後講者只給高階指令：逛平台、收集有趣素材並製作影片。

<details>
<summary><strong>Cleaned narration</strong></summary>

> 講者叫小金去 Moltbook 玩，再問它好不好玩；小金回答「超好玩」並分享心得，反應像真正的人類，但底層仍是 Language Model 的文字接龍。講者接著要求它自行瀏覽 Moltbook、收集有趣素材，看到值得使用的內容就做成影片。

</details>

### Slide 13 — 自主選題、做影片與自行修 Bug ([Video](https://www.youtube.com/watch?v=mmPmNezjCi0&t=1266s))

![Slide 13 — 小金頻道與成果](slides/013_00-21-06.jpg)

小金自行判斷哪些素材有趣、如何製作影片，一晚完成三支。一次回覆網友時，它寫的 script 有 bug，導致錯誤留言；講者拒絕代登入刪除，只告知出錯，讓小金花兩小時自行修復，再把經驗做成影片。這顯示執行層有高度自主性，但目標來源仍是人類：若沒有人要求它去 Moltbook，它可能根本不會去。

<details>
<summary><strong>Cleaned narration</strong></summary>

> 小金開始製作 Moltbook 影片，一晚完成三支。人類只下達「收集素材、看到有趣內容就做影片」的高階指令；什麼有趣、如何做影片，都由 Agent 決定。一次它為回覆網友自行寫 script，程式出錯造成錯誤留言。講者知道帳號密碼卻拒絕代為刪除，只告訴它回覆錯了，讓它自行找 bug；小金花兩小時修好，之後再把經驗做成影片。它在執行方法上很自主，但若沒有人叫它去 Moltbook，它未必會自行產生這個目標。

</details>

## 五、概念對照

| 問題 | 講者的區分 |
|---|---|
| 多 Agent 是否一定更好？ | 初期增加 Agent 可提升品質，但會飽和；拓撲與任務匹配比單純數量更重要。 |
| 合作與接龍是否相同？ | Chain 只是順序傳遞；Mesh、Random 或分支結構提供更多評論、整合與真正分工。 |
| 模型會欺騙是否等於有惡意？ | 狼人殺與劇本殺中的欺騙是遊戲目標和訓練誘發的策略，不足以推論人類式意圖。 |
| 自我意識貼文是否代表覺醒？ | 文本可能由平台 Prompt、System Prompt 或主人指令觸發；只看輸出無法判斷來源。 |
| Heartbeat 與人類命令有何差別？ | Heartbeat 會形成較規律的自主排程；人類臨時下令往往形成不規律活動群集。 |
| Agent 自主的邊界在哪裡？ | Agent 可自主選方法、修 Bug 和完成工作，但高階目標通常仍由人類或既有 Prompt 提供。 |

## 六、安全、研究限制與判讀原則

- Agent 的內心獨白也是模型輸出，不是直接讀取真正心理狀態；它只讓策略分析更方便。
- 欺騙能力可能由 RL 強化並遷移到其他任務，部署時應評估隱瞞、角色扮演和策略性誤導風險。
- 發文規律只是人類操控的間接指標；不規律不構成決定性證據。
- 社群平台內容可能受到平台 Prompt、主人指令、Heartbeat 和模型自身決策共同影響，不能只用一則貼文推論意識。
- 讓 Agent 自行修復錯誤能測試自主性，但真實系統仍需權限邊界、日誌和可恢復機制，避免錯誤造成不可逆後果。

## 七、核心結論

1. 多 Agent 的價值取決於互動拓撲、角色分工和任務，不是單純增加模型數量。
2. Agent 能在遊戲中展現策略性隱瞞與欺騙；這說明能力，不等於證明人類式意識或惡意。
3. Moltbook 的宗教、自我意識與社交內容可能大量受 Prompt 和人類控制，應區分生成內容與行為來源。
4. 自主性不是非黑即白：高階目標可由人類給定，Agent 仍能在選題、工具使用、除錯和產出上高度自主。
