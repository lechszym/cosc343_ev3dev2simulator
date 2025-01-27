from setuptools import setup, find_packages
from ev3dev2simulator.version import __version__ as simversion

setup(
    name="ev3dev2simulator",
    version=simversion,
    description="EV3 simulator for the ev3dev2 library",
    long_description="""
Simulator for an EV3 robot; a program using the ev3dev2 API can run both on the rover and on the simulator without any modifications to the code.

For more info: https://github.com/lechszym/cosc343_ev3dev2simulator
""",
    url="https://github.com/lechszym/cosc343_ev3dev2simulator",
    author="Harco Kuppens, Sam Jansen, Niels Okker, Lech Szymanski",
    author_email="lech.szymanski@otago.ac.nz",
    license="MIT",
    classifiers=[
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "License :: Freeware",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Education",
        "Topic :: Software Development",

    ],
    keywords="IDE education programming EV3 mindstorms lego",
    platforms=["Windows", "macOS", "Linux"],
    python_requires=">=3.6",
    install_requires=['ev3devlogging', 'arcade==2.4.1', 'pypiwin32; platform_system=="Windows"',
                      'pyobjc;sys.platform=="darwin"', 'pymunk==5.6.0',
                      'simpleaudio==1.0.4', 'pyttsx3==2.7', 'numpy', 'pyglet', 'strictyaml'],
    py_modules=["bluetooth"],
    packages=find_packages(exclude=['tests', 'tests.*', '*.tests.*', ]),
    package_data={
        "ev3dev2simulator": [
            "config/*", "config/world_configurations/*", "config/robot_configurations/*", "assets/images/*"
        ],
        "cosc343-a1-simulator": [
            "config/*", "config/world_configurations/*", "config/robot_configurations/*", "assets/images/*"
        ],

    },
    entry_points={
        'console_scripts': [
            'ev3dev2simulator = ev3dev2simulator.__main__:main',
            'create_ev3dev2simulator_package = scripts.create_package:main'
        ]
    }
)
