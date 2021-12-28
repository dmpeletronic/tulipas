from oplab import Client

class Robot():
    def __init__(self, trading_account_id, portifolio_id, mode, spread, strategy_name, underlying, positions):
        self.trading_account_id = trading_account_id
        self.portifolio_id = portifolio_id
        self.mode = mode
        self.spread = spread
        self.strategy_name = strategy_name
        self.underlying = underlying
        self.positions = positions

    def send(self, client: Client, dry_run=False):
        robot = {
            'trading_account_id': self.trading_account_id,
            'debug': 2,
            'mode': self.mode,
            'spread': self.spread,
            'strategy': {
                'name': self.strategy_name,
                'underlying': self.underlying,
            },
            'positions': self.positions
        }
        data = client.domain.create_robot(self.portifolio_id, robot, dry_run)
        return data