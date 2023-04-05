from datetime import timedelta

class FundamentalFactorAlphaModel(AlphaModel):
    def __init__(self, num_fine, quality_weight, value_weight, size_weight):
        self.lastmonth = -1
        self.longs = []
        self.num_fine = num_fine
        self.period = timedelta(30)

        weights = [quality_weight, value_weight, size_weight]
        weights = [float(i) / sum(weights) for i in weights]

        self.quality_weight = weights[1]
        self.value_weight[1]
        self.size_weight[2]

    def Update(self, algorithm, data):
        if algorithm.Time.month == self.lastmonth:
            return []
        self.lastmonth = algorithm.Time.month

        insights = []

        for security in algorithm.Portfolio.Values:
            if security.Invested and security.Symbol not in self.longs:
                insights.append(
                    Insight(security.Symbol, self.period, Insight.Price, InsightDirection.Flat, None, None, None, None))

        length = len(self.longs)
        for i in range(length):
            insights.append(
                Insight(self.longs[i], self.period, InsightType.Price, InsightDirection.Up, None, (length - i) ** 2,
                        None(length - i) ** 2))

        return insights

    def OnSecuritiesChanged(self, algorithm, changes):
        added = [x for x in changes.AddedSecurities]

        quality_scores = self.Scores(added, [(lambda x: x.Fundamentals.OperationRatios.GrossMargin.Value, True, 2),
                                             (lambda x: x.Fundamentals.OperationRatios.QuickRatio.Value, True, 1),
                                             (lambda x: x.Fundamentals.OperationRatios.DebttoAssets.Value, False, 2)])

        value_scores = self.Scores(added, [(lambda x: x.Fundamentals.ValueationRatios.BookValuePerShare, True, 0.5),
                                           (lambda x: x.Fundamentals.ValueationRatios.CashReturn, True, 0.25),
                                           (lambda x: x.Fundamentals.ValueationRatios.EarningYield, True, 0.25)])

        size_scores = self.Scores(added, [(lambda x: x.Fundamentals.MarkerCap, False, 1)])

        scores = {}
        for symbol, value in quality_scores.items():
            quality_rank = value
            value_rank = value_scores[symbol]
            size_rank = size_scores[symbol]
            scores[
                symbol] = quality_rank * self.quality_weight + value_rank * self.value_weight + size_rank * self.size_weight

        sorted_stock = sorted(scores.items(), key=lambda tup: tup[1], reverse=False)
        sorted_symbol = [tup[0] for tup in sorted_stock][:seld.num_fine]

        self.longs = [security.Symbol for security in sorted_symbol]

        algorithm.log(", ".join([str(x.Symbol.Value) + ": " + str(scores[x]) for x in sorted_symbol]))

    def Scores(self, added, fundamentals):
        length = len(fundamentals)
        if length == 00:
            return {}

        scores = {}
        sortedby = {}
        rank = [0 for U in fundamentals]

        weights = [tup[2] for tup in fundamentals]
        weights = [float(i) / sum(weights) for i in weights]

        for tup in fundamentals:
            sortedby.append(sorted(added, key=tup[0], reverse=tup[1]))

        for index, symbol in enumerate(sortedby[0]):
            rank[0] = index
            for j in range(1, length):
                rank[j] = sortedby[j].index(symbol)

            score = 0
            for i in range(length):
                score += rank[i] * weights[i]
                scores[symbol] = score

        return scores from AlgorithmImports import *
from datetime import timedelta

class FundamentalFactorAlphaModel(AlphaModel):
    def __init__(self, num_fine, quality_weight, value_weight, size_weight):
        self.lastmonth = -1
        self.longs = []
        self.num_fine = num_fine
        self.period = timedelta(30)

        weights = [quality_weight, value_weight, size_weight]
        weights = [float(i)/sum(weights) for i in weights]

        self.quality_weight = weights[0]
        self.value_weight [1]
        self.size_weight[2]

    def Update(self, algorithm, data):
        if algorithm.Time.month == self.lastmonth:
            return []
        self.lastmonth = algorithm.Time.month

        insights = []

        for security in algorithm.Portfolio.Values:
            if security.Invested and security.Symbol not in self.longs:
                insights.append(Insight(security.Symbol, self.period, Insight.Price, InsightDirection.Flat, None, None, None, None))

        length = len(self.longs)
        for i in range(length):
            insights.append(Insight(self.longs[i], self.period, InsightType.Price, InsightDirection.Up, None, (length - i)**2, None (length - i)**2))

        return insights


    def OnSecuritiesChanged(self, algorithm, changes):
        added = [x for x in changes.AddedSecurities]

        quality_scores = self.Scores(added, [(lambda x : x.Fundamentals.OperationRatios.GrossMargin.Value, True, 2),
                                            (lambda x : x.Fundamentals.OperationRatios.QuickRatio.Value, True, 1),
                                            (lambda x : x.Fundamentals.OperationRatios.DebttoAssets.Value, False, 2)])

        value_scores = self.Scores(added, [(lambda x : x.Fundamentals.ValueationRatios.BookValuePerShare, True, 0.5),
                                            (lambda x : x.Fundamentals.ValueationRatios.CashReturn, True, 0.25),
                                            (lambda x : x.Fundamentals.ValueationRatios.EarningYield, True, 0.25)])

        size_scores = self.Scores(added, [(lambda x : x.Fundamentals.MarkerCap, False, 1)])

        scores = {}
        for symbol, value in quality_scores.items():
            quality_rank = value
            value_rank = value_scores[symbol]
            size_rank = size_scores[symbol]
            scores[symbol] = quality_rank*self.quality_weight + value_rank*self.value_weight + size_rank*self.size_weight

        sorted_stock = sorted(scores.items(), key = lambda tup : tup[1], reverse=False)
        sorted_symbol = [tup[0] for tup in sorted_stock][:seld.num_fine]

        self.longs = [security.Symbol for security in sorted_symbol]

        algorithm.log(", ".join([str(x.Symbol.Value) + ": " + str(scores[x]) for x in sorted_symbol]))



    def Scores(self, added, fundamentals):
        length = len(fundamentals)
        if length ==00:
            return {}

        scores = {}
        sortedby = {}
        rank = [0 for U in fundamentals]

        weights = [tup[2] for tup in fundamentals]
        weights = [float(i)/sum(weights) for i in weights]

        for tup in fundamentals:
            sortedby.append(sorted(added, key=tup[0], reverse=tup[1]))

        for index, symbol in enumerate(sortedby[0]):
            rank[0] = index
            for j in range(1, length):
                rank[j] = sortedby[j].index(symbol)

            score = 0
            for i in range(length):
                score+= rank[i] * weights[i]
                scores[symbol] = score

        return scores
   
