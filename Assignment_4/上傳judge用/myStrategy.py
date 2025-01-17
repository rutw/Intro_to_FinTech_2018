'''
Ｉｎｔｒｏｄｕｃｔｉｏｎ　ｔｏ　Ｆｉｎｔｅｃｈ
Ａｓｓｉｇｎｍｅｎｔ　４

ｂｙ　ＣｈｉｎｇＲｕｕ
２０１８．１０．３０

所使用的技術指標：ＭＡ（有不同計算方法的ＭＡ）和ＲＳＩ


執行買賣的概念　：和簡單的ＲＳＩ策略一樣的概念，
　　　　　　　　　在ＲＳＩ過高時（如高於７０，代表市場過熱，呈超買狀態）賣出，
　　　　　　　　　在ＲＳＩ過低時（如低於３０，代表市場過冷，呈超賣狀態）買入。

　　　　　　　　　不過因為單純的ＲＳＩ策略在進行買賣時會有一個盲點，
　　　　　　　　　它只單純把兩個數字（如上面的７０和３０）應用在整個市場的時間中，
　　　　　　　　　而沒有考慮到當今市場是熊市還是牛市，此時ＲＳＩ會有鈍化的現象。

　　　　　　　　　如果是牛市，那本來市場就會呈現熱絡狀態，ＲＳＩ的低點會比平常還高，
　　　　　　　　　如果我們還是設成跟熊市一樣，那在牛市時會找不到買點買入，
　　　　　　　　　因為可能都不會低到我們所設的值；
　　　　　　　　　而高點也是一樣，如果我們還是設成一樣熊市一樣，那我們會太早賣出而得不到更大的利潤。

　　　　　　　　　因此，在牛市時我們應該將我們所設的ＲＳＩ低值和高值向上調整。
　　　　　　　　　反之，在熊市時我們應該將我們所設的ＲＳＩ低值和高值向下調整。

　　　　　　　　　而我們簡單判斷當今市場是牛市或熊市的方法就是用長線ＭＡ和短線ＭＡ是否交叉，
　　　　　　　　　我們假設在買賣的當下，長線ＭＡ在短線ＭＡ之上，代表近期趨勢走勢低於長期趨勢，視為熊市，
　　　　　　　　　而若長線ＭＡ在短線ＭＡ之下，代表近期趨勢走勢高於長期趨勢，視為牛市。


策略所包含的參數：共九個
　　　　　　　　　１．ma_long_day：我們要參考的ＭＡ長期趨勢天數
　　　　　　　　　２．ma_short_day：我們要參考的ＭＡ短期趨勢天數
　　　　　　　　　３．rsi_day：我們要參考的ＲＳＩ天數

　　　　　　　　　４．ma_long_type：在計算長線ＭＡ時，我們採取的ＭＡ算法
　　　　　　　　　５．ma_short_type：在計算短線ＭＡ時，我們採取的ＭＡ算法
　　　　　　　　　其實這兩個應該算是內生，因為是ｔａｌｉｂ函式所用的方法
　　　　　　　　　在這裡０代表ＳＭＡ（簡單ＭＡ），１代表ＥＭＡ（指數ＭＡ），２代表ＷＭＡ（加權ＭＡ）
　　　　　　　　　　　　３代表ＤＥＭＡ（二重ＥＭＡ），４代表ＴＥＭＡ（三重ＥＭＡ）
　　　　　　　　　／／
　　　　　　　　　　　　　　　　　　EMA(n)=EMA[x(n)]
　　　　　　　　　　　　　　　　　　DEMA(n)=2EMA[x(n)]−EMA[EMA[x(n)]]
　　　　　　　　　　　　　　　　　　TEMA(n)=3EMA[x(n)]−3EMA[EMA[x(n)]]+EMA[EMA[EMA[x(n)]]]
　　　　　　　　　／／

　　　　　　　　　６．bull_rsi_high：牛市時ＲＳＩ高值，超過這個值就賣
　　　　　　　　　７．bull_rsi_low：牛市時ＲＳＩ低值，超過這個值就買

　　　　　　　　　８．bear_rsi_high：熊市時ＲＳＩ高值，超過這個值就賣
　　　　　　　　　９．bear_rsi_low：牛市時ＲＳＩ低值，超過這個值就買
　　　
　　　　　　
如何找出最適值　：理論上好像可以用ＤＰ去對九個參數求出最適值，我大概知道那個概念，但我不會寫ㄏㄏ
　　　　　　　　　有想過用硬爆的方式拉九層ｆｏｒ去找極值，但按了按計算機發現可能性好像有點多
　　　　　　　　　所以考慮用較少的範圍去跑ｆｏｒ迴圈（好啦我知道很低能但我就學不好ＤＰ啊ＱＱ）
　　　　　　　　　
　　　　　　　　　假設市場會對預期自我實現，那麼單一市場的走勢會和其他市場走勢接近，
　　　　　　　　　因此參考我對股市的理解對參數做調整

　　　　　　　　　ma_long_day：只考慮３０天以上６０天以下，太短就不較長期趨勢
　　　　　　　　　ma_short_day：考慮３到５天，太長就不較短期趨勢
　　　　　　　　　rsi_day：考慮３到７天，發明ＲＳＩ指標的人認為１４天剛好，但我長期的觀察認為太長的ＲＳＩ會失去敏銳度
　　　　　　　　　ma_long_type：只考慮ＤＥＭＡ和ＴＥＭＡ，因為經多次計算後會更ｍａｔｃｈ真實走勢
　　　　　　　　　ma_short_type：只考慮ＤＥＭＡ和ＴＥＭＡ，因為經多次計算後會更ｍａｔｃｈ真實走勢
　　　　　　　　　bull_rsi_high：假設牛市ＲＳＩ理想高值恆不會低於５０且不高於７０以上
　　　　　　　　　bull_rsi_low：假設牛市ＲＳＩ理想低值恆不會低於４０且不高於bull_rsi_high值
　　　　　　　　　bear_rsi_high：假設熊市ＲＳＩ理想高值恆不會低於４０且不高於７０以上
　　　　　　　　　bear_rsi_low：假設熊市ＲＳＩ理想低值恆不會低於３０且不高於bear_rsi_high


碎碎念　　　　　：考慮到我的腦袋跟參數限制，這邊只單純把市場拆分成牛和熊兩種，
　　　　　　　　　但或許可以再將牛或熊拆分成小牛市、大牛市、小熊市、大熊市等更細的拆分。

　　　　　　　　　此外，因為我們只看的到收盤價，所以這邊判定牛熊的指標是用單除的ＭＡ去判斷，
　　　　　　　　　但實務上應該也必須加入最高最低價去判斷，如引入ＤＭＩ判斷ＡＤＸ線、引入ＫＤ判斷超買超賣。
　　　　　　　　　除了最高最低價，在實務上也應考慮每日的成交量，
　　　　　　　　　否則上漲無量這種明顯是主力在出貨卻幫抬轎、利空時無量下殺卻傻傻憑指標去接盤嗎？

　　　　　　　　　如果要當沖或是玩短線，也應該讓策略在買入後，掛一個高於一點點買入價的賣單；
　　　　　　　　　在賣出時，也應該往下掛一個低於賣出價的買單，透過短線反彈積少成多。

　　　　　　　　　如果是風險驅避者，也應該讓策略在買入後，設置一個不低於買點的觸發價（判斷的支撐位），
　　　　　　　　　當價格向下突破觸發價時立刻掛出賣單，以避免被向下套牢。
　　　　　　　　　如當今買入價為１００元，判斷市場支撐位在９８元，同時將觸發價設於９８元，突破後立刻掛１０１元的賣單
　　　　　　　　　這樣一來，一但市場價格跌破判斷的支撐，雖然在短時間有可能小補回１００之上，但長期可能會向下走，
　　　　　　　　　而我們在１０１賣出可以有效避免要向下攤平的悲劇。
　　　　　　　　　反之亦然，一但市場突破觸發價（阻力位），判斷市場短期會有小反彈回阻力之下，但長期看漲，
　　　　　　　　　也應該在阻力位設置觸發價，一但突破觸發價馬上往下掛買單。

　　　　　　　　　最後，其實我是隨機漫步的信仰者，對於把技術指標動不動就要畫線、
　　　　　　　　　畫黃金分割線、用費柏那戚數列切割找規律、畫箱型線等抱持保留態度。
　　　　　　　　　對於什麼Ｍ頭、Ｗ底、左肩、右肩、頸線、長陰、長陽、Ｖ轉、Ｗ轉、島狀反轉、
　　　　　　　　　下影鎚子、旭日東昇、長紅吞噬、長紅貫穿、紅三兵、孤島晨星、母子脫困、
　　　　　　　　　上升三法、缺口脫困、抵擋五連陽、川上三鴉、上影吊首、屋雲罩頂、長黑吞噬、
　　　　　　　　　長黑貫穿、黑三兵、孤島夜星、母子棄守、下降三法、缺口棄守、高檔五連陰有的沒的的線形
　　　　　　　　　（我是覺得技術分析派能發明這些聽起來蠻二又羞恥的名詞也是蠻厲害的）
　　　　　　　　　我認為都是市場對於技術指標的自我實現和心理壓力所造成。

　　　　　　　　　技術指標做出的圖形會先在市場上自我實現，進而強化趨勢，
　　　　　　　　　一旦價格突破多數人認為的頸線開始接近阻力位，便開始吸引更多的買家想逢低買入，市場買單增加價格自然上升。
　　　　　　　　　接著超越一般人的預期，吸引更多買家進場畫圖分析，並對當下的線型做更高的預期，新的阻力位和支撐位就此生成，
　　　　　　　　　而這個更高的預期，也正是自我毀滅的開始。

　　　　　　　　　這也不是說我不相信技術指標，既然市場會回應技術指標的自我實現，那麼技術指標仍然有他的存在意義。
　　　　　　　　　在這次的作業中使用的參數是為了讓過去回測得到最大報酬，這是用已知的東西去做讓已知資料最大化利潤的過程，
　　　　　　　　　這是「讓過去資料生成最大利潤」的參數，而非「讓未來產生正利潤的參數」。
　　　　　　　　　事實上，我們要求的是穩定的正利潤，而非最大利潤。畢竟我們看不到未來，歷史也沒有如果，回測去後悔也沒有用。

　　　　　　　　　或許，在實務上，我不會採用這些很奇怪的數字，而會用代表週、月、季的整數更為保險且具代表性，
　　　　　　　　　畢竟所有的指標用的都過去的資料，皆是落後指標，都只能當參考而不是定理，
　　　　　　　　　我們只能在能控制的範圍裡去預測未來，想辦法讓我們獲利，而不是直接看到未來，讓我們獲利能最大化。
　　　　　　　　　
　　　　　　　　　總歸兩句，本多終勝、千線萬線還是比不上內線。
'''

def myStrategy(pastData, currPrice):
    # 已知 pastData 是一個 array ，裡面有到今天為止的所有價格，currPrice 是一個數，代表今天的價格。
    import numpy as np
    import talib

    comb = np.append(pastData, currPrice)   

    # set action as defalut
    action = 0
    
    # 這個是用來判定牛熊的指標
    bull_bear_indicator = 0
    # bear = 1 熊市時設為1
    # bull = -1 熊市時設為2
    # default = 0
   
    # set parameters
    ma_long_day = 56
    ma_short_day = 4
    rsi_day = 5

    ma_long_type = 4
    ma_short_type = 3
    
    bull_rsi_high = 65
    bull_rsi_low = 60
    bear_rsi_high = 50
    bear_rsi_low = 41
    
    # 當下的MA長線值
    ma_long  = (talib.MA(comb, timeperiod = ma_long_day, matype = ma_long_type))[-1]
    # 當下的MA短線值
    ma_short = (talib.MA(comb, timeperiod = ma_short_day, matype = ma_short_type))[-1]
    # 當下的RSI值
    rsi_current = (talib.RSI(comb, timeperiod = rsi_day))[-1]    

    # 檢查當下是牛市還是熊市
    if (ma_long > ma_short):
        bull_bear_indicator = 1
        # set as bear
        # 近期趨勢走勢低於長期趨勢，視為熊市
    elif (ma_long < ma_short):
        bull_bear_indicator = -1
        # set as bull
        # 近期趨勢走勢高於長期趨勢，視為牛市
    else:
        bull_bear_indicator = 0

    # 從RSI判斷買賣
    if (bull_bear_indicator == 1):
        # bear
        if (rsi_current >= bear_rsi_high):
            # sell
            action = -1
        elif (rsi_current <= bear_rsi_low):
            # buy
            action = 1
        else:
            # do nothing
            action = 0
    elif (bull_bear_indicator == -1):
        # bull
        if (rsi_current >= bull_rsi_high):
           # sell
            action = -1
        elif (rsi_current <= bull_rsi_low):
           # buy
            action = 1
        else:
            # do nothing
            action = 0
    
    return action
