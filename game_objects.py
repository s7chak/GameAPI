class Stock:
    def __init__(self):
        self.ticker = None
        self.company_name = None
        self.current_price = None
        self.market_cap = None
        self.enterprise_value = None
        self.shares_outstanding = None
        self.pe_ratio_ttm = None
        self.pe_ratio_forward = None
        self.peg_ratio = None
        self.pb_ratio = None
        self.ps_ratio = None
        self.ev_ebitda = None
        self.eps_ttm = None
        self.eps_forward = None
        self.revenue_ttm = None
        self.net_income = None
        self.gross_margin = None
        self.operating_margin = None
        self.roe = None
        self.roa = None
        self.debt_to_equity = None
        self.current_ratio = None
        self.quick_ratio = None
        self.dividend_yield = None
        self.dividend_rate = None
        self.ex_dividend_date = None
        self.payout_ratio = None
        self.beta = None
        self.fifty_two_week_high = None
        self.fifty_two_week_low = None
        self.one_year_target = None
        self.earnings_date = None
        self.sector = None
        self.industry = None
        self.employees = None

    def to_dict(self):
        return self.__dict__