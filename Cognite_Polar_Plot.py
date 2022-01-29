import matplotlib.pyplot as plt
import numpy as np
def polar_plot(df, mo, da):
    movec = df['datetime'].dt.month == mo
    davec = df['datetime'].dt.day == da
    index = movec & davec
    if np.sum(index) > 0:
        times = df.loc[index, 'datetime']
        wdir  = np.mean(df.loc[index, 'WDIR'].to_numpy().astype(float))
        wspd  = np.mean(df.loc[index, 'WSPD'].to_numpy().astype(float))
        maxwspd = np.max(df['WSPD'].to_numpy().astype(float))
        fig = plt.figure()
        plt.polar(wdir, wspd, 'b^', markersize=12)
        plt.yticks(np.linspace(0, maxwspd, 6))
        plt.ylim([0, maxwspd])
        return fig
    else:
        print('No wind data is provided for this date.')