import matplotlib.pyplot as plt
import pandas as pd

def plots(marg_gain):
    """ Plots marginal change and returns a plt object """
    # Prep Data frame
    df = pd.DataFrame.from_dict(marg_gain, orient="index")
    df['Einkommen in €'] = df.index
    df = df.reset_index()
    df["Marginal in €"] = df[0]
    df.drop([0, 'index'], inplace=True, axis=1)

    plt.plot(df['Einkommen in €'], df["Marginal in €"])   
    return plt

if __name__ == "__main__":
    df = {10: 1, 11: 2}
    print(plots(df))