# グラフ作成

import csv
import matplotlib.pyplot as plt

# ---------- CSVファイルからデータ読み込み ----------- #
# 時刻
t = []
# 出力の真値
y_true = [[], [], [], [], [], []]
# 出力の観測値
y = [[], [], [], [], [], []]
# オイラー角の真値
ypr = [[], [], []]
# オイラー角の推定値
ypr_hat = [[], [], []]
# 四元数以降の状態変数の真値
x = [[], [], [], [], [], [], [], [], [], []]
# 四元数以降の状態変数の推定値
xhat = [[], [], [], [], [], [], [], [], [], []]

# CSVからデータを読み出して配列に追加
with open('./result.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        nums = [float(v) for v in row]  # 文字列から浮動小数点数に変換

        # 時刻
        t.append(nums[0])
        # 出力
        for i in range(6):
            y_true[i].append(nums[i+1])  # 真値
            y[i].append(nums[i+7])       # 観測値
        # オイラー角
        for i in range(3):
            ypr[i].append(nums[i+13])
            ypr_hat[i].append(nums[i+16])
        # 状態変数
        for i in range(10):
            x[i].append(nums[i+19])     # 真値
            xhat[i].append(nums[i+29])  # 推定値


# ----------------- グラフ描画の準備 ------------------ #
# Figureを追加
fig1 = plt.figure(figsize = (13, 7))

ax1 = fig1.add_subplot(331, ylabel='X axis (Roll)', title='Euler angles [rad]')
ax2 = fig1.add_subplot(334, ylabel='Y axis (Pitch)')
ax3 = fig1.add_subplot(337, ylabel='Z axis (Yaw)', xlabel='time [s]')
ax4 = fig1.add_subplot(332, title='Bias of Angular velocity [rad/s]')
ax5 = fig1.add_subplot(335)
ax6 = fig1.add_subplot(338, xlabel='time [s]')
ax7 = fig1.add_subplot(333, title='Acceleration disturbance [m/s^2]')
ax8 = fig1.add_subplot(336)
ax9 = fig1.add_subplot(339, xlabel='time [s]')

ax1.plot(t, ypr[2],     label="True", color="black")
ax1.plot(t, ypr_hat[2], label="Estimated", color="red", linestyle = "--")
ax2.plot(t, ypr[1],     label="True", color="black")
ax2.plot(t, ypr_hat[1], label="Estimated", color="red", linestyle = "--")
ax3.plot(t, ypr[0],     label="True", color="black")
ax3.plot(t, ypr_hat[0], label="Estimated", color="red", linestyle = "--")
ax4.plot(t, x[4],    label="True", color="black")
ax4.plot(t, xhat[4], label="Estimated", color="red", linestyle = "--")
ax5.plot(t, x[5],    label="True", color="black")
ax5.plot(t, xhat[5], label="Estimated", color="red", linestyle = "--")
ax6.plot(t, x[6],    label="True", color="black")
ax6.plot(t, xhat[6], label="Estimated", color="red", linestyle = "--")
ax7.plot(t, x[7],    label="True", color="black")
ax7.plot(t, xhat[7], label="Estimated", color="red", linestyle = "--")
ax8.plot(t, x[8],    label="True", color="black")
ax8.plot(t, xhat[8], label="Estimated", color="red", linestyle = "--")
ax9.plot(t, x[9],    label="True", color="black")
ax9.plot(t, xhat[9], label="Estimated", color="red", linestyle = "--")
ax1.legend()
ax4.legend()
ax7.legend()

# 四元数だけ別ウィンドウで表示
fig2 = plt.figure(figsize = (7, 7))
ax1 = fig2.add_subplot(411, ylabel='q0', title='Quaternion')
ax2 = fig2.add_subplot(412, ylabel='q1')
ax3 = fig2.add_subplot(413, ylabel='q2')
ax4 = fig2.add_subplot(414, xlabel='time [s]', ylabel='q3')
ax1.plot(t, x[0],    label="True", color="black")
ax1.plot(t, xhat[0], label="Estimated", color="red", linestyle = "--")
ax2.plot(t, x[1],    label="True", color="black")
ax2.plot(t, xhat[1], label="Estimated", color="red", linestyle = "--")
ax3.plot(t, x[2],    label="True", color="black")
ax3.plot(t, xhat[2], label="Estimated", color="red", linestyle = "--")
ax4.plot(t, x[3],    label="True", color="black")
ax4.plot(t, xhat[3], label="Estimated", color="red", linestyle = "--")
ax1.legend()
ax2.legend()
ax3.legend()
ax4.legend()

plt.show()