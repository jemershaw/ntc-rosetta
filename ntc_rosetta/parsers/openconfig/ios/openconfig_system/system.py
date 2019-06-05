from typing import Any, Dict, Iterator, Tuple, cast

from ntc_rosetta.helpers import json_helpers as jh

from yangify.parser import Parser, ParserData

import json

class ClockConfig(Parser):
    class Yangify(ParserData):
        path = "/openconfig-system:system/clock/config"

    def timezone_name(self) -> str:
        v = jh.query('clock.timezone."#text"', self.yy.native)
        if v is not None:
            return str(v)
        else:
            return None

class Clock(Parser):
    config = ClockConfig

    class Yangify(ParserData):
        path = "/openconfig-system:system/clock"

class DnsConfig(Parser):
    class Yangify(ParserData):
        path = "/openconfig-system:system/dns/config"

    def search(self) -> str:
        return None

class DnsServerConfig(Parser):
    class Yangify(ParserData):
        path = "/openconfig-system:system/dns/servers/server/config"

    def port(self) -> int:
        return 32

class DnsServer(Parser):
    config = DnsServerConfig

    class Yangify(ParserData):
        path = "/openconfig-system:system/dns/servers/server"

        def extract_elements(self) -> Iterator[Tuple[str, Dict[str, Any]]]:
            for k, v in self.native["ip"]["name-server"].items():
                if k == "#text":
                    continue
                yield k, v


class DnsServers(Parser):
    server = DnsServer

    class Yangify(ParserData):
        path = "/openconfig-system:system/dns/servers"



class Dns(Parser):
    config = DnsConfig
    servers = DnsServers

    class Yangify(ParserData):
        path = "/openconfig-system:system/dns"

class NtpConfig(Parser):
    class Yangify(ParserData):
        path = "/openconfig-system:system/ntp/config"

    def enabled(self) -> bool:
        return True

    def ntp_source_address(self) -> str:
        return None

    def enable_ntp_auth(self) -> bool:
        return False

class NtpServerConfig(Parser):
    class Yangify(ParserData):
        path = "/openconfig-system:system/ntp/servers/server/config"

    def address(self) -> str:
        return ""

class NtpServer(Parser):
    config = NtpServerConfig

    class Yangify(ParserData):
        path = "/openconfig-system:system/ntp/servers/server"

class NtpServers(Parser):
    server = NtpServer

    class Yangify(ParserData):
        path = "/openconfig-system:system/ntp/servers"

class Ntp(Parser):
    config = NtpConfig
    servers = NtpServers

    class Yangify(ParserData):
        path = "/openconfig-system:system/ntp"


class SystemConfig(Parser):
    class Yangify(ParserData):
        path = "/openconfig-system:system/config"

    def hostname(self) -> str:
        # print(self.yy.native["ip"]["name-server"])
        v = jh.query('hostname."#text"', self.yy.native)
        if v is not None:
            return str(v)
        else:
            return None

    def domain_name(self) -> str:
        v = jh.query('ip."domain-name"."#text"', self.yy.native)
        if v is not None:
            return str(v)
        else:
            return None

    def login_banner(self) -> str:
        return None

    def motd_banner(self) -> str:
        return None

class System(Parser):
    config = SystemConfig
    clock = Clock
    dns = Dns
    ntp = Ntp

    class Yangify(ParserData):
        path = "/openconfig-system:system"
        metadata = {"key": "dev_conf", "command": "show running-config all"}

        def pre_process(self) -> None:
            self.native: Dict[str, Any] = self.root_native["dev_conf"]
