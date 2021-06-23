# FinalProject

組裝BOE BOT car車，openmv TX/RX 接到D0/D1，Xbee TX/RX A1/A0

再將openmv.py放進openmv裡

最後將場地布置好

首先會先透過openmv 實作line detection 的功能，讓BOE BOT car 沿著線走，
這邊我是利用回歸直線的方法去算出我應該要如何走，透過openmv的照片我先設定好LAB色彩空間的Threshold，
讓我的回歸直線是完全的利用我所標示的線去算，然後再根據那條回歸線算出現在應該怎麼走。

第一個apriltag視為障礙物，我是利用apriltag做成仿ping的功能的，利用了三軸的量去推算詳細的距離，
然後加上判斷apriltag 的id 來決定這是第幾個障礙物。遇到第一個apriltag會左轉，這邊的左轉是我自己打的function，
會讓車子是用自轉的方式，所以轉動的過程，車子位置是不會移動的。

再來還會有一小段的line detection直到遇到第二個障礙物，
第二個apriltag也視為障礙物，當判斷夠近時會以自轉的方式右轉。

再來還會有一小段的line detection，當距離到openmv足夠偵測到第三個apriltag時，
這邊會利用apriltag來校正自己的位置，當校正成功時，BOE BOT car會藉由Xbee發出
"april tag calibrate success!"到電腦上，電腦再藉由screen印出來，然後校正成功之後，
會再以自轉的方式右轉一次，順著最後的藍線，再跑一次line detection。

