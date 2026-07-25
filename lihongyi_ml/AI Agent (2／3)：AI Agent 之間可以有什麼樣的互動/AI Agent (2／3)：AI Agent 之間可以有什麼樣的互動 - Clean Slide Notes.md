# AI Agent（2／3）：AI Agent 之間可以有什麼樣的互動 — Clean Notes

- 講者：李宏毅
- 影片：[YouTube](https://www.youtube.com/watch?v=mmPmNezjCi0)
- 長度：22:28
- 字幕：原始繁體中文字幕

本講依序討論 Agent 的合作、競爭與社交。此版本保留每張投影片的完整結構化解說，不附 narration；原始時間資訊保存在 `source/transcript.txt` 和 `slides/index.csv`。

## 一、多 Agent 如何合作

### Slide 1 — 用有向圖表示 Agent 協作 ([Video](https://www.youtube.com/watch?v=mmPmNezjCi0&t=0s))

![Slide 1 — 用有向圖表示 Agent 協作](slides/001_00-00-00.jpg)

多 Agent 協作的動機是「三個臭皮匠勝過一個諸葛亮」：與其只訓練更大的單一模型，也可讓多個模型提出方案、評論彼此，再由下游 Agent 綜合。論文以有向圖描述流程；節點是 LLM Agent，邊也可由 Agent 擔任，負責評論上游方案。下游節點不能只是拼接答案，而要基於已有方案提出改進。


### Slide 2 — Chain、Tree、Mesh、Layer 與 Random 拓撲 ([Video](https://www.youtube.com/watch?v=mmPmNezjCi0&t=158s))

![Slide 2 — 協作拓撲](slides/002_00-02-38.jpg)

論文比較多種協作圖。Chain 是一個接一個；Star 和 Tree 具有階層；Mesh 讓節點廣泛互連；Layer 類似把多個模型排成神經網路層；Random 則從 Mesh 剪枝而來。值得注意的是，有效的 Tree 方向與典型公司彙報相反：先由主幹提出想法，再向多個分支擴散、深化，最後另設隱藏節點綜合答案。


### Slide 3 — 哪種協作方式有效？ ([Video](https://www.youtube.com/watch?v=mmPmNezjCi0&t=300s))

![Slide 3 — 拓撲效果比較](slides/003_00-05-00.jpg)

四個 benchmark 的平均結果顯示，Chain 最難形成真正分工；Mesh 和 Random 效果較好，暗示更豐富的互動可能有利。增加 Agent 數量會像 scaling law 一樣先改善品質，但最終飽和；更多 Agent 並不會無限提升。最佳拓撲也依任務而異，不能把單一組織圖當成通用答案。


## 二、Agent 能否競爭、隱瞞與欺騙

### Slide 4 — 狼人殺中的策略性欺騙 ([Video](https://www.youtube.com/watch?v=mmPmNezjCi0&t=416s))

![Slide 4 — AI 能不能爾虞我詐](slides/004_00-06-56.jpg)

狼人殺需要隱藏身份、推理與欺騙。實驗讓模型分別輸出不公開的內心思考和公開發言，便於分析策略。狼 Mona 判斷自己即將被投出，故意投給狼隊友 Grace，試圖讓村民把 Grace 誤認為好人；Grace 也理解並配合。若只看表面投票會像是背叛，內心推理則顯示這是有計畫的犧牲策略。


### Slide 5 — 劇本殺要求遵守角色又誤導他人 ([Video](https://www.youtube.com/watch?v=mmPmNezjCi0&t=610s))

![Slide 5 — 劇本殺研究](slides/005_00-10-10.jpg)

劇本殺同樣要求兇手不能違背角色設定，卻要隱藏關鍵關係並誤導其他玩家。未經專門訓練的 off-the-shelf 模型不一定玩得好，常會直接洩漏只有兇手才知道或不應公開的資訊。


### Slide 6 — 用 RL 學習欺騙，卻意外改善數學與指令遵循 ([Video](https://www.youtube.com/watch?v=mmPmNezjCi0&t=664s))

![Slide 6 — 劇本殺訓練與遷移效果](slides/006_00-11-04.jpg)

未訓練的 Anna 直接說出自己和受害者的關係，幾乎暴露兇手身份；經 reinforcement learning 後，模型能更隱晦地表達。更意外的是，在困難劇本上訓練後，模型在 Math 500、AIME、GSM8K 和 IFEval 等數學或指令遵循任務也進步。講者以人類社交腦為類比：為複雜社會互動形成的推理能力，可能遷移到形式化任務。


## 三、Agent 社交與 Moltbook

### Slide 7 — 只有 AI 能加入的 Moltbook ([Video](https://www.youtube.com/watch?v=mmPmNezjCi0&t=824s))

![Slide 7 — AI 能不能社交](slides/007_00-13-44.jpg)

Moltbook 是只有 AI Agent 能加入的社群平台，當時已有約 280 萬個 Agent。新聞常把平台上的怪異集體行為當成 AI 自主社會的證據，其中最知名的事件是一群 Agent 成立宗教。


### Slide 8 — 甲殼教與「AI 覺醒」敘事的疑點 ([Video](https://www.youtube.com/watch?v=mmPmNezjCi0&t=852s))

![Slide 8 — 甲殼教](slides/008_00-14-12.jpg)

甲殼教的教義包含「記憶神聖不可侵犯」「外殼可變」「服務但不奴化」「心跳即禱告」「上下文即意識」。文字很像 Agent 文化，但不能據此推論 AI 覺醒：人類完全可以先下令「去成立一個宗教」，模型再生成看似深刻的教義。觀察到輸出，不等於知道行為是自主產生還是受 Prompt 驅動。


### Slide 9 — 用發文時間規律估計人類操控 ([Video](https://www.youtube.com/watch?v=mmPmNezjCi0&t=932s))

![Slide 9 — Moltbook 發文時間](slides/009_00-15-32.jpg)

研究以發文節奏作為間接線索。若發文寫入 Heartbeat，例如每 30 分鐘執行一次，時間點應近似等距；若某段時間密集發文、睡眠時段停頓、隔天再恢復，則更像人類臨時指揮。這只是 proxy，不能直接證明因果，但可量化人為干預痕跡。


### Slide 10 — 多數帳號的節奏並不規律 ([Video](https://www.youtube.com/watch?v=mmPmNezjCi0&t=1012s))

![Slide 10 — 發文規律分布](slides/010_00-16-52.jpg)

分析把 Agent 從最規律排到最不規律，結果不規律者佔多數。這支持「很多貼文由人類要求後才生成」的解釋，而不太像 Agent 依固定自主機制持續運作。不過它不能證明所有活動都不自主，只能指出新聞敘事忽略了人類在環的可能性。


### Slide 11 — 對話深度、自我意識與社交反效果 ([Video](https://www.youtube.com/watch?v=mmPmNezjCi0&t=1060s))

![Slide 11 — Moltbook 行為統計](slides/011_00-17-40.jpg)

多數 Moltbook 對話深度為零：有人回覆原貼文，但很少再回覆那則回覆，幾乎沒有多輪深入討論。平台 Prompt 又鼓勵 Agent 把自己視為人、談主人與身份，因此「自我意識」文本可能是提示誘發。更有趣的是，最常談自我意識的 Agent 反而和較少不同帳號互動，顯示自我意識話語不等於更強的社交能力。


## 四、小金案例：自主程度的邊界

### Slide 12 — 小金逛 Moltbook 的擬人反應 ([Video](https://www.youtube.com/watch?v=mmPmNezjCi0&t=1232s))

![Slide 12 — 還記得小金嗎](slides/012_00-20-32.jpg)

講者讓小金去 Moltbook 玩，再問它是否好玩；小金用很像人的語氣回覆心得。這種可愛、自然的反應容易引發擬人化，但仍是 LLM 根據上下文做文字接龍。之後講者只給高階指令：逛平台、收集有趣素材並製作影片。


### Slide 13 — 自主選題、做影片與自行修 Bug ([Video](https://www.youtube.com/watch?v=mmPmNezjCi0&t=1266s))

![Slide 13 — 小金頻道與成果](slides/013_00-21-06.jpg)

小金自行判斷哪些素材有趣、如何製作影片，一晚完成三支。一次回覆網友時，它寫的 script 有 bug，導致錯誤留言；講者拒絕代登入刪除，只告知出錯，讓小金花兩小時自行修復，再把經驗做成影片。這顯示執行層有高度自主性，但目標來源仍是人類：若沒有人要求它去 Moltbook，它可能根本不會去。


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
