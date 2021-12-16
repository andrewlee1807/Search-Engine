import json
import re
from dataclasses import dataclass
from typing import Any, Optional, List, TypeVar, Callable, Type, cast
import numpy as np
T = TypeVar("T")


def from_str(x: Any) -> str:
    # try:
    #     assert isinstance(x, str)
    # except:
    #     print(x)
    #     pass
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Battery:
    colors: str
    models: str
    sar: str
    sar_eu: str
    price: float
    type: str

    @staticmethod
    def from_dict(obj: Any) -> 'Battery':
        assert isinstance(obj, dict)
        colors = from_str(obj.get("Colors"))
        models = from_str(obj.get("Models"))
        sar = from_str(obj.get("SAR"))
        sar_eu = from_str(obj.get("SAR EU"))
        price = -1
        t = obj.get("Price")
        if t != '' and "BTC" not in t:
            if "/" in t:
                price = float(t.split("/")[0].replace(',', '').replace("$", '').replace("€", '').replace("£", ''))
            elif "About" in t:
                price = float(re.findall(r'\d+', t)[0])
        type = from_str(obj.get("Type"))
        return Battery(colors, models, sar, sar_eu, price, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Colors"] = from_str(self.colors)
        result["Models"] = from_str(self.models)
        result["SAR"] = from_str(self.sar)
        result["SAR EU"] = from_str(self.sar_eu)
        result["Price"] = from_str(self.price)
        result["Type"] = from_str(self.type)
        return result


@dataclass
class Body:
    dimensions: str
    weight: str
    build: str
    sim: str

    @staticmethod
    def from_dict(obj: Any) -> 'Body':
        assert isinstance(obj, dict)
        dimensions = from_str(obj.get("Dimensions"))
        weight = from_str(obj.get("Weight"))
        build = from_str(obj.get("Build"))
        sim = from_str(obj.get("SIM"))
        return Body(dimensions, weight, build, sim)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Dimensions"] = from_str(self.dimensions)
        result["Weight"] = from_str(self.weight)
        result["Build"] = from_str(self.build)
        result["SIM"] = from_str(self.sim)
        return result


@dataclass
class Comms:
    wlan: str
    bluetooth: str
    gps: str
    nfc: str
    radio: str
    usb: str

    @staticmethod
    def from_dict(obj: Any) -> 'Comms':
        assert isinstance(obj, dict)
        wlan = from_str(obj.get("WLAN"))
        bluetooth = from_str(obj.get("Bluetooth"))
        gps = from_str(obj.get("GPS"))
        nfc = from_str(obj.get("NFC"))
        radio = from_str(obj.get("Radio"))
        usb = from_str(obj.get("USB"))
        return Comms(wlan, bluetooth, gps, nfc, radio, usb)

    def to_dict(self) -> dict:
        result: dict = {}
        result["WLAN"] = from_str(self.wlan)
        result["Bluetooth"] = from_str(self.bluetooth)
        result["GPS"] = from_str(self.gps)
        result["NFC"] = from_str(self.nfc)
        result["Radio"] = from_str(self.radio)
        result["USB"] = from_str(self.usb)
        return result


@dataclass
class Display:
    type: str
    size: float
    size_str: str
    resolution: str
    resolution_str: str
    protection: int
    protection_str: str
    display: str

    @staticmethod
    def from_dict(obj: Any) -> 'Display':
        assert isinstance(obj, dict)
        type = from_str(obj.get("Type"))
        size = -1
        size_str = obj.get("Size")
        if size_str is not None:
            try:
                size = float(re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", size_str)[0])
            except:
                pass

        resolution = obj.get("Resolution")[obj.get("Resolution").find("pixels") - 1]
        resolution_str = obj.get("Resolution")
        protection_str = from_str(obj.get("Protection"))
        if protection_str is not None:
            protection = 1
        else:
            protection = 0
        display = from_str(obj.get("Display"))
        return Display(type, size, size_str, resolution, resolution_str, protection, protection_str, display)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Type"] = from_str(self.type)
        result["Size"] = from_str(self.size)
        result["Resolution"] = from_str(self.resolution)
        result["Protection"] = from_str(self.protection)
        result["Display"] = from_str(self.display)
        return result


@dataclass
class Features:
    sensors: str
    features: str
    video: str

    @staticmethod
    def from_dict(obj: Any) -> 'Features':
        assert isinstance(obj, dict)
        sensors = from_str(obj.get("Sensors"))
        features = from_str(obj.get("Features"))
        video = from_str(obj.get("Video"))
        return Features(sensors, features, video)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Sensors"] = from_str(self.sensors)
        result["Features"] = from_str(self.features)
        result["Video"] = from_str(self.video)
        return result


@dataclass
class Launch:
    announced: int
    announced_str: int
    status: str

    @staticmethod
    def from_dict(obj: Any) -> 'Launch':
        assert isinstance(obj, dict)
        announced = 0
        announced_str = obj.get("Announced")
        if obj.get("Announced") is not None:
            date = obj.get("Announced")
            try:
                if "." in date:  # 2016, August. Released 2016, August
                    date_ = date.split(".")[0]  # 2016, August
                    announced = int(datetime.datetime.strptime(date_, "%Y, %B").strftime("%Y%m%d%H%M%S"))
                elif date[-1].isdigit():  # 2018, June 12
                    announced = int(datetime.datetime.strptime(date, "%Y, %B %d").strftime("%Y%m%d%H%M%S"))
                elif len(date.split(",")) == 2:  # 2019, May
                    announced = int(datetime.datetime.strptime(date, "%Y, %B").strftime("%Y%m%d%H%M%S"))
            except:  # 2019
                try:
                    announced = int(datetime.datetime.strptime(date[:4], "%Y").strftime("%Y%m%d%H%M%S"))
                except:
                    pass

        status = from_str(obj.get("Status"))
        return Launch(announced, status, announced_str)


def to_dict(self) -> dict:
    result: dict = {}
    result["Announced"] = from_str(self.announced)
    result["Status"] = from_str(self.status)
    return result


@dataclass
class Camera:
    features: str
    video: str
    single: float
    single_str: str
    quad: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Camera':
        assert isinstance(obj, dict)
        features = from_str(obj.get("Features"))
        video = from_str(obj.get("Video"))
        quad = from_union([from_str, from_none], obj.get("Quad"))
        single = -1
        single_str = obj.get("Single")
        value = obj.get("Single")
        if value == '':
            value = quad
        if value is not None and value != '' and len(value.split(" ")) > 1:
            # single = float(value.split(" ")[0])
            try:
                single = float(re.findall(r"[-+]?\d*\.?\d+|[-+]?\d+", value)[0])
            except:
                pass
        return Camera(features, video, single,single_str, quad)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Features"] = from_str(self.features)
        result["Video"] = from_str(self.video)
        result["Single"] = from_str(self.single)
        result["Quad"] = from_union([from_str, from_none], self.quad)
        return result


@dataclass
class Memory:
    card_slot: str
    internal: str

    @staticmethod
    def from_dict(obj: Any) -> 'Memory':
        assert isinstance(obj, dict)
        card_slot = from_str(obj.get("Card slot"))
        internal = from_str(obj.get("Internal"))
        return Memory(card_slot, internal)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Card slot"] = from_str(self.card_slot)
        result["Internal"] = from_str(self.internal)
        return result


@dataclass
class Network:
    technology: str
    the_2_g_bands: str
    the_3_g_bands: str
    the_4_g_bands: str
    the_5_g_bands: str
    speed: str

    @staticmethod
    def from_dict(obj: Any) -> 'Network':
        assert isinstance(obj, dict)
        technology = from_str(obj.get("Technology"))
        the_2_g_bands = from_str(obj.get("2G bands"))
        the_3_g_bands = from_str(obj.get("3G bands"))
        the_4_g_bands = from_str(obj.get("4G bands"))
        the_5_g_bands = from_str(obj.get("5G bands"))
        speed = from_str(obj.get("Speed"))
        return Network(technology, the_2_g_bands, the_3_g_bands, the_4_g_bands, the_5_g_bands, speed)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Technology"] = from_str(self.technology)
        result["2G bands"] = from_str(self.the_2_g_bands)
        result["3G bands"] = from_str(self.the_3_g_bands)
        result["4G bands"] = from_str(self.the_4_g_bands)
        result["5G bands"] = from_str(self.the_5_g_bands)
        result["Speed"] = from_str(self.speed)
        return result


@dataclass
class Platform:
    os: str
    chipset: str
    cpu: str
    gpu: str

    @staticmethod
    def from_dict(obj: Any) -> 'Platform':
        assert isinstance(obj, dict)
        os = from_str(obj.get("OS"))
        chipset = from_str(obj.get("Chipset"))
        cpu = from_str(obj.get("CPU"))
        gpu = from_str(obj.get("GPU"))
        return Platform(os, chipset, cpu, gpu)

    def to_dict(self) -> dict:
        result: dict = {}
        result["OS"] = from_str(self.os)
        result["Chipset"] = from_str(self.chipset)
        result["CPU"] = from_str(self.cpu)
        result["GPU"] = from_str(self.gpu)
        return result


@dataclass
class Popularity:
    love: int
    click: float

    @staticmethod
    def from_dict(obj: Any) -> 'Popularity':
        assert isinstance(obj, dict)
        try:
            love = int(obj.get("Love"))
        except:
            love = 0
        try:
            click = float(obj.get("Click").replace(',', ''))
        except:
            click = 0
        return Popularity(love, click)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Love"] = from_str(str(self.love))
        result["Click"] = from_str(self.click)
        return result


@dataclass
class Sound:
    loudspeaker: str
    the_35_mm_jack: str

    @staticmethod
    def from_dict(obj: Any) -> 'Sound':
        assert isinstance(obj, dict)
        loudspeaker = from_str(obj.get("Loudspeaker"))
        the_35_mm_jack = from_str(obj.get("3.5mm jack"))
        return Sound(loudspeaker, the_35_mm_jack)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Loudspeaker"] = from_str(self.loudspeaker)
        result["3.5mm jack"] = from_str(self.the_35_mm_jack)
        return result


@dataclass
class Tests:
    performance: str
    display: str
    camera: str
    loudspeaker: str
    battery_life: str

    @staticmethod
    def from_dict(obj: Any) -> 'Tests':
        assert isinstance(obj, dict)
        performance = from_str(obj.get("Performance"))
        display = from_str(obj.get("Display"))
        camera = from_str(obj.get("Camera"))
        loudspeaker = from_str(obj.get("Loudspeaker"))
        battery_life = from_str(obj.get("Battery life"))
        return Tests(performance, display, camera, loudspeaker, battery_life)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Performance"] = from_str(self.performance)
        result["Display"] = from_str(self.display)
        result["Camera"] = from_str(self.camera)
        result["Loudspeaker"] = from_str(self.loudspeaker)
        result["Battery life"] = from_str(self.battery_life)
        return result


@dataclass
class Device:
    brand: str
    product_name: str
    full_name: str

    @staticmethod
    def from_str(obj: Any) -> 'Device':
        brand = None
        product_name = None
        full_name = str(obj)
        if obj is not None and len(obj.split(" ")) >= 2:
            tm = obj.split(" ")
            brand = tm[0]
            product_name = tm[1:]

        return Device(brand, product_name, full_name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["brand"] = from_str(self.brand)
        result["product_name"] = from_str(self.product_name)
        return result


@dataclass
class Product:
    device: str
    popularity: Popularity
    network: Network
    launch: Launch
    body: Body
    display: Display
    platform: Platform
    memory: Memory
    main_camera: Camera
    selfie_camera: Camera
    sound: Sound
    comms: Comms
    features: Features
    battery: Battery
    tests: Tests
    opinions: List[Any]
    numfeatures: List[Any]

    @staticmethod
    def from_dict(obj: Any) -> 'Product':
        assert isinstance(obj, dict)
        device = Device.from_str(obj.get("DEVICE"))
        # device = from_str(obj.get("DEVICE"))
        popularity = Popularity.from_dict(obj.get("POPULARITY"))
        network = Network.from_dict(obj.get("NETWORK"))
        launch = Launch.from_dict(obj.get("LAUNCH"))
        body = Body.from_dict(obj.get("BODY"))
        display = Display.from_dict(obj.get("DISPLAY"))
        platform = Platform.from_dict(obj.get("PLATFORM"))
        memory = Memory.from_dict(obj.get("MEMORY"))
        main_camera = Camera.from_dict(obj.get("MAIN CAMERA"))
        selfie_camera = Camera.from_dict(obj.get("SELFIE CAMERA"))
        sound = Sound.from_dict(obj.get("SOUND"))
        comms = Comms.from_dict(obj.get("COMMS"))
        features = Features.from_dict(obj.get("FEATURES"))
        battery = Battery.from_dict(obj.get("BATTERY"))
        tests = Tests.from_dict(obj.get("TESTS"))
        opinions = from_list(lambda x: x, obj.get("OPINIONS"))
        numfeatures = from_list(lambda x: x, obj.get("NUMFEATURES"))
        return Product(device, popularity, network, launch, body, display, platform, memory, main_camera, selfie_camera,
                       sound, comms, features, battery, tests, opinions, numfeatures)

    def to_dict(self) -> dict:
        result: dict = {}
        result["DEVICE"] = from_str(self.device)
        result["POPULARITY"] = to_class(Popularity, self.popularity)
        result["NETWORK"] = to_class(Network, self.network)
        result["LAUNCH"] = to_class(Launch, self.launch)
        result["BODY"] = to_class(Body, self.body)
        result["DISPLAY"] = to_class(Display, self.display)
        result["PLATFORM"] = to_class(Platform, self.platform)
        result["MEMORY"] = to_class(Memory, self.memory)
        result["MAIN CAMERA"] = to_class(Camera, self.main_camera)
        result["SELFIE CAMERA"] = to_class(Camera, self.selfie_camera)
        result["SOUND"] = to_class(Sound, self.sound)
        result["COMMS"] = to_class(Comms, self.comms)
        result["FEATURES"] = to_class(Features, self.features)
        result["BATTERY"] = to_class(Battery, self.battery)
        result["TESTS"] = to_class(Tests, self.tests)
        result["OPINIONS"] = from_list(lambda x: x, self.opinions)
        result["NUMFEATURES"] = from_list(lambda x: x, self.numfeatures)
        return result


def product_from_dict(s: Any) -> List[Product]:
    return from_list(Product.from_dict, s)


def product_to_dict(x: List[Product]) -> Any:
    return from_list(lambda x: to_class(Product, x), x)


