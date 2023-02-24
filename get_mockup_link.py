from MockupEngineer import MockupEngineerInstance
import urllib.request


def generate_image(device_name: str) -> str:
    mockup = MockupEngineerInstance()

    if device_name == "iphone":
        urllib.request.urlretrieve(
            'https://source.unsplash.com/random/1400x3100', "/wp.jpg")
        device = mockup.templates[16]
    elif device_name == 'macbook':
        urllib.request.urlretrieve(
            'https://source.unsplash.com/random/3500x2300', "/wp.jpg")
        device = mockup.templates[26]
    return mockup.generate(template_id=device.id,
                           screenshot_path='/wp.jpg',
                           color=device.colors[0].color,
                           external_storage=True)
