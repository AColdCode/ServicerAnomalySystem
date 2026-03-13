import os


class ResultSaver:

    def __init__(self, output_dir="../../results"):

        self.output_dir = output_dir

        if not os.path.exists(output_dir):

            os.makedirs(output_dir)

    def save(self, df, filename):

        path = os.path.join(self.output_dir, filename)

        df.to_csv(path, index=False)

        print("结果保存:", path)
