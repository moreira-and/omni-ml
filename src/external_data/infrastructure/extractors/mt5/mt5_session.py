from typing import Any, cast

import MetaTrader5 as mt5

from src.config import MT5_SECRETS, load_secrets

mt5 = cast(Any, mt5)


class MT5Session:

    def __enter__(self):
        if not mt5.initialize():
            raise RuntimeError("MT5 initialize failed")

        if mt5.account_info() is None:

            secrets = load_secrets(MT5_SECRETS)
            mt5_secrets = secrets.get("mt5")
            mt5.login(
                login=int(mt5_secrets["login"]),
                password=mt5_secrets["password"],
                server=mt5_secrets["server"],
            )

        if mt5.account_info() is None:
            raise RuntimeError("MT5 login failed")

        return self

    def __exit__(self, exc_type, exc, tb):
        mt5.shutdown()
