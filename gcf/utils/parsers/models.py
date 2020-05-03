from dataclasses import dataclass, field
from typing import Dict


@dataclass
class CsMouseConfig:
    dpi: int = None
    sens: float = None
    edpi: int = None
    mouse_hz: int = None
    zoom_sens: float = None
    mouse_acc: float = None
    win_sesn: int = None
    raw_input: bool = True


@dataclass
class CsVideoConfig:
    res_height: int = None
    res_width: int = None
    ratio_height: int = None
    ratio_width: int = None
    scale_mode: str = None
    monitor_hz: int = None


@dataclass
class CsDevices:
    monitor: Dict = None
    mouse: Dict = None
    mousepad: Dict = None
    keyboard: Dict = None
    headset: Dict = None
    gpu: Dict = None


@dataclass
class CsCrosshairConfig:
    crosshair: str = None


@dataclass
class CsViewModelConfig:
    viewmodel: str = None


@dataclass
class CsPlayerInfo:
    nickname: str = None
    firstname: str = None
    lastname: str = None
    city: str = None
    age: int = None
    description: str = None
    social_links: dict = field(default_factory=dict)

    def view_as_list(self):
        return [
            self.nickname,
            self.firstname,
            self.lastname,
            self.city,
            self.age,
            self.description
        ]


@dataclass
class CsPlayer:
    player_info: CsPlayerInfo = CsPlayerInfo()
    mouse_config: CsMouseConfig = CsMouseConfig()
    video_config: CsVideoConfig = CsVideoConfig()
    crosshair_config: CsCrosshairConfig = CsCrosshairConfig()
    viewmodel_config: CsViewModelConfig = CsViewModelConfig()
    devices: CsDevices = CsDevices()

    def view_as_list(self):
        return [self.player_info.nickname,
                self.player_info.name,
                self.player_info.age,
                self.player_info.description,
                self.player_info.social_links['steam'],
                self.player_info.social_links['twitch'],
                self.mouse_config.dpi,
                self.mouse_config.edpi,
                self.mouse_config.mouse_acc,
                self.mouse_config.mouse_hz,
                self.mouse_config.raw_input,
                self.mouse_config.sens,
                self.mouse_config.win_sesn,
                self.mouse_config.zoom_sens,
                self.video_config.monitor_hz,
                self.video_config.scale_mode,
                f'{self.video_config.res_width}x{self.video_config.res_height}',
                f'{self.video_config.ratio_width}x{self.video_config.ratio_height}',
                self.crosshair_config.crosshair,
                self.viewmodel_config.viewmodel
                ]
