# AI Agent（1／3）：核心技術 Context Engineering 基本概念解說

- 講者：李宏毅
- 影片：[YouTube](https://www.youtube.com/watch?v=urwDLyNa9FU)
- 長度：53:05
- 字幕：原始繁體中文字幕
- 整理方式：每張畫面依出現時間到下一個轉場對齊字幕；逐張保留定義、推理、實驗、例子、限制與失敗案例。

> 部分標題依畫面和講者內容推定。`Context`、`Prompt`、`Memory` 等詞依本講定義保留英文，避免中文譯名混淆。

## 一、為什麼 Agent 需要 Context Engineering

### Slide 1 — 課程定位與三段式架構 ([Video](https://www.youtube.com/watch?v=urwDLyNa9FU&t=0s))

![Slide 1](slides/001_00-00-00.jpg)

本段是 AI Agent 系列的第一部分，聚焦核心技術 Context Engineering；後兩部分將討論 Agent 之間的互動，以及 Agent 對未來工作的影響。本講和前一堂 OpenClaw 課程有重疊，但改用近期論文把已經出現在 OpenClaw 裡的技術系統化。

講者強調，這不是遙遠的研究構想：許多引用論文只發表了數月到半年，相關方法卻已進入可用的 Agent 框架。

<details>
<summary><strong>整理後字幕</strong></summary>


> 今天，我們要繼續來講 AI Agent 今天的課程 還是比較科普性的 我們分成三個段落 第一段 我們來講 AI Agent 背後的核心技術 我們比較系統化地來講 Context Engineering 然後第二段 我們來講 AI Agent 之間的互動 然後最後我們來講 AI Agent 對於我們未來的工作 可能造成什麼樣的衝擊 我們就先從 AI Agent 的核心技術 Context Engineering 開始講起 等一下這段課程 也許你聽了會覺得似曾相識 因為很多 Context Engineering 的技術 都已經在這個 OpenClaw 裡面被實作 今天這段課程比較不一樣的地方 是會引用大量的論文 你發現這些論文都是非常新的論文 幾個月前、半年前的論文 而這些技術都已經被實作在 OpenClaw 裡面 所以上週很多技術我們都已經有提到 只是今天 再從另外一個角度來談 Context Engineering

</details>

### Slide 2 — 語言模型與不斷增長的互動歷史 ([Video](https://www.youtube.com/watch?v=urwDLyNa9FU&t=68s))

![Slide 2](slides/002_00-01-08.jpg)

語言模型只根據「這一次」收到的輸入做文字接龍，並不自行保留前一次呼叫。工具呼叫後，框架不能只把最新工具輸出送回模型；它必須連同使用者原始要求、模型先前的工具指令與所有相關結果一起串成新 Prompt。

若模型依序呼叫工具 1、2、3，歷史會持續累積。問題是模型的輸入長度有限，因此不能無限把所有內容原封不動地接下去；這正是 Agent 必須管理 Context 的原因。

<details>
<summary><strong>整理後字幕</strong></summary>


> 在談 Context Engineering 之前 這邊有一個開場 我們還是跟大家複習一下 為什麼需要 Context Engineering 我們知道語言模型 就是在做文字接龍 你給它一個輸入 給它一個 prompt 它就接一段話出來 人類給語言模型一個輸入 語言模型給人類一個回應 這個回應不一定是一句話 它可能是一個使用工具的指令 這個使用工具的指令 可能會去驅動環境裡面的某一個程式 被執行 然後得到工具的輸出 當我們要把工具的輸出 傳給語言模型 告訴它這個工具執行的結果的時候 你不能夠只給它工具的輸出 大家要記得 語言模型是活在當下的 它只管現在的輸入 它不管你之前曾經給它過什麼 所以當你得到工具 1 的輸出的時候 你要把之前人類給的命令 語言模型自己 操控工具的指令 加上工具的輸出 全部接在一起 丟給語言模型 有的同學可能會說 這邊不是輸入三個東西嗎 語言模型不是應該回 三個回應 你誤會這個投影片的意思了 這邊是這三段話 被接成一段 對語言模型來說 它看到的 就是一串非常長的輸入 然後它再給一個回應 比如說它決定 使用另外一個工具 然後它再得到工具 2 的輸出 工具 2 的輸出 要丟給語言模型的時候 切記不能只給它工具 2 的輸出 之前發生所有的事情 串成一串非常長的輸入 再丟給語言模型 同樣的步驟就反覆下去 語言模型說它要使用工具 3 得到工具 3 的輸出 把一串非常長的輸入 傳給語言模型 這裡會遇到的難點就是 語言模型的輸入長度是有限的 它不能夠吃無限長的輸入 這就是為什麼我們需要 AI Agent

</details>

### Slide 3 — Agent 是模型的守門人與經紀人 ([Video](https://www.youtube.com/watch?v=urwDLyNa9FU&t=188s))

![Slide 3](slides/003_00-03-08.jpg)

AI Agent 位於人、外部環境和語言模型之間，像守門人或經紀人，決定模型實際看見什麼。OpenClaw 只是其中一種早期框架；講者把它比作相對於未來 Agent 的 Nokia 原型機。

輸入不能太長，否則超過模型上限；也不能太短，否則模型不知道先前發生什麼，無法做出正確下一步。讓模型看到「長度合適且資訊足夠」的內容，就是 Context Engineering。

<details>
<summary><strong>整理後字幕</strong></summary>


> AI Agent 就是攔截在語言模型跟人類 或者是語言模型要執行的環境之間的一個介面 它就像是語言模型的守門人 語言模型的經紀人 它決定語言模型會看到什麼 所以來自外界的輸入會經過 AI Agent 這個 AI Agent 不一定是 OpenClaw OpenClaw 只是 AI Agent 的其中一個例子 今天 OpenClaw 還非常的原始 你可以想成它是初代的 AI Agent 它也許在過幾年以後 我們再回頭看 OpenClaw 就好像今天你拿著 iPhone 去看過去的 Nokia 手機一樣的感覺 我們現在看到的只是 AI Agent 的原型 以後一定還會有更多的進展 OpenClaw 做的事情 或 AI Agent 做的事情 就是選擇給語言模型看的內容 所以語言模型真正看到的是 AutoGPT AI Agent 篩選過的長度合適的輸入 這個輸入 它不能太長 因為語言模型 它的輸入就是有上限 但也不能夠太短 如果太短 語言模型就不知道 剛才發生了什麼事 就沒有辦法正確地做接龍了 所以對 AI Agent 來說 它要做的事情 非常的複雜 它需要產生一個 長度合適的輸入 不能太長 也不能太短 而這個 AI Agent 幫語言模型管理它的輸入 讓輸入的長度是合適的 這件事情就叫做 Context Engineering 剛才是概念性的介紹 Context Engineering

</details>

### Slide 4 — Context Engineering 的迴圈與壓縮函數 ([Video](https://www.youtube.com/watch?v=urwDLyNa9FU&t=284s))

![Slide 4](slides/004_00-04-44.jpg)

講者用無限迴圈描述長期運作的 Agent。初始指令為 $I_1$，例如「成為 YouTuber」；$C_t$ 是目前累積的 Context；模型根據新輸入與 Context 產生輸出：

$$
O_t = \operatorname{LLM}(I_t, C_t)
$$

沒有 Context Engineering 時，更新只是把輸入和輸出接到歷史後方：

$$
C_{t+1}=C_t\,\|\,I_t\,\|\,O_t
$$

有 Context Engineering 時，更新改由函數 $F$ 決定：

$$
C_{t+1}=F(C_t,I_t,O_t)
$$

$F$ 可以摘要舊歷史、刪減工具輸出或重組資訊。OpenClaw 的 compaction 會保留 System Prompt，將較早歷史交給模型摘要；另一種粗暴方法是把龐大工具輸出替換成「這裡曾有一個工具輸出」。看似簡陋，但後續實驗顯示它可能和 LLM 摘要同樣有效。

<details>
<summary><strong>整理後字幕</strong></summary>


> 如果我們今天要用 比較程式語言的方法來描述它的話 可能看起來像是這樣的 現在左邊這段程式碼 是沒有做 Context Engineering 的狀況 沒有做 Context Engineering 的時候 你可以想成語言模型跟外界的互動 就是一個 for 迴圈 這個 for 迴圈是從 1 到無限大 這個 1 要執行多少個 step 這個取決於你想要讓語言模型運作多久 你想要讓這個 AI 運作多久 我們希望它永遠地執行下去 執行到天荒地老 所以這邊放一個無限大 然後 這邊會有一個初始的輸入 這個可能就是你給語言模型的指令 今天這個指令甚至可以 就是一個非常 high level 的目標 比如說成為 YouTuber 或者是跟魯夫一樣 就是成為海賊王 然後它就去做它自己該做的事情 然後這個我們把輸入叫做 I 第一個輸入我們叫做 I_1 然後我們用 C 來表示 現在所有環境中發生的事情 這個我們通常就叫做 context 然後用 C 來表示 最開始的時候 C 是空的 在每一個 for 迴圈裡面會做的事情就是 把之前發生的所有事情 C_t 加上現在目前的輸入叫做 I_t 它可能是人對語言模型說這一句話 它可能是語言模型執行某個工具後的結果 是某一個現在發生的事情 現在要給語言模型的輸入 把 I_t 跟 C_t 接起來給語言模型 它給你一個回應叫做 O_t 然後接下來就把 I_t 跟 O_t 都接到 剛才的 context C_t 後面 我們更新我們的 context 變成 C_{t+1} 這是沒有做 Context Engineering 的狀態 如果有做 Context Engineering 你唯一改變的 只有最後這一行程式 其他部分運作的都還是一樣的 語言模型吃一個輸入 吃一個 context 得到新的輸出 但是我們現在不是 直接把輸入跟輸出 接到語言模型的 context 上 我們可能做了一個 比較複雜的操作 我們把比較複雜的操作 用大 F 來表示 我們現在還沒有仔細說明 這個複雜的操作是什麼 你可以在這邊定義各式各樣 自己開發各式各樣複雜的操作 把 context 剛才的輸入 剛才的輸出 轉換成新的 context 叫做 C_{t+1} 然後 C_{t+1} 在下一個 for 迴圈的時候 會被當作語言模型的輸入 至於這個 F 要做什麼 就要問你自己 這個就是 Context Engineering 也就是一個 AI Agent 要做的事情 AI Agent 這個 Context Engineering 在這個大 F 裡面會做什麼樣的事情 接下來我們就來舉幾個例子 一個最需要做的事情就是壓縮 因為之所以要做 Context Engineering 最核心的需求就是語言模型的輸入 不能夠太長 所以那個大 F 裡面最重要的一個功能 就是壓縮 把本來很長的歷史紀錄把它壓短 怎麼壓短 上週在最後課程結尾的時候 我們有講說 這個龍蝦(OpenClaw)裡面 是內建這個 compaction 的功能的 它做的事情 說穿了也不值錢 就把整個歷史紀錄裡面 扣掉 system prompt 的部分 比較久遠的歷史紀錄 通過某一個語言模型 然後把它變成摘要 所以本來很長的歷史紀錄 就變成了一段簡短的摘要 然後再繼續去接上新的資訊 這個是 龍蝦(OpenClaw) 做的事情 上週在課程快結束的時候 我們也說龍蝦(OpenClaw)還有別的處理壓縮的方式 比如說有一個非常簡單粗暴的方式是 如果某一段文字 它原來是某一個工具的輸出 有時候工具輸出 它會輸出非常長篇大論的東西 把那一段長篇大論改成 這裡曾經有個工具的輸出就結束了 上週講到這邊的時候 我看到同學笑了 你可能覺得這個什麼爛方法 這個方法真的會有用嗎 神奇的事情是 這個方法還真的有用

</details>

## 二、壓縮策略、成本與失敗模式

### Slide 5 — SWE-bench：摘要、遮蔽與軌跡延長 ([Video](https://www.youtube.com/watch?v=urwDLyNa9FU&t=536s))

![Slide 5](slides/005_00-08-56.jpg)

SWE-bench 要求 Agent 根據 GitHub repository 和 issue 修復程式。圖的縱軸是正確率，橫軸以美元表示 token 成本；黑點是不壓縮的 raw agent，紅方塊是 LLM summarization，三角形是 observation masking。

多數模型上，LLM 摘要與 raw agent 的正確率相近但成本更低；更意外的是，把工具輸出直接遮蔽掉，常與 LLM 摘要相近。壓縮卻不保證一定省錢：若重要步驟被隱藏，模型可能不確定某工具是否已執行而重做工作，形成「軌跡延長」。單次 Prompt 變短，但步驟數增加，總 token 反而未必下降。

<details>
<summary><strong>整理後字幕</strong></summary>


> 這個就是引用之一篇 去年年中的論文 有人就嘗試在 SWE-bench 上面 比較用語言模型做壓縮 還有單純把工具的輸出換成 這裡曾經有個工具的輸出 這兩個方法 它們在表現上有什麼樣的差異 這邊這些實驗是做在 SWE-bench 上面 SWE 就是 Software Engineering 的縮寫 就是要讓語言模型去做一些 平常軟體工程師在做的事情 在 SWE-bench 裡面 語言模型要解的問題就是 給它一個 GitHub Repo 給它一個 Issue 然後它要去把這個 GitHub Repo 的這個 Issue 把它解掉 就一般軟體工程師在做的事情 雖然非常有挑戰性 不過今天很多語言模型 在這樣有挑戰的任務上面 都可以做得非常的不錯 這邊就是嘗試了 各式各樣不同的語言模型 縱軸是正確率 橫軸它這邊的單位是用美金 你就想成是 我們今天在整個解問題的過程 在 fix 這個 issue 的過程 用了多少的 token 花了多少的錢 付出了多少的成本 黑色的點 它這邊叫做 raw agent 也就是沒有做任何的壓縮 反正環境裡面發生什麼事情 就通通丟到你的歷史紀錄裡面去 這個時候你會發現 雖然在多數的情況下 raw agent 都表現得不錯 但是相較於其他方法 它會耗費更多的 token 耗費更多的成本 才能解決問題 這個紅色的正方形 代表的是拿一個語言模型 對上下文進行壓縮 如果今天上下文太長了 就用個語言模型進行壓縮 你得到的是紅色這一個點 你發現紅色這個點 跟黑色這個點多數的時候比起來是差不多的 所以用 LLM 做壓縮 跟沒有做壓縮 表現在 SWE-bench 上面差別沒有非常大 代表這個壓縮是蠻有效的 但是一個神奇的地方是這個三角形 這個三角形這篇論文裡面叫 observation masking 就是我剛才講的 把工具的輸出換成這邊曾經有個工具的輸出 你發現三角形的表現 很多時候跟 LLM summary 的表現 是差不多的 也就是你與其去呼叫一個語言模型做摘要 跟你直接把今天 agent 使用某個工具的輸出 直接換成這裡曾經有個工具的輸出 結果表現是差不多的 它並不會真的比 LLM summary 好 但是 LLM summary 並沒有在所有的 case 都穩定地比 observation masking 好 然後多數時候 當然有做壓縮都是比較省錢的 但是你會發現在這個例外上面 有做壓縮沒有比較省錢 作者也提供了一個解釋 他說這是因為發生了一個叫做軌跡延長的現象 當你做壓縮以後 當然你的上下文變短了 但是因為有一些步驟就不見了 所以對一個語言模型來說 它覺得我剛才到底執行過這個工具了嗎 還沒有嗎 它重複做了剛才已經做過的事 所以變成它執行的步驟反而變多了 雖然輸入語言模型的 content 變短 但它執行的步驟變多了 所以最後解一個問題 所耗費的 token 就沒有下降

</details>

### Slide 6 — 分階段混合壓縮 ([Video](https://www.youtube.com/watch?v=urwDLyNa9FU&t=744s))

![Slide 6](slides/006_00-12-24.jpg)

最佳策略不必在 masking 和 summarization 之間二選一。前期先用 observation masking 把龐大工具輸出替換成短標記，成本低且能延緩 Context 增長；等短標記也累積到一定規模，再用 summarization 一次濃縮較長歷史。

兩階段策略反映不同方法的角色：masking 適合局部、頻繁、便宜的修剪；summary 適合較少發生但幅度較大的全局壓縮。

<details>
<summary><strong>整理後字幕</strong></summary>


> 我們剛才講了 兩個不同的壓縮方式 你可能問說 實際上到底哪一個比較好 當然你可以兩個同時執行 是在同篇論文裡面 它最後提出來的方法就是 不同的壓縮方法 是可以同時執行的 它最後試出來 最好的策略就是 在前期的時候 先用這個 observation masking 的方法 把工具的輸出換掉 把工具的輸出縮短 但是這一招 終究會讓你的 context 越來越長 因為就算你只是把工具的輸出換成一句 這裡曾經有個工具的輸出 你的 context 最終還是會越來越長 所以長到某一個地步以後 再用 summarization 的方式 一次把非常長的輸入 直接壓縮壓短 把這兩個方法同時使用 可以得到最好的結果 做完壓縮以後

</details>

### Slide 7 — 把工具輸出移到硬碟，必要時再讀回 ([Video](https://www.youtube.com/watch?v=urwDLyNa9FU&t=794s))

![Slide 7](slides/007_00-13-14.jpg)

與其只留下「這裡曾有工具輸出」，可以把完整輸出保存成 `log1.txt`，Prompt 只留下檔案連結。讀論文、程式碼或 log 時，模型通常只需要其中一小部分，沒必要讓全文永久佔據 Context。

如果模型後來真的需要細節，可再呼叫 `read` 工具取回。這種設計既縮短 Prompt，又保留可恢復性；它不是把資訊永久刪掉，而是將資訊從昂貴的模型輸入移到便宜的外部儲存。

<details>
<summary><strong>整理後字幕</strong></summary>


> 這邊要留一個句子 代表它曾經被壓縮過 但這個句子應該要留什麼 與其放一句話說 這邊曾經有個工具的輸出 換別的字眼 放別的符號 會不會更有效 所以在後來的論文裡面 有人就說 我們能不能夠在這邊 放一個連結 放一段紀錄 說這個工具的輸出 詳見 log1.txt 你就真的把這個工具的輸出 存到你的硬碟裡面 存成一個檔案叫 log1.txt 這樣做之後 可能多數的時候 語言模型都不會再 回來看這個 log1.txt 裡面有什麼 因為多數的時候 工具的輸出可能沒有那麼重要 很多時候工具的輸出可能是 執行 read 然後去讀了一篇論文 然後把整篇論文的內容讀了進來 可能你根本不需要整篇論文的內容 你只需要論文的其中一段 只需要它的某一個摘要 所以這些內容不需要一直存留在你的上下文裡面 但是如果你不做壓縮的話 直接執行工具 這一些非常長篇大論的文章 或非常長的程式碼 就會一直存留在你的上下文中 所以你可以把這一些內容 存到某一個檔案裡面 它就從你的這個語言模型的輸入裡面消失了 語言模型的輸入裡面就只留下一句話 詳見 log1.txt 如果語言模型有一天 它真的很需要知道這個工具當初到底輸入了什麼 輸出了什麼 這個時候它可以再執行一個工具 它可以執行 read 這個指令 去 log1.txt 裡面 把它需要的內容再讀取出來 它就可以重拾它的記憶

</details>

### Slide 8 — Morty’s Mind Blowers：外部記憶的比喻 ([Video](https://www.youtube.com/watch?v=urwDLyNa9FU&t=896s))

![Slide 8](slides/008_00-14-56.jpg)

講者用《Rick and Morty》的情節比喻：Morty 被移除的記憶存放在地下室管子裡，平時不在腦中，但仍可被找回。這對應把 Agent 歷史移到硬碟，需要時再讀取。

這段也提醒，現在的 Agent 已使一些科幻構想變得具體，例如從腳本自動產生影片。類比的重點不是故事細節，而是「從活躍 Context 移除」不等於「永久消失」。

<details>
<summary><strong>整理後字幕</strong></summary>


> 這就讓我想到 Rick and Morty 裡面的其中一段 這是第三季的其中一段 就是有一天 Morty 發現 他家有一個地下室 他爺爺 Rick 把他很多的記憶 通通都存在這個地下室裡面 他的每一個記憶就存在一個一個管子裡面 多數都是 Morty 感到難堪的記憶 比如說他不小心害死了一個人等等 但也有一些是 Rick 本身覺得難堪的記憶 比如說他發音唸出一個字 被 Morty 糾正等等 然後 Morty 發現 原來我的大半生人生的記憶 通常都存在這個地下室的管子裡面 就爆氣 然後就跟他爺爺打了一架 就把他爺爺打倒 然後兩個人記憶就都消失了 就是一個這樣莫名其妙的故事 最近我重看了一下 Rick & Morty 我現在覺得 自從有了 AI Agent 以後 很多這個科幻電影 科幻小說裡面有的情節 感覺就沒有那麼神奇 比如說 Morty 最新一季裡面 有一個電影製造機 就是你輸入一個腳本 它就輸出一個電影 你想想看 現在根本就已經有電影製造機了 不是很多現在的短電影 都是直接用 AI 生成的嗎 所以這個技術現在看起來 也沒有那麼遙遠了 就是一個記憶清除 然後再讀取的故事 對語言模型來說

</details>

## 三、Memory、Prompt 與 Context 的區別

### Slide 9 — Memory 是自主保存與讀取外部資訊 ([Video](https://www.youtube.com/watch?v=urwDLyNa9FU&t=970s))

![Slide 9](slides/009_00-16-10.jpg)

Agent 的記憶可視為模型在適當時機呼叫工具，把資訊寫入資料庫或硬碟，之後再自主取回。研究會用圖結構表示記憶關係、加入時間資訊，或設計不同搜尋機制。

真正困難的不是「硬碟能不能存字」，而是決定何時把活躍 Context 抽離成外部記憶，以及何時把哪一小段記憶載回 Prompt。這兩個決策都屬於 Context Engineering。

<details>
<summary><strong>整理後字幕</strong></summary>


> 剛才把存在上下文中的這個內容 放到 hard disk 裡面 之後再讀取出來 就是它的記憶 所以語言模型的記憶 就是它在某一些時候 它可以自主的去執行 把內容放到資料庫 放到硬碟裡面的指令 然後它就把資料放到硬碟裡面 在這邊要怎麼把資料儲存在硬碟裡面 不同的文獻就有非常多不同的方式 比如說有人會把這一些檔案建成 graph 的形狀 然後讓你之後在搜尋的時候 比較能夠了解不同記憶之間的關聯性 或者是有人會幫記憶標上時間 你比較知道說要存取什麼時間段的記憶 或者是比較新的記憶 它可能就比較需要被讀出來 然後接下來 只要在某個時間點 模型能夠執行抽取記憶的指令 它就可以從你的資料庫裡面 把記憶抽取出來 這邊需要研究的就是 怎麼讓模型在適當的時機 抽出它原來存在 Prompt 裡面的記憶 到你的檔案系統裡面 什麼時候要從檔案系統裡面 把失去的記憶讀取回來 我這邊就是列了比較多的論文 然後給大家參考 這方面跟這個 AI Agent 記憶有關的文獻 可以說是汗牛充棟 我就列了幾個 reference 放在這邊給大家參考

</details>

### Slide 10 — Context 拆成 Prompt $P$ 與 Memory $M$ ([Video](https://www.youtube.com/watch?v=urwDLyNa9FU&t=1060s))

![Slide 10](slides/010_00-17-40.jpg)

更完整的表示把 Context 拆成兩部分：

$$
C_t=(P_t,M_t)
$$

$P_t$ 是實際送入 LLM 的 Prompt；$M_t$ 是存在硬碟、不直接送入模型的外部資訊。因此模型呼叫應寫成 $O_t=\operatorname{LLM}(I_t,P_t)$，更新函數則可能同時改變 $P$ 與 $M$。讀記憶會把資訊從 $M$ 載入 $P$；存記憶會更新 $M$。

本講刻意區分 Context 與 Prompt：Context 是 Agent 經歷和可用狀態的總體，包含硬碟內容；Prompt 只是其中當下交給模型看的部分。日常與論文中兩詞常混用，但設計系統時最好分清楚。

<details>
<summary><strong>整理後字幕</strong></summary>


> 講到記憶 我們需要稍微修改一下 剛才有關 context engineering 的式子 我們剛才說 我們有一個東西叫做 context 叫做 C 然後我們會有一個大 F 來更新這個 C 如果我們要把記憶的概念 加進來的話 講得更精確一點 這個 C 應該被分成兩部分 我們在這邊 用 P 和 M 這兩個符號 來代表 C 的兩部分 這個 P 和 M 有什麼不同 P 就是會被丟進語言模型的資訊 M 就是不會被丟進語言模型 存在你的硬碟中的資訊 所以 context 我們可以把它包含 有存在硬碟中的資訊 有可以放到語言模型中的資訊 我們這邊把 context 裡面 兩種不同的資訊 分別用 P 和 M 來表示它 左邊這個演算法 跟右邊這個演算法 除了 C 我們告訴你說 它裡面有兩個 component 以外 唯一不同的地方就是 這個呼叫 LLM 的輸入變了 從 Ct 變成 Pt 就是要告訴你說 我們只需要把 C 裡面 我們準備要給 LLM 看的部分 給 LLM 看就好 其他部分就存在硬碟裡面 所以當我們更新 Ct 的時候 是把 Ct 裡面的兩個 component Pt 跟 Mt 分別更新成 Pt+1 Mt+1 有時候你更新的是 P 的部分 就放進語言模型的部分 當你執行 load memory 當你把記憶從那個硬碟中讀取出來的時候 你就更新了 P 有時候 你是執行 save memory 你是要把 memory 存到硬碟裡面 你就更新了 M 所以這是一個 context engineering 更完整的式子 講到這邊 我想要對我們常常用的幾個詞彙 做一下 clarification 就有幾個詞彙 在我上課的時候 往往是被混用的 比如說 context 比如說 prompt 這兩個詞彙 在上課的時候 像幾乎差不多是同樣的意思 但實際上如果細分起來的話 我認為這兩個詞彙還是有所不同的 這邊所謂的 context 指的就是這個演算法的 C 它包含了會被輸入語言模型的部分 也包含了存在硬碟中的部分 你可以想像所謂的 context 它是 AI Agent 所經歷過的一切事情 P P 是真正會被輸進語言模型的部分 所以 P 是 context 的一部分 它是語言模型會看到的部分 這個部分才是 Prompt 所以 Prompt 跟 Context 我認為它還是有差別的 Context 不一定會成為 語言模型的輸入 只有 Context 的一部分 會被作為 Prompt 不過在上課的時候 或者在文獻上 或者在你看到別人 在討論的時候 往往 Prompt 跟 Context 現在就是混雜成一團 但我覺得這兩者 還是可以做出區別的

</details>

### Slide 11 — Context Collapse 與 ACON 的反省式回饋 ([Video](https://www.youtube.com/watch?v=urwDLyNa9FU&t=1238s))

![Slide 11](slides/011_00-20-38.jpg)

摘要能生成不代表摘要有用。若壓縮後原本能完成的任務失敗，就是 context collapse：摘要遺失了任務真正需要的資訊。講者再次引用郵件事件：Agent 在 compaction 時弄丟「刪信前需人類同意」的規則，之後便未經同意刪除郵件。

ACON 蒐集「壓縮前成功、壓縮後失敗」的軌跡，讓另一個 LLM 比較並反省，產生一段文字 feedback，指出摘要時應保留什麼。這裡的「訓練資料」並未更新模型參數；feedback 只是日後摘要時附加在 Prompt 裡的指導文字。

<details>
<summary><strong>整理後字幕</strong></summary>


> 我們剛才講到 在做摘要的時候 你就是呼叫 某一個語言模型 跟它說把這一段記憶做摘要 今天語言模型都有摘要的能力 所以它就會輸出摘要來 但是有一篇 paper 叫做 ACON 它就發現說語言模型在做摘要的時候 很多時候是會失敗的 所謂的失敗並不是說它沒辦法產生摘要 而是它產生完摘要 把摘要放到 Prompt 裡面以後 結果本來能夠答對的問題 本來做得了的任務做不了了 這一件事情 叫做 context collapse 就今天在做壓縮的時候 損失了一些資訊 如果損失的是最重要的資訊 語言模型就非常有可能犯錯 就像我們上一堂課 舉的最後一個例子 有一個 AI 的研究 有一個 Meta 的研究人員 他讓 AI 幫他收信 結果 AI 在做 compress 的時候 把最重要的指令 刪除郵件 要經過人類同意這個指令 把它壓縮變不見了 所以模型就開始不聽人類的話 所以今天在做壓縮的時候 它不是一個普通的壓縮 它不是一個普通的摘要 我們應該要想辦法告訴語言模型 什麼樣的資訊 是最應該被留在 Prompt 裡面的 這篇論文的解法是 它呢拿另外一個語言模型出來 然後呢它有一些訓練資料 這些訓練資料是 本來沒有做壓縮的時候可以做得對 但是語言模型在壓縮之後 就做不對的一些例子 然後它把這一些例子 給一個語言模型看 然後跟那個語言模型看說 你看壓縮以後結果變差了 你能不能夠說明一下 反省一下 為什麼壓縮會變差 然後這個語言模型 就檢查了這兩個 trajectory 以後 它就會得出它的結論 把這個結論 寫成 feedback 這個 feedback 就是一段文字 它沒有什麼特別的 這邊完全沒有訓練模型 這個 feedback 就是一段文字 下一次 有不一樣的任務進來的時候 再把這段 feedback 給負責摘要的語言模型看 希望有多這段額外的 feedback 可以讓語言模型做得更好 在這篇論文裡面 它也把它的資料集 分成訓練資料跟測試資料 不過這邊要注意 這邊所謂的訓練資料 並沒有真的去改變模型的參數 這些訓練資料 就是拿來得到這個 feedback 然後測試資料 會拿這一個 feedback 來強化模型做摘要的能力 當語言模型看到這個 feedback 的時候 它裡面的參數是沒有任何改變的 但它只是因為看到這個 feedback 更知道說在做摘要的時候 什麼資訊是重要的 如果漏了什麼資訊 之後可能就會任務失敗 所以它更能夠做摘要 更能夠做人類要的摘要 任務要的摘要 所以可以表現得更好 ACON 這招真的有用嗎

</details>

### Slide 12 — AppWorld：ACON 同時降低 Token 並提高正確率 ([Video](https://www.youtube.com/watch?v=urwDLyNa9FU&t=1410s))

![Slide 12](slides/012_00-23-30.jpg)

AppWorld 測試 Agent 組合多個 App 完成複雜任務。圖的橫軸是執行中 Prompt 的 peak token，縱軸是任務正確率。無壓縮的黑點 token 最多；一般 LLM 摘要雖減少 token，有時會降低正確率。

加入 ACON feedback 的紫點不僅更省 token，正確率也更高。關鍵不是寫出語言流暢的摘要，而是保留對下游任務有決定性的狀態、限制與已完成步驟。

<details>
<summary><strong>整理後字幕</strong></summary>


> 還真的有用 它這個 work 是做在 AppWorld 上面 AppWorld 就是要讓語言模型去操控一大堆的 App 然後來執行一些比較複雜的事情 就跟今天 AI Agent 在做的事情是一樣的 所以你就知道說今天這些 AI Agent 能夠執行各式各樣的程式 把它組合起來完成複雜的任務 早就有這樣的 Benchmark 在評量 AI Agent 能夠執行複雜任務的能力 這邊橫軸是 peak token 也就是在整個 Prompt 裡面 token 最多的時候 多到什麼樣的地步 如果今天你是黑色的點 就代表沒有做 compression 這個時候你的 token 量 當然是最多的 這三張圖就是比較三個不同的模型 然後縱軸 縱軸就是正確率 正確率當然是越高越好 如果你只是做一般的 LLM Prompt 在 AppWorld 這個 Benchmark 上面 做 LLM 只做 LLM 壓縮 有時候結果是會變差的 壓縮完之後 本來解得了的任務就解不了了 雖然做完壓縮以後 你當然用的 token 量比較少 但是正確率是會下降的 它發現說 當它用 ACON 這個作法 也就是讓語言模型 更能夠做摘要 更能夠做任務需要的摘要的時候 它得到的是紫色這一個點 不只所耗費的 token 變少 表現也變得更好 所以這個是 ACON 做的事情 在 ACON 那篇論文裡面

</details>

### Slide 13 — 用強化學習訓練專門的摘要行為 ([Video](https://www.youtube.com/watch?v=urwDLyNa9FU&t=1500s))

![Slide 13](slides/013_00-25-00.jpg)

若要直接微調模型做 Context 壓縮，難點是沒有唯一「正確摘要」可當標籤。解法是讓模型產生摘要後繼續完成任務，最後以任務成功作正獎勵、失敗作負獎勵，用 reinforcement learning 訓練。

因摘要模型和後續解題模型可能是同一模型，訓練成果不一定只表示摘要文字更好，也可能表示模型更會從短摘要恢復任務狀態、規劃工具使用並完成工作。

<details>
<summary><strong>整理後字幕</strong></summary>


> 是完全沒有訓練模型的 當然你想要訓練模型也是可以的 也當然有論文 我就引用在這邊 嘗試去 finetune 一個 LLM 這個 LLM 是專門對 context 做壓縮的 但你可能想說 我們要怎麼訓練這樣的 LLM 我們一般訓練一個模型的時候 你不只要輸入 也要有正確的答案 才能夠訓練模型 但是今天假設沒有正確的答案 或實際上我們就是沒有正確的答案 我們要怎麼訓練這個模型 你又不知道正確的摘要 應該要長什麼樣子 你又不知道什麼樣的摘要 才是對任務有幫助的 所以實際上在訓練這個模型的時候 是用一個 reinforcement learning 的方法 它是說 讓這個模型產生摘要之後 還不算完 還不知道這個摘要好不好 接下來再繼續去解這個任務 然後直到最後 解完任務之後 看有沒有做對 有做對 就是 positive reward 沒有做對 就是 negative reward 用 reinforcement learning 的方法 來訓練這個做摘要的語言模型 但做摘要的語言模型 跟負責做其他事情 比如說產生執行工具指令的模型 是同一個模型 所以實際上在訓練的時候 你不只是強化了語言模型做摘要的能力 你強化了解整個任務的能力 包括語言模型根據摘要來解任務的能力 也許你今天這個訓練 一定不只是讓摘要寫得更好 可能同時也是讓模型 更能夠讀取摘要 更知道怎麼從一個簡短的摘要裡面 去執行它的任務 訓練一個 LLM 它的目標是特化在 Agent 的這個情況下 可以做得更好

</details>

## 四、何時壓縮，以及模型為何抗拒壓縮

### Slide 14 — 固定門檻與模型的「不願忘記」 ([Video](https://www.youtube.com/watch?v=urwDLyNa9FU&t=1600s))

![Slide 14](slides/014_00-26-40.jpg)

OpenClaw 以寫死的 Context 長度門檻觸發壓縮，而不是完全讓模型自行決定。既有研究發現，模型常不願主動執行會抹除歷史的工具；講者再次以 Morty 抗拒被刪記憶作比喻。

因此「提供一個壓縮工具」不等於模型會適時使用。觸發策略本身必須由框架規則或額外訓練保障。

<details>
<summary><strong>整理後字幕</strong></summary>


> 講到目前為止 我們都還沒有講 什麼時候應該開始壓縮 但直覺上今天 context 太長的時候 就應該開始壓縮 但是長到什麼樣的地步 應該開始壓縮 如果你去看這個 OpenClaw 的話 裡面就是一條寫死的規則 反正長度超過某個上限的時候 就開始壓縮 為什麼是用寫死的規則 為什麼不讓語言模型 自己決定什麼時候要壓縮 因為前人的文獻已經發現 語言模型不喜歡做壓縮 對它來說 壓縮就是抹除記憶 它非常不喜歡這件事 就像 Morty 發現 自己大半生的記憶 都被藏在一個地下室的時候 他非常的生氣 就毆打了他的爺爺 所以這個語言模型 跟 Morty 一樣 它不喜歡它的記憶 無緣無故就消失了 就算是你在給它一個工具 跟它說 這邊有個好用的工具 這個工具會把你過去的記憶 某一些地方抹除 它聽了就不高興 聽了就不想執行這個工具 甚至在這篇論文裡面 他還嘗試逼迫模型

</details>

### Slide 15 — Erase 工具的指令遵循失敗 ([Video](https://www.youtube.com/watch?v=urwDLyNa9FU&t=1662s))

![Slide 15](slides/015_00-27-42.jpg)

實驗要求模型在收到 `reflection` 時只能呼叫 `erase` 工具，刪掉部分歷史；模型卻無視明確要求，繼續原任務。這個失敗展示：Prompt 中有規則不保證模型可靠執行，尤其當行為和模型當前解題傾向衝突。

<details>
<summary><strong>整理後字幕</strong></summary>


> 使用這個工具 他跟模型說 現在有一個工具叫做 erase 就是會抹去模型部分的記憶 然後他說當我跟妳說 reflection 反省的時候 你就要執行 erase 這個工具 然後這個模型就開始做事情 做著做著做著 人類在這邊強制輸入說 reflection 然後非常重要 你只能做 erase 不能做其他事 語言模型才不做 它就繼續做它的事情 它不想要抹除它自己的記憶 所以語言模型沒那麼喜歡被抹除記憶 所以怎麼辦

</details>

### Slide 16 — AgentFold：訓練模型使用 Fold 工具 ([Video](https://www.youtube.com/watch?v=urwDLyNa9FU&t=1696s))

![Slide 16](slides/016_00-28-16.jpg)

OpenDevin 採用 Context 超限就強制 `memory flush` 的規則；AgentFold 則訓練模型自主使用 `fold`。模型選擇要折疊的步驟範圍，並留下短摘要，例如把搜尋過程濃縮成「已查得台灣最高峰是玉山」。

研究發現只靠 Prompt 很難穩定學會這種行為，需要調整模型參數。這和 ACON 不同：ACON 以文字 feedback 改善摘要，不微調參數；AgentFold 的核心正是訓練模型何時、如何使用壓縮工具。

<details>
<summary><strong>整理後字幕</strong></summary>


> 有一篇 paper 叫做 AgentFold 所以你會發現說今天 因為有一個模型不太喜歡被抹除記憶 所以 OpenDevin 用的是強制執行的方法 只要 context 超過一個上限 它就執行一個動作叫 memory flush 這強制執行的 會讓模型自己開始壓縮自己的記憶 有一篇 paper 叫做 AgentFold 它做的事情是 它去訓練模型 訓練模型使用壓縮記憶的工具 它把壓縮記憶的工具叫做 fold 叫做折疊 這個 fold 會吃兩個輸入 一個輸入是 我們要把剛才整個對話的 第幾步到第幾步做壓縮 我們說壓縮完之後 你最好還可以留一個小紙條 說這邊曾經被壓縮過 這個小紙條內容寫什麼 也可以讓語言模型 透過這個工具自己決定 所以它就可以說 第三步到第四步 剛才是上網搜尋 搜到了一大堆的資料 也許太冗長了 我們就改成一句話 上網搜尋 我已經知道 我要有資訊 比如說台灣最高的山是玉山 然後 就執行這個 fold 的指令要的事情 把前面第三步驟跟第四步驟 置換成一段文字 講到這邊 你可能會想說 剛才不是說語言模型不喜歡 壓縮或抹除自己的記憶嗎 這邊怎麼能夠壓縮或抹除自己的記憶 這篇論文正好就是呼應了 過去的研究 發現語言模型不喜歡壓縮記憶 因為這篇論文的核心是 使用壓縮記憶工具這件事情 必須要透過訓練才能取得 所以他們是微調了模型的參數 這跟剛才前面 ACON 不一樣 ACON 那個 paper 教模型做 summary 的時候 是沒調參數的 這邊是得調參數才能夠做到 你得逼迫去訓練語言模型 使用這些壓縮的工具 它才有辦法自己做壓縮 在這篇論文裡面 又有提到說 他們試圖硬是 Prompt 模型 努力的 Prompt 模型 看看能不能夠在 不微調模型的情況下 讓模型自己使用壓縮工具 他們發現模型很難 透過 Prompt 的情況下 穩定的使用壓縮工具 所以壓縮這個能力 是需要另外訓練的

</details>

## 五、Sub-agent 是一種自主壓縮

### Slide 17 — Spawn、Return 與上下文折疊 ([Video](https://www.youtube.com/watch?v=urwDLyNa9FU&t=1822s))

![Slide 17](slides/017_00-30-22.jpg)

主 Agent 透過 `spawn` 建立帶有 subtask 的 sub-agent。子 Agent 在獨立 Context 內呼叫同一類 LLM 和工具；完成後以 `return` 把結果交回主 Agent。

一旦 return，子 Agent 的完整搜尋與工具軌跡不再塞入主幹，只留下回傳摘要。因此從 Context Engineering 看，sub-agent 不只是「派小弟工作」，也是把一整段工作歷史自主壓成一個結果。

<details>
<summary><strong>整理後字幕</strong></summary>


> 我們上週也講到 sub-agent 的概念 sub-agent 可以看作是一種 自主的壓縮行為 當模型到某一個時間 它產生一個使用工具的指令 叫做 spawn 繁殖的時候 它就可以產生一個 sub-agent sub-agent 它仍然是跟原來的語言模型互動 sub-agent 它的 context 裡面可能有一個 subtask 告訴這個 sub-agent 要做什麼 這個 sub-agent 就把它的任務傳給語言模型 語言模型給它一個回覆 叫它用指令 它可能傳回指令導致的工具的輸出 然後這個狀況就一直下去 sub-agent 可能會有一個動作叫做 return 它可以執行一個工具叫 return return 裡面會告訴主 Agent 說 現在 sub-agent 它的輸出是什麼 它想給主 Agent 的資訊是什麼 當 sub-agent 執行 return 以後 它就把 return 的資訊丟給主 Agent 主 Agent 就可以繼續再跟 LLM 互動下去 當 sub-agent 執行 return 之後 它之前所做的事情 就通通從這一串 context 裡面被抹除 你就可以想成 這也是自動刪除記憶的一種方式 這一整段記憶就被改成了 return 裡面 寫的這句話 所以本來一直到 sub-agent 運作的時候 它的 context 都從這邊一直到這邊 但是當執行 return 以後 等於執行了一個自主壓縮 這一段對話紀錄就通通不見了 對話紀錄就從這邊開始 為了讓大家可以更直觀的了解

</details>

### Slide 18 — 鋸齒狀 Context 長度 ([Video](https://www.youtube.com/watch?v=urwDLyNa9FU&t=1918s))

![Slide 18](slides/018_00-31-58.jpg)

論文案例要求 Agent 找出符合多個條件的論文。每個子 Agent 分別搜尋論文、驗證作者等，工作期間 Context 上升，return 後只留下結論而驟降，形成鋸齒線。

若所有中間步驟都累積在主 Context，長度會超過十萬 token，突破模型上限。Sub-agent 使每段探索可局部膨脹、完成後收斂，讓主線維持可管理大小。

<details>
<summary><strong>整理後字幕</strong></summary>


> sub-agent 是怎麼運作的 我就截了這一篇 paper 裡面的一張圖 裡面就非常清晰的用個具體的例子 展示 sub-agent 對於 context 的長度的影響 這邊就是有一個很複雜的問題 它就說有一篇發表在 2023 年的論文 內容是跟什麼什麼主題有關的 然後這個作者有 3 個人 其中一個人是某個教授等等等等 我想說你都知道這麼多資訊 還自己找不到這篇論文 還要 Agent 幫你找 所以這顯然是一個蠻 artificial 的問題 但這是一個特別拿來考驗 Agent 能力的問題 看看 Agent 解不解得了 然後 Agent 看到這個問題之後 它就會首先開始搜尋相關的文章 每次 Agent 執行一個動作的時候 這個時候它的 context 都會逐漸的越來越長 它這邊就記錄了 context length 但是這一個語言模型 是有產生 sub-agent 的能力的 所以它先產生一個 sub-agent 所以我們來搜尋相關的論文 然後找到相關論文以後 它只把找到的論文的標題 傳回給主 Agent 所以這個時候整個 context 就縮短了 然後主 Agent 會再分裂一個 sub-agent 去執行另外一個任務 比如說驗證作者數是對的 這時候 context 又逐漸伸長 然後等找到這個作者的資訊之後 這個 context 又開始縮短 所以當你執行 sub-agent 的時候 對 context 而言 你當然是可以把 sub-agent 看作是 有一個主 Agent 帶了一堆小弟在工作 但是如果從 context engineering 的角度而言 所謂的 sub-agent 就是 對 context 做自主的壓縮 每次分裂一個 sub-agent 的時候 就是預示了某一段的 context 之後 會被壓縮掉 所以每次產生一個 sub-agent 的時候 你就可以累積 context 這個 sub-agent 結束的時候 一段 context 就不見了 你就會看到這個 context 有鋸齒狀的上升跟下降 它另外還特別說明說 假設如果沒有這個 sub-agent 所有的 context 都不斷的累積的話 最終會累積到十萬多個 token 超過了他們語言模型 可以吃的 token 的上限 所以對他們來說 能夠產生 sub-agent 也是蠻重要的能力 不過就像我剛才說的 語言模型不喜歡自主做壓縮 所以 sub-agent 這個能力

</details>

### Slide 19 — 訓練 Sub-agent 的獎勵設計 ([Video](https://www.youtube.com/watch?v=urwDLyNa9FU&t=2058s))

![Slide 19](slides/019_00-34-18.jpg)

只以答案正確作 reward，模型未必有理由使用 sub-agent；它可能直接把所有工作做在主 Context。研究因此加入主幹過長的懲罰，迫使模型委派。

反過來，子 Agent 也可能越界，把整題當成自己的任務而永不 return，所以还要懲罰超出 subtask 範圍的行為。有效委派需要同時約束主幹長度、子任務邊界與終止行為。

<details>
<summary><strong>整理後字幕</strong></summary>


> 通常不是天生的 它是後天取得的 它是需要經過訓練取得的 但今天很多模型 它都有產生 sub-agent 的能力 當你把你的 OpenClaw 接給 Claude 的時候 它有產生 sub-agent 的能力 但這可能不是一個自然原生的能力 它是需要經過特別的訓練 才能夠具備這種能力 在這篇論文裡面 他們就有針對產生 sub-agent 的能力 做了特別的訓練 怎麼訓練 他們是用 reinforcement learning 的方法 他們去用 reinforcement learning 的方法 去訓練語言模型 希望語言模型可以得到正確的答案 但他們發現 如果只用答案正確與否 來當作語言模型學習的信號的話 它不見得能夠學會正確的產生 sub-agent 因為假設你的目標只是得到正確的答案 對語言模型來說 有什麼理由它一定要產生 sub-agent 嗎 它就是努力得到正確的答案就好了 所以它是需要加上一些額外的 reward 才能夠去促使逼迫誘導語言模型 去使用 sub-agent 這個工具 比如說它有一個 reward 是 如果主幹的 context 過長就會被懲罰 主幹的 context 太長的話 就會有一個懲罰 所以今天語言模型會不得不 去分裂出一些 sub-agent 讓主幹不會太長 然後它又怕 sub-agent 永遠都不結束 有時候分裂出一個 sub-agent sub-agent 就自己把自己當作主 Agent 然後把所有事情都做完了 就失去產生 sub-agent 的意義 這種事情也是有可能發生的 所以它也要去懲罰一下 如果 sub-agent 做出超越範圍的事情 它直接自己把整個問題解完了 也是會受到懲罰的 用這種方法 才能夠訓練語言模型 使用 sub-agent 這個工具 講到目前為止

</details>

## 六、從源頭過濾，而不只是事後壓縮

### Slide 20 — Observation 才是 Context 的主要來源 ([Video](https://www.youtube.com/watch?v=urwDLyNa9FU&t=2166s))

![Slide 20](slides/020_00-36-06.jpg)

兩篇研究得到一致結論：模型產生的 action 約佔 6.5%，reasoning 約佔 9.6%，外部 observation 卻約佔 84%。軟體工程任務中也類似：執行和修改程式只佔小部分，約 76% Context 花在讀 repository 程式碼。

因此事後壓縮只是治標。若能在工具輸出進入 Prompt 前過濾，就能從源頭阻止無關文字膨脹。

<details>
<summary><strong>整理後字幕</strong></summary>


> 我們剛才都是在提壓縮 也就當我們 context 過長的時候 把過長的 context 把它弄短 但是那是治標 我們能不能治本，一開始 就不要讓 context 過長 怎麼樣不讓 context 過長 你就要分析一下說 現在到底是什麼樣的資訊 讓 context 過長 這邊 有兩篇論文都有做類似的分析 而且分析的結果非常的一致 所以左邊這篇論文 它說 它分析了 假設我們沒有做 context engineering 就記錄 現在在整個對話的歷程中 到底模型做了什麼事情 到底這些 token 來自於什麼樣的行為 到底這些 token 都代表了什麼樣的事情 它做了一個分析 它分析的結果是這樣的 這邊 action 指的是 模型去產生執行工具的指令 這些指令通常很簡短 所以只佔了歷史記錄的 6.5% Reasoning 指的是模型自己說出來的話 語言模型自己說出來的話 這個也很簡短 只佔 9.6% 在整個 context 裡面 什麼樣的 token 佔據了多數的 context 它發現所謂的 observation 佔據了幾乎 84% 左右的 context 這些 observation 指的是來自外界的輸入 比如說語言模型讀了一個檔案 打開 裡面整個檔案所有的資訊 都變成 context 的一部分 它執行了某一個工具 工具有非常長的輸出 些輸出變成 context 的一部分 這些來自外界的輸入 才佔據了多數 context 的內容 另外一篇論文 它也得到幾乎一樣的結論 另外一篇論文 它是主要 focus 在 個 software engineering 上面 所以它主要是讓模型 去改程式 還有執行程式 它發現當模型 在做 software engineering 的時候 它只有 12% 的 context 是在執行程式碼 只有 11.8% 的 context 是在修改程式碼 多數的時候它都在讀程式碼 有 76% 的 context 是花在 把整個 repo 裡面的程式碼讀進來 所以佔了非常大量的 context 所以有沒有辦法直接治本 一開始就不要讓這麼多的文字進入 context

</details>

### Slide 21 — 智慧型 Read：只返回和任務相關的片段 ([Video](https://www.youtube.com/watch?v=urwDLyNa9FU&t=2304s))

![Slide 21](slides/021_00-38-24.jpg)

傳統 `read` 會把整個 log 原封不動送入模型，大檔案可能讓模型「噎到」。改良介面讓模型同時指定檔案和需求，例如「讀取 log 中和修 bug 有關的內容」。

工具內部可用小型語言模型先篩選，再把相關片段交給主 Agent。這把智慧移到資料入口，減少主模型必須消化的噪音，但也增加工具實作和小模型判斷錯誤的風險。

<details>
<summary><strong>整理後字幕</strong></summary>


> 所以就有一些論文提出了一些想法 我們也許應該在 observation 進到語言模型之前 就做一些過濾的行為 一般我們在執行讀一個檔案 或讀一個文件的時候 常見的做法就是語言模型 它輸出一個指令 說我要讀一個 log 檔案 然後你有一個叫做 read 的工具 這 read 的工具就把 log 檔案找到 然後把 log 檔案的內容 原封不動地、一口氣地 逼語言模型吞下去 如果這個 log 檔案非常大 有時候語言模型就會哽到 所以怎麼辦 也許我們需要一個更聰明的 read 的工具 我們也許可以讓語言模型 它在輸出指令的時候 它不只說我想要讀 log 檔案 它還說我想要讀 log 檔案裡面 跟修復 bugs 有關的內容 希望這個 read 的指令夠聰明 它不只能夠打開一個檔案 它還能夠從檔案裡面 找出真正重要的部分 這個 read 的指令 顯然它需要有一點 intelligence 在 它去讀了這個 log 從 log 裡面 把跟 bug fixing 有關的 content 把它讀出來 語言模型只 focus 在 跟 bug fixing 有關的內容上面 我剛才說這個 read 的指令 顯然它需要有一點智能 或者是你需要 做比較多的 engineering 去 implement read 的這個函式 在這篇論文裡面 他們就是訓練了一個 小的語言模型 所以這個 read 本身 也是一個小的語言模型 這個小的語言模型本來就可以吃這個指令 根據這個指令找出合適的內容 再傳給主要的 agent 講到這邊我們也可以回顧一下

</details>

### Slide 22 — Memory Search 與 Memory Get 的分工 ([Video](https://www.youtube.com/watch?v=urwDLyNa9FU&t=2404s))

![Slide 22](slides/022_00-40-04.jpg)

OpenClaw 不直接用一般讀檔把整份 Memory 塞進 Prompt。`memory_search` 先找相關位置；`memory_get` 再根據起始行和行數只載入小片段。

兩者分工體現「檢索」與「取值」的區別：search 決定哪裡可能重要，get 控制實際進入 Context 的範圍。Memory 是外部資料；只有被 get 載入的片段才成為當下 Prompt。

<details>
<summary><strong>整理後字幕</strong></summary>


> 看看之前在講 OpenClaw 的時候 它是怎麼處理 memory 的 在講處理 memory 的時候 我們說它有兩個函式 一個叫 memory search 一個叫 memory get 它有兩個工具 我們並沒有細講 為什麼它需要 memory get 這個工具 你可以想說 為什麼讀 memory 還需要個特別的工具 讀 memory memory 又不是什麼神奇的東西 它就是文字檔 它不是什麼神奇的東西 用一般的函式 用一般讀檔的函式 也可以把那個檔案的內容 通通讀出來 為什麼在讀 memory 的時候 OpenClaw 要設計一個 特別的工具去讀 memory 就是為了做到 我剛才在前一頁投影片裡面 講的過濾 memory get 這個函式 它不是只給它要讀的檔案 它還會給額外的兩個數字 代表說從這個檔案的第幾行開始讀起 然後我們總共要讀多少行 所以 memory get 是從整個巨大的 memory 檔案裡面 只存取一部分出來 因為 OpenClaw 當初在設計的時候 害怕 memory 裡面存了非常大量的資料 把所有資料一次都讀到語言模型的 context 裡面 語言模型會哽到 所以它就只從 memory 裡面選一小段的內容 至於要怎麼選一小段的內容 到底一整個 memory file 要取哪裡 由 memory search 的結果來決定 根據 memory search 的結果 還有語言模型自己的判斷 去使用 memory get 這個工具 只存取 memory 這個檔案的一小部分 這個也是過濾的概念

</details>

### Slide 23 — MCP-Zero、按需載入工具與 Skill ([Video](https://www.youtube.com/watch?v=urwDLyNa9FU&t=2496s))

![Slide 23](slides/023_00-41-36.jpg)

工具描述本身也會佔 Context；單一 GitHub 工具的說明可能就有 4,600 token。若把所有工具永久寫入 System Prompt，很快會超過窗口，因此工具應按需載入。

只靠使用者原始要求搜尋工具並不可靠，例如「修 bug」隱含 read、edit 等多步需求。MCP-Zero 讓 LLM 先推理並表達工具需求，再用該需求搜尋工具庫。這和 OpenClaw Skill 相似：Skill 是描述工作流程的外部檔案，需要時才讀入 Prompt；它不同於 Tool，Tool 是真正执行操作的介面。

<details>
<summary><strong>整理後字幕</strong></summary>


> 另外一個過濾的概念 就是按需加載 有一篇 paper 叫做 MCP-Zero 我們一般在讓 AI agent 使用工具的時候 你就是把使用工具的指令 有哪些工具 這些工具可以拿來幹 把它放在語言模型的 system prompt 裡面 這個 system prompt 在有了這些工具的指令之後 可能會非常的長 MCP 這篇 paper 裡面 就特別提到說 舉個例子 比如說有一個使用 GitHub 的工具 這個使用 GitHub 的工具 足足有 4600 個 token 而且這只是使用 GitHub 的工具而已 如果有更多的工具 模型就會直接超過它的 context window 可以承受的上限 所以怎麼辦 工具這種東西 應該是要動態加載的 過去比較傳統的方法是說 根據使用者輸入的任務 再去挑選合適的工具 這跟 RAG 的概念是非常類似的 假設這些工具的說明 都被存在一個非常巨大的資料庫裡面 今天有一個新的任務進來 根據這個任務去啟動一個搜尋引擎 去工具的資料庫裡面進行搜尋 把相關的工具指令 把它抽取出來 讓模型知道有哪些工具可以用 它就可以執行這些工具 來得到我們想要的結果 但這篇論文就是發現說 這不是一個特別好的方法 因為今天使用者的需求往往非常的模糊 所以不容易根據使用者的需求來判斷需要使用哪些工具 比如說今天使用者的需求可能是幫我修改這個 bug 但是修改 bug 要用的工具不止一個 比如說模型會需要至少先用讀檔的工具能讀檔 然後看了這個程式以後 再用一個這個 edit 編輯的工具才能夠修改這個程式 所以今天雖然使用者只說了 幫我修改這個程式 或幫我 debug 但被喚用的工具 是好幾個 你很難直接從使用者 問到這個問題 讓搜尋引擎決定 要使用哪些工具 所以這篇 paper 它提出來的核心想法就是 我們何不讓語言模型 用 AI 動態地決定 它自己需要什麼工具 讓語言模型輸出 它想要什麼 所以語言模型 可能在讀到任務的指令之後 它想一想 就輸出一個任務的需求 輸出一個工具的需求 用這個工具的需求去操控搜尋引擎 讓搜尋引擎找出它需要的工具 然後它就可以使用它需要的工具 來解接下來的任務 這件事情 你可能覺得聽起來很熟悉 這個就是 OpenClaw 裡面 所用的 skill 的概念 skill 這個東西 它也是按需加載的 我們不會把所有的 skill 都放到 context 裡面 我們不會把所有的 skill 都放到這個 prompt 裡面 只有在需要的時候 才從硬碟裡面 把 skill 讀出來 放到 prompt 裡面 這個就是按需加載的概念

</details>

## 七、Agentic Context Engineering

### Slide 24 — 把 Context 更新函數交給 LLM ([Video](https://www.youtube.com/watch?v=urwDLyNa9FU&t=2674s))

![Slide 24](slides/024_00-44-34.jpg)

傳統 $F$ 由工程師寫死；Agentic Context Engineering 則讓另一個 LLM 讀取舊 Context、輸入和輸出，自行產生下一版 Context。這把 Context Engineering 本身變成 Agent 能做的任務。

實作通常不讓模型任意修改全部內容。System Prompt 含身份和關鍵規則，應固定保護；只提供一個可編輯區塊讓模型整理。郵件事件已說明，若安全約束被納入可壓縮區，可能在摘要中消失。

<details>
<summary><strong>整理後字幕</strong></summary>


> 講到這邊 我們就講了一些有關 context engineering 的想法 但到目前為止 多數 context engineering 也就是這個大 F 要做的事情 都是人類決定的 人類編寫好、寫死了固定的指令 這邊就是一些寫死的指令 然後讓你的電腦 讓你的程式按照這些寫死的指令 來處理 context 但是有沒有辦法 讓這個 context engineering 做得更複雜 更有智慧 做得更好 有一個想法叫做 Agentic Context Engineering 這個說法就是來自於一篇 叫 Agentic Context Engineering 的 paper 然後把論文的連結也放在這邊 這邊想法的核心就是 把 context engineering 也交給語言模型 也不給人類設計 直接交給語言模型 讓它自己想辦法 幫自己做 context engineering 你覺得本來大 F 是人類工程師設計的 現在直接交給語言模型工程師 看看它有沒有更好的想法 這邊這個 Agentic Context Engineering 的概念 如果要畫成圖的話就是這樣 你現在有一個 context 然後呢這個 context 會加上一個輸入 語言模型給一個輸出 接下來把 context 輸入輸出 全部串起來 直接丟給一個語言模型 然後它愛幹嘛就幹 得到一個新的 context 我們叫 context t+1 然後呢前面可能接個 system prompt 然後後面加個 input 然後再從語言模型那邊得到 output t+1 然後再有一個語言模型 把 context t+1、input t+1、output t+1 再變成 context t+2 這個步驟就反覆繼續下去 我這邊在畫圖的時候 沒有把 system prompt 加到 context 裡面 你要把 system prompt 視為 context 的一部分也可以 不過如果你細讀這些 Agentic Context Engineering 的 paper 的話 你會發現實際上它讓語言模型 自己處理的 context 是全部 context 的一部分 它們通常就是留一個區塊 這個區塊給語言模型 愛玩什麼就玩什麼 但是比較重要的東西 比如說 system prompt 裡面是包含了 這個 AI agent 本身的 identity 真正重要的資訊的 這個是不能夠隨便亂動的 所以通常你就固定住它 不要動它 這一系列 Agentic Context Engineering 的 paper 通常只改整個 context 裡面的 其中一部分而已 Agentic Context Engineering 一個比較早期的 paper

</details>

### Slide 25 — Dynamic Cheatsheet：用 Prompt Engineering 管理 Context ([Video](https://www.youtube.com/watch?v=urwDLyNa9FU&t=2822s))

![Slide 25](slides/025_00-47-02.jpg)

Dynamic Cheatsheet 把可更新 Context 稱為「小抄」。它用一段長 Prompt 指示模型保留未來可重用的策略、程式片段和關鍵發現，捨棄只適用於當前案例的瑣碎資訊。

本質上，這是用 Prompt Engineering 實現 Context Engineering：效果高度依賴更新指令是否清楚界定長期價值、具體性和資訊淘汰原則。

<details>
<summary><strong>整理後字幕</strong></summary>


> 可能是 Dynamic Cheatsheet 它就把這個 context 叫做 cheatsheet 叫做小抄 只是這個小抄 是會隨時間變化的 概念非常簡單 就是呼叫一個語言模型 給它一段 prompt 跟它說 我們這個 context 要怎麼改比較好 然後它就把 context t input t output t 改成 context t+1 就結束了 這邊它的核心 就是 prompt engineering 把這段 prompt 寫好 希望語言模型讀了這段 prompt 自己知道怎麼做 context engineering 也就是用 prompt engineering 來做 context engineering 這段 prompt 非常的長 仔細讀下來 它的核心精神就是 存下未來能用的東西 就它告訴語言模型說 你不要存一些很 specific 的東西 你要存的是精神概念 比如說什麼有效的策略 可以把它存起來 如果你寫一段程式 你覺得之後用得上 也把它存起來 關鍵的發現也存起來 但是非常跟現在這個任務 有具體關聯的東西 可能之後都用不上了 就不要存起來 這邊就是用 prompt engineering 來做 context engineering 像這樣的 paper 呢

</details>

### Slide 26 — Playbook：多模型審查與增量修改 ([Video](https://www.youtube.com/watch?v=urwDLyNa9FU&t=2894s))

![Slide 26](slides/026_00-48-14.jpg)

Agentic Context Engineering 論文把 Context 稱為 playbook（工作守則），並用三個 LLM 模組從不同角度檢查後，產生「修改指令」而非整本重寫。

增量修改可降低舊知識被整體生成意外破壞的機率，類似對文件做 patch。代價是流程更複雜，而且多個模型的審查仍可能共享盲點。

<details>
<summary><strong>整理後字幕</strong></summary>


> 現在很多 比如像 Agentic Context Engineering 這篇 paper 裡面 它就做了更複雜的 它把它的這個 context t 到 context t+1 就經過了更複雜的流程 它把它的 context 取了另外一個名字叫做 playbook 就是一個守則手冊 它希望語言模型 看著這個手冊 做它應該做的事情 這篇 paper 實際上做的事情 我就不細講 這個 playbook 的演化 不是只有一個步驟 要過三個語言模型 這三個語言模型 分別做了不同的檢查之後 最後產生一個修改 playbook 的指令 它不是直接產生新的 playbook 因為它怕直接產生新的 playbook 搞不好一些舊的資訊就被弄壞了 所以它是去修改舊的 playbook 所以這三個模組合起來 會產生一個修改的指令 用這個修改的指令 去修改原來 playbook 的內容 把 context t 原來的 playbook 變成 context t+1 變成一本新的員工守則 這是 Agentic Context Engineering 這篇 paper 做的事情 還有另外一篇 paper 呢

</details>

### Slide 27 — Recursive Language Model 與外部無限 Context ([Video](https://www.youtube.com/watch?v=urwDLyNa9FU&t=2960s))

![Slide 27](slides/027_00-49-20.jpg)

Recursive Language Model 宣稱可處理近乎無限長輸入，實際做法是把大部分 Context 放在硬碟 $M$，Prompt $P$ 只保留長度、分段和位置等 metadata。LLM 寫程式搜尋硬碟，取回所需內容並更新 $P$。

這可看作模型自主實作 RAG。講者提醒不要過度神化：論文 Prompt 已多次暗示模型應搜尋和檢索，因此成功不完全是模型憑空發明策略； nevertheless，實驗效果仍然很好。

<details>
<summary><strong>整理後字幕</strong></summary>


> 叫做 Recursive Language Model 它也是 Agentic Context Engineering 的 其中一個可能性 這篇 paper 曾經一度非常的知名 因為它 號稱說 它發明了一個新的語言模型 這個語言模型 可以吃無窮長的輸入 它真正做的事情 就是 context engineering 它做的事情是這樣 它說 假設現在的 context 真的可以非常非常的長 非常非常長怎麼辦 就通通放到 hard disk 裡面 我們只把這邊的 context 拿非常非常小一部分 load 到 memory 的 prompt 裡面 它這邊 paper 裡面說 這些資訊呢叫做 metadata 比如說它只記了 現在這個 context 到底有多長 然後 context 呢被切成幾段 context 呢被存在哪裡等等 非常簡短的資訊 如果用我們這篇 paper 的符號來講 這些存在 hard disk 裡面的東西 就是 M 這些會真的 load 到 memory 裡面 被 load 這邊不應該講 memory 這邊講 memory 大家可能會覺得很困惑 這邊真的被放到 prompt 裡面的 叫做 P LLM 做的事情就是 看著這個 P 然後去詳細看看 它要從 M 裡面 找尋什麼樣的資訊 然後發現語言模型很厲害 因為這個語言模型可以寫程式 它會寫程式 去對 hard disk 裡面的內容做搜尋 因為它會自己自主地知道要做 RAG 然後它自己知道說 它要去 hard disk 裡面搜尋一些東西出來 把這些搜尋的東西拿出來 去修改它的 metadata 所以 P_t 就變成 P_t+1 這邊 paper 裡面還有一個章節 討論了這個模型的這些自主產生的 pattern 但是實際上到底有沒有那麼神奇 真的是見仁見智 因為如果你仔細去讀它的 prompt 的話 因為這些做 context engineering 的 LLM 背後是需要做 prompt engineering 的 你只要去讀它的 prompt 的話 就只差沒有教語言模型 說你直接做 RAG 了 它花了蠻多力氣 不斷地暗示語言模型 說你可以做 RAG 這件事 所以語言模型就寫了一個程式做 RAG 實際讀它的 prompt 我覺得也沒那麼神奇 不過它的表現是非常好的

</details>

### Slide 28 — 長 Context Benchmark 的效果 ([Video](https://www.youtube.com/watch?v=urwDLyNa9FU&t=3096s))

![Slide 28](slides/028_00-51-36.jpg)

原生 GPT-5 隨輸入增長，在部分長 Context 任務上正確率顯著下降。外掛 Recursive Language Model 後，即使總資料達一百萬 token，模型仍可在多個 benchmark 維持較好表現。

重點不是擴大模型物理窗口，而是避免把全部資料同時送入：大量內容存在外部，只讓模型反覆檢索和載入當下需要的部分。

<details>
<summary><strong>整理後字幕</strong></summary>


> 它說你看原來的 GPT-5 這個是個很好的模型 如果輸入越來越長 輸入越來越長 到某個長度 有些任務 它就解不了了 這邊 All-Long 這些 benchmark 就是測試語言模型 在 context 非常長的情況下 它能不能夠好好的運作 但是加上它的 這個 Recursive Language Model 以後 因為它的 Recursive Language Model 是一個 context engineering 的方法 所以它可以外掛在 任何現有的語言模型上 所以如果外掛在 GPT-5 上 就可以讓本來 已經很厲害的 GPT-5 變得更厲害 在輸入真的非常長 比如說長達 1M 100 萬個 token 的時候 仍然可以在這一些 長 context 的 benchmark 上面 做出不錯的效果

</details>

### Slide 29 — 總結：$F$ 是 Context Engineering 的核心 ([Video](https://www.youtube.com/watch?v=urwDLyNa9FU&t=3146s))

![Slide 29](slides/029_00-52-26.jpg)

本講以 $C=(P,M)$ 統整：$P$ 是送入 LLM 的 Prompt，$M$ 是外部儲存；更新函數 $F$ 決定摘要、遮蔽、記憶讀寫、過濾、工具載入與子 Agent 邊界。

新研究進一步嘗試把 $F$ 從人類寫死的規則，變成由 LLM 自主維護。但關鍵安全資訊不應任意交給可壓縮區處理，仍需固定規則、保護區和驗證。

<details>
<summary><strong>整理後字幕</strong></summary>


> 今天就是比較系統化的 跟大家介紹了 context engineering 我們這邊有一個演算法 這個演算法 摘要了 context engineering 實際上做的事情 我們也跟大家說 context 分成兩部分 一部分是 M 它是存在你的 hard disk 裡面的 一部分是 P 它是真的會當作 prompt 丟給語言模型的 有一系列比較新的研究 嘗試說 把 context engineering 裡面 這個最關鍵的 F 看能不能不要由 人類工程師來設計 也把它交給語言模型 這個部分 要跟大家分享的是 context engineering

</details>

## 八、概念對照

| 概念 | 定義 | 與相近概念的區別 |
|---|---|---|
| Context $C$ | Agent 可用的全部歷史與外部狀態 | 包含會進模型的 $P$ 和不直接進模型的 $M$ |
| Prompt $P$ | 本輪真正送入 LLM 的內容 | 只是 Context 的子集，不等於所有記憶 |
| Memory $M$ | 硬碟、資料庫或檔案中的外部資訊 | 只有被搜尋並載入的片段才進 Prompt |
| Tool | Read、write、search、fold、spawn 等可執行介面 | Tool 改變或讀取外部狀態 |
| Skill | 描述何時及如何使用工具的外部 SOP | Skill 按需載入 Prompt，本身不是執行器 |
| Summarization | 用模型把一段歷史濃縮 | 可能 context collapse，且不等同永久記憶 |
| Observation masking | 用短標記替換工具輸出 | 便宜，但可能造成模型重複工具步驟 |
| Filtering | 資料進 Prompt 前只選相關片段 | 從源頭控制長度，而非累積後再壓縮 |
| Sub-agent | 獨立 Context 中完成子任務並 return | 從主幹看，相當於把整段子軌跡壓成回傳值 |
| Agentic Context Engineering | 由 LLM 自主更新可編輯 Context | 重要 System Prompt／安全規則通常仍需固定 |

## 九、安全與可靠性教訓

- 壓縮不是無害的文字摘要；遺失任務約束會直接改變 Agent 行為。
- 「刪除前需同意」等不可違反的規則應置於受保護的 System Prompt 或政策層，而非只留在可壓縮對話。
- 模型可能拒絕或忽略壓縮工具，因此要有框架門檻、強制策略或經過驗證的訓練。
- 工具輸出過濾會省 Context，但篩選器可能漏掉關鍵證據；應保留原始資料的可回溯位置。
- Sub-agent 要限制子任務範圍並要求 return，避免子 Agent 無限延伸或越權完成整個任務。
- Agentic Context 更新應使用可編輯區、增量修改和驗證，不應讓模型任意重寫身份與安全約束。

## 十、關鍵結論

1. Context Engineering 的目標不是讓輸入越短越好，而是以有限 token 保留完成任務所需的資訊。
2. 壓縮、外部記憶、過濾、按需載入與 sub-agent 是同一問題的不同解法：控制什麼在何時進入 Prompt。
3. Context 與 Prompt 不同；Memory 只有在取回後才成為 Prompt 的一部分。
4. Context collapse 和軌跡延長說明，縮短單輪 Prompt 不等於提高正確率或降低總成本。
5. 未來的方向是讓模型參與維護 Context，但不可把不可違反的規則也交給它自由壓縮。
