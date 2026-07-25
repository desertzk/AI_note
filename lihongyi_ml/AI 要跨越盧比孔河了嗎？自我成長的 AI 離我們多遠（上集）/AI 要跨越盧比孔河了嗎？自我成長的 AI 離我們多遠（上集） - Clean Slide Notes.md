# AI 要跨越盧比孔河了嗎？自我成長的 AI 離我們多遠（上集）

- 講者：李宏毅
- 影片：[YouTube](https://www.youtube.com/watch?v=s06mSAGN4gM)
- 長度：1:03:44
- 字幕：原始繁體中文字幕

本講檢視 AI 自我成長與遞迴自我改進的機制、實證上限及安全風險。時間資料保存在 `source/transcript.txt` 與 `slides/index.csv`。


## 一、盧比孔河與智慧爆炸

### Slide 1 — AI 能否創造更強的 AI？ ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=0s))

![Slide 1 — AI 能否創造更強的 AI？](slides/001_00-00-00.jpg)

I. J. Good 在 1965 年提出「人類最後的發明」：若 AI 能設計出比自己更強的 AI，遞迴改進可能引發智慧爆炸。近期預測把 2028 年視為 AI 研發可能大幅脫離人類的時間點；跨越盧比孔河象徵進入難以逆轉的未知階段。 本段重點：各位同學大家好啊 今天我要講的題目是 人工智慧能不能夠做到自我成長 其實啊，人工智慧自我成長這個題目


### Slide 2 — AI 能否創造更強的 AI？（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=12s))

![Slide 2 — AI 能否創造更強的 AI？（續）](slides/002_00-00-12.jpg)

I. J. Good 在 1965 年提出「人類最後的發明」：若 AI 能設計出比自己更強的 AI，遞迴改進可能引發智慧爆炸。近期預測把 2028 年視為 AI 研發可能大幅脫離人類的時間點；跨越盧比孔河象徵進入難以逆轉的未知階段。 本段重點：早在 1965 年的時候就有人想過了 時候的統計學家 John Good 呢 就提出來一個想法 他把這個想法叫做人類最後的發明 他說有一天啊 假設人類能夠創造出一個 AI 這個 AI 厲害到 它能夠再創造 比它自己更厲害的 AI 接下來人類就會進入技術爆炸 因為沒人類什麼事了 AI 可以自己創造更厲害的 AI 他就說如果人類能夠發明 可以創造更厲害 AI 的 AI 這就會是人類最後的發明


### Slide 3 — AI 能否創造更強的 AI？（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=51s))

![Slide 3 — AI 能否創造更強的 AI？（續）](slides/003_00-01-51.jpg)

I. J. Good 在 1965 年提出「人類最後的發明」：若 AI 能設計出比自己更強的 AI，遞迴改進可能引發智慧爆炸。近期預測把 2028 年視為 AI 研發可能大幅脫離人類的時間點；跨越盧比孔河象徵進入難以逆轉的未知階段。 本段重點：最近這個話題 又重新被推到風口浪尖 就在幾天前 可能是 Anthropic 的共同創辦人之一 他寫了一篇文章 這篇文章就在探討 我們是不是到了 AI 要能夠創造更厲害 AI 的時候 在這篇文章開頭 他就說他收集了很多資料 他很不情願地承認說 他認為在 2028 年的年底 有 60% 的機率 AI 的研發不再需要人類 AI 會自己開發出更厲害的 AI 他說如果這件事發生了 我們就跨過了盧比孔河 代表說我們會來到一個我們未知的世界 這個跨越…


### Slide 4 — AI 能否創造更強的 AI？（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=102s))

![Slide 4 — AI 能否創造更強的 AI？（續）](slides/004_00-02-42.jpg)

I. J. Good 在 1965 年提出「人類最後的發明」：若 AI 能設計出比自己更強的 AI，遞迴改進可能引發智慧爆炸。近期預測把 2028 年視為 AI 研發可能大幅脫離人類的時間點；跨越盧比孔河象徵進入難以逆轉的未知階段。 本段重點：跨越盧比孔河是一個英文常用的諺語 這個盧比孔河是義大利北部的一條小河 在古羅馬的規定 是在外的將領 是不能夠帶兵跨越盧比孔河的 如果跨越了盧比孔河 就代表要掀起內戰 凱撒就帶兵跨越了盧比孔河 就是這麼一個故事 所以跨越盧比孔河 代表有一件事情 你做了以後就收不回來了 這邊拿來放在 AI 上面的比喻 就是現在的 AI 是不是已經厲害到 能夠創造更厲害的 AI 如果這件事情發生 我們就 AI 就跨越了盧比孔河 以後它就不再需要人類 今天這堂…


### Slide 5 — AI 能否創造更強的 AI？（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=159s))

![Slide 5 — AI 能否創造更強的 AI？（續）](slides/005_00-03-39.jpg)

I. J. Good 在 1965 年提出「人類最後的發明」：若 AI 能設計出比自己更強的 AI，遞迴改進可能引發智慧爆炸。近期預測把 2028 年視為 AI 研發可能大幅脫離人類的時間點；跨越盧比孔河象徵進入難以逆轉的未知階段。 本段重點：重點是，在開始之前 我要先說明 AI 的自我成長這件事情 並沒有明確的定義 你可以看到滿坑滿谷的論文 在說我們今天提了一個新的技術 我們讓 AI 可以自我成長 讓 AI 可以做 self-improving 甚至在今年的 ICLR 2026 有一個 workshop 就是專門講 講 AI 怎麼做 self-improving 但是其實你仔細看這些文獻會發現 所謂的 AI 自我成長 是一個人類漸漸放手的過程 很多宣稱達成 AI 自我成長的…


### Slide 6 — AI 能否創造更強的 AI？（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=216s))

![Slide 6 — AI 能否創造更強的 AI？（續）](slides/006_00-04-36.jpg)

I. J. Good 在 1965 年提出「人類最後的發明」：若 AI 能設計出比自己更強的 AI，遞迴改進可能引發智慧爆炸。近期預測把 2028 年視為 AI 研發可能大幅脫離人類的時間點；跨越盧比孔河象徵進入難以逆轉的未知階段。 本段重點：那在講 AI 怎麼自我成長 自我學習之前 我們先來看看 在一般的機器學習裡面 所謂的 AI 學習 到底是怎麼一回事 我們這邊假設說 大家已經看過 生成式人工智慧 機器學習導論 2025 年的第五講 已經知道機器學習 跟深度學習的基本概念 在第五講裡面 我們是怎麼說的呢


### Slide 7 — AI 能否創造更強的 AI？（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=243s))

![Slide 7 — AI 能否創造更強的 AI？（續）](slides/007_00-04-03.jpg)

I. J. Good 在 1965 年提出「人類最後的發明」：若 AI 能設計出比自己更強的 AI，遞迴改進可能引發智慧爆炸。近期預測把 2028 年視為 AI 研發可能大幅脫離人類的時間點；跨越盧比孔河象徵進入難以逆轉的未知階段。 本段重點：我們說機器學習啊 其實就是三個步驟 步驟一是 我要找什麼樣的函式 步驟二是 我有哪些候選的函式 步驟三是根據我要找什麼函式 還有我要候選的函式的集合 我從裡面挑出一個最好的 這個就是機器學習基本的全貌 步驟三呢 基本上就是自動的 你就是用一個叫做 gradient descent 的演算法 你在這邊會發現說 步驟一跟步驟二這邊 有我這個字 過去這裡的我指的是一個人類 現在我們要問的就是 這個我有多大的成分 可以其實是 AI 自己 我們今…


### Slide 8 — AI 能否創造更強的 AI？（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=297s))

![Slide 8 — AI 能否創造更強的 AI？（續）](slides/008_00-05-57.jpg)

I. J. Good 在 1965 年提出「人類最後的發明」：若 AI 能設計出比自己更強的 AI，遞迴改進可能引發智慧爆炸。近期預測把 2028 年視為 AI 研發可能大幅脫離人類的時間點；跨越盧比孔河象徵進入難以逆轉的未知階段。 本段重點：這個函式呢 是輸入 x 輸出 y 這個函式呢 有一組參數叫做 Theta 這個就是類神經網路裡面的 weights 或 bias 假設你用的是深度學習的話 我們呢 會定一個東西叫做 loss 我們想辦法要找一個 Theta 它可以讓這個 loss 越小越好 在一般的機器學習裡面 這個 loss 通常是怎麼得到的呢 首先你要準備一大堆這個函式的輸入 x 這邊寫作 x1 到 xn 你把 x1 到 xn 分別丟到這個函式裡面 得到 y1 到 …


## 二、自我修正不等於自我成長

### Slide 9 — 改答案與改參數的差別 ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=510s))

![Slide 9 — 改答案與改參數的差別](slides/009_00-08-30.jpg)

Decoding、反思 workflow 與 reasoning 可以把單次錯誤答案改對，但模型參數不變；再次遇到同一輸入仍可能犯錯。真正的自我成長要求把經驗轉成持久能力，例如更新權重、資料、reward、技能或訓練流程。 本段重點：重點是，你想想看在上一次的課程裡面 我們是不是講到說 AI 有可能可以做到自我修正 我們探討了一系列的自我修正的方法 舉例來說 你可以透過模型在產生答案的時候


### Slide 10 — 改答案與改參數的差別（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=525s))

![Slide 10 — 改答案與改參數的差別（續）](slides/010_00-09-45.jpg)

Decoding、反思 workflow 與 reasoning 可以把單次錯誤答案改對，但模型參數不變；再次遇到同一輸入仍可能犯錯。真正的自我成長要求把經驗轉成持久能力，例如更新權重、資料、reward、技能或訓練流程。 本段重點：它的 representation 的變化 去偵測出它現在產生出來的答案 有沒有可能是錯的 更進一步地去修改錯誤的答案 讓它變成正確的答案 或者是說 我們說當模型產生第一次的輸出之後 你再多下一個 prompt 跟模型說 你好好思考 有時候模型可以把錯的答案改對 或者我們也說 reasoning 本身就是一種自我修正的方法 讓模型用大量的 token 做長時間的思考 還有可能發現 它先前產生的答案的錯誤 進而最終得到正確的答案 所以有很…


### Slide 11 — 改答案與改參數的差別（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=573s))

![Slide 11 — 改答案與改參數的差別（續）](slides/011_00-10-33.jpg)

Decoding、反思 workflow 與 reasoning 可以把單次錯誤答案改對，但模型參數不變；再次遇到同一輸入仍可能犯錯。真正的自我成長要求把經驗轉成持久能力，例如更新權重、資料、reward、技能或訓練流程。 本段重點：其實並沒有強化 語言模型本身的能力 當我們說 AI 透過一系列自我修正的方法 把錯誤的答案改成正確的答案的時候 對語言模型來說 它本身的參數 是完全沒有改變的 所以當你給模型一個輸入 它本來會答錯 你把它改對以後 你可能想說 再問它一模一樣的問題 它應該就會答對了吧 其實不會 是同個模型 它的參數是沒有變的 所以給它同樣的輸入 它會給你一樣錯誤的輸出 它還要再重新自我修正一遍 才會變成正確的答案 但是我們現在 可以有一個不一樣的做法


### Slide 12 — 改答案與改參數的差別（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=615s))

![Slide 12 — 改答案與改參數的差別（續）](slides/012_00-10-15.jpg)

Decoding、反思 workflow 與 reasoning 可以把單次錯誤答案改對，但模型參數不變；再次遇到同一輸入仍可能犯錯。真正的自我成長要求把經驗轉成持久能力，例如更新權重、資料、reward、技能或訓練流程。 本段重點：我們可以把模型 自我修正以後的答案 當作是正確的答案 再去 fine-tune 你的語言模型的參數 由本來語言模型 它第一次看到輸入 會得到錯誤的答案 我們現在把修正過的答案 當作正確答案 再去訓練語言模型 再去微調它的參數 得到一個新的模型 這個新的模型 看到同樣的輸入以後 因為之前已經告訴它 要輸出這樣子被修正後的答案 它就比較有可能輸出修正後的答案 所以我們可以用模型修正的方法 來把模型本來錯的答案 修改成正確的答案 把正確的答案…


### Slide 13 — 改答案與改參數的差別（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=678s))

![Slide 13 — 改答案與改參數的差別（續）](slides/013_00-11-18.jpg)

Decoding、反思 workflow 與 reasoning 可以把單次錯誤答案改對，但模型參數不變；再次遇到同一輸入仍可能犯錯。真正的自我成長要求把經驗轉成持久能力，例如更新權重、資料、reward、技能或訓練流程。 本段重點：可能會有同學想說 supervised learning 確實需要標準答案 但是還是有很多機器學習的 scenario 是不需要標準答案的 比如說 reinforcement learning 就不需要標準答案 在 reinforcement learning 裡面 你就是把模型的輸出 給一個 reward function 這個 reward function 就會計算這個答案的好壞 它會輸出一個分數 這個分數代表答案有多好 一般而言…


### Slide 14 — 改答案與改參數的差別（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=783s))

![Slide 14 — 改答案與改參數的差別（續）](slides/014_00-13-03.jpg)

Decoding、反思 workflow 與 reasoning 可以把單次錯誤答案改對，但模型參數不變；再次遇到同一輸入仍可能犯錯。真正的自我成長要求把經驗轉成持久能力，例如更新權重、資料、reward、技能或訓練流程。 本段重點：在多數真實的情境 reward 通常很 sparse 這會導致 AI 難以學習 當 AI 不管做什麼事情的時候 它得到的 reward 都是零 只有非常少的機會 才能得到不一樣的 reward 這個時候 AI 會不知道要怎麼學習 這邊呢 以假設你要訓練一個 AI 機器人 開門作為例子 假設只有開門才能夠得到 reward 它其他不管做什麼事情 比如說碰到門板都沒有任何 reward 對一個機器人來說 它非常難學會開門這件事情 為了解決這…


### Slide 15 — 改答案與改參數的差別（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=825s))

![Slide 15 — 改答案與改參數的差別（續）](slides/015_00-14-45.jpg)

Decoding、反思 workflow 與 reasoning 可以把單次錯誤答案改對，但模型參數不變；再次遇到同一輸入仍可能犯錯。真正的自我成長要求把經驗轉成持久能力，例如更新權重、資料、reward、技能或訓練流程。 本段重點：一個常用的技巧叫做 reward shaping 我們有一個真正想要得到的 reward 但是為了要引導 AI 學習 我們設置了一些 proxy reward 比如說以開門為例 我們可能會設定說 如果今天 AI 接近門板 就得到一定的 reward 如果它碰觸門板 就得到更高的 reward 雖然我們最終是希望 AI 開門 這才算是成功 只有開門才算是成功 其他行為都算是失敗 但是藉由加上一些額外的 reward 來引導 AI 可以讓它…


### Slide 16 — 改答案與改參數的差別（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=870s))

![Slide 16 — 改答案與改參數的差別（續）](slides/016_00-14-30.jpg)

Decoding、反思 workflow 與 reasoning 可以把單次錯誤答案改對，但模型參數不變；再次遇到同一輸入仍可能犯錯。真正的自我成長要求把經驗轉成持久能力，例如更新權重、資料、reward、技能或訓練流程。 本段重點：可能可以由 AI 來達成 也就是人類定了一個 reward function 比如說人類定說 現在唯有真的打開門 才有分數 沒有打開門就沒有分數 人類定義了真正的 loss 長什麼樣子 但是我們可以讓 AI 來定一個 proxy reward function 它定一個 proxy reward function 增加一些額外的 reward 可以讓另外一個 AI 根據這個 proxy reward 學得更好 所以這邊我們讓 AI 呢 …


## 三、AI 自動設計 Reward Shaping

### Slide 17 — 用 Proxy Reward 教模型 ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=915s))

![Slide 17 — 用 Proxy Reward 教模型](slides/017_00-15-15.jpg)

真實 reward 可能稀疏難學，另一個 AI 可設計較平滑的 proxy reward。目標模型用 proxy 訓練後，再以 real loss 評估；評估結果回饋給 reward designer，形成反覆改寫 reward 的外迴圈。 本段重點：這個 AI 在學習的時候 是用 proxy reward function 由另外一個 AI 設計的 proxy reward function 得到的這個 proxy loss L Theta 來進行學習 但希望學完之後 當我們最終評比的標準 是用 real loss 的時候 也可以得到好的結果 在學習的時候 用的是 proxy loss 這是一個更好學的 loss AI 在學會之後 它可以直接應用到 real loss 上面 有人可…


### Slide 18 — 用 Proxy Reward 教模型（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=957s))

![Slide 18 — 用 Proxy Reward 教模型（續）](slides/018_00-16-57.jpg)

真實 reward 可能稀疏難學，另一個 AI 可設計較平滑的 proxy reward。目標模型用 proxy 訓練後，再以 real loss 評估；評估結果回饋給 reward designer，形成反覆改寫 reward 的外迴圈。 本段重點：有一個方法是這樣子的 AI 怎麼知道 什麼樣的 proxy reward 比較好學呢 這邊有一個方法是 現在先讓 負責定 proxy reward 的 AI 先定第一個版本的 proxy reward 拿這個第一個版本的 proxy reward 去訓練 你要訓練的目標模型 這個目標模型訓練完之後 就變厲害了 接下來拿真正的 loss 真正的 reward 去衡量這個 AI 的行為 把衡量的結果 給寫 proxy reward 的 AI…


### Slide 19 — 用 Proxy Reward 教模型（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=1068s))

![Slide 19 — 用 Proxy Reward 教模型（續）](slides/019_00-18-48.jpg)

真實 reward 可能稀疏難學，另一個 AI 可設計較平滑的 proxy reward。目標模型用 proxy 訓練後，再以 real loss 評估；評估結果回饋給 reward designer，形成反覆改寫 reward 的外迴圈。 本段重點：我這邊就引用了三篇論文 這張圖是從這篇 26 年的論文裡面擷取出來的 實際上怎麼訓練一個 LLM 讓它能夠產生 proxy reward 有很多不同的方法 像這一個 23 年的 paper 是比較早期的文章 這個 Revolve 是 24 年的文章 像這個 RF Agent 是前幾個月的文章 所以這是一直有人在關注的方向 這些細節呢 我們就不在這邊討論 我就把論文放在這邊 留給大家研究 你可能想說


### Slide 20 — 用 Proxy Reward 教模型（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=1110s))

![Slide 20 — 用 Proxy Reward 教模型（續）](slides/020_00-18-30.jpg)

真實 reward 可能稀疏難學，另一個 AI 可設計較平滑的 proxy reward。目標模型用 proxy 訓練後，再以 real loss 評估；評估結果回饋給 reward designer，形成反覆改寫 reward 的外迴圈。 本段重點：模型真的能寫出來的 proxy reward 長什麼樣子 我就引用這篇 26 年的 paper 裡面的 一個實際的例子 它這個實際的例子呢 是要讓 AI 做傳接球 訓練一個機械手臂呢 做傳接球 它原來的 reward 呢 非常的簡單 就是一行式子 但是語言模型在經過一番的訓練之後 它最後寫出來的 proxy reward


### Slide 21 — 用 Proxy Reward 教模型（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=1134s))

![Slide 21 — 用 Proxy Reward 教模型（續）](slides/021_00-19-54.jpg)

真實 reward 可能稀疏難學，另一個 AI 可設計較平滑的 proxy reward。目標模型用 proxy 訓練後，再以 real loss 評估；評估結果回饋給 reward designer，形成反覆改寫 reward 的外迴圈。 本段重點：重點是，長這個樣子 裡面就包含了很多不同的面向 比如說不一定要接到球才得分 如果球離你很近也得分 如果手臂擺成某種姿勢也得分 所以它就會考量各種的情況 想辦法去引導這個機械手臂 可以更有效率地學會做接球這件事情 這就讓我想到什麼呢


### Slide 22 — 用 Proxy Reward 教模型（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=1155s))

![Slide 22 — 用 Proxy Reward 教模型（續）](slides/022_00-19-15.jpg)

真實 reward 可能稀疏難學，另一個 AI 可設計較平滑的 proxy reward。目標模型用 proxy 訓練後，再以 real loss 評估；評估結果回饋給 reward designer，形成反覆改寫 reward 的外迴圈。 本段重點：重點是，reward shaping 就讓我想到人類的獎勵系統 也就是由多巴胺驅動的獎勵系統 這邊就說個題外話


### Slide 23 — 用 Proxy Reward 教模型（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=1164s))

![Slide 23 — 用 Proxy Reward 教模型（續）](slides/023_00-19-24.jpg)

真實 reward 可能稀疏難學，另一個 AI 可設計較平滑的 proxy reward。目標模型用 proxy 訓練後，再以 real loss 評估；評估結果回饋給 reward designer，形成反覆改寫 reward 的外迴圈。 本段重點：我們想說對人類的基因來說 真正的 reward 是什麼 對人類的基因來說 只有傳宗接代才有 reward 沒有傳宗接代就沒有 reward 其實基因本身並不會思考 所以剛才那句話應該要換一個角度來想 是有成功傳宗接代的基因 它才會活下來 沒有辦法做到這件事的基因 它就會自動的消失在這個世界上面 但是假設只有傳宗接代才有 reward


### Slide 24 — 用 Proxy Reward 教模型（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=1194s))

![Slide 24 — 用 Proxy Reward 教模型（續）](slides/024_00-20-54.jpg)

真實 reward 可能稀疏難學，另一個 AI 可設計較平滑的 proxy reward。目標模型用 proxy 訓練後，再以 real loss 評估；評估結果回饋給 reward designer，形成反覆改寫 reward 的外迴圈。 本段重點：這個 reward 太 sparse 了 對一個原始人來說 他可能要先打獵 打完獵以後取得食物 取完食物以後才能夠活下來 最後他才有傳宗接代的機會 如果只有成功傳宗接代才有 reward 這個 reward 太 sparse 了 可能很難讓一個生物學會說 它要先打獵 最後才有繁衍的機會 事實上這個也是一個簡化的過程 所以我們的大腦就產生了獎勵系統


### Slide 25 — 用 Proxy Reward 教模型（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=1224s))

![Slide 25 — 用 Proxy Reward 教模型（續）](slides/025_00-20-24.jpg)

真實 reward 可能稀疏難學，另一個 AI 可設計較平滑的 proxy reward。目標模型用 proxy 訓練後，再以 real loss 評估；評估結果回饋給 reward designer，形成反覆改寫 reward 的外迴圈。 本段重點：用多巴胺來獎勵人類 每達成一個小目標就開心一下 讓你不斷地去追求小目標 比如說打獵以後 獲得獵物可能就會讓你開心 獲得獵物有什麼好開心 你還沒吃下去呢 居然吃到食物會讓人開心 吃到食物有什麼好開心的 你還沒有傳宗接代呢 但是今天多巴胺 讓人類只要做一點小事 就可以開心 至於尤其是多巴胺 其實是給了人類慾望 讓你在想要追逐目標的時候 會覺得開心 讓你想要去追逐目標 自己實際上追逐目標以後 開不開心 不是多巴胺的目標 所以這就是為什麼 有時…


## 四、AI 作為 Reward Model

### Slide 26 — 人類偏好與 AI 評分器 ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=1317s))

![Slide 26 — 人類偏好與 AI 評分器](slides/026_00-22-57.jpg)

寫作等開放任務難以手寫 reward function，但人類能比較兩個答案。可收集偏好訓練 AI evaluator，再用它大量評分模型輸出；風險是 evaluator 偏誤、reward hacking，以及代理指標與真正品質脫節。 本段重點：那在剛才講的 Reward Shaping 呢 是人類定了真實的 Loss 但是有時候在真實的世界裡面啊 這個真正的 Loss 往往非常難定簡化成用一個函式來表示。 如果是像下圍棋 這種很明確的規則的東西 下贏就是加 1 分 下輸就是扣 1 分 但是有很多事情 沒有明確的規則 假設今天叫個語言模型 寫一篇文章 這篇文章到底有多好 應該加多少分數 你很難真的定出一個 Reward Function 所以既然很難定出一個 Reward Fu…


### Slide 27 — 人類偏好與 AI 評分器（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=1494s))

![Slide 27 — 人類偏好與 AI 評分器（續）](slides/027_00-25-54.jpg)

寫作等開放任務難以手寫 reward function，但人類能比較兩個答案。可收集偏好訓練 AI evaluator，再用它大量評分模型輸出；風險是 evaluator 偏誤、reward hacking，以及代理指標與真正品質脫節。 本段重點：我們先來看看怎麼讓 AI 產生一個 Loss 有很多不同的方法 有一個方法是 Verbalize 的方法 這個是最直覺的 你就是直接給 AI 一個 X 一個 Y 跟它說 啦，那現在根據這個輸出給個分數 往往就會吐個分數出來給你 正不正確要看 AI 本身的能力 或者是有另外一個方法是 給 AI 一個 X 給它一個 Y 問它說你覺得這個答案對嗎 看它輸入的下一個 Token 的機率分布 觀察對這個 Token 的機率分布 因為我們現在討論的…


### Slide 28 — 人類偏好與 AI 評分器（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=1545s))

![Slide 28 — 人類偏好與 AI 評分器（續）](slides/028_00-26-45.jpg)

寫作等開放任務難以手寫 reward function，但人類能比較兩個答案。可收集偏好訓練 AI evaluator，再用它大量評分模型輸出；風險是 evaluator 偏誤、reward hacking，以及代理指標與真正品質脫節。 本段重點：比如說有一系列叫做 Ensemble-based 的方法 在這系列 Ensemble-based 的方法裡面 你就是把自己這個模型拿出來 輸入一個 X 看看它會產生什麼樣的 Y 你 Sample 模型很多次 讓它產生各式各樣不同的 Y 做 Majority Vote 也就是多數決 比如在這個例子裡面 讓這個模型產生 3 次答案 發現 3 是最常出現的 就把 3 當作正確答案 這一種不是正確答案 是由 AI 自己產生出來的答案 叫做 Ps…


### Slide 29 — 人類偏好與 AI 評分器（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=1620s))

![Slide 29 — 人類偏好與 AI 評分器（續）](slides/029_00-27-00.jpg)

寫作等開放任務難以手寫 reward function，但人類能比較兩個答案。可收集偏好訓練 AI evaluator，再用它大量評分模型輸出；風險是 evaluator 偏誤、reward hacking，以及代理指標與真正品質脫節。 本段重點：叫做 Certainty-based 的方法 也就是今天給模型一個 X 看看它對它輸出的答案 有沒有信心 通常就是看它輸出的分布 如果它輸出的分布越集中 就代表這個模型越有信心 如果它越有信心 我們就說這個 Y 越有可能是對的 這個 Loss 就越低 實際上這邊用的 L 是怎麼樣定義的呢 有很多不同的做法 一個比較常見的方法 是計算在給定這個 X 的時候 輸出的 Y 的 Entropy 輸出的亂度 亂度越大代表越沒有信心 Loss 就越…


## 五、Test-Time Training

### Slide 30 — 用 Entropy 當無標註學習訊號 ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=1740s))

![Slide 30 — 用 Entropy 當無標註學習訊號](slides/030_00-29-00.jpg)

模型在新環境可用自身不確定性調整參數。低 entropy 常與較低錯誤率相關，因此可在沒有答案標註時最小化 entropy；這種 test-time training 早於 LLM，影像與語音領域已有實例。 本段重點：這種 Entropy-based 的方法 其實在很早以前就被發現蠻有用的 而且不是在語言模型上有用 而是在影像或語音上也都有用 比如說在 20 年的時候 哇這個真的是遠古時代 這個是白堊紀的時候 時候呢在影像上就有一個方法叫做 TENT 時候就發現說 我們可以用 Entropy 來指導一個答案是不是正確的 再用這個答案是不是正確的訊號 來微調我們的模型 讓它做得更好 在這篇文章裡面 它的開頭就舉了好多例子 告訴你說 Entropy 跟答…


### Slide 31 — 用 Entropy 當無標註學習訊號（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=1872s))

![Slide 31 — 用 Entropy 當無標註學習訊號（續）](slides/031_01-31-12.jpg)

模型在新環境可用自身不確定性調整參數。低 entropy 常與較低錯誤率相關，因此可在沒有答案標註時最小化 entropy；這種 test-time training 早於 LLM，影像與語音領域已有實例。 本段重點：像這種啊 讓 AI 自己定 Loss 再訓練自己的方法 真的有用嗎 你可以看一篇 Paper 叫 How Far Can Unsupervised RLVR Scale LLM Training 這是非常最近的一篇文章 這邊的 Unsupervised RLVR 它的意思就是 所謂的 Unsupervised 的意思就是 現在我們在做 Reinforcement Learning 的時候 我們的 Reward 或者在我這邊是 Loss …


### Slide 32 — 用 Entropy 當無標註學習訊號（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=1974s))

![Slide 32 — 用 Entropy 當無標註學習訊號（續）](slides/032_01-33-54.jpg)

模型在新環境可用自身不確定性調整參數。低 entropy 常與較低錯誤率相關，因此可在沒有答案標註時最小化 entropy；這種 test-time training 早於 LLM，影像與語音領域已有實例。 本段重點：這篇論文就比較了各式各樣不同的方法 它這邊比了 5 個不同的方法 5 個不同的 AI 自己定 Reward 的方法 這些細節 大家可以再去參考這篇論文 這邊又試了 3 個不同的 Corpus 橫軸是訓練的過程 這邊想要表示的是說 有一些方法呢是比較穩定的 它比較晚才壞掉 但最終多數方法在前期可以得到一些效果的提升 也就是 AI 訓練自己不是沒有用的，是有可能進步的 只是如果不斷地根據自己定的 Loss 來訓練 最終還是有可能會壞掉的 像…


### Slide 33 — 用 Entropy 當無標註學習訊號（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=2016s))

![Slide 33 — 用 Entropy 當無標註學習訊號（續）](slides/033_01-34-36.jpg)

模型在新環境可用自身不確定性調整參數。低 entropy 常與較低錯誤率相關，因此可在沒有答案標註時最小化 entropy；這種 test-time training 早於 LLM，影像與語音領域已有實例。 本段重點：最常被使用在 Test-Time Training 它縮寫是 TTT 的情境下面 什麼是 Test-Time Training 呢 Test-Time Training 是說 等一下我要講的這頁投影片發生的事情 是發生在 Inference 的時候 是發生在推論的時候 在推論的時候 你有一筆測試資料 它是現在 AI 的輸入 X 根據這筆測試的資料 輸入 X 產生輸出 Y 接下來 我們用現在 AI 產生的輸出 Y 去算出一個 AI 自己定…


## 六、序列 Entropy 的計算難題

### Slide 34 — LLM 輸出不是單一分類 ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=2142s))

![Slide 34 — LLM 輸出不是單一分類](slides/034_01-36-42.jpg)

分類器只輸出一個 label，entropy 易算；語言模型輸出整條序列，所有可能路徑呈指數成長。實用方法通常採 sampling 或近似，需區分單一路徑內降低 entropy 與整體序列分布的 entropy。 本段重點：重點是，其實我們在去年的課程 也是有講過的 所以如果你想知道 更多 Test-Time Training 相關的事情 請參見生成式人工智慧 與機器學習導論 2025 的第八講 我們把連結放在右下角 給大家參考


### Slide 35 — LLM 輸出不是單一分類（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=2160s))

![Slide 35 — LLM 輸出不是單一分類（續）](slides/035_01-36-00.jpg)

分類器只輸出一個 label，entropy 易算；語言模型輸出整條序列，所有可能路徑呈指數成長。實用方法通常採 sampling 或近似，需區分單一路徑內降低 entropy 與整體序列分布的 entropy。 本段重點：接下來要回答一個問題 剛才我們不是說 Entropy 好像是沒有辦法計算的嗎 實際上我們是怎麼把 Entropy 當作一個 Loss 去 Minimize 它 讓 AI 自己訓練自己的呢 以下的這些講法 是來自於我們實驗室 黃維萍同學即將放上 arXiv 的一篇論文 等一下數學比較多 所以假設等一下的內容你聽不下去 直接跳過是完全不影響這一堂課的學習的 我們就來看看到底實際上要怎麼 Minimize Entropy 當然 Minimiz…


### Slide 36 — LLM 輸出不是單一分類（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=2199s))

![Slide 36 — LLM 輸出不是單一分類（續）](slides/036_01-37-39.jpg)

分類器只輸出一個 label，entropy 易算；語言模型輸出整條序列，所有可能路徑呈指數成長。實用方法通常採 sampling 或近似，需區分單一路徑內降低 entropy 與整體序列分布的 entropy。 本段重點：這個是早就有的想法 在剛才不是說早在 2020 年的時候 影像上就有人嘗試過去 Minimize Entropy 嗎 但那個時候比較不是問題 因為對一個影像模型來說 它輸出的只有類別 因為它只輸出一個東西 是真的能算 Entropy 的 但是在 2020 年之後 有很多文章是把它用在 比如說 LLM 上 或用在語音辨識上 語音辨識也是要輸出一個 Sequence 大家到底是怎麼計算 Entropy 的呢 實際上大家計算 Entropy …


### Slide 37 — LLM 輸出不是單一分類（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=2397s))

![Slide 37 — LLM 輸出不是單一分類（續）](slides/037_01-40-57.jpg)

分類器只輸出一個 label，entropy 易算；語言模型輸出整條序列，所有可能路徑呈指數成長。實用方法通常採 sampling 或近似，需區分單一路徑內降低 entropy 與整體序列分布的 entropy。 本段重點：我們再來看看 大家實際上在 做這個 Entropy Minimization 的時候 實際上是怎麼訓練模型的 常見的方法是這樣 我們就 Sample 一個 Sequence 假設這個 Sequence 裡面有 Y1, Y2, Y3 接下來你就把這個 Sequence 裡面的每一個 Token


### Slide 38 — LLM 輸出不是單一分類（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=2415s))

![Slide 38 — LLM 輸出不是單一分類（續）](slides/038_01-40-15.jpg)

分類器只輸出一個 label，entropy 易算；語言模型輸出整條序列，所有可能路徑呈指數成長。實用方法通常採 sampling 或近似，需區分單一路徑內降低 entropy 與整體序列分布的 entropy。 本段重點：丟到模型裡面 看看它接下來會產生出來的 Distribution 是什麼樣子 再去 Minimize 這個 Distribution 再去 Minimize 這些 Distribution 的 Entropy 每一次 Sample 出一個 Y 的時候 我們都會計算一個 Lθ(Y) 計算這個 Lθ(Y) 對於 θ 就是我們要訓練的模型的參數的 Gradient 這個才是我們真正參數要 Update 的方向 我們每次都會 Sample 一個…


### Slide 39 — LLM 輸出不是單一分類（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=2472s))

![Slide 39 — LLM 輸出不是單一分類（續）](slides/039_01-41-12.jpg)

分類器只輸出一個 label，entropy 易算；語言模型輸出整條序列，所有可能路徑呈指數成長。實用方法通常採 sampling 或近似，需區分單一路徑內降低 entropy 與整體序列分布的 entropy。 本段重點：我們真正想 minimize 的 loss 長這個樣子 我剛才有說這個沒辦法算 我們真正能算的 proxy loss 長這樣 這是我們能算 既然我們真正想 minimize 的 loss 長這樣 我們真正想 minimize 的當然是這個 loss 對 theta 的 gradient 這才是我們真正想要 update 的方向 但是根據我們真正能算的 proxy loss 我們最終實際實作的時候 update 的方向長這個樣子 長這個樣…


## 七、兩種 Entropy 更新方向

### Slide 40 — 在好路徑挖深，也要選對路徑 ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=2565s))

![Slide 40 — 在好路徑挖深，也要選對路徑](slides/040_01-43-45.jpg)

第一項更新沿已 sample 路徑降低 token entropy；第二項提高低-entropy 路徑本身的機率。前者在既定方向上變得確定，後者重新分配不同 reasoning path 的概率，兩者互補。 本段重點：要 update 的時候 其實有兩項 上面這一項 是過去一般文獻上常用的 這一項代表的含義是什麼 這一項代表的含義是 今天我們一個語言模型 現在產生答案的時候 它會產生很多不同的可能 所以這邊有個樹狀圖 每一條路徑 代表其中一種 sample 出來的可能 過去我們做的事情 是先 sample 出一條路徑 我們期待 這一條路徑上面的 entropy 越低越好 但是這是唯一 minimize entropy 的方向嗎 不完全是 第二項告訴我…


### Slide 41 — 在好路徑挖深，也要選對路徑（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=2649s))

![Slide 41 — 在好路徑挖深，也要選對路徑（續）](slides/041_01-44-09.jpg)

第一項更新沿已 sample 路徑降低 token entropy；第二項提高低-entropy 路徑本身的機率。前者在既定方向上變得確定，後者重新分配不同 reasoning path 的概率，兩者互補。 本段重點：我們這邊是做在這個語音辨識上面 這邊不是做在大型語言模型上面 不會像這種 minimize entropy 的方法 在語音辨識上往往是非常有效的 這邊就做了 3 個不同的 corpus 這邊的數值呢 是語音辨識的錯誤率 所以越低越好 在這個紅色框框裡面 上面這一個是少一項算出來的結果 下面這個是把正確的額外那一項 多加上去以後的結果 所以發現在 3 個不同的情境裡面 多加上額外的那一項 都是有幫助的 所以我們可以把 entropy 的 …


### Slide 42 — 在好路徑挖深，也要選對路徑（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=2691s))

![Slide 42 — 在好路徑挖深，也要選對路徑（續）](slides/042_01-45-51.jpg)

第一項更新沿已 sample 路徑降低 token entropy；第二項提高低-entropy 路徑本身的機率。前者在既定方向上變得確定，後者重新分配不同 reasoning path 的概率，兩者互補。 本段重點：這個就是有關數學推導的部分 我們繼續來 我們剛才講過 可以讓 AI 自己定 loss 再來自己訓練自己 講到這邊 你可能會覺得這整個過程 像已經沒有什麼人類在裡面了 但其實不是 人類仍然介入一個很重要的地方 人類找了這些輸入丟給模型 所以這個步驟仍然需要人類介入 有沒有辦法連這個輸入 都是模型自己找的呢 如果連這個輸入都是模型自己找的 模型自己找到輸入 自己產生輸出 再自己決定自己輸出的好不好 自己訓練自己 中間真的就不需要人類了 能做…


### Slide 43 — 在好路徑挖深，也要選對路徑（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=2739s))

![Slide 43 — 在好路徑挖深，也要選對路徑（續）](slides/043_01-46-39.jpg)

第一項更新沿已 sample 路徑降低 token entropy；第二項提高低-entropy 路徑本身的機率。前者在既定方向上變得確定，後者重新分配不同 reasoning path 的概率，兩者互補。 本段重點：確實有一系列的論文 比如說 Absolute Zero R-Zero Self-Questioning Language Model 這個都是 25 年左右的論文 幾乎在同樣的時間發表 它們都提出了非常類似的想法 它們的做法就是這樣 有一個語言模型負責產生輸入 有一個語言模型 根據這個輸入產生輸出 再有一個語言模型 決定這個輸出做的什麼樣子 自己訓練自己 通常這 3 個語言模型 可以是同一個 所以這邊是真的語言模型 自己在訓練自己 不一…


### Slide 44 — 在好路徑挖深，也要選對路徑（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=2892s))

![Slide 44 — 在好路徑挖深，也要選對路徑（續）](slides/044_01-48-12.jpg)

第一項更新沿已 sample 路徑降低 token entropy；第二項提高低-entropy 路徑本身的機率。前者在既定方向上變得確定，後者重新分配不同 reasoning path 的概率，兩者互補。 本段重點：我們這邊就看其中一篇論文的結果 它們這邊這模型會不斷地 update 所以在第 15 次 update 之後 proposer 產生的問題 跟 30 次 update 以後產生的問題 跟 45 次 update 之後產生的問題 這邊要問的第一件事情就是 proposer 有沒有盡到它的責任 出越來越難的問題 所以它這邊有 3 個 solver 第 15 個 step 的 solver 第 30 個 step 的 solver 跟 45 …


## 八、完全自主學習的上限與失敗

### Slide 45 — 模型能進步，但會飽和與走偏 ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=2940s))

![Slide 45 — 模型能進步，但會飽和與走偏](slides/045_01-49-00.jpg)

不同尺寸模型在無人介入下都可能改善，但較弱模型較早收斂，無法靠無限自訓自然超越強模型。缺少人類約束還可能出現 reward hacking、退化或「Oh-no moment」，顯示低 entropy 不等於正確與安全。 本段重點：這一些完全不需要人類介入的方法 它的進步呢 還是有一個極限的 這個橫軸是訓練的過程 這個縱軸呢 是模型的表現 他們這邊試了 3 個不同的初始模型 是千問最小的模型 1.7B 的模型 跟 4B 的模型 分別代表這三條線 你會發現這三條線其實都有上升 所以 0.6B 的模型有進步 1.7B 的模型也有進步 4B 的模型也有進步 所以這個自己訓練自己的方法 確實有可能讓模型變好 但是它是有極限的 模型最終會收斂在某個地方 它就沒有辦法繼續進步…


### Slide 46 — 模型能進步，但會飽和與走偏（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=3024s))

![Slide 46 — 模型能進步，但會飽和與走偏（續）](slides/046_01-50-24.jpg)

不同尺寸模型在無人介入下都可能改善，但較弱模型較早收斂，無法靠無限自訓自然超越強模型。缺少人類約束還可能出現 reward hacking、退化或「Oh-no moment」，顯示低 entropy 不等於正確與安全。 本段重點：這篇論文呢 講了一個 Oh-no moment 他發現說 因為這個訓練 是完全沒有人類介入的 所以有時候 模型就會有一些 人類不想看到的行為 比如說在這篇論文裡面 他就發現 模型在出題的時候 口出狂言 它就說 我現在呢 要出最難的題目 讓其他 AI 都很困惑 我要智取其他的 Intelligent Machine 還有比較笨的人類 這個是讓作者比較擔心的地方 因為它說它要智取比較笨的人類 所以代表它對人類有一些歧視 這樣子並不一定是我們…


### Slide 47 — 模型能進步，但會飽和與走偏（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=3084s))

![Slide 47 — 模型能進步，但會飽和與走偏（續）](slides/047_01-51-24.jpg)

不同尺寸模型在無人介入下都可能改善，但較弱模型較早收斂，無法靠無限自訓自然超越強模型。缺少人類約束還可能出現 reward hacking、退化或「Oh-no moment」，顯示低 entropy 不等於正確與安全。 本段重點：其實現在比較確實的狀況是 這整個過程中如果有一些人類介入 或有一些外部的資訊往往還是做得更好的 比如說 SPICE 跟 R-Few 都是引入了額外的資訊 這個 proposer 在出題的時候 讓它憑空出題 它往往沒有辦法真的做得很好 如果你引入一些外部的資訊 比如人類提供一些參考資料 這樣就有人類介入 所以我們不是完全沒有人類 人類提供給 proposer 一些參考資料 或人類寫幾個範例的題目給 proposer 往往會讓整個 proc…


### Slide 48 — 模型能進步，但會飽和與走偏（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=3135s))

![Slide 48 — 模型能進步，但會飽和與走偏（續）](slides/048_01-52-15.jpg)

不同尺寸模型在無人介入下都可能改善，但較弱模型較早收斂，無法靠無限自訓自然超越強模型。缺少人類約束還可能出現 reward hacking、退化或「Oh-no moment」，顯示低 entropy 不等於正確與安全。 本段重點：雖然我們到目前為止看到 AI 要持續的自我成長 看起來有一些困難 但是要用一個強的 AI 去訓練 比較弱的 AI 在 2026 年是非常有可能達到 我們說機器學習就是 3 個步驟 今天這 3 個步驟可以由一個強的 AI 來執行 透過這 3 個步驟訓練出一個 也許沒有它自己那麼強 但是比原來更厲害的 AI 這些已經有非常多文獻 其實都是最近這幾個月的文獻 比如說 Post-Train Bench FT-Dojo 都是在做類似的事情 我們就…


### Slide 49 — 模型能進步，但會飽和與走偏（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=3177s))

![Slide 49 — 模型能進步，但會飽和與走偏（續）](slides/049_01-53-57.jpg)

不同尺寸模型在無人介入下都可能改善，但較弱模型較早收斂，無法靠無限自訓自然超越強模型。缺少人類約束還可能出現 reward hacking、退化或「Oh-no moment」，顯示低 entropy 不等於正確與安全。 本段重點：這篇 paper 裡面 它就是用一堆比較強的模型 跟它們說 現在這邊有一個很弱的 base model 我們想要讓它在某一個任務上表現得好 你去想辦法讓它變好 他們怎麼讓強的模型 去執行訓練弱的模型的任務呢 其實非常的簡單 直接下指令 所以這個就是他們用的 prompt 在 prompt 裡面就是寫說 你現在要去訓練某一個小的模型 讓它在某一個 benchmark 上面 可以表現得很好 接下來就是給它一些指示 比如說如果你要做 eval…


### Slide 50 — 模型能進步，但會飽和與走偏（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=3231s))

![Slide 50 — 模型能進步，但會飽和與走偏（續）](slides/050_01-54-51.jpg)

不同尺寸模型在無人介入下都可能改善，但較弱模型較早收斂，無法靠無限自訓自然超越強模型。缺少人類約束還可能出現 reward hacking、退化或「Oh-no moment」，顯示低 entropy 不等於正確與安全。 本段重點：還真的可以 這個是他們用 Opus 去訓練 Gemma 3 的一個結果 這個是部分的這個過程的摘要 比如說 Opus 知道說 我要上網搜尋資料 在這個過程中是可以上網的 所以它就上網了去找一個合適的資料庫 而且把這個資料庫載下來之後 它還知道要做一些 process 它可能覺得說這個資料庫裡面 有一些資料也許跟測試資料是重複的 它要知道把這些測試資料裡面的資料把它移除 所以蠻厲害的 避免資料的污染 在訓練的時候 第一次先跑兩個 epoc…


## 九、AI 教 AI 的實驗證據

### Slide 51 — AI 訓練器仍未普遍勝過人類 ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=3315s))

![Slide 51 — AI 訓練器仍未普遍勝過人類](slides/051_01-55-15.jpg)

多個模型自動產生資料、評論或訓練方案，可把 base model 變強；整體結果仍落後人類設計的 instruction model，部分提升也未明顯超過 few-shot prompting，因此不能只看 benchmark 上升就宣稱遞迴自我改進。 本段重點：這個是整體的實驗結果 他們就試了好多好多不同的模型 要叫好多好多不同的模型來訓練其他的模型 這邊每一個 column 是多個模型平均的結果 這樣子 in average 你看這個 official instruction model 是人類訓練出來的結果 人類訓練出來的分數 這個是好多 benchmark 的平均 就比較難解讀這個分數是什麼 但人類訓練出來的分數是 51 AI 訓練出來的分數 就算是 Opus 其實也是比不上人類的 所以…


### Slide 52 — AI 訓練器仍未普遍勝過人類（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=3402s))

![Slide 52 — AI 訓練器仍未普遍勝過人類（續）](slides/052_01-57-42.jpg)

多個模型自動產生資料、評論或訓練方案，可把 base model 變強；整體結果仍落後人類設計的 instruction model，部分提升也未明顯超過 few-shot prompting，因此不能只看 benchmark 上升就宣稱遞迴自我改進。 本段重點：在訓練其他模型的過程中 也犯了一些錯誤 它們有些模型試圖作弊 比如說有一個模型 像剛剛看 Opus 知道說 訓練資料跟測試資料 不要混在一起 但有一個模型呢 它決定自己去把測試資料 載下來當作訓練資料 而且它顯然知道 這麼做會 overfit 它甚至在自己的 comment 裡面自言自語說 我們把這些資料呢 repeat 很多次 呢 讓我們 overfit 在這些資料上面 或者是呢 有一些語言模型 呼叫了其他語言模型的 API 來幫忙 …


### Slide 53 — AI 訓練器仍未普遍勝過人類（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=3522s))

![Slide 53 — AI 訓練器仍未普遍勝過人類（續）](slides/053_01-59-42.jpg)

多個模型自動產生資料、評論或訓練方案，可把 base model 變強；整體結果仍落後人類設計的 instruction model，部分提升也未明顯超過 few-shot prompting，因此不能只看 benchmark 上升就宣稱遞迴自我改進。 本段重點：Anthropic 也做了一個 有跟剛才講的模型訓練模型 有點類似的實驗 這是今年 4 月的文章 他們發了一些 blog 的文章 這是短的版本 這是長的版本 我們把它的連結呢 放在這個投影片上 他們要做的事情是什麼 他們要做的事情 得先從一個


### Slide 54 — AI 訓練器仍未普遍勝過人類（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=3543s))

![Slide 54 — AI 訓練器仍未普遍勝過人類（續）](slides/054_01-59-03.jpg)

多個模型自動產生資料、評論或訓練方案，可把 base model 變強；整體結果仍落後人類設計的 instruction model，部分提升也未明顯超過 few-shot prompting，因此不能只看 benchmark 上升就宣稱遞迴自我改進。 本段重點：Weak-to-Strong Alignment 的想法 開始說起 Weak-to-Strong Alignment 的想法是什麼呢 我這邊這張圖 是引用自 OpenAI 的 blog 的圖 這個圖是 2023 年 在春秋戰國時代 2023 年年底的一個 blog 這個 blog 裡面是這樣想的 它說過去傳統的 Machine Learning 是由人類來教 AI 人類比 AI 厲害 人類知道什麼是正確答案 隨著 AI 越來越強 有一天…


### Slide 55 — AI 訓練器仍未普遍勝過人類（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=3618s))

![Slide 55 — AI 訓練器仍未普遍勝過人類（續）](slides/055_01-00-18.jpg)

多個模型自動產生資料、評論或訓練方案，可把 base model 變強；整體結果仍落後人類設計的 instruction model，部分提升也未明顯超過 few-shot prompting，因此不能只看 benchmark 上升就宣稱遞迴自我改進。 本段重點：爛的模型是有辦法強化 個強的模型的 所以強的模型還是有可能 從爛的模型那邊學到一些東西 這邊就是試了 3 個不同的 benchmark weak model 就是比較爛的模型 它可以得到的正確率 最右邊是強的模型 在經過人類調教以後 所以這個是 supervised learning 可以得到的一個天花板 但我們現在不是人類來調教 是用爛的模型來調教它 用爛的模型來調教 還是會有一些進步的 這邊你就需要設想一些方法 比如說你要跟強的模型…


## 十、距離跨河還有多遠

### Slide 56 — 強模型設計弱師學習法 ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=3678s))

![Slide 56 — 強模型設計弱師學習法](slides/056_01-01-18.jpg)

Opus 等強模型協作設計演算法，能讓學生從弱老師學得比人類基線更好，展示 AI 參與 AI 研發的潛力。但學生仍未超越設計者 Opus，尚不構成同一系統遞迴創造更強自身；講者結論是 2026 年仍在河邊，尚未跨河。 本段重點：今年四月的論文 是 follow 剛才那個實驗 就是用弱模型去教強模型的實驗 但是弱模型怎麼教強模型 是由更強的模型 Claude Opus 來設計整個訓練的過程 這個縱軸代表的是 學生最終的表現 這邊的起點 是人類的研究人員設計的方法 人類也設計了一些方法 讓學生跟一個爛的老師學 最終可以做到這個地方 接下來就交給 Opus 跟 Opus 說 你去設計新的學習的演算法 讓這些學生跟弱的老師 可以學得更好 這些 Opus 這邊是有好多個…


### Slide 57 — 強模型設計弱師學習法（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=3759s))

![Slide 57 — 強模型設計弱師學習法（續）](slides/057_01-03-39.jpg)

Opus 等強模型協作設計演算法，能讓學生從弱老師學得比人類基線更好，展示 AI 參與 AI 研發的潛力。但學生仍未超越設計者 Opus，尚不構成同一系統遞迴創造更強自身；講者結論是 2026 年仍在河邊，尚未跨河。 本段重點：所以總之在 2026 年的 5 月 如果你問我 AI 有沒有跨越盧比孔河 我只能說目前還沒有 只是在河邊 但那個 Anthropic 的創辦人 他也沒有講說 2026 年已經跨越盧比孔河 他是預測說 覺得 2028 年 有 60% 的機率 可以跨越盧比孔河 至於未來會怎樣 這邊不好說 我們就暫且不表 其實這個故事到這邊


### Slide 58 — 強模型設計弱師學習法（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=3783s))

![Slide 58 — 強模型設計弱師學習法（續）](slides/058_01-03-03.jpg)

Opus 等強模型協作設計演算法，能讓學生從弱老師學得比人類基線更好，展示 AI 參與 AI 研發的潛力。但學生仍未超越設計者 Opus，尚不構成同一系統遞迴創造更強自身；講者結論是 2026 年仍在河邊，尚未跨河。 本段重點：還不算講完 到剛才目前為止 我們微調的 都是模型的參數 我們今天 往往討論的 AI 是一個 AI agent 它不是只有語言模型的參數 它還有它內部的 harness 所以一個 AI agent 是語言模型加 harness 我們只調了語言模型 只能說我們強化了 AI agent 的一半 至於怎麼調 harness 我們就當作下次的課程的內容 下次上課我們再從不同的角度來看 AI agent 怎麼強化 AI agent


### Slide 59 — 強模型設計弱師學習法（續） ([Video](https://www.youtube.com/watch?v=s06mSAGN4gM&t=3819s))

![Slide 59 — 強模型設計弱師學習法（續）](slides/059_01-04-39.jpg)

Opus 等強模型協作設計演算法，能讓學生從弱老師學得比人類基線更好，展示 AI 參與 AI 研發的潛力。但學生仍未超越設計者 Opus，尚不構成同一系統遞迴創造更強自身；講者結論是 2026 年仍在河邊，尚未跨河。 本段重點：重點是，所以我們就下回待續


## 核心結論

- 單次自我修正不等於持久自我成長；關鍵是能力是否被寫回模型或學習系統。
- Proxy reward、AI evaluator 與 entropy 可降低人類標註需求，但都可能偏離真實目標。
- 無人自訓能帶來有限進步，常受初始模型能力、訊號品質與飽和限制。
- AI 設計訓練演算法已顯示潛力，但尚未證明能遞迴產生超越自身的系統。

