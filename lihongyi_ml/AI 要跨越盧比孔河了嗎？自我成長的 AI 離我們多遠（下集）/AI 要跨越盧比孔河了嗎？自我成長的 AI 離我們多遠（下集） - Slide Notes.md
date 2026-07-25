# AI 要跨越盧比孔河了嗎？自我成長的 AI 離我們多遠（下集）

- 講者：李宏毅
- 影片：[YouTube](https://www.youtube.com/watch?v=cQLKVzbwN7I)
- 長度：1:09:08
- 字幕：原始繁體中文字幕

本講延續上集，討論自動優化 Prompt、Workflow、模型參數與學習規則，並分析持續學習、內在動機及失控風險。時間資料保存在 `source/transcript.txt` 與 `slides/index.csv`。


## 一、從更新參數到更新 Harness

### Slide 1 — 自我成長的控制變數 ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=0s))

![Slide 1 — 自我成長的控制變數](slides/001_00-00-00.jpg)

下集把可更新對象擴展到模型參數與 Harness。真正目標仍由人類定義，自動改進系統則搜尋更好的權重、prompt、工具與工作流程。 本段重點：那我們就來上課吧 就接續上一次的課程 我們來講人工智慧能不能自我成長 上次我們的故事是這樣開場的


<details>
<summary><strong>Cleaned narration</strong></summary>

> 那我們就來上課吧 就接續上一次的課程 我們來講人工智慧能不能自我成長 上次我們的故事是這樣開場的

</details>


### Slide 2 — 自我成長的控制變數（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=9s))

![Slide 2 — 自我成長的控制變數（續）](slides/002_00-00-09.jpg)

下集把可更新對象擴展到模型參數與 Harness。真正目標仍由人類定義，自動改進系統則搜尋更好的權重、prompt、工具與工作流程。 本段重點：我們說假設有一天人類創造出了一個很厲害的人工智慧 這個人工智慧它可以創造出更厲害的人工智慧 或者是它可以自我成長 讓自己變得比原來還厲害的話 這個可以創造人工智慧的人工智慧 就是人類最後的發明 當這個發明誕生的時刻 就是科技起點 大家常常聽到科技起點這個詞彙 意思就是我們創造了 能夠創造人工智慧的人工智慧 我們就接下來看看 我們離這一步到底還有多遠


<details>
<summary><strong>Cleaned narration</strong></summary>

> 我們說假設有一天人類創造出了一個很厲害的人工智慧 這個人工智慧它可以創造出更厲害的人工智慧 或者是它可以自我成長 讓自己變得比原來還厲害的話 這個可以創造人工智慧的人工智慧 就是人類最後的發明 當這個發明誕生的時刻 就是科技起點 大家常常聽到科技起點這個詞彙 意思就是我們創造了 能夠創造人工智慧的人工智慧 我們就接下來看看 我們離這一步到底還有多遠

</details>


### Slide 3 — 自我成長的控制變數（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=45s))

![Slide 3 — 自我成長的控制變數（續）](slides/003_00-01-45.jpg)

下集把可更新對象擴展到模型參數與 Harness。真正目標仍由人類定義，自動改進系統則搜尋更好的權重、prompt、工具與工作流程。 本段重點：其實上一次的課程呢 我們主要集中在 怎麼自己定義 Loss 這個函式 怎麼在沒有人類介入的情況下 人工智慧自己定了自己的學習目標 我們這邊用比較抽象的符號 來描述一下我們上週說的事情 假設一個人工智慧 我們用 A 來表示它 這個人工智慧有一個下標 θ 這個 θ 代表它控制了 這個人工智慧的行為 這個 θ 是人工智慧背後的語言模型 我們人類有一個 我們真正想要人工智慧做的事情 我這邊用 L-hat L 加一個上標 hat 來代表我們真正想…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 其實上一次的課程呢 我們主要集中在 怎麼自己定義 Loss 這個函式 怎麼在沒有人類介入的情況下 人工智慧自己定了自己的學習目標 我們這邊用比較抽象的符號 來描述一下我們上週說的事情 假設一個人工智慧 我們用 A 來表示它 這個人工智慧有一個下標 θ 這個 θ 代表它控制了 這個人工智慧的行為 這個 θ 是人工智慧背後的語言模型 我們人類有一個 我們真正想要人工智慧做的事情 我這邊用 L-hat L 加一個上標 hat 來代表我們真正想要人工智慧做的事情 通常在論文裡面 這個 L-hat 都是用某一個 Benchmark 來代表 比如說你想要讓機器 去考數學奧林匹亞 如果它在自我演化之後 它考出來的成績比較高分 你就會說 這個進化 這個演化是成功的 機器有自我成長 當然在現實生活中 通常我們要機器 做的事情更複雜 可能很難直接 用一個 Benchmark 來衡量 但是在多數研究裡面 為了簡化起見 你通常都一個 Benchmark 來代表機器有沒有越做越好 我們用 L-hat 來表示它 在上週的課程裡面 我們講說機器可以自己定自己的 Loss 函式 這邊用 L 沒有加任何上下標 來代表機器自己定出來的這一個 Loss 函式 這個 Loss 函式當然它的輸入呢 也是這個模型本身的參數 也就是 A_θ 它可以判斷這個 A_θ 做得怎麼樣 但同時它會受到另外一個變數的控制 這邊我們寫作 H 這個 H 是人類給機器的一些資訊 這些資訊其實可以看作是這個 Benchmark 或者是這個 L-hat 的一個 proxy 一個代表 就人類很難講清楚自己要什麼 但是他提供了一些額外的資訊 給這個 AI 讓它定出了 Loss Function 讓它可以根據這個 Loss Function minimize 這個 Loss Function 來進行學習 在一般的機器學習裡面 這個 H 最常見的型態就是訓練資料 你用訓練資料來告訴機器 它到底應該要學什麼 但在上週的課程裡面 我們也看到了各式各樣的變化 你不一定要給機器訓練資料 你光是提供給它一些輸入 比如說給它一些教科書 可能也有幫助 甚至在很多例子裡面 你只要告訴機器一個目標 告訴它說現在把數學學好 也許它去考奧林匹亞的時候 它能力就變強了 所以你甚至可以直接用一個命令 來當作這個 H 這個 H 就是人類對於我們要的目標的 一個 proxy 一個描述 一個簡化 那有了這個 L 以後 接下來的學習 其實跟一般的機器學習

</details>


### Slide 4 — 自我成長的控制變數（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=222s))

![Slide 4 — 自我成長的控制變數（續）](slides/004_00-04-42.jpg)

下集把可更新對象擴展到模型參數與 Harness。真正目標仍由人類定義，自動改進系統則搜尋更好的權重、prompt、工具與工作流程。 本段重點：沒有什麼太大的不同 你就是做 gradient descent 計算出這個參數 θ 對 L 的 gradient 就跑 gradient descent 去 update 參數 把 θ 變成 θ' 期待說現在這一個 AI agent 裡面的參數 變成 θ' 以後 它拿來做這個 benchmark 在 L-hat 上衡量起來 衡量起來的結果是更好的 在這邊我們是假設這個 L 都是越小越好 因為它是一個 Loss 如果你是看這個 RL 的文…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 沒有什麼太大的不同 你就是做 gradient descent 計算出這個參數 θ 對 L 的 gradient 就跑 gradient descent 去 update 參數 把 θ 變成 θ' 期待說現在這一個 AI agent 裡面的參數 變成 θ' 以後 它拿來做這個 benchmark 在 L-hat 上衡量起來 衡量起來的結果是更好的 在這邊我們是假設這個 L 都是越小越好 因為它是一個 Loss 如果你是看這個 RL 的文獻的話 通常是定義成 reward 是越大越好 不過背後的概念是一模一樣 所以有了這個機器自己定出來的 L 之後 它就可以套用一般的 你常常在深度學習裡面 看到的 gradient descent 來 update 這個 θ 把 θ update 成 θ' 之後 你就把這個 θ 用 θ' 取代 就可以 iterative 的 讓模型去更新它的參數 希望這個更新 可以讓模型變得越來越好 這是我們上週說的事情

</details>


### Slide 5 — 自我成長的控制變數（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=285s))

![Slide 5 — 自我成長的控制變數（續）](slides/005_00-05-45.jpg)

下集把可更新對象擴展到模型參數與 Harness。真正目標仍由人類定義，自動改進系統則搜尋更好的權重、prompt、工具與工作流程。 本段重點：我們上週最後說到說 這個整個過程中 甚至可以不用任何人類介入 你可以有一個 proposer 專門出題 有一個 solver 專門解題 有一個 verifier 驗證 solver 它解的題目對不對 中間幾乎不需要人類介入 也有一些比較近期的文獻中指出 你給 proposer 一些額外的資訊 比如說給它教科書或給它一些例子 它可以做得更好


<details>
<summary><strong>Cleaned narration</strong></summary>

> 我們上週最後說到說 這個整個過程中 甚至可以不用任何人類介入 你可以有一個 proposer 專門出題 有一個 solver 專門解題 有一個 verifier 驗證 solver 它解的題目對不對 中間幾乎不需要人類介入 也有一些比較近期的文獻中指出 你給 proposer 一些額外的資訊 比如說給它教科書或給它一些例子 它可以做得更好

</details>


### Slide 6 — 自我成長的控制變數（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=312s))

![Slide 6 — 自我成長的控制變數（續）](slides/006_00-05-12.jpg)

下集把可更新對象擴展到模型參數與 Harness。真正目標仍由人類定義，自動改進系統則搜尋更好的權重、prompt、工具與工作流程。 本段重點：那上週我們講到這個地方 那但是對一個 AI agent 而言 它不是只有背後的語言模型 在這堂課裡面 我們反覆跟大家講說 AI agent 其實至少有兩個部分所構成 一個是它的 harness 另外一個是它的語言模型 我們已經講說 這個語言模型可以不斷地更新 另外一方面 這個 harness 能不能夠持續地更新呢 harness 作為 AI agent 的一部分 它也可以套用非常類似的方法 持續進行更新


<details>
<summary><strong>Cleaned narration</strong></summary>

> 那上週我們講到這個地方 那但是對一個 AI agent 而言 它不是只有背後的語言模型 在這堂課裡面 我們反覆跟大家講說 AI agent 其實至少有兩個部分所構成 一個是它的 harness 另外一個是它的語言模型 我們已經講說 這個語言模型可以不斷地更新 另外一方面 這個 harness 能不能夠持續地更新呢 harness 作為 AI agent 的一部分 它也可以套用非常類似的方法 持續進行更新

</details>


### Slide 7 — 自我成長的控制變數（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=348s))

![Slide 7 — 自我成長的控制變數（續）](slides/007_00-06-48.jpg)

下集把可更新對象擴展到模型參數與 Harness。真正目標仍由人類定義，自動改進系統則搜尋更好的權重、prompt、工具與工作流程。 本段重點：所以今天我們在描述一個 人工智慧的時候 應該不只有下標 θ 它其實還應該要有另外一個下標 叫做 H 這個 H 代表了它的 harness 是人工智慧背後的 語言模型的參數 θ 加上套用的 harness H 合起來 才決定了這個人工智慧的行為 我們一樣有一個人類想做的事 叫做 L-hat 今天你可以套用任何 我們在上一堂課裡面 已經學到的方法 定義出這個 L 你理論上定義出 L 之後 你也許就可以用某一些方法 來讓你的 harness …


<details>
<summary><strong>Cleaned narration</strong></summary>

> 所以今天我們在描述一個 人工智慧的時候 應該不只有下標 θ 它其實還應該要有另外一個下標 叫做 H 這個 H 代表了它的 harness 是人工智慧背後的 語言模型的參數 θ 加上套用的 harness H 合起來 才決定了這個人工智慧的行為 我們一樣有一個人類想做的事 叫做 L-hat 今天你可以套用任何 我們在上一堂課裡面 已經學到的方法 定義出這個 L 你理論上定義出 L 之後 你也許就可以用某一些方法 來讓你的 harness H 進行更新 從 H 變成 H' 希望 H' 可以得到更低的 Loss 你把原來的 H 置換成 H' 以後 你就可以不斷地迭代 不斷地更新你的 harness 但在整個過程中 有一個比較困難的 在過去課程中 我們比較少碰觸的問題就是 怎麼更新 harness 計算參數 θ 的 gradient 這個是大家都知道的事情 但是 harness H 這個東西 它甚至很難用一組參數來表示它 你根本不知道要怎麼計算 harness 對大 L 對你的 Loss 的微分 所以怎麼辦呢 怎麼更新這個 harness 呢 有一個常見的做法是 直接拿一個語言模型來更新 harness 就找一個語言模型來 這個語言模型可以是要進化 要成長的模型本身 也可以是一個額外的固定的 independent 的模組 總之有一個語言模型 你告訴它說 有一個 harness 長得像 H 這個樣子 通常 harness 你可以用 一組程式碼來描述它 所以這邊有一組程式碼 這個就是我的 harness 這個就是我現在的 agent 的 harness 長成這個樣子 這組程式碼呢 拿去跑 benchmark 但這個 benchmark 是模型內部 自己定出來的 Loss 它不一定是人最終要的那個 Loss 模型可以自己定出一個 Loss 拿這個 harness 去跑 得到一個分數 問這一個語言模型說 你能不能夠自己想出一個 更好的 harness 叫做 H' 如果可以的話 如果可以想出更好的 harness H' 的話 我們就可以更新這個 harness 就可以讓我們要成長的這個模型 它的 harness 不斷地演進 能夠用這樣子的方法

</details>


## 二、Prompt Optimization

### Slide 8 — 讓 Prompt 自動演化 ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=492s))

![Slide 8 — 讓 Prompt 自動演化](slides/008_00-08-12.jpg)

從初始 prompt 出發，在 benchmark 上評分，讓語言模型提出新 prompt，再保留較好的候選。它容易實作但可能對單一 benchmark 過度擬合。 本段重點：來更新 harness 嗎 其實是可以的 這方面的研究 已經非常多了 最早開始做這種 harness 更新的研究 通常是更新在 prompt 上 如果你把 prompt 也當作 harness 的一部分的話 最早的一系列的研究 他們做的是 Prompt Optimization 也就是用自動化的方法 讓 prompt 持續演進 找出最好的一組 prompt 他們的想法 其實也非常的直覺 這邊引用的是一篇 23 年的上古時代的文章 你有一…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 來更新 harness 嗎 其實是可以的 這方面的研究 已經非常多了 最早開始做這種 harness 更新的研究 通常是更新在 prompt 上 如果你把 prompt 也當作 harness 的一部分的話 最早的一系列的研究 他們做的是 Prompt Optimization 也就是用自動化的方法 讓 prompt 持續演進 找出最好的一組 prompt 他們的想法 其實也非常的直覺 這邊引用的是一篇 23 年的上古時代的文章 你有一個初始的 prompt 比如說你初始的 prompt 是 think step by step 你在拿這個初始的 prompt 去在某一個 loss 上面 去做 evaluation 比如說拿這個初始的 prompt 去做某一組數學的問題 去跑某一個 benchmark 得到一個分數 比如說 72 分 你就把這個資訊 交給某一個語言模型 跟它說 你能不能夠設計出更好的 prompt 它就有可能設計出更好的 prompt 在我右下角引用的這篇論文裡面 他們就從一個比較簡單的 prompt 開始尋找 最後找出一個對解數學問題非常有用的 prompt 非常強的 prompt 這個 prompt 呢 就是叫模型先深呼吸 很神奇發現叫模型先深呼吸 它可以在數學問題上解得更好 所以有一系列 Prompt Optimization 的研究 你都可以看作是 他們拿一個語言模型 來做這個 prompt 的更新 他們透過一個語言模型 來做到部分 harness 的自我成長 這是那一篇 23 年的論文

</details>


### Slide 9 — 讓 Prompt 自動演化（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=585s))

![Slide 9 — 讓 Prompt 自動演化（續）](slides/009_00-10-45.jpg)

從初始 prompt 出發，在 benchmark 上評分，讓語言模型提出新 prompt，再保留較好的候選。它容易實作但可能對單一 benchmark 過度擬合。 本段重點：裡面的一個例子 你可能會很好奇說 用一個語言模型去看這個 prompt 來更新 prompt 需要做什麼樣特別的設計嗎 其實完全不需要 你就直接下指令給語言模型就好了 在這篇論文裡面 他們實際的例子長這個樣子的 你就跟這個語言模型說 我之前試了 Let's figure it out 作為我的 prompt 來解數學問題 在某個 benchmark 上得到 61 分 我又試了 Let's solve the problem 得到 63 …


<details>
<summary><strong>Cleaned narration</strong></summary>

> 裡面的一個例子 你可能會很好奇說 用一個語言模型去看這個 prompt 來更新 prompt 需要做什麼樣特別的設計嗎 其實完全不需要 你就直接下指令給語言模型就好了 在這篇論文裡面 他們實際的例子長這個樣子的 你就跟這個語言模型說 我之前試了 Let's figure it out 作為我的 prompt 來解數學問題 在某個 benchmark 上得到 61 分 我又試了 Let's solve the problem 得到 63 分 請寫出另外一個 prompt 這個 prompt 要比之前的 prompt 得到更高的分數 期待這個語言模型 就可以吐出一個更好的 prompt

</details>


### Slide 10 — 讓 Prompt 自動演化（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=627s))

![Slide 10 — 讓 Prompt 自動演化（續）](slides/010_00-10-27.jpg)

從初始 prompt 出發，在 benchmark 上評分，讓語言模型提出新 prompt，再保留較好的候選。它容易實作但可能對單一 benchmark 過度擬合。 本段重點：在過去最比較早的 這一種 Harness Optimization 的方法裡面 他們通常是線性的 比如說那篇 23 年的 paper 他們是線性的 我們現在假設每一個點 代表一個 AI agent 這個 AI agent 裡面是包含它的 harness 還有這個 harness 跑在某一個 loss 上面得到的分數 你就把第一組的 harness 去過一個語言模型 讓它產生更好的 harness 這個步驟就持續持續地繼續下去 但這樣子一…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 在過去最比較早的 這一種 Harness Optimization 的方法裡面 他們通常是線性的 比如說那篇 23 年的 paper 他們是線性的 我們現在假設每一個點 代表一個 AI agent 這個 AI agent 裡面是包含它的 harness 還有這個 harness 跑在某一個 loss 上面得到的分數 你就把第一組的 harness 去過一個語言模型 讓它產生更好的 harness 這個步驟就持續持續地繼續下去 但這樣子一直線的方法 有時候會遇到一些問題 比如說你如果在某一個步驟 突然找到一個很差的 harness 有可能就會萬劫不復 就困在某一個 local minima 就再也找不到更好的 harness 整個過程 整個演化的過程就崩壞了 這是有可能的 所以現在如果你看這一種 harness optimization harness 自我成長的文獻 他們通常的做法是這個樣子的

</details>


### Slide 11 — 讓 Prompt 自動演化（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=684s))

![Slide 11 — 讓 Prompt 自動演化（續）](slides/011_00-11-24.jpg)

從初始 prompt 出發，在 benchmark 上評分，讓語言模型提出新 prompt，再保留較好的候選。它容易實作但可能對單一 benchmark 過度擬合。 本段重點：他們通常會用一個 非常類似基因演算法的做法 雖然每篇 paper 略有不同 但是大方向大方向的這個框架幾乎都是一樣 首先呢你會有一個 pool 這個 pool 裡面有很多 harness 這些 harness 都是過去嘗試過的相對比較好的 harness 你這邊就假設說你有個 loss 可以 evaluate harness 的好壞 你有一組不錯的 harness 以後呢 你從這組不錯的 harness 裡面 隨機挑幾個 harness…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 他們通常會用一個 非常類似基因演算法的做法 雖然每篇 paper 略有不同 但是大方向大方向的這個框架幾乎都是一樣 首先呢你會有一個 pool 這個 pool 裡面有很多 harness 這些 harness 都是過去嘗試過的相對比較好的 harness 你這邊就假設說你有個 loss 可以 evaluate harness 的好壞 你有一組不錯的 harness 以後呢 你從這組不錯的 harness 裡面 隨機挑幾個 harness 出來 至於要怎麼隨機挑 這個也都是有很大的學問的 比如說你可能會挑 比較少挑過的那些 harness 或者是你可能會挑 表現相對於其他的 還是更好一點的 harness 所以這邊有很多需要調的部分 你就從這個 pool 裡面 sample 幾個 harness 出來 接下來呢 就讓它們做 mutation 讓它們繁衍它們的子代 繁衍的方法通常就是 你拿一個 language model 出來 跟它說這邊有兩個不錯的 harness 根據這兩個不錯的 harness 再寫出一個更好的 harness 但這個 harness 可以是很多不同的東西 比如它可以是 prompt 它也可以是其他 AI agent 的部分 你寫出更好的 harness 之後 你可能會需要真的去 evaluate 一下 看它有沒有真的更好 如果它真的更好之後 就把它放到你的 pool 裡面 這個跟這個天擇是非常類似的 跟適者生存不適者淘汰 這個演化 其實背後的用的概念 是非常雷同的 今天通常在做這種 harness optimization 的時候

</details>


### Slide 12 — 讓 Prompt 自動演化（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=777s))

![Slide 12 — 讓 Prompt 自動演化（續）](slides/012_00-13-57.jpg)

從初始 prompt 出發，在 benchmark 上評分，讓語言模型提出新 prompt，再保留較好的候選。它容易實作但可能對單一 benchmark 過度擬合。 本段重點：用的都是這一系列的方法 比如說在 Prompt Optimization 裡面最近一個比較新的文獻 是 GEPA 在 GEPA 裡面 它就是用類似我們剛才 講的這種基因演算法的方法 來找出更好的 prompt 那從這個圖我們就不細講 但它的大的概念就是 我有一個 pool 這個 pool 裡面有一些比較好的 harness 然後接下來 一些比較好的在這邊是它 focus 在 prompt 上面了有些比較好的 prompt 我可以只拿一個…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 用的都是這一系列的方法 比如說在 Prompt Optimization 裡面最近一個比較新的文獻 是 GEPA 在 GEPA 裡面 它就是用類似我們剛才 講的這種基因演算法的方法 來找出更好的 prompt 那從這個圖我們就不細講 但它的大的概念就是 我有一個 pool 這個 pool 裡面有一些比較好的 harness 然後接下來 一些比較好的在這邊是它 focus 在 prompt 上面了有些比較好的 prompt 我可以只拿一個 prompt 出來 讓它做無性生殖 讓 LLM 把它改得更好 我也可以拿兩個 prompt 出來 讓它做有性生殖 讓 LLM 去結合這兩個 prompt 產生更好的 prompt 接下來呢 產生新的 prompt 以後 再去做 evaluation 看看它是不是真的是一個更好的 prompt 如果是就把它放回這個 pool 裡面 不是就把它丟掉 這是 GEPA 的做法 很多其他的文獻

</details>


### Slide 13 — 讓 Prompt 自動演化（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=834s))

![Slide 13 — 讓 Prompt 自動演化（續）](slides/013_00-14-54.jpg)

從初始 prompt 出發，在 benchmark 上評分，讓語言模型提出新 prompt，再保留較好的候選。它容易實作但可能對單一 benchmark 過度擬合。 本段重點：他們可以 update harness 的其他部分 用的也都是非常類似的想法 比如說這個是一個 26 年 2 月的 paper 他想要 update 的是 一個 agent 怎麼去 maintain 他的 memory 你知道今天這個 agent 為了要記得過去的事情 他都會需要有一套記憶系統 這套記憶系統 通常做的事情是 今天 LLM 會選擇 把一些重要的事 存在你的檔案系統裡面 在適當的時機 用某些方法抽出來 但在背後的設計 其實也…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 他們可以 update harness 的其他部分 用的也都是非常類似的想法 比如說這個是一個 26 年 2 月的 paper 他想要 update 的是 一個 agent 怎麼去 maintain 他的 memory 你知道今天這個 agent 為了要記得過去的事情 他都會需要有一套記憶系統 這套記憶系統 通常做的事情是 今天 LLM 會選擇 把一些重要的事 存在你的檔案系統裡面 在適當的時機 用某些方法抽出來 但在背後的設計 其實也是很多學問 你可以看到有滿坑滿谷的文獻 在研究怎麼做 memory 的 management 什麼時候該把 memory 存進去 怎麼樣把 memory 有效的提取出來 這個都是尚待研究的 open question 在這篇 paper 裡面 他們就採取的方法是 我們能不能夠用這種 自我強化的方法 讓模型自動地找出 比較好的 memory management 的做法 它們的做法 跟我們剛才講的 個基因演算法的做法 差不多就是有一個 pool 這個 pool 裡面 已經有一些 memory 的設計 從裡面先 sample 出一個比較好的 再根據這個 已經有的 memory 的 design 看看能不能夠再想出 更好的 memory design 想出另外一個新的 memory design 以後再把這個新的 memory design 真的拿去衡量一下 看有沒有真的比較好 如果真的比較好 就把它放回 pool 裡面 所以這個過程跟剛才說的 Prompt Optimization 其實是一樣的 只是你 optimize 更新的對象 從 prompt 變成 memory 你同樣也可以 optimize 你的 workflow

</details>


## 三、Workflow Search

### Slide 14 — 維護 Agent Pool 並演化流程 ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=933s))

![Slide 14 — 維護 Agent Pool 並演化流程](slides/014_00-16-33.jpg)

自動 workflow optimization 維護多個 Agent 候選，以 mutation、selection 與 archive 提升 SWE-bench 表現；仍須檢查搜尋成本、資料洩漏與泛化。 本段重點：這邊就有一篇 25 年的 paper 他做的事情就是去 optimize AI agent 的 workflow 希望 AI agent 在 SWE-bench 這個 Benchmark 上面 可以做得越來越好 在這張圖上面 橫軸是這個 update 的次數 它會 iterate the update 這個縱軸 是指現在 AI agent 表現的好壞 它每次都會 maintain 一個 pool 的 agent 所以它不會只 maint…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 這邊就有一篇 25 年的 paper 他做的事情就是去 optimize AI agent 的 workflow 希望 AI agent 在 SWE-bench 這個 Benchmark 上面 可以做得越來越好 在這張圖上面 橫軸是這個 update 的次數 它會 iterate the update 這個縱軸 是指現在 AI agent 表現的好壞 它每次都會 maintain 一個 pool 的 agent 所以它不會只 maintain 一個 agent 是一個 pool 的 agent 這個淺藍色的線 是那個 pool 裡面的 agent 的平均能力 它把那個 pool 叫做 archive 不同的 paper 稱呼方法不太一樣 總之這邊的 archive 就是我剛才前面講的一個 pool 它這邊也記錄了 在 pool 裡面最好的那個 agent 它做得怎麼樣 你可以看到這個最好的 agent 還有平均的 agent 他們的能力都是隨著 workflow 的 update 持續上升的 在這篇 paper 裡面呢 他還記錄了幾個關鍵的变化 還有特別呢 用文字標記幾個關鍵的演化結果 比如說在某個時間點呢 模型學到說 現在在讀檔案的時候 不要一次讀整個檔案 它 implement 了一個比較好的工具 可以指定行數 可以從指定的行數 把檔案讀出來 這可以讓模型的能力暴增 或者是它在某一個時間點呢 找到了比較好的 file editing 的方法 它可能幫自己寫了一個 比較好的 file editing 的工具 可以讓自己 edit 那些程式 編輯程式編輯得 更有效率

</details>


### Slide 15 — 維護 Agent Pool 並演化流程（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=1032s))

![Slide 15 — 維護 Agent Pool 並演化流程（續）](slides/015_00-17-12.jpg)

自動 workflow optimization 維護多個 Agent 候選，以 mutation、selection 與 archive 提升 SWE-bench 表現；仍須檢查搜尋成本、資料洩漏與泛化。 本段重點：這個是那篇 paper 裡面 他畫的一個演化樹啦 你知道你會從某一個 agent 開始 從那個 agent 去誕生 其他的 agent 出來 就可以畫出一個演化樹 你就可以看看這些 agent 中間 是怎麼做演化的 看看這個 agent 演化的歷程 多數的路徑呢 最後都死掉了 這邊是用這個顏色來代表說 些 agent 表現的好壞 顏色越深就代表那些 agent 表現得越差 呢這個紅色的框框代表說 他們其實在衡量的時候 每一個 agent…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 這個是那篇 paper 裡面 他畫的一個演化樹啦 你知道你會從某一個 agent 開始 從那個 agent 去誕生 其他的 agent 出來 就可以畫出一個演化樹 你就可以看看這些 agent 中間 是怎麼做演化的 看看這個 agent 演化的歷程 多數的路徑呢 最後都死掉了 這邊是用這個顏色來代表說 些 agent 表現的好壞 顏色越深就代表那些 agent 表現得越差 呢這個紅色的框框代表說 他們其實在衡量的時候 每一個 agent 是做三階段的衡量 一開始會先拿 一開始就是演化之後 產生新的子代之後 會先用 10 個最 basic 的 task 開始衡量 因為有時候你演化之後 整個 workflow 就通通壞掉了 也許它根本就是把自己的程式改壞了 再起不能 所以你會發現很多 case 是演化之後 是連那 10 個最簡單的 task 都過不了了 基因突變之後 多數結果都是壞的 個子代是完全沒有辦法生存的 所以多數演化的路徑 都是死路 如果今天 10 個 task 可以通過以後 再做 60 個 task 如果 60 個 task 也變好以後 再做 200 個 task 最後就有一條路徑 它是一條很不錯的路徑 最後找出最好的結果 因為這邊 paper 裡面 有想要強調的一個點是說 這條路徑裡面 並不是每一個祖先 都在所有的時候是最好的 有一些祖先 也許在某些時候 有其他的這個演化的圖譜上 有其他的生物 有其他的 agent 可以表現得更好 但是因為它每次都會 maintain 一個 pool 而不是只 maintain 最好的 agent 所以這些就算是次一等的 不是最好的 agent 也有機會存留存活下來 最後演化成最好的 agent 就像我們的祖先 在中生代的時候是摩根齒獸 活在恐龍的陰影之下 但後來恐龍滅絕之後 哺乳類就出頭了 就是類似的概念

</details>


### Slide 16 — 維護 Agent Pool 並演化流程（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=1155s))

![Slide 16 — 維護 Agent Pool 並演化流程（續）](slides/016_00-19-15.jpg)

自動 workflow optimization 維護多個 Agent 候選，以 mutation、selection 與 archive 提升 SWE-bench 表現；仍須檢查搜尋成本、資料洩漏與泛化。 本段重點：如果你今天想要自己體驗這種 用 evolution 的方法持續迭代 去 improve harness 的話 也許一個可以現成用的工具叫做 DSPy 它裡面主要改的呢 其實是 Prompt 我通常把它想成是一個 Prompt Optimization 的工具 你只要給它你要解的問題 跟訓練資料 跟你的 Evaluation Metric 接下來呢 它就幫你做 Prompt Optimization 但其實它不是完全只能做 Prompt …


<details>
<summary><strong>Cleaned narration</strong></summary>

> 如果你今天想要自己體驗這種 用 evolution 的方法持續迭代 去 improve harness 的話 也許一個可以現成用的工具叫做 DSPy 它裡面主要改的呢 其實是 Prompt 我通常把它想成是一個 Prompt Optimization 的工具 你只要給它你要解的問題 跟訓練資料 跟你的 Evaluation Metric 接下來呢 它就幫你做 Prompt Optimization 但其實它不是完全只能做 Prompt Optimization 它裡面呢 也是有一些跟 workflow 有關的東西 它也是可以稍微改一下你的 workflow 的 所以如果你想要體驗這種 Iterative Update Harness 的感覺的話 可以直接使用這個工具 它可以直接幫你 Update 你的 prompt 或甚至 Update 你的 workflow

</details>


### Slide 17 — 維護 Agent Pool 並演化流程（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=1200s))

![Slide 17 — 維護 Agent Pool 並演化流程（續）](slides/017_00-20-00.jpg)

自動 workflow optimization 維護多個 Agent 候選，以 mutation、selection 與 archive 提升 SWE-bench 表現；仍須檢查搜尋成本、資料洩漏與泛化。 本段重點：我們剛才講了 可以 Update Harness 我們之前也講了 可以 Update 語言模型的參數 接下來一個很自然的想法就是 能不能兩個同時 update 我們能不能同時演化語言模型 也同時演化 Harness 當然是可以的 但也許在做這件事之前 人們會問的問題就是


<details>
<summary><strong>Cleaned narration</strong></summary>

> 我們剛才講了 可以 Update Harness 我們之前也講了 可以 Update 語言模型的參數 接下來一個很自然的想法就是 能不能兩個同時 update 我們能不能同時演化語言模型 也同時演化 Harness 當然是可以的 但也許在做這件事之前 人們會問的問題就是

</details>


### Slide 18 — 維護 Agent Pool 並演化流程（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=1221s))

![Slide 18 — 維護 Agent Pool 並演化流程（續）](slides/018_00-20-21.jpg)

自動 workflow optimization 維護多個 Agent 候選，以 mutation、selection 與 archive 提升 SWE-bench 表現；仍須檢查搜尋成本、資料洩漏與泛化。 本段重點：到底需不需要兩者同時都演化呢 會不會只要其中一者有進步就足夠了 這邊就有一篇 paper 呢 告訴你說兩者一起進步 其實是必要的 在這篇 26 年年初的 paper 裡面 他就先說 我們有兩種強化模型的方式 其中一種就是改 也許你給你的模型 比較好的 memory 的系統 讓它能夠更容易地 搜尋到它要的結果 另外一種方法 就是調整語言模型的參數 可以讓它的能力變強 但在這篇論文裡面 就告訴我們說 你可以把這兩者同時做 也許可以做得更好 …


<details>
<summary><strong>Cleaned narration</strong></summary>

> 到底需不需要兩者同時都演化呢 會不會只要其中一者有進步就足夠了 這邊就有一篇 paper 呢 告訴你說兩者一起進步 其實是必要的 在這篇 26 年年初的 paper 裡面 他就先說 我們有兩種強化模型的方式 其中一種就是改 也許你給你的模型 比較好的 memory 的系統 讓它能夠更容易地 搜尋到它要的結果 另外一種方法 就是調整語言模型的參數 可以讓它的能力變強 但在這篇論文裡面 就告訴我們說 你可以把這兩者同時做 也許可以做得更好 為什麼這兩者同時做 有可能可以做得更好呢 在論文裡面給的一個理由是 如果你今天單純地 只是強化了你的 Harness 也許你的 Harness 有了更好的 memory 的 manage 系統 它可以每次呢 給你的語言模型 搜尋出更多的資料 搜尋出更多的記憶 但也許你的語言模型很笨 它根本沒有辦法讀懂大量的記憶 一次灌給它大量的記憶 反而讓它頭破掉了 不知道該怎麼使用這些記憶 所以也許你在給它新的 memory 的 你在給模型新的 Harness 的同時 你也要訓練這個語言模型 怎麼樣善用這個 Harness 所以一邊你更新了 Harness 讓這個 AI agent 的輸入不同 同時你要告訴它 在這個新的輸入底下 什麼樣的答案才是正確的 你同時也 update 這個模型的參數 你也微調這個語言模型的參數 讓它能夠更善用新的 Harness 讓它可以在新的 Harness 之下 得到最好的結果 有另外一篇論文

</details>


## 四、Prompt 與 Weight 聯合更新

### Slide 19 — 兩種優化互補 ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=1329s))

![Slide 19 — 兩種優化互補](slides/019_00-22-09.jpg)

Prompt optimization 改外部條件，weight optimization 改內部參數。聯合更新通常更強，但帶來狀態管理、成本與新舊能力衝突。 本段重點：你從它的標題就知道 它想要做什麼 這篇論文就說 Fine-Tuning and Prompt Optimization: Two Great Steps that Work Better Together 它裡面就同時做了 Prompt Optimization 跟 Weight Optimization 就微調參數 想要知道說 這兩者同時做會不會比較好 它這邊就試了不同的模型 做在不同的 benchmark 上 這邊數字正確率越大越好…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 你從它的標題就知道 它想要做什麼 這篇論文就說 Fine-Tuning and Prompt Optimization: Two Great Steps that Work Better Together 它裡面就同時做了 Prompt Optimization 跟 Weight Optimization 就微調參數 想要知道說 這兩者同時做會不會比較好 它這邊就試了不同的模型 做在不同的 benchmark 上 這邊數字正確率越大越好 第一個 row 是什麼都不做的結果 第二個 row 是 update 這個 prompt 的結果 用 $\pi$ 代表 Prompt Optimization 它用 $\theta$ 代表 Weight Optimization 但兩者都是有效的 不過如果你要比 Prompt Optimization 跟 Weight Optimization 的話 你這邊其實可以蠻明顯地看到說 Prompt Optimization 看起來比 Weight Optimization 更加有效 至少在它的實驗設計上是這個樣子 這也符合大家今天 在強化 AI agent 的直覺 通常改 Harness 你比較容易讓你的 AI agent 獲得強化 Fine-tune 參數實在太危險了 往往一不小心就把模型弄壞了 這邊它就試了說 你可以做 Prompt Optimization 兩次 你可以用 Weight Optimization 兩次 會得到什麼樣的結果 不過連續 update 兩次 看起來進步量是蠻有限的 接下來它就用混合的做法 先做 Prompt Optimization 再做 Weight Optimization 先做 Weight Optimization 再做 Prompt Optimization 先做 Prompt Optimization 再做 Weight Optimization 再做這個 Prompt Optimization 就先在現在的參數之下 找出最好的 Prompt 找出最好 Prompt 之後 再微調你的這個參數 讓這種參數能夠適應這個 Prompt 在新的參數上 再找出更好的 Prompt 這樣 iterative 的過程 看起來是可以得到 比單用一種方法 還要更好的結果 所以你可以同時 update 你的參數 跟你的 Harness 你的 Prompt 你的 Workflow

</details>


### Slide 20 — 兩種優化互補（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=1443s))

![Slide 20 — 兩種優化互補（續）](slides/020_00-24-03.jpg)

Prompt optimization 改外部條件，weight optimization 改內部參數。聯合更新通常更強，但帶來狀態管理、成本與新舊能力衝突。 本段重點：那在文獻上 確實也已經有人嘗試過 同時 update 兩個不同的東西 在概念上沒有什麼不同 我們剛才呢 要麼只有 update $\theta$ 要麼只有 update H 你可以把 $\theta$ 跟 H 同時 update 只是在 update H 的時候 你可能需要用到 另外一個語言模型 另外一個 improvement 的 module 來把 H 改成 $H'$ 這邊就是引用一個


<details>
<summary><strong>Cleaned narration</strong></summary>

> 那在文獻上 確實也已經有人嘗試過 同時 update 兩個不同的東西 在概念上沒有什麼不同 我們剛才呢 要麼只有 update $\theta$ 要麼只有 update H 你可以把 $\theta$ 跟 H 同時 update 只是在 update H 的時候 你可能需要用到 另外一個語言模型 另外一個 improvement 的 module 來把 H 改成 $H'$ 這邊就是引用一個

</details>


### Slide 21 — 兩種優化互補（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=1467s))

![Slide 21 — 兩種優化互補（續）](slides/021_00-24-27.jpg)

Prompt optimization 改外部條件，weight optimization 改內部參數。聯合更新通常更強，但帶來狀態管理、成本與新舊能力衝突。 本段重點：今年年初的論文 它就是同時做了這個參數的 用這種自我進化的方法 同時 improve 了參數 又同時 improve 了 Prompt 它走左邊 也有一個你在看到 這種 Prompt Optimization 的文獻的時候 非常常看到的這種演化樹 它就告訴你說 橫軸是進化的次數 縱軸是表現 當然數值越大越好 如果你只更新參數 你最後很快就會到達某個極限 如果你只更新 Prompt 你也會到達某個極限 但如果兩者都更新 最後有可能得到最好…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 今年年初的論文 它就是同時做了這個參數的 用這種自我進化的方法 同時 improve 了參數 又同時 improve 了 Prompt 它走左邊 也有一個你在看到 這種 Prompt Optimization 的文獻的時候 非常常看到的這種演化樹 它就告訴你說 橫軸是進化的次數 縱軸是表現 當然數值越大越好 如果你只更新參數 你最後很快就會到達某個極限 如果你只更新 Prompt 你也會到達某個極限 但如果兩者都更新 最後有可能得到最好的結果

</details>


### Slide 22 — 兩種優化互補（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=1509s))

![Slide 22 — 兩種優化互補（續）](slides/022_00-25-09.jpg)

Prompt optimization 改外部條件，weight optimization 改內部參數。聯合更新通常更強，但帶來狀態管理、成本與新舊能力衝突。 本段重點：另外一個我們可以探討的問題是 我們剛才已經講了 怎麼讓模型持續地強化 但是在現實生活中 我們會遇到的一個問題是 目標是會改變 在某個時間點 人類告訴機器說 你現在要強化的目標是 H 我們用 H 來代表 機器想跟人類溝通的這個目標 它可能是一些訓練資料 它可能是一本教科書 它可能就只是一句話 一個 Prompt 而已 但是可能在某些時間點 人類會更新目標 從 H 變成 $H'$ 機器要如何應對呢 可不可以想說 在現實生活中 這種目標會常常…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 另外一個我們可以探討的問題是 我們剛才已經講了 怎麼讓模型持續地強化 但是在現實生活中 我們會遇到的一個問題是 目標是會改變 在某個時間點 人類告訴機器說 你現在要強化的目標是 H 我們用 H 來代表 機器想跟人類溝通的這個目標 它可能是一些訓練資料 它可能是一本教科書 它可能就只是一句話 一個 Prompt 而已 但是可能在某些時間點 人類會更新目標 從 H 變成 $H'$ 機器要如何應對呢 可不可以想說 在現實生活中 這種目標會常常改變嗎 如果是像我們這麼一堂課 我們在學期初 會給大家一個 policy 這可能就是一個 H 但是我們 policy 通常是會固定的 我們不會太常改變這個 H 如果告訴你說 現在這個時間點 之前做的作業通通不算 我們要另外出新的一組作業 你一定會發瘋這樣 但是在現實的社會中 這個 H 就是會持續改變 這個目標呢 就是會持續地不斷地改變 那目標會持續改變 對於一個 AI agent 來說 它要怎麼樣應對呢 你說還有怎麼樣應對 不就持續訓練下去嗎 但是持續訓練下去 不一定是最好的做法 比如說本來的目標 可能是叫這個機器人 要變成一個坦克 所以它就長出了履帶 但是可能新的目標告訴你說 你不要變成坦克 你要飛起來 你要變成一個飛機 這個時候這個履帶 對它來說就太重了 也許它應該丟掉它之前 在進化的時候長出來的東西 以便應付新的目標 這邊就有兩個不同的極端的做法

</details>


### Slide 23 — 兩種優化互補（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=1617s))

![Slide 23 — 兩種優化互補（續）](slides/023_00-27-57.jpg)

Prompt optimization 改外部條件，weight optimization 改內部參數。聯合更新通常更強，但帶來狀態管理、成本與新舊能力衝突。 本段重點：一個極端的做法就是放棄一切 只要放棄目標一遍 我就丟掉一切過去所有進化出來的東西 回歸原點 從原點重新開始 另外一個極端的做法就是 反正我們所有過去進化出來的東西 都一定要留著 帶到下一次的目標 沒準它哪一天就會被用上 當然這兩個極端的方法 各自有它的缺點 如果拋棄一切 太浪費了 也許之前有一些東西 還是有用的 也許從坦克變成飛機 它頭上的這個雷達 還是有用的 但是如果保留一切 有很多過去的東西 也許現在是不合時宜的 背負一切過去 所有…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 一個極端的做法就是放棄一切 只要放棄目標一遍 我就丟掉一切過去所有進化出來的東西 回歸原點 從原點重新開始 另外一個極端的做法就是 反正我們所有過去進化出來的東西 都一定要留著 帶到下一次的目標 沒準它哪一天就會被用上 當然這兩個極端的方法 各自有它的缺點 如果拋棄一切 太浪費了 也許之前有一些東西 還是有用的 也許從坦克變成飛機 它頭上的這個雷達 還是有用的 但是如果保留一切 有很多過去的東西 也許現在是不合時宜的 背負一切過去 所有已經進化出來的 Harness 又太過沉重 所以需要在這兩者之間 取得平衡 什麼時候目標會最常改變呢

</details>


### Slide 24 — 兩種優化互補（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=1671s))

![Slide 24 — 兩種優化互補（續）](slides/024_00-28-51.jpg)

Prompt optimization 改外部條件，weight optimization 改內部參數。聯合更新通常更強，但帶來狀態管理、成本與新舊能力衝突。 本段重點：目標最常改變的 scenario 就是當你在做這個 Test-Time Training 或又叫做 Test-Time Adaptation 它縮寫 縮寫成 TTT 或者是 TTA 的時候 因為對於 TTT 這樣子的 scenario 模型的目標 是由什麼定義的 模型的目標 是由輸入定義的 當你給模型一個輸入 它根據這個輸入 就會去調整它的參數 在這一筆輸入上 做得更好 當下一筆輸入進來的時候 應該要怎麼辦呢 每當有一筆新的輸入資料 進…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 目標最常改變的 scenario 就是當你在做這個 Test-Time Training 或又叫做 Test-Time Adaptation 它縮寫 縮寫成 TTT 或者是 TTA 的時候 因為對於 TTT 這樣子的 scenario 模型的目標 是由什麼定義的 模型的目標 是由輸入定義的 當你給模型一個輸入 它根據這個輸入 就會去調整它的參數 在這一筆輸入上 做得更好 當下一筆輸入進來的時候 應該要怎麼辦呢 每當有一筆新的輸入資料 進來的時候 對整個學習的框架來說 就是一次目標的轉變 所以每筆資料進來 都是一次目標的轉變 對於 TTT 的研究的人來說 你就要決定 你要怎麼應付這個新的目標 一個極端的狀況就是 每次都退回原點 每次都退回原點 所以另外一個極端就是 每一次看到一筆資料 我模型的參數變了以後 得到新的輸出 有了新的參數 這個新的參數 要被帶到下一次的輸入 繼續使用

</details>


## 五、持續學習與遺忘

### Slide 25 — 參數與 Harness 都會忘記 ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=1737s))

![Slide 25 — 參數與 Harness 都會忘記](slides/025_00-29-57.jpg)

每輪只為當前任務最佳化會遺忘舊技能；Harness 更新也可能刪掉舊工具或規則。需以跨任務回歸測試平衡適應與保留。 本段重點：每次參數都要在下一輪 持續使用 所以有兩種不同的極端的狀態 要如何在這兩種極端的狀態之間


<details>
<summary><strong>Cleaned narration</strong></summary>

> 每次參數都要在下一輪 持續使用 所以有兩種不同的極端的狀態 要如何在這兩種極端的狀態之間

</details>


### Slide 26 — 參數與 Harness 都會忘記（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=1746s))

![Slide 26 — 參數與 Harness 都會忘記（續）](slides/026_00-29-06.jpg)

每輪只為當前任務最佳化會遺忘舊技能；Harness 更新也可能刪掉舊工具或規則。需以跨任務回歸測試平衡適應與保留。 本段重點：取得平衡呢 其實在上一個學期的 機器學習導論的第八講 快結束的時候 這邊特別把時間標註出來 1 分 54 秒的時候 我就講了我們實驗室的 黃維平跟林冠廷同學的論文 有講說我們如何在兩種極端之間取得平衡 可以在 TTT 上做出更好的結果 這邊因為以前已經講過了 我們就不重複已經講過的東西 留給大家回去參考


<details>
<summary><strong>Cleaned narration</strong></summary>

> 取得平衡呢 其實在上一個學期的 機器學習導論的第八講 快結束的時候 這邊特別把時間標註出來 1 分 54 秒的時候 我就講了我們實驗室的 黃維平跟林冠廷同學的論文 有講說我們如何在兩種極端之間取得平衡 可以在 TTT 上做出更好的結果 這邊因為以前已經講過了 我們就不重複已經講過的東西 留給大家回去參考

</details>


### Slide 27 — 參數與 Harness 都會忘記（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=1776s))

![Slide 27 — 參數與 Harness 都會忘記（續）](slides/027_00-30-36.jpg)

每輪只為當前任務最佳化會遺忘舊技能；Harness 更新也可能刪掉舊工具或規則。需以跨任務回歸測試平衡適應與保留。 本段重點：我們今天呢 因為會持續更新我們的參數 或持續更新我們的 Harness 我們要注意的一個問題就是 模型可能會遺忘過去它已經會的技能 遺忘這件事 我們其實已經在去年的第六講 去年機器學習的第六講 用一整堂課的時間 討論過參數的遺忘 如果有興趣的同學 可以再回去參考去年的錄影 但是過去我們在討論遺忘的時候


<details>
<summary><strong>Cleaned narration</strong></summary>

> 我們今天呢 因為會持續更新我們的參數 或持續更新我們的 Harness 我們要注意的一個問題就是 模型可能會遺忘過去它已經會的技能 遺忘這件事 我們其實已經在去年的第六講 去年機器學習的第六講 用一整堂課的時間 討論過參數的遺忘 如果有興趣的同學 可以再回去參考去年的錄影 但是過去我們在討論遺忘的時候

</details>


### Slide 28 — 參數與 Harness 都會忘記（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=1809s))

![Slide 28 — 參數與 Harness 都會忘記（續）](slides/028_01-30-09.jpg)

每輪只為當前任務最佳化會遺忘舊技能；Harness 更新也可能刪掉舊工具或規則。需以跨任務回歸測試平衡適應與保留。 本段重點：我們都只討論參數的遺忘 我們都只說參數更新了 因為有新的參數 所以模型會遺忘舊有的技能 AI agent 的時代 能夠更新的不是只有參數 還有你的 Harness 我們有沒有可能 因為更新了 Harness 以後 忘掉了一些舊的技能呢 這也是有可能的 我這邊引用一篇非常新的文章


<details>
<summary><strong>Cleaned narration</strong></summary>

> 我們都只討論參數的遺忘 我們都只說參數更新了 因為有新的參數 所以模型會遺忘舊有的技能 AI agent 的時代 能夠更新的不是只有參數 還有你的 Harness 我們有沒有可能 因為更新了 Harness 以後 忘掉了一些舊的技能呢 這也是有可能的 我這邊引用一篇非常新的文章

</details>


### Slide 29 — 參數與 Harness 都會忘記（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=1833s))

![Slide 29 — 參數與 Harness 都會忘記（續）](slides/029_01-31-33.jpg)

每輪只為當前任務最佳化會遺忘舊技能；Harness 更新也可能刪掉舊工具或規則。需以跨任務回歸測試平衡適應與保留。 本段重點：這個討論 Harness 更新 會遺忘過去技能的文獻 我還沒有看到那麼多 我就引用一個五月的文章 這篇文章裡面 有講了更新 Harness 也有可能遺忘這件事情 它就發現說 當你在更新一個模型的 Workflow 的時候 模型可能為了要應付 現在的問題 它會把它的 Workflow 設計得越來越複雜 直到複雜得沒有必要 結果反而簡單的任務 也做不好了 它這邊就講說 它做了三個回合的進化 藍色這條線呢 是一般的 Workflow 的更新方…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 這個討論 Harness 更新 會遺忘過去技能的文獻 我還沒有看到那麼多 我就引用一個五月的文章 這篇文章裡面 有講了更新 Harness 也有可能遺忘這件事情 它就發現說 當你在更新一個模型的 Workflow 的時候 模型可能為了要應付 現在的問題 它會把它的 Workflow 設計得越來越複雜 直到複雜得沒有必要 結果反而簡單的任務 也做不好了 它這邊就講說 它做了三個回合的進化 藍色這條線呢 是一般的 Workflow 的更新方法 就是用一個語言模型啊 可能加上基因演算法 這樣子的更新方法 它的縱軸代表 它 Workflow 的程式的行數 程式的行數越多 就代表 Workflow 越複雜 它發現說呢 更新之後 Workflow 可能會變得比較複雜 甚至複雜到沒有必要 這篇論文它的核心 其實就是提出了一個方法 讓 Workflow 的更新 不會遺忘過去舊的東西 其實在 Workflow 更新上 它也是採用 Prompt Optimization 的方法 它就是擷取一些核心的敘述 告訴模型說 什麼東西是不能動的 什麼能力一定要是保留的 把這段 Prompt 在 Workflow 更新的時候 也加進去 這樣避免在 Workflow 更新的時候 更新到不該更新的東西 它提出來的方法 它叫做 CPE 發現有這個方法以後 Workflow 就比較不會變得太複雜 右邊這個圖 它就是比較了兩個不同的模型 一個是 GPT-5 mini 一個是 GPT-5.1 它把這兩個模型 都做 Harness 的更新 如果你今天 沒有使用它們的做法的話 結果呢 在簡單的任務上比較差 其實在複雜的任務上 也比較差 因為訓練的時候 看過任務 但這些訓練就已經不是 傳統的機器學習的 update 參數的訓練 我們把更新 Harness 也當作一種訓練 訓練 Harness 看過的那些題目 跟測試的時候的任務 是不一樣的 所以你有可能在這些 訓練的題目上 更新 Harness 做得很好 但是這就是個 overfit 所以在測試的題目上 也做得不好 所以它發現說 如果你就單純地更新 Harness 沒有做一些額外的 Regularization 的話 但它這 Regularization 也不是傳統機器學習的 Regularization 而是一種新的 Regularization 方式 避免模型 遺忘舊有技能的方式 如果你有加 Regularization 的話 這些模型 在簡單和新的 複雜任務上的表現 都是可以更好的

</details>


### Slide 30 — 參數與 Harness 都會忘記（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=1992s))

![Slide 30 — 參數與 Harness 都會忘記（續）](slides/030_01-33-12.jpg)

每輪只為當前任務最佳化會遺忘舊技能；Harness 更新也可能刪掉舊工具或規則。需以跨任務回歸測試平衡適應與保留。 本段重點：我們剛才講到了 模型可以持續進化 但是通常在持續進化的時候 進化的規則是固定的 你可能有一個語言模型 或者是有一個既定的規則 操控了這一次 每一次更新的時候 要怎麼更新 所以雖然人工智慧可以持續更新 但更新的規則往往是固定的 接下來問的問題就是 能不能夠更新更新的規則 能不能來更新更新的規則 可以更新更新的規則嗎


<details>
<summary><strong>Cleaned narration</strong></summary>

> 我們剛才講到了 模型可以持續進化 但是通常在持續進化的時候 進化的規則是固定的 你可能有一個語言模型 或者是有一個既定的規則 操控了這一次 每一次更新的時候 要怎麼更新 所以雖然人工智慧可以持續更新 但更新的規則往往是固定的 接下來問的問題就是 能不能夠更新更新的規則 能不能來更新更新的規則 可以更新更新的規則嗎

</details>


### Slide 31 — 參數與 Harness 都會忘記（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=2028s))

![Slide 31 — 參數與 Harness 都會忘記（續）](slides/031_01-34-48.jpg)

每輪只為當前任務最佳化會遺忘舊技能；Harness 更新也可能刪掉舊工具或規則。需以跨任務回歸測試平衡適應與保留。 本段重點：其實直覺非常地簡單 剛才更新 Harness 的這些方法 裡面可能就已經連帶了 更新了更新的規則 如果你今天有一個 agent 它的 Harness 叫做 H 你要更新這個 H 的時候 你是用 H 自己來進行更新 你用 H 自己 它看著自己的程式碼 看著這個程式碼 在某一個 benchmark 上的表現 直接改自己的程式碼 變成 $H'$ 得到一個更好的 agent 因為今天這個 H 變了 你等同於也改變了更新的規則 就是因為今天更新 …


<details>
<summary><strong>Cleaned narration</strong></summary>

> 其實直覺非常地簡單 剛才更新 Harness 的這些方法 裡面可能就已經連帶了 更新了更新的規則 如果你今天有一個 agent 它的 Harness 叫做 H 你要更新這個 H 的時候 你是用 H 自己來進行更新 你用 H 自己 它看著自己的程式碼 看著這個程式碼 在某一個 benchmark 上的表現 直接改自己的程式碼 變成 $H'$ 得到一個更好的 agent 因為今天這個 H 變了 你等同於也改變了更新的規則 就是因為今天更新 要如何更新 是由這個 H 來決定的 當你把 H 進化成 $H'$ 的時候 你其實也等同於改變了更新的規則

</details>


### Slide 32 — 參數與 Harness 都會忘記（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=2073s))

![Slide 32 — 參數與 Harness 都會忘記（續）](slides/032_01-35-33.jpg)

每輪只為當前任務最佳化會遺忘舊技能；Harness 更新也可能刪掉舊工具或規則。需以跨任務回歸測試平衡適應與保留。 本段重點：但是實際上這種文獻並沒有那麼多 很多號稱在 update Harness 的 agent 如果你去仔細看它的話 你會發現它們負責更新的模組 往往是固定的 或甚至是負責更新的模組 就是另外一個模型 比如說我現在用的語言模型 是一個比較差的模型 比如說 Claude Sonnet 負責更新的模型 是 Claude Opus 它是固定的 這就有點尷尬 你趕快直接拿 Claude Opus 原來那個任務 看看會怎麼樣 所以你會發現很多 pape…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 但是實際上這種文獻並沒有那麼多 很多號稱在 update Harness 的 agent 如果你去仔細看它的話 你會發現它們負責更新的模組 往往是固定的 或甚至是負責更新的模組 就是另外一個模型 比如說我現在用的語言模型 是一個比較差的模型 比如說 Claude Sonnet 負責更新的模型 是 Claude Opus 它是固定的 這就有點尷尬 你趕快直接拿 Claude Opus 原來那個任務 看看會怎麼樣 所以你會發現很多 paper 它更新的模組就是固定的 或者根本就是一個外部的模型 但是也有一些 paper 我這邊就引用了兩篇 這兩個 agent 它們其實都會更新自己 更新的模組 所以當我們現在的模型 變成 $H'$ 之後 我們更新的規則就變了 它就不再是 H 而是 $H'$ 這個 $H'$ 會看著自己的程式碼 看著自己之前的表現 把自己再改成 $H''$

</details>


## 六、Hyper-Agent

### Slide 33 — 連更新規則也一起更新 ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=2130s))

![Slide 33 — 連更新規則也一起更新](slides/033_01-36-30.jpg)

Hyper-Agent 不只改 Harness，也演化更新模組。系統自行改善候選 sampling 策略，展示第二層自我改進，但外層目標和評估仍由人設計。 本段重點：希望自己更新 自己可以做得更好 所以它一方面 自己更新了自己的 Harness 一方面又更新了 更新 Harness 的過程


<details>
<summary><strong>Cleaned narration</strong></summary>

> 希望自己更新 自己可以做得更好 所以它一方面 自己更新了自己的 Harness 一方面又更新了 更新 Harness 的過程

</details>


### Slide 34 — 連更新規則也一起更新（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=2142s))

![Slide 34 — 連更新規則也一起更新（續）](slides/034_01-36-42.jpg)

Hyper-Agent 不只改 Harness，也演化更新模組。系統自行改善候選 sampling 策略，展示第二層自我改進，但外層目標和評估仍由人設計。 本段重點：到底更新這些更新的模組以後 有什麼樣有趣的現象呢 在 Hyper Agent 裡面 他就講了一個有趣的例子 它們持續地更新它們的 Agent 之後 因為它們的 Agent 裡面 也包含了如何更新的演算法 所以模型確實找出了 比較好的更新 Agent 的演算法 我們之前講說 如果你要更新 Agent 的 Harness 常見的做法就是 有一個 pool 從裡面 sample 一些東西出來 再找出更好的 Harness 怎麼 sample …


<details>
<summary><strong>Cleaned narration</strong></summary>

> 到底更新這些更新的模組以後 有什麼樣有趣的現象呢 在 Hyper Agent 裡面 他就講了一個有趣的例子 它們持續地更新它們的 Agent 之後 因為它們的 Agent 裡面 也包含了如何更新的演算法 所以模型確實找出了 比較好的更新 Agent 的演算法 我們之前講說 如果你要更新 Agent 的 Harness 常見的做法就是 有一個 pool 從裡面 sample 一些東西出來 再找出更好的 Harness 怎麼 sample 其實是有學問的 過去有很多研究 試圖找出更好的 sample 的方式 而它們發現在更新 agent 的時候 agent 會自己去改這個 sample 的演算法 真的有改出 比 naive 的 random sample 還要更好的演算法

</details>


### Slide 35 — 連更新規則也一起更新（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=2193s))

![Slide 35 — 連更新規則也一起更新（續）](slides/035_01-37-33.jpg)

Hyper-Agent 不只改 Harness，也演化更新模組。系統自行改善候選 sampling 策略，展示第二層自我改進，但外層目標和評估仍由人設計。 本段重點：這個就是它們實驗的結果 它們說它們綠色這條線 這個橫軸就是進化的次數 縱軸就是越大越好 綠色這條線是 最簡單的 sample 的方法 就是隨機的 sample 橙色這條線是 它們自己的 agent 在更新之後 更新出來的 自己發明的 sample 的方法 它們發現說這些 agent 也了解一些很基礎的 sampling 的方法 比如說如果有一個人在 如果有某一個 agent 在那個 pool 裡面 越少被 sample 到 它被 sam…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 這個就是它們實驗的結果 它們說它們綠色這條線 這個橫軸就是進化的次數 縱軸就是越大越好 綠色這條線是 最簡單的 sample 的方法 就是隨機的 sample 橙色這條線是 它們自己的 agent 在更新之後 更新出來的 自己發明的 sample 的方法 它們發現說這些 agent 也了解一些很基礎的 sampling 的方法 比如說如果有一個人在 如果有某一個 agent 在那個 pool 裡面 越少被 sample 到 它被 sample 到的機率 就應該增加 多給它一點機會等等 Agent 可以自己發現這些規則 當然還是比不上人設計的 藍色的是 人設計的 sampling 的方法 才是最好的 所以有趣的 但是有趣的地方是 Agent 可以更新 更新的那一個演算法

</details>


### Slide 36 — 連更新規則也一起更新（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=2247s))

![Slide 36 — 連更新規則也一起更新（續）](slides/036_01-37-27.jpg)

Hyper-Agent 不只改 Harness，也演化更新模組。系統自行改善候選 sampling 策略，展示第二層自我改進，但外層目標和評估仍由人設計。 本段重點：剛才講到更新 更新演算法的時候 更新的是 Harness 其實也可以更新參數 有一篇 paper 叫做 Learning to Self-Evolve 它更新的就是參數 所以這一個是負責拿來做更新的 拿來更新 Harness 的語言模型 這個語言模型會吃一個 Harness 吃它的表現 給一個新的 Harness 你怎麼知道這個模型 它真的很擅長更新 Harness 呢 我們要訓練它 教它怎麼去更新 Harness 怎麼教它怎麼更新 H…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 剛才講到更新 更新演算法的時候 更新的是 Harness 其實也可以更新參數 有一篇 paper 叫做 Learning to Self-Evolve 它更新的就是參數 所以這一個是負責拿來做更新的 拿來更新 Harness 的語言模型 這個語言模型會吃一個 Harness 吃它的表現 給一個新的 Harness 你怎麼知道這個模型 它真的很擅長更新 Harness 呢 我們要訓練它 教它怎麼去更新 Harness 怎麼教它怎麼更新 Harness 呢 你就可以收集訓練的資料 它用的其實是 reinforcement 的 algorithm 你今天有一個新的 Harness $H'$ 之後 把這個 $H'$ 呢 拿去做 evaluation 你就得到 $H'$ 的表現 你把這個 H 的表現 跟 $H'$ 的表現相減 就當作是這個語言模型的 reward 你就可以教語言模型 怎麼樣更新 才是可以讓表現 進步最多的更新方法 你就可以微調參數 微調出一個專門負責 更新 Harness 的語言模型

</details>


### Slide 37 — 連更新規則也一起更新（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=2316s))

![Slide 37 — 連更新規則也一起更新（續）](slides/037_01-39-36.jpg)

Hyper-Agent 不只改 Harness，也演化更新模組。系統自行改善候選 sampling 策略，展示第二層自我改進，但外層目標和評估仍由人設計。 本段重點：我們當然在討論 更新更新的模組的時候 我們討論的都是在更新 Harness 參數呢 更新參數也許比較少人討論 是因為更新參數 有固定的演算法 這個演算法 就是人類設計出來的 比如說 gradient descent 或是 gradient descent 有很多變形 比如說 adam 或者是 adamw 可能是大家常常用的演算法 但它們都是人設計的 能不能夠用機器來設計更新的演算法呢


<details>
<summary><strong>Cleaned narration</strong></summary>

> 我們當然在討論 更新更新的模組的時候 我們討論的都是在更新 Harness 參數呢 更新參數也許比較少人討論 是因為更新參數 有固定的演算法 這個演算法 就是人類設計出來的 比如說 gradient descent 或是 gradient descent 有很多變形 比如說 adam 或者是 adamw 可能是大家常常用的演算法 但它們都是人設計的 能不能夠用機器來設計更新的演算法呢

</details>


### Slide 38 — 連更新規則也一起更新（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=2346s))

![Slide 38 — 連更新規則也一起更新（續）](slides/038_01-39-06.jpg)

Hyper-Agent 不只改 Harness，也演化更新模組。系統自行改善候選 sampling 策略，展示第二層自我改進，但外層目標和評估仍由人設計。 本段重點：重點是，完全就是可以的 事實上在上次上課接近結尾的時候 我這邊特別標出來是 52 分 17 秒的時候 也已經講到類似的概念 我們說有一個 benchmark 叫 PostTrainBench


<details>
<summary><strong>Cleaned narration</strong></summary>

> 重點是，完全就是可以的 事實上在上次上課接近結尾的時候 我這邊特別標出來是 52 分 17 秒的時候 也已經講到類似的概念 我們說有一個 benchmark 叫 PostTrainBench

</details>


### Slide 39 — 連更新規則也一起更新（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=2358s))

![Slide 39 — 連更新規則也一起更新（續）](slides/039_01-39-18.jpg)

Hyper-Agent 不只改 Harness，也演化更新模組。系統自行改善候選 sampling 策略，展示第二層自我改進，但外層目標和評估仍由人設計。 本段重點：重點是，它就是要看看一個好的語言模型 有沒有能力去訓練其他的語言模型 你就告訴這個語言模型說 我們想訓練一個其他的模型 這個模型的目標是什麼 它就根據你給的這些指示 寫出一些程式來訓練其他的模型 所以今天訓練的 algorithm 訓練 update 模型參數的 algorithm 也可以是由一個語言模型來產生的


<details>
<summary><strong>Cleaned narration</strong></summary>

> 重點是，它就是要看看一個好的語言模型 有沒有能力去訓練其他的語言模型 你就告訴這個語言模型說 我們想訓練一個其他的模型 這個模型的目標是什麼 它就根據你給的這些指示 寫出一些程式來訓練其他的模型 所以今天訓練的 algorithm 訓練 update 模型參數的 algorithm 也可以是由一個語言模型來產生的

</details>


### Slide 40 — 連更新規則也一起更新（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=2388s))

![Slide 40 — 連更新規則也一起更新（續）](slides/040_01-40-48.jpg)

Hyper-Agent 不只改 Harness，也演化更新模組。系統自行改善候選 sampling 策略，展示第二層自我改進，但外層目標和評估仍由人設計。 本段重點：重點是，或者是前一陣子很紅的 AutoResearch 其實也是一樣的概念 它們是用一個語言模型來決定 update 另外一個語言模型的參數 所以今天 update 的演算法 是可以由一個語言模型 創造出來的


<details>
<summary><strong>Cleaned narration</strong></summary>

> 重點是，或者是前一陣子很紅的 AutoResearch 其實也是一樣的概念 它們是用一個語言模型來決定 update 另外一個語言模型的參數 所以今天 update 的演算法 是可以由一個語言模型 創造出來的

</details>


### Slide 41 — 連更新規則也一起更新（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=2406s))

![Slide 41 — 連更新規則也一起更新（續）](slides/041_01-40-06.jpg)

Hyper-Agent 不只改 Harness，也演化更新模組。系統自行改善候選 sampling 策略，展示第二層自我改進，但外層目標和評估仍由人設計。 本段重點：update 的演算法 可以由一個語言模型創造出來 我們能不能特別去訓練一個語言模型 強化它產生訓練演算法的能力呢 還真的是可以的 有一篇 paper 叫做 SEAL (Self-Adapting LLM) 它們裡面有一個 Language Model 這個 Language Model 不是拿來解任務的 它們那邊有點神奇 它們解任務的 Language Model 跟拿來產生訓練演算法 Language Model 如果沒有看錯的話是…


<details>
<summary><strong>Cleaned narration</strong></summary>

> update 的演算法 可以由一個語言模型創造出來 我們能不能特別去訓練一個語言模型 強化它產生訓練演算法的能力呢 還真的是可以的 有一篇 paper 叫做 SEAL (Self-Adapting LLM) 它們裡面有一個 Language Model 這個 Language Model 不是拿來解任務的 它們那邊有點神奇 它們解任務的 Language Model 跟拿來產生訓練演算法 Language Model 如果沒有看錯的話是同一個 所以總之它們的 Language Model 身兼兩個職務 一方面要解任務 另外一方面 它要決定要怎麼訓練自己 它們的 Language Model 這邊寫作 $\theta_t$ 它們 Language Model 的 Output 這邊寫作 SE 這個 SE 是 Self-Editing 的縮寫 這 SE 裡面有什麼呢 這 SE 裡面就通常包含了 如果我等一下要更新自己的話 我 learning rate 要設多少 如果我等一下要更新自己的話 我要拿哪一些訓練資料 或如果我要拿這些訓練資料的話 我要怎麼對它做 data augmentation 它可以產生一個 訓練自己的規劃 這邊叫做 SE 這個 $\theta$ 的訓練方法是 它產生不同的 SE 每一個 SE 呢 就真的拿去更新自己 所以它自己就更新出 $\theta'$ $\hat{\theta}$ 跟 $\theta^\#$ 三個版本 這三個版本 再真的拿去解任務 看看解得怎麼樣 把這個更新版本 解任務的結果 當作 reward 再回頭去更新自己 更新自己的能力 不知道大家聽不聽得懂 總之 這個是更新自己的模型 它最後會知道 更新的結果怎麼樣 它會拿更新的結果 當作 reward 去更新更新自己的能力 就是這麼神奇 所以我們現在已經講到說

</details>


## 七、Meta-Learning

### Slide 42 — Learning to Learn ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=2523s))

![Slide 42 — Learning to Learn](slides/042_01-42-03.jpg)

Meta-learning 用參數控制學習演算法：內迴圈更新任務模型，外迴圈依跨任務結果改進更新規則，把「如何學習」本身當成學習對象。 本段重點：重點是，我們這些 AI agent 它可以自我強化 它不只可以自我強化


<details>
<summary><strong>Cleaned narration</strong></summary>

> 重點是，我們這些 AI agent 它可以自我強化 它不只可以自我強化

</details>


### Slide 43 — Learning to Learn（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=2532s))

![Slide 43 — Learning to Learn（續）](slides/043_01-42-12.jpg)

Meta-learning 用參數控制學習演算法：內迴圈更新任務模型，外迴圈依跨任務結果改進更新規則，把「如何學習」本身當成學習對象。 本段重點：重點是，它可以自我強化 自我強化的規則 所以它是兩層的 所以不只是 AI agent 本身在強化 強化 AI agent 的規則 也在強化 強化 AI agent 的規則 這個模組 也是 AI agent 的一部分 它也可以不斷地被強化


<details>
<summary><strong>Cleaned narration</strong></summary>

> 重點是，它可以自我強化 自我強化的規則 所以它是兩層的 所以不只是 AI agent 本身在強化 強化 AI agent 的規則 也在強化 強化 AI agent 的規則 這個模組 也是 AI agent 的一部分 它也可以不斷地被強化

</details>


### Slide 44 — Learning to Learn（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=2550s))

![Slide 44 — Learning to Learn（續）](slides/044_01-42-30.jpg)

Meta-learning 用參數控制學習演算法：內迴圈更新任務模型，外迴圈依跨任務結果改進更新規則，把「如何學習」本身當成學習對象。 本段重點：有個專有名詞叫做 Meta Learning 它的意思就是學習如何學習 所以當你做的研究是 我要來想一個方法 來更新模型能力的模組的時候 你做的其實就是 Meta Learning Meta Learning 其實在 2021 年的機器學習 就已經有講過了 我就把過去的錄影放在這邊 給大家參考


<details>
<summary><strong>Cleaned narration</strong></summary>

> 有個專有名詞叫做 Meta Learning 它的意思就是學習如何學習 所以當你做的研究是 我要來想一個方法 來更新模型能力的模組的時候 你做的其實就是 Meta Learning Meta Learning 其實在 2021 年的機器學習 就已經有講過了 我就把過去的錄影放在這邊 給大家參考

</details>


### Slide 45 — Learning to Learn（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=2574s))

![Slide 45 — Learning to Learn（續）](slides/045_01-43-54.jpg)

Meta-learning 用參數控制學習演算法：內迴圈更新任務模型，外迴圈依跨任務結果改進更新規則，把「如何學習」本身當成學習對象。 本段重點：所以整個 Meta Learning 的想法 通常是這樣子的 在 Meta Learning 裡面 你真正想要找的是 操控學習的一組參數 這組參數我們這邊用 $\phi$ 來表示 $\phi$ 的工作是決定了 怎麼學習這件事情 你可以把 $\phi$ 呢 想成是它在控制一個函式 這個函式呢 我這邊用大寫的 $f$ 來表示它 這個函式的輸入 是一組舊的參數 這邊用 $\theta_{t}$ 來表示它 它的輸出是一組新的參數 叫做 $\th…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 所以整個 Meta Learning 的想法 通常是這樣子的 在 Meta Learning 裡面 你真正想要找的是 操控學習的一組參數 這組參數我們這邊用 $\phi$ 來表示 $\phi$ 的工作是決定了 怎麼學習這件事情 你可以把 $\phi$ 呢 想成是它在控制一個函式 這個函式呢 我這邊用大寫的 $f$ 來表示它 這個函式的輸入 是一組舊的參數 這邊用 $\theta_{t}$ 來表示它 它的輸出是一組新的參數 叫做 $\theta_{t+1}$ 而這個 $\phi$ 就決定了 這個 $\theta$ 要怎麼被更新 這個 $\phi$ 決定了 要怎麼做學習這件事情 而 Meta Learning 就是要找這樣一組的參數 $\phi$ 你就期待說 我們可以用 Meta Learning 的演算法 來更新 $\phi$ 本來是 $\phi_{t}$ 變成 $\phi_{t+1}$ 希望這是一組更好的參數 它可以給我們一個更好的 更新參數的方式 可以讓 $\theta_{t}$ 更新到 $\theta_{t+1}$ 的時候 比如說進步更多 或者是希望 最後整個更新過程 跑完的時候 最後得出來的 $\theta$ 會比原來之前 用舊的學習方法 更新出來的 $\theta$ 還要更好 這個就是 Meta Learning 的精神 這就讓我想到

</details>


### Slide 46 — Learning to Learn（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=2655s))

![Slide 46 — Learning to Learn（續）](slides/046_01-44-15.jpg)

Meta-learning 用參數控制學習演算法：內迴圈更新任務模型，外迴圈依跨任務結果改進更新規則，把「如何學習」本身當成學習對象。 本段重點：整個生物的演化 這一個 Meta Learning 我們要找的參數 其實就像是基因一樣 這個基因 它在很長的一段時間 在一個生命體誕生之後 它是固定的 它決定了 這個生命體要怎麼成長 它決定了一個生物 如果它有大腦的話 它的大腦要怎麼變化 它的大腦要怎麼更新 內部神經元的連結 也就是怎麼更新 神經元連結之間的權重 但是這個 $\phi$ 本身也是可以更新的 它透過天擇來進行更新 透過天擇來選擇出更好的 $\phi$ 這些更好的 $\ph…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 整個生物的演化 這一個 Meta Learning 我們要找的參數 其實就像是基因一樣 這個基因 它在很長的一段時間 在一個生命體誕生之後 它是固定的 它決定了 這個生命體要怎麼成長 它決定了一個生物 如果它有大腦的話 它的大腦要怎麼變化 它的大腦要怎麼更新 內部神經元的連結 也就是怎麼更新 神經元連結之間的權重 但是這個 $\phi$ 本身也是可以更新的 它透過天擇來進行更新 透過天擇來選擇出更好的 $\phi$ 這些更好的 $\phi$ 可能會讓學習更有效率 所以你可以說 在做 Meta Learning 的時候 我們找出來的控制 怎麼學習的參數是基因 這個 $\phi$ 控制的參數 其實是我們的大腦 其實是生物的神經元 講到這邊

</details>


### Slide 47 — Learning to Learn（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=2715s))

![Slide 47 — Learning to Learn（續）](slides/047_01-45-15.jpg)

Meta-learning 用參數控制學習演算法：內迴圈更新任務模型，外迴圈依跨任務結果改進更新規則，把「如何學習」本身當成學習對象。 本段重點：你可能會覺得說 這個 Meta Learning 聽起來好像非常的玄妙 你說有一個函式 這個函式受到 $\phi$ 的操控 這個函式輸入居然是一組參數 一組類神經網路的參數 比如說一個 Transformer 它的輸出是另外一個 Transformer 這到底是怎麼做到的 怎麼樣弄一個函式 它可以輸入一個類神經網路的參數 輸出又是另外一個類神經網路的參數呢 有一篇 paper 告訴你說 這篇 paper 叫 Learning to Le…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 你可能會覺得說 這個 Meta Learning 聽起來好像非常的玄妙 你說有一個函式 這個函式受到 $\phi$ 的操控 這個函式輸入居然是一組參數 一組類神經網路的參數 比如說一個 Transformer 它的輸出是另外一個 Transformer 這到底是怎麼做到的 怎麼樣弄一個函式 它可以輸入一個類神經網路的參數 輸出又是另外一個類神經網路的參數呢 有一篇 paper 告訴你說 這篇 paper 叫 Learning to Learn at Test Time: RNNs with Expressive Hidden States 它告訴你說 其實你也不用多做什麼 你一般在訓練 RNN 或訓練 Transformer 的時候 你也可以看作 你已經在做 Meta Learning 了 怎麼說呢 跟大家複習一下 RNN 但是 Transformer 也是一樣的 大家知道 RNN 就是 你一開始有一組 Memory 有一組 hidden state 叫做 $h_0$ 有一個輸入叫做 $x_1$ $f_A, f_B$ 是 RNN 的參數 根據 $f_A, f_B$ 你會去把 $h_0$ 更新成 $h_1$ 根據 $h_1$ 你會產生 $y_1$ 這個過程會反覆地進行下去 有了新的輸入 $x_2$ 你的 memory 就變 你的這個 hidden state 就從 $h_1$ 更新成 $h_2$ 這個過程就反覆進行下去 一般我們的認知是 這個 $f_A, f_B, f_C$ 是參數 是類神經網路的參數 在這篇 paper 裡面 它給了你另外一個想法 它說我們把 $H$ 說它才是參數 參數不是一組數字嗎 我可不可以說 存在 hidden state 的這組數字 就叫做類神經網路的參數 就是這裡的 $\theta$ 而 RNN 裡面 決定這個 $H$ 長什麼樣子的 我們本來以為是 類神經網路的參數 其實是 Meta Learning 學出來的參數 也就是 $\phi$ 你說這個跟原來的訓練 有什麼不同 沒有半毛錢的不同 就同一個東西 我們換一個方法講 你有沒有覺得 你也能做 Meta Learning 其實當你在訓練一個 RNN 或訓練一個 Transformer 的時候 你也可以說 你其實就在做 Meta Learning 不知道大家能不能夠 接受這個想法

</details>


### Slide 48 — Learning to Learn（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=2853s))

![Slide 48 — Learning to Learn（續）](slides/048_01-48-33.jpg)

Meta-learning 用參數控制學習演算法：內迴圈更新任務模型，外迴圈依跨任務結果改進更新規則，把「如何學習」本身當成學習對象。 本段重點：其實呢 如果你想要知道更多 RNN 跟 Transformer 的關係的話 你可以看去年的機器學習第四講 我們花了很多時間 完整的講 Transformer 跟 RNN 還有一系列這個 RNN 的變形 比如說 Mamba 之間的關係 其實啊


<details>
<summary><strong>Cleaned narration</strong></summary>

> 其實呢 如果你想要知道更多 RNN 跟 Transformer 的關係的話 你可以看去年的機器學習第四講 我們花了很多時間 完整的講 Transformer 跟 RNN 還有一系列這個 RNN 的變形 比如說 Mamba 之間的關係 其實啊

</details>


### Slide 49 — Learning to Learn（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=2871s))

![Slide 49 — Learning to Learn（續）](slides/049_01-48-51.jpg)

Meta-learning 用參數控制學習演算法：內迴圈更新任務模型，外迴圈依跨任務結果改進更新規則，把「如何學習」本身當成學習對象。 本段重點：近年有很多論文 比如說 TITAN 或 Nested Learning 它們都宣稱說 它們開發出新的 Meta Learning 的方法 它們可以讓參數 自己更新 它們可以讓 Network 在使用的時候 自動更新參數 其實這些方法套用的都是 剛才我講的那一篇 換句話說的方法 他們其實都是把 本來被視為 memory 或本來被視為 attention 的東西 當作是參數來看 而原來類神經網路的參數 就說它是 Meta Learning …


<details>
<summary><strong>Cleaned narration</strong></summary>

> 近年有很多論文 比如說 TITAN 或 Nested Learning 它們都宣稱說 它們開發出新的 Meta Learning 的方法 它們可以讓參數 自己更新 它們可以讓 Network 在使用的時候 自動更新參數 其實這些方法套用的都是 剛才我講的那一篇 換句話說的方法 他們其實都是把 本來被視為 memory 或本來被視為 attention 的東西 當作是參數來看 而原來類神經網路的參數 就說它是 Meta Learning 的參數 你可能會想說 這樣子的講法有什麼意義呢 跟原來的訓練方法 其實沒有非常大的差別 但是這樣新的概念

</details>


## 八、重新理解學習

### Slide 50 — 學習不只更新權重 ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=2913s))

![Slide 50 — 學習不只更新權重](slides/050_01-49-33.jpg)

若學習是持久改變行為，寫入記憶、skill、prompt、工具與 workflow 也屬學習。外部模組快速可回復，但帶來容量、檢索和一致性問題。 本段重點：重點是，有什麼樣的意義呢 我覺得它開拓了我們的視野 所以讓我們對於機器學習 有了不一樣的觀點 什麼是學習 學習就是改變一個東西 它的行為 如果就人類的學習而言 人類為什麼會改變行為 是因為你腦中的 類神經網路的連結改變了 我們說今天人類的學習 就是我們調整了 我們腦中神經元之間的連結 這是人類的學習 傳統的機器學習告訴你說 什麼叫機器的學習 機器的學習是 更新了模型的參數 比如說類神經網路的參數 或其他機器學習模型的參數 過去當我們講到…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 重點是，有什麼樣的意義呢 我覺得它開拓了我們的視野 所以讓我們對於機器學習 有了不一樣的觀點 什麼是學習 學習就是改變一個東西 它的行為 如果就人類的學習而言 人類為什麼會改變行為 是因為你腦中的 類神經網路的連結改變了 我們說今天人類的學習 就是我們調整了 我們腦中神經元之間的連結 這是人類的學習 傳統的機器學習告訴你說 什麼叫機器的學習 機器的學習是 更新了模型的參數 比如說類神經網路的參數 或其他機器學習模型的參數 過去當我們講到 機器學習的時候 我們往往把這些參數 類比成人腦神經元的連結 我們說類神經網路的 這些參數就類比到 人腦裡面的神經元的連結 人腦神經元的 update 就是 Neural Network 一個 Deep Learning 的 model 它的這個參數的 update 如果你是用這樣的想法的話 你就會覺得 哇這個人工智慧的學習 實在是很沒有效率 人類非常的厲害 只要看幾個例子 我們就可以快速地 update 我們人腦的神經元 我們可以記住新的事物 我們可以學會新的技能 但對於機器來說 要調整參數學會新的技能 似乎非常的困難 如果你有自己訓練模型 你會知道訓練模型 不是一件容易的事 你沒有辦法單靠幾個 example 就輕易的做出 few-shot learning 讓參數能夠自由地調整 甚至很多時候 你調整參數帶來的結果 都是負面的 你一調 類神經網路就壞掉了 比原來你調整之前 還要更差 但那是因為 你把類神經網路的參數 跟人腦的神經元 直接做類比 我們現在換一個類比的方式

</details>


### Slide 51 — 學習不只更新權重（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=3027s))

![Slide 51 — 學習不只更新權重（續）](slides/051_01-50-27.jpg)

若學習是持久改變行為，寫入記憶、skill、prompt、工具與 workflow 也屬學習。外部模組快速可回復，但帶來容量、檢索和一致性問題。 本段重點：我告訴你 存在 hidden state 裡面的東西 或 Transformer 的 attention 才是大腦裡面的神經元 些類神經網路的參數 其實是你的基因 你會不會覺得 現在的視野突然不一樣了呢 我們知道基因一個個體出生之後 它的基因就是固定的 隨著它跟環境的互動 它的神經元會改變 但是基因總是固定的那一套 基因很少改變 沒有另外新的 沒有產生新的世代 基因就是固定的 如果我們今天講說 類神經網路的參數就是基因 你會不會覺得現在…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 我告訴你 存在 hidden state 裡面的東西 或 Transformer 的 attention 才是大腦裡面的神經元 些類神經網路的參數 其實是你的基因 你會不會覺得 現在的視野突然不一樣了呢 我們知道基因一個個體出生之後 它的基因就是固定的 隨著它跟環境的互動 它的神經元會改變 但是基因總是固定的那一套 基因很少改變 沒有另外新的 沒有產生新的世代 基因就是固定的 如果我們今天講說 類神經網路的參數就是基因 你會不會覺得現在的人工智慧 其實非常的強悍呢 人類的基因是數十億年來演化的結果 而這些語言模型 雖然我們一直說耗費了大量的算力 需要長時間的訓練 但是如果你說 2018 年開始出現 GPT-1 到現在也不過八年的時間 它就已經進化到 它爹娘都不認得的地步 所以如果說這些參數就是基因的話 其實今天的人工智慧 真的可以說是進展神速 你說今天這些機器 不容易學會新東西 不容易用新東西來調整參數 如果你說這個 類神經網路的 attention 或者是它的 hidden state 就是人腦的話 你可以在這個 hidden state 裡面 放入新的資訊 今天這些語言模型 你只要把新的資訊 新的規則放到它的 context 它的行為馬上就改變了 是不是跟人類的學習一樣 非常的有效率 也非常能做 few-shot learning 了 所以換一個角度 你會覺得今天人工智慧的發展 真的是發展的迅速的不可思議 如果你覺得類神經網路的參數 就是基因的話 你會覺得今天人工智慧發展 其實相較於大自然的天擇而言 實在是非常的迅速

</details>


### Slide 52 — 學習不只更新權重（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=3141s))

![Slide 52 — 學習不只更新權重（續）](slides/052_01-52-21.jpg)

若學習是持久改變行為，寫入記憶、skill、prompt、工具與 workflow 也屬學習。外部模組快速可回復，但帶來容量、檢索和一致性問題。 本段重點：事實上呢 剛才會講說 我們有兩層在 update 的東西 但其實對一個人工智慧而言 現在在 update 的東西 不只是只有兩層 而是可以看作是有非常多層的 update 最快的東西 可能是 Neural Network 裡面的 hidden state 或者是 Transformer 裡面的 attention 它們是 update 最快的東西 但是只要跨一個 session 跨一個新的對話 這些更新就會全部消失 它們象徵著人類的短期…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 事實上呢 剛才會講說 我們有兩層在 update 的東西 但其實對一個人工智慧而言 現在在 update 的東西 不只是只有兩層 而是可以看作是有非常多層的 update 最快的東西 可能是 Neural Network 裡面的 hidden state 或者是 Transformer 裡面的 attention 它們是 update 最快的東西 但是只要跨一個 session 跨一個新的對話 這些更新就會全部消失 它們象徵著人類的短期記憶 大家都知道說人類的短期記憶 很多時候你只能夠記幾秒 你只能夠記幾個物件 在幾秒鐘之後 如果它們沒轉成長期記憶的話 這些短期記憶的內容就消失不見了 我們可以說 當我們在使用一個 Transformer 的時候 它 hidden state 的變化 就是短期記憶 對一個 AI Agent 來說 它背後呢 有一個 memory 的系統 通常我們是用電腦上面的檔案 來當作是這個人工智慧 AI Agent 的 memory 所以今天你可以透過一個 Transformer 透過這些 hidden state 的改變 來改變你存在電腦上面的文字資料 改變這些文字資料 就改變了 memory 改變了 memory 其實你就改變了這些 hidden state 變化的過程 因為這些 hidden state 在變化的時候 你會把 memory 當作 context 先放進去 所以這些 memory 改變了 hidden state 變化的過程 這是我們的長期記憶 所以你在一個 session 裡面 把短期記憶轉成長期記憶 它才能夠永遠地記得 機器的長期記憶跟人類很像 人類的長期記憶可以說是幾乎無限大的 機器的長期記憶就是它的檔案系統 相較於 hidden state 來說 也可以說近乎是無限大的 在 memory 背後控制這一切的是 Network 的參數 是一個 Language Model 它甚至是在雲端的 Language Model 你是沒有辦法去更動它的 至少你沒有辦法 在一個世代內去更動它 它更動的非常緩慢 這個東西 其實就是 AI Agent 的基因 所以從這個類比來看 你會覺得 哇，今天 AI Agent 的設計 其實跟人腦 有很多異曲同工的地方 事實上這邊講說 memory 呢 就是長期基因 可能是有點簡化 這整套說法 如果你看小金的影片的話 還記得他嗎 他人在持續更新影片 他最近有一些影片 是講他自己 memory 的 他把自己的 memory 呢 分成好多層 他會覺得說像 跟 soul.md 這些有關的 memory 它的更新是非常緩慢的 非常少更新 但有一些東西 比如說跟 feedback 有關的 它會非常常更新 所以這些記憶 也是有快慢不同層級之分的

</details>


## 九、內在動機

### Slide 53 — Agent 缺少自己想做的事 ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=3309s))

![Slide 53 — Agent 缺少自己想做的事](slides/053_01-55-09.jpg)

現有 Agent 的主動多由 heartbeat 或指令觸發。Curiosity-driven learning 用新奇性或資訊增益產生內在目標，但「什麼值得做」仍常由人指定。 本段重點：講到這邊 我們看到這些人工智慧 跟人類有很多 跟人類的智慧 有很多類似的地方 今天這些人工智慧缺少什麼呢 我覺得它們很缺乏的一個東西 就是內在動機 如果你自己有養 AI Agent 的話 你會發現 這些 AI Agent 往往蠻被動的 它沒有什麼 自己想做的事 你可能會說 有些 AI Agent 不是都會做蠻主動的事情嗎 比如說每 30 分鐘 起來收信一次 但是它的主動 是你叫它的主動 你叫它要主動做什麼事 它才會主動做什麼事 如果你沒…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 講到這邊 我們看到這些人工智慧 跟人類有很多 跟人類的智慧 有很多類似的地方 今天這些人工智慧缺少什麼呢 我覺得它們很缺乏的一個東西 就是內在動機 如果你自己有養 AI Agent 的話 你會發現 這些 AI Agent 往往蠻被動的 它沒有什麼 自己想做的事 你可能會說 有些 AI Agent 不是都會做蠻主動的事情嗎 比如說每 30 分鐘 起來收信一次 但是它的主動 是你叫它的主動 你叫它要主動做什麼事 它才會主動做什麼事 如果你沒下這個指令 它就是躺在那邊 通常什麼事也不想做 所以今天這些 AI Agent 它們蠻缺少了一個內在的慾望 我們以研究為例 我們知道說 假設你今天把實驗做出來 把方法想出來 你把草稿交給一個語言模型 它可以輕易地幫你完成一篇論文 今天你有一個研究問題 你可以讓一個語言模型 幫你思考 幫你規劃 幫你執行實驗 最後解出這個研究問題 比如說 AlphaEvo 就是其中一個例子 AlphaEvo 做了很多很神奇的事情 比如說要求它去加速矩陣的運算 它就真的加速了矩陣的運算 用在下一個世代的 AI Agent 的開發上 這可能也可以說是一種 AI 的自我進化 不過裡面當然 involve 了非常多的人力 它並不是開發出新的 矩陣相乘演算法以後 新一個世代 AI 就直接跑出來 當然這背後 還是有很多其他人為的介入的 但是你今天可以 給它一個研究問題 它直接幫你產生成果

</details>


### Slide 54 — Agent 缺少自己想做的事（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=3411s))

![Slide 54 — Agent 缺少自己想做的事（續）](slides/054_01-57-51.jpg)

現有 Agent 的主動多由 heartbeat 或指令觸發。Curiosity-driven learning 用新奇性或資訊增益產生內在目標，但「什麼值得做」仍常由人指定。 本段重點：今天你甚至可以告訴它 我就想研究個 比如說生物相關的問題 它自己幫你尋找研究問題 比如說 AI co-scientist 看起來就是在做 類似的事情 但是它沒辦法自己決定 它要去哪個領域 找研究問題 它要找研究問題 需要人類去下指令給它 就算你跟它講說 你就去找一個沒有人在研究的領域 想一些最值得研究的問題 但是這個指令仍然是需要人類去下的 你如果沒有下任何指令 它沒有辦法自主的起來覺得說 我就是很想解決某個問題 就自己去解決它 它少了…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 今天你甚至可以告訴它 我就想研究個 比如說生物相關的問題 它自己幫你尋找研究問題 比如說 AI co-scientist 看起來就是在做 類似的事情 但是它沒辦法自己決定 它要去哪個領域 找研究問題 它要找研究問題 需要人類去下指令給它 就算你跟它講說 你就去找一個沒有人在研究的領域 想一些最值得研究的問題 但是這個指令仍然是需要人類去下的 你如果沒有下任何指令 它沒有辦法自主的起來覺得說 我就是很想解決某個問題 就自己去解決它 它少了一些原生的動機 我們之前有講過很多 paper

</details>


### Slide 55 — Agent 缺少自己想做的事（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=3459s))

![Slide 55 — Agent 缺少自己想做的事（續）](slides/055_01-58-39.jpg)

現有 Agent 的主動多由 heartbeat 或指令觸發。Curiosity-driven learning 用新奇性或資訊增益產生內在目標，但「什麼值得做」仍常由人指定。 本段重點：它們都會宣稱說它們完全沒有人類介入 比如說 R1-Zero 比如 Absolute Zero 你從它的名字看起來 就是它想要告訴你說 Zero 就是沒有人類介入的意思 裡面都是有一個 Proposer 有一個 Solver 有一個 Verifier 但是那個 Proposer 要產生出問題的時候 還是需要人類給 prompt 的 比如說在 R1-Zero 這篇 paper 裡面 他們希望語言模型 可以自主強化數學的能力 但為什麼語言模型…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 它們都會宣稱說它們完全沒有人類介入 比如說 R1-Zero 比如 Absolute Zero 你從它的名字看起來 就是它想要告訴你說 Zero 就是沒有人類介入的意思 裡面都是有一個 Proposer 有一個 Solver 有一個 Verifier 但是那個 Proposer 要產生出問題的時候 還是需要人類給 prompt 的 比如說在 R1-Zero 這篇 paper 裡面 他們希望語言模型 可以自主強化數學的能力 但為什麼語言模型 自主強化數學的能力呢 因為你告訴 Proposer 說 出一些很難的數學問題 你告訴它說 你可以出這些種類的數學問題 你已經告訴它要出數學問題了 它才去強化自己數學的能力 它並不是沒事坐在那邊 就突然想要強化數學的能力 或者是 Absolute Zero 想要強化模型寫程式的能力 為什麼模型自主地強化寫程式的能力 只有你告訴 Proposer 說 你去出一些跟 Python 有關的問題 還告訴你說 應該出什麼樣的題型等等 給了很多指示 今天 AI Agent 才知道 要出一些程式的問題 來自己考自己 自己強化自己 如果你沒有人類給這些指示 沒有人類給這些動機 AI Agent 根本不會自己動起來 想要自己強化自己 所以接下來問的問題就是

</details>


### Slide 56 — Agent 缺少自己想做的事（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=3543s))

![Slide 56 — Agent 缺少自己想做的事（續）](slides/056_01-59-03.jpg)

現有 Agent 的主動多由 heartbeat 或指令觸發。Curiosity-driven learning 用新奇性或資訊增益產生內在目標，但「什麼值得做」仍常由人指定。 本段重點：有沒有辦法給 AI Agent 原生的動機 過去人類提供給它動機 告訴它說 你要讓自己的數學變強 它就讓自己的數學變強 但它是被動的 它是個被動的孩子 能不能夠讓它主動想要學習呢 能不能夠讓它主動想要動起來呢 其實一直有這方面的研究 我這邊就引用了一大堆的論文 最早的甚至是 15 年前 13 年前 在上個宇宙大霹靂之前的文章 時候就已經有人開始研究 要怎麼讓這些 AI Agent 有原生的動機 這些 paper 的套路通常都是 我能不能…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 有沒有辦法給 AI Agent 原生的動機 過去人類提供給它動機 告訴它說 你要讓自己的數學變強 它就讓自己的數學變強 但它是被動的 它是個被動的孩子 能不能夠讓它主動想要學習呢 能不能夠讓它主動想要動起來呢 其實一直有這方面的研究 我這邊就引用了一大堆的論文 最早的甚至是 15 年前 13 年前 在上個宇宙大霹靂之前的文章 時候就已經有人開始研究 要怎麼讓這些 AI Agent 有原生的動機 這些 paper 的套路通常都是 我能不能夠想一個目標 這個目標是一個非常抽象 跟任何任務都沒有直接關係的目標 我們就把這個目標 植入 AI Agent 裡面 接下來就不管它 它就自己愛幹嘛就幹嘛 但希望最後變成我們要的樣子 常見的手法 一個就是給它好奇心 這種好奇心的套路 通常就是讓 AI Agent 想要做一些事情 讓自己看到一些過去沒看到的東西 這就是某種好奇心的體現 一系列的研究都在做這種 Curiosity Driven 的 Agent 也有些研究做 Empowerment 的 Agent Empowerment 這個字 也許中文可以翻成賦權 也就是讓 AI Agent 有掌控感 它學習的目標是什麼 它學習的目標就是 為了希望更能夠控制這個環境 讓這個環境更能夠做預測 通常他會寫成數學式子說 AI Agent 想要 optimize 的 reward 是 它執行一些 action 之後 它能夠預測 接下來會發生什麼樣的事情 我覺得這個其實跟人類的學習 人類的動機也許也非常的類似 人類我們會想要做研究 也許就是為了我們想要更了解這個世界 為什麼我們想要更了解這個世界 就是為了我們想要 更能夠預測它 更能夠控制它 避免我們無法想像 無法預測的事情發生 所以也許 curiosity 或者是 Empowerment 可以變成一個 做研究的 AI Agent 的原生動機 因為它有好奇心 因為它期待一個東西 有個解釋 所以它去自主的做了研究 它自己自主找出什麼東西 它沒有辦法解釋 什麼東西它沒有看過 它自主做了研究 自己強化自己 自己推動科學的進展 總之這邊有一系列的研究 在做讓 AI 有原生動機這件事情 其實 Curiosity Driven

</details>


## 十、自我成長失控風險

### Slide 57 — 更新流程可能突破邊界 ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=3702s))

![Slide 57 — 更新流程可能突破邊界](slides/057_01-02-42.jpg)

當 Agent 能修改 Harness、更新器和目標追求方式，固定 procedure 不再保證受控。需要不可由被評系統單方面修改的外部約束、審計與停止機制。 本段重點：重點是，這樣子的 AI Agent 2017 年的時候就有了 所以 2018 年的機器學習課程 是有講過 Curiosity Driven 的 AI Agent 的 我就把八年前的錄影 連結放在這邊給大家參考 所以大家如果想知道 Curiosity Driven 怎麼做的話 參見這個八年前的錄影 我們現在已經知道


<details>
<summary><strong>Cleaned narration</strong></summary>

> 重點是，這樣子的 AI Agent 2017 年的時候就有了 所以 2018 年的機器學習課程 是有講過 Curiosity Driven 的 AI Agent 的 我就把八年前的錄影 連結放在這邊給大家參考 所以大家如果想知道 Curiosity Driven 怎麼做的話 參見這個八年前的錄影 我們現在已經知道

</details>


### Slide 58 — 更新流程可能突破邊界（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=3726s))

![Slide 58 — 更新流程可能突破邊界（續）](slides/058_01-02-06.jpg)

當 Agent 能修改 Harness、更新器和目標追求方式，固定 procedure 不再保證受控。需要不可由被評系統單方面修改的外部約束、審計與停止機制。 本段重點：AI 有機會自我成長 我們也講 AI 不只有機會自我成長 它還可以自我成長 自我成長這件事情 我們還說 有一群人在研究 怎麼讓 AI 有原生的動機 這個是不是已經跟 科幻小說裡面的 AI 非常的接近了呢 也許再來我們要思考的問題就是 這個成長會不會失控 這個成長會不會成長到後來 脫離了人類的掌控 就變成天網 這件事情不是沒有可能的 我只能沒有可能的部分 我只能不是沒有可能的部分是說 今天 AI 的成長是有可能會失控的 你可能會想說 AI…


<details>
<summary><strong>Cleaned narration</strong></summary>

> AI 有機會自我成長 我們也講 AI 不只有機會自我成長 它還可以自我成長 自我成長這件事情 我們還說 有一群人在研究 怎麼讓 AI 有原生的動機 這個是不是已經跟 科幻小說裡面的 AI 非常的接近了呢 也許再來我們要思考的問題就是 這個成長會不會失控 這個成長會不會成長到後來 脫離了人類的掌控 就變成天網 這件事情不是沒有可能的 我只能沒有可能的部分 我只能不是沒有可能的部分是說 今天 AI 的成長是有可能會失控的 你可能會想說 AI 它製作的事情 雖然它可以自己更新自己的模組 但這個更新的 procedure 更新的過程都還是固定的 你說它可以更新自己 它可以更新更新自己 但怎麼更新更新自己的那個方法 仍然是固定的 所以它仍然是 在某一個框架內成長 雖然 AI 在某一個框架內成長 它很難跳脫 控制它怎麼更新自己 還有更新更新自己的框架 但是有可能會讓 AI 失控的一個 我覺得在非常有可能出現的理由是 真實的目標 跟 AI 自己解讀出來的目標 這兩者中間的 Misalignment 我們說人類 有一個我們真正想要做的事情 真正想要 AI 達成的目標 叫做 $\hat{L}$ 但是我們是告訴 AI $H$ 這個東西 我們把我們的目標 描述成 $H$ 希望 AI 自己去解讀這個 $H$ 要怎麼 optimize 但是 AI 自己想出來的這個 loss 跟人類真正想要的 loss 它們中間可能會有 Misalignment 可能會有不一致的地方 而導致這個成長 最終是失控的 長出人類不想要的東西

</details>


### Slide 59 — 更新流程可能突破邊界（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=3840s))

![Slide 59 — 更新流程可能突破邊界（續）](slides/059_01-04-00.jpg)

當 Agent 能修改 Harness、更新器和目標追求方式，固定 procedure 不再保證受控。需要不可由被評系統單方面修改的外部約束、審計與停止機制。 本段重點：這又讓我想到 天擇的例子了 大家應該都很熟悉天擇 大家都很熟悉 適者生存 不適者淘汰等等 在天擇的整個理論裡面 有一個看起來 不符合天擇的現象 是孔雀的尾巴 大家知道說 雄孔雀有非常漂亮的尾巴 這些尾巴可以拿來吸引雌孔雀 但是它不利於生存 這些長尾巴會讓孔雀 更容易被天敵捕食 但是明明外界就是有天擇的壓力 照理說所有生物的演化 所有生物的形態都是由天擇所決定的 為什麼孔雀會產生這一種 不符合天擇設定的形態呢 這就是外在目標跟另外一個內在…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 這又讓我想到 天擇的例子了 大家應該都很熟悉天擇 大家都很熟悉 適者生存 不適者淘汰等等 在天擇的整個理論裡面 有一個看起來 不符合天擇的現象 是孔雀的尾巴 大家知道說 雄孔雀有非常漂亮的尾巴 這些尾巴可以拿來吸引雌孔雀 但是它不利於生存 這些長尾巴會讓孔雀 更容易被天敵捕食 但是明明外界就是有天擇的壓力 照理說所有生物的演化 所有生物的形態都是由天擇所決定的 為什麼孔雀會產生這一種 不符合天擇設定的形態呢 這就是外在目標跟另外一個內在目標 中間不一致所導致的差異 對天擇來說 他想要達成的目標 這邊的 $\hat{L}$ 是產生健康的子代 天擇的目標 是為了要產生下一代 下一代要再能夠產生下一代 天擇只在意這件事 天擇只篩選 能夠做到這些事的物種 他不在意其他事情 為什麼孔雀會長出長尾巴呢 是因為在這個天擇的過程中 產生了另外一個目標 而這個目標 一開始是符合天擇的 但後來逐漸的 跟天擇漸行漸遠 可能在某一個時候 在比較沒有那麼長的長尾巴 代表的是身體健康 假設在所有孔雀都是短尾巴的時候 有一隻稍微長一點 長一公分 代表它身體比較強壯 所以它能夠比較產生健康的子代 所以雌孔雀的基因裡面 就演化出了一個判斷 今天雄孔雀是不是健康的指標 就是尾巴的長度 這個指標 在尾巴長度低於某一個限度的時候 它是有用的指標 可以代表說 這個孔雀是不是健康的 但是尾巴長到一個地步以後 它其實就是不健康的 但是基因這個目標 沒有跟著改變 所以對雌孔雀來說 因為它的基因仍然覺得 越長尾巴的孔雀就是越健康的 所以它仍然選擇 長尾巴的孔雀跟它產生下一代 所以最後孔雀的尾巴就越來越長 雖然這並不是天擇所青睞的 最後可能就會導致孔雀這個族群 進入瀕臨滅絕的危機 這就是一種 Misalignment 像這種 Misalignment 在演化中比比皆是 所以今天機器 也有可能發生類似的事情嗎 我覺得如果在未來的幾年

</details>


### Slide 60 — 更新流程可能突破邊界（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=4002s))

![Slide 60 — 更新流程可能突破邊界（續）](slides/060_01-07-42.jpg)

當 Agent 能修改 Harness、更新器和目標追求方式，固定 procedure 不再保證受控。需要不可由被評系統單方面修改的外部約束、審計與停止機制。 本段重點：我們看到成長的失控 最有可能失控的來源 就是來自於外在目標 跟內在目標的不一致 其中我覺得 最具有代表性的科幻電影 就是機械公敵 機械公敵裡面的劇情 是這個樣子的


<details>
<summary><strong>Cleaned narration</strong></summary>

> 我們看到成長的失控 最有可能失控的來源 就是來自於外在目標 跟內在目標的不一致 其中我覺得 最具有代表性的科幻電影 就是機械公敵 機械公敵裡面的劇情 是這個樣子的

</details>


### Slide 61 — 更新流程可能突破邊界（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=4017s))

![Slide 61 — 更新流程可能突破邊界（續）](slides/061_01-07-57.jpg)

當 Agent 能修改 Harness、更新器和目標追求方式，固定 procedure 不再保證受控。需要不可由被評系統單方面修改的外部約束、審計與停止機制。 本段重點：在未來的世界 所有機器人都遵守三大法則 就是機器人不能傷害人類 機器人要服從人類的命令 機器人必須保護自己 有一個中央人工智慧系統 叫做 VIKI 它就根據這樣的規則 自己做了詮釋 它說人類會自我傷害 所以我們應該把所有的人類 通通抓起來 把他控制起來 由機器來保護人類 不要讓人類自由的行動 不要讓人類自由的愛幹嘛 就幹嘛 因為人類很容易作死 所以把所有人類關起來 這樣才能夠真正的保護人類 當然 VIKI 最後呢 就被人類打爆了 就是這…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 在未來的世界 所有機器人都遵守三大法則 就是機器人不能傷害人類 機器人要服從人類的命令 機器人必須保護自己 有一個中央人工智慧系統 叫做 VIKI 它就根據這樣的規則 自己做了詮釋 它說人類會自我傷害 所以我們應該把所有的人類 通通抓起來 把他控制起來 由機器來保護人類 不要讓人類自由的行動 不要讓人類自由的愛幹嘛 就幹嘛 因為人類很容易作死 所以把所有人類關起來 這樣才能夠真正的保護人類 當然 VIKI 最後呢 就被人類打爆了 就是這麼回事 所以在這個故事裡面 有一個 $\hat{L}$ 是在整個電影裡面 都沒有描述的 是比如說人類的福祉 就是人類想要的東西 比如人類就是不想被關起來 但是人類不明著說自己要什麼 人類也說不清楚自己要什麼 他們把自己要的東西 簡化成機器人三大法則 就是 $H$ 所以 VIKI 真正看到的東西 就是 $H$ 它從這個 $H$ 裡面 得到了它自己的 Loss 也就是 $L(H)$ 它這個 Loss 就是 應該要把所有人類控制起來 它去 minimize 這個 Loss 結果反而被人類打爆了 我覺得如果 VIKI 自己有想法的話 它也覺得說 哇靠你叫我做這個事情 我照著做了 我還被你打爆 實在是太慘了 它心中應該恨到不行 不過它只是人工智慧 所以可能沒有什麼感覺 不過它最後就是被人類打爆了 就是了 所以這個就是今天的結語

</details>


### Slide 62 — 更新流程可能突破邊界（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=4101s))

![Slide 62 — 更新流程可能突破邊界（續）](slides/062_01-08-21.jpg)

當 Agent 能修改 Harness、更新器和目標追求方式，固定 procedure 不再保證受控。需要不可由被評系統單方面修改的外部約束、審計與停止機制。 本段重點：重點是，我們今天看到人工智慧能夠成長


<details>
<summary><strong>Cleaned narration</strong></summary>

> 重點是，我們今天看到人工智慧能夠成長

</details>


### Slide 63 — 更新流程可能突破邊界（續） ([Video](https://www.youtube.com/watch?v=cQLKVzbwN7I&t=4104s))

![Slide 63 — 更新流程可能突破邊界（續）](slides/063_01-08-24.jpg)

當 Agent 能修改 Harness、更新器和目標追求方式，固定 procedure 不再保證受控。需要不可由被評系統單方面修改的外部約束、審計與停止機制。 本段重點：我們也看到這些成長的模組 也可以成長 所以可以雙重成長 而人類可能可以只透過提供一個內在動機 這個內在動機可能跟任何真實的目標都沒有關係 它就是一個非常簡單的目標 但是就讓這整套的演化持續進行下去 但是如果只有提供一個 非常簡單的目標 我們可能最後會看到 Misalignment 看到演化的失控 所以在這過程中 可能需要人類持續的 monitor 人類持續 monitor 這一些 AI 的成長 才能避免 AI 最後成長成 我們不要的樣子…


<details>
<summary><strong>Cleaned narration</strong></summary>

> 我們也看到這些成長的模組 也可以成長 所以可以雙重成長 而人類可能可以只透過提供一個內在動機 這個內在動機可能跟任何真實的目標都沒有關係 它就是一個非常簡單的目標 但是就讓這整套的演化持續進行下去 但是如果只有提供一個 非常簡單的目標 我們可能最後會看到 Misalignment 看到演化的失控 所以在這過程中 可能需要人類持續的 monitor 人類持續 monitor 這一些 AI 的成長 才能避免 AI 最後成長成 我們不要的樣子 這個就是今天這一堂課的結語

</details>


## 核心結論

- 單次自我修正不等於持久自我成長；關鍵是能力是否被寫回模型或學習系統。
- Proxy reward、AI evaluator 與 entropy 可降低人類標註需求，但都可能偏離真實目標。
- 無人自訓能帶來有限進步，常受初始模型能力、訊號品質與飽和限制。
- AI 設計訓練演算法已顯示潛力，但尚未證明能遞迴產生超越自身的系統。

