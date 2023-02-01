from Execution.immediateExecutionModel import immediateExecutionModel
from Risk.MaximumDrawdownPercentPerSecurity import MaximumDrawdownPercentPerSecurity
from AlphaModel import FundamentalFactorAlphaModel

class NadionOptimizedAutosequencers(QCAlgorithm):

    def Initialise(self):
        self.SetStartDate(2012, 5, 1)
        self.SetEndDate(2021, 5, 1)
        self.SetCash(10000)

        self.SetExecution(immediateExecutionModel())

        self.SetPortfolioConstruction(InsightWeightingPortfolioConstructionModel())
        StopRisk = 0.1 # 10%
        self.SetRiskManagement(MaximumDrawdownPercentPerSecurity(StopRisk))

        self.num_coarse = 200
        self.num_fine = 20
        self.lastmonth = -1
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelectionFunction, self.FineSelectionFunction)

        quality_weight = 2
        size_weight = 1
        value_weight = 2

        self.AddAlpha(FundamentalFactorAlphaModel(self.num_fine, quality_weight, size_weight, value_weight))

        self.Schedule.On(self.DataRules.Every(DayOfWeek.Monday), self.TimeRules.At(14,30), self.Plotting)

    def Plotting(self):
        self.Plot("Positions", "Num", len([x.Symbol for x in self.Portfolio.Values if self.Portfolio[x.Symbol].Invested]))


    def CoarseSelectionFunction(self, Coarse):
        if self.Time.nonth == self.lastmonth:
            return Universe.Unchanged
        self.lastmonth = self.Time.month

        selected = sorted([x for x in coarse if x.HasFundamentalData and x.Price > 5],
                            key = lambda x : x.DollarVOlume, reverse=True)

        return [x.Symbol for x in selected[:self.num_coarse]]

    def FineSelectionFunction(self, fine):
        filtered_fine = [x.Symbol for x in fine if x.OperationRatios.GrossMargin.Value > 0
                                                and x.OperationRatios.QuickRatio.Value > 0
                                                and x.OperationRatios.DebttoAssets.Value > 0
                                                and x.ValueationRatios.BookValuePerShare > 0
                                                and x.ValueationRatios.CashReturn > 0
                                                and x.ValueationRatios.EarningYield > 0
                                                and x.MarkerCap > 0]
        return filtered_fine